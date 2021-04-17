from typing import Dict, List, Text
import sqlalchemy
from gino_admin.types import types_map
from gino_admin.utils import (GinoAdminError, HashColumn, get_table_name,
                              logger, parse_db_uri)


def extract_column_data(model_id: Text) -> Dict:
    """ extract data about column """
    _hash = "_hash"
    columns_data, hashed_indexes = {}, []
    table_name = get_table_name(model_id)
    for num, column in enumerate(cfg.app.db.tables[table_name].columns):
        if _hash in column.name:
            name = column.name.split(_hash)[0]
            type_ = HashColumn
            hashed_indexes.append(num)
        else:
            name = column.name
            type_ = types_map.get(str(column.type).split("(")[0])
            if not type_:
                logger.error(f"{column.type} was not found in types_map")
                type_ = str
        if len(str(column.type).split("(")) > 1:
            len_ = int(str(column.type).split("(")[1].split(")")[0])
        else:
            len_ = None
        columns_data[name] = {
            "type": type_,
            "len": len_,
            "nullable": column.nullable,
            "unique": column.unique,
            "primary": column.primary_key,
            "foreign_keys": column.foreign_keys,
            "db_type": column.type,
            "sequence": isinstance(column.default, 
                                   sqlalchemy.sql.schema.Sequence),
        }
    required = [
        key
        for key, value in columns_data.items()
        if value["nullable"] is False or value["primary"]
    ]
    unique_keys = [
        key for key, value in columns_data.items() if value["unique"] is True
    ]
    foreign_keys = {}
    for column_name, data in columns_data.items():
        for key in data["foreign_keys"]:
            foreign_keys[key._colspec.split(".")[0]] = (
                column_name,
                key._colspec.split(".")[1],
            )

    primary_keys = [
        key for key, value in columns_data.items() if value["primary"] is True
    ]
    table_details = {
        "unique_columns": unique_keys,
        "required_columns": required,
        "columns_data": columns_data,
        "primary_keys": primary_keys,
        "columns_names": list(columns_data.keys()),
        "hashed_indexes": hashed_indexes,
        "foreign_keys": foreign_keys,
        "identity": primary_keys,
    }
    return table_details