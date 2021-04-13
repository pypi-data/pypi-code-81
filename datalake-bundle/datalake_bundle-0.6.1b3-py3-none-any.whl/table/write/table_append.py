from logging import Logger
from databricksbundle.notebook.decorator.DecoratedDecorator import DecoratedDecorator
from databricksbundle.notebook.decorator.ResultProcessingDecorator import ResultProcessingDecorator
from injecta.container.ContainerInterface import ContainerInterface
from pyspark.sql import DataFrame
from datalakebundle.table.TableManager import TableManager
from datalakebundle.table.TableWriter import TableWriter


@DecoratedDecorator
class table_append(ResultProcessingDecorator):  # noqa: N801
    def __init__(self, table_identifier: str):
        self.__table_identifier = table_identifier

    def process_result(self, result: DataFrame, container: ContainerInterface):
        logger: Logger = container.get("datalakebundle.logger")
        table_manager: TableManager = container.get(TableManager)
        table_writer: TableWriter = container.get(TableWriter)

        output_table_name = table_manager.get_name(self.__table_identifier)

        logger.info(f"Data to be appended into table: {output_table_name}")

        table_manager.create_if_not_exists(self.__table_identifier)

        logger.info(f"Appending data to table: {output_table_name}")

        table_config = table_manager.get_config(self.__table_identifier)

        table_writer.append(result.select([field.name for field in table_config.schema.fields]), table_config)

        logger.info(f"Data successfully appended to: {output_table_name}")
