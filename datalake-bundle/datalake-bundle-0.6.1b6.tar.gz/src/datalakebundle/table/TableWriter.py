from logging import Logger
from pyspark.sql.session import SparkSession
from pyspark.sql.dataframe import DataFrame
from datalakebundle.table.config.TableConfig import TableConfig
from datalakebundle.table.schema.DeltaTableSchema import DeltaTableSchema
import pyspark.sql.types as t
import yaml
import string
import random


class TableWriter:
    def __init__(
        self,
        logger: Logger,
        spark: SparkSession,
    ):
        self.__logger = logger
        self.__spark = spark

    def append(self, df: DataFrame, table_config: TableConfig):
        self.__insert_into(df, table_config, False)

    def overwrite(self, df: DataFrame, table_config: TableConfig):
        self.__insert_into(df, table_config, True)

    def upsert(self, df: DataFrame, table_config: TableConfig):
        if not isinstance(table_config.schema, DeltaTableSchema):
            raise Exception("In order to perform upsert operation schema must be of type DeltaTableSchema")

        if len(table_config.schema.primary_key_columns) == 0:
            raise Exception(f"Table {table_config.table_name} has no primary keys defined, define them in 'schema.py' file")

        self.__check_schema(df, table_config)

        temp_source_table = f"upsert_{table_config.table_identifier}_{''.join(random.choice(string.ascii_lowercase) for _ in range(6))}"

        df.createOrReplaceTempView(temp_source_table)

        upsert_sql_statement = self.__create_sql_upsert_statement(table_config, temp_source_table)

        try:
            self.__spark.sql(upsert_sql_statement)

        except BaseException:
            raise

        finally:
            self.__spark.catalog.dropTempView(temp_source_table)

    def write_if_not_exist(self, df: DataFrame, table_config: TableConfig):
        self.__check_schema(df, table_config)

        (
            df.write.partitionBy(table_config.partition_by)
            .format("delta")
            .option("overwriteSchema", "true")
            .mode("errorifexists")
            .saveAsTable(table_config.full_table_name, path=table_config.target_path)
        )

    def __check_schema(self, df: DataFrame, table_config: TableConfig):
        table_schema = table_config.schema

        def print_schema(schema: t.StructType):
            return yaml.dump(schema.jsonValue())

        def remove_metadata(json_schema):
            for field in json_schema["fields"]:
                field["metadata"] = dict()

            return json_schema

        if remove_metadata(table_schema.jsonValue()) != remove_metadata(df.schema.jsonValue()):
            self.__logger.warning(
                "Table and dataframe schemas do NOT match",
                extra={
                    "df_schema": print_schema(df.schema),
                    "table_schema": print_schema(table_schema),
                    "table_schema_loader": table_config.schema_loader,
                    "table": table_config.full_table_name,
                },
            )

    def __insert_into(self, df: DataFrame, table_config: TableConfig, overwrite: bool):
        self.__check_schema(df, table_config)

        df.write.insertInto(table_config.full_table_name, overwrite=overwrite)

    def __create_sql_upsert_statement(self, table_config: TableConfig, temp_source_table: str) -> str:
        conditions = []
        updates = []
        columns_to_update = set(table_config.schema.fieldNames()) - set(table_config.schema.primary_key_columns)

        for primary_key in table_config.schema.primary_key_columns:
            conditions.append(f"source.`{primary_key}` = target.`{primary_key}`")

        for col in columns_to_update:
            updates.append(f"target.`{col}` = source.`{col}`")

        statement = (
            f"MERGE INTO {table_config.full_table_name} AS target\n"
            f"USING {temp_source_table} AS source\n"
            f"ON {' AND '.join(conditions)}\n"
            f"{{matched_clause}}"
            f"WHEN NOT MATCHED THEN INSERT *\n"
        )

        if len(updates) > 0:
            statement = statement.format(matched_clause=f"WHEN MATCHED THEN UPDATE SET {', '.join(updates)}\n")
        else:
            statement = statement.format(matched_clause="")

        return statement
