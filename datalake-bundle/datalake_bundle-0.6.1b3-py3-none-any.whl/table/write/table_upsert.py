from logging import Logger
from databricksbundle.notebook.decorator.DecoratedDecorator import DecoratedDecorator
from databricksbundle.notebook.decorator.ResultProcessingDecorator import ResultProcessingDecorator
from injecta.container.ContainerInterface import ContainerInterface
from pyspark.sql import DataFrame
from datalakebundle.table.TableManager import TableManager


@DecoratedDecorator
class table_upsert(ResultProcessingDecorator):  # noqa: N801
    def __init__(self, table_identifier: str):
        self.__table_identifier = table_identifier

    def process_result(self, result: DataFrame, container: ContainerInterface):
        logger: Logger = container.get("datalakebundle.logger")
        table_manager: TableManager = container.get(TableManager)

        output_table_name = table_manager.get_name(self.__table_identifier)

        logger.info(f"Data to be upserted into table: {output_table_name}")

        table_manager.create_if_not_exists(self.__table_identifier)

        logger.info(f"Upserting data to table: {output_table_name}")

        schema = table_manager.get_config(self.__table_identifier).schema

        # TODO: upsert zápis
        result.select([field.name for field in schema.fields])

        logger.info(f"Data successfully upserted to: {output_table_name}")
