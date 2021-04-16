from pathlib import Path
from typing import Any, Mapping, Optional

import pytest

import atoti as tt
from atoti._plugins import MissingPluginError
from atoti.session import Session

DATABASE_PATH = Path(__file__).parent / "resources" / "h2database"
DATABASE_URL = "h2:" + str(DATABASE_PATH.absolute())
H2_USERNAME = "root"
H2_PASSWORD = ""

SCHEMA = {
    "ID": tt.type.INT,
    "CITY": tt.type.STRING,
    "MY_VALUE": tt.type.NULLABLE_DOUBLE,
}
CREDENTIALS = {"username": H2_USERNAME, "password": H2_PASSWORD}
SQL_QUERY = "SELECT * FROM MYTABLE;"


@pytest.mark.sql
def test_load_sql_h2_database(session: Session):
    store = session.create_store(SCHEMA, "test sql", keys=["ID"])
    assert len(store) == 0
    store.load_sql(DATABASE_URL, SQL_QUERY, **CREDENTIALS)
    assert len(store) == 5


@pytest.mark.sql
def test_read_sql_h2_database(session: Session):
    store = session.read_sql(
        "jdbc:" + str(DATABASE_URL),
        SQL_QUERY,
        **CREDENTIALS,
        store_name="sql",
        keys=["ID"],
    )
    assert len(store) == 5
    assert store.columns == ["ID", "CITY", "MY_VALUE"]
    assert store._types == SCHEMA


@pytest.mark.sql
@pytest.mark.parametrize(
    "types", [None, {"MY_VALUE": {"java_type": "double", "nullable": False}}]
)
def test_read_sql_h2_database_with_types(
    session: Session, types: Optional[Mapping[str, Any]]
):
    store = session.read_sql(
        "jdbc:" + str(DATABASE_URL),
        SQL_QUERY,
        **CREDENTIALS,
        store_name="SQL store",
        keys=["ID"],
        types={
            column_name: tt.type.DataType(**kwargs)
            for column_name, kwargs in types.items()
        }
        if types
        else None,
    )
    assert len(store) == 5
    assert store.columns == ["ID", "CITY", "MY_VALUE"]
    assert (
        store._types["MY_VALUE"] == tt.type.DataType(**types["MY_VALUE"])
        if types
        else tt.type.NULLABLE_FLOAT
    )


def test_missing_plugin_load_sql(session: Session):
    store = session.create_store(SCHEMA, "test sql", keys=["ID"])
    with pytest.raises(MissingPluginError):
        store.load_sql(DATABASE_URL, SQL_QUERY, **CREDENTIALS)


def test_missing_plugin_create_sql(session: Session):
    with pytest.raises(MissingPluginError):
        session.read_sql(
            DATABASE_URL,
            SQL_QUERY,
            store_name="sql",
            **CREDENTIALS,
        )
