from logging import Logger
from injecta.container.ContainerInterface import ContainerInterface
from pyspark.sql import SparkSession
from databricksbundle.notebook.function.node_argument_function import node_argument_function
from datalakebundle.table.TableManager import TableManager


@node_argument_function
def read_table(identifier: str):
    def wrapper(container: ContainerInterface):
        table_manager: TableManager = container.get(TableManager)
        table_name = table_manager.get_name(identifier)

        logger: Logger = container.get("datalakebundle.logger")
        logger.info(f"Reading table `{table_name}`")

        spark: SparkSession = container.get(SparkSession)

        return spark.read.table(table_name)

    return wrapper
