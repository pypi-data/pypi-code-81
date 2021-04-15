from logging import Logger
from injecta.container.ContainerInterface import ContainerInterface
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from databricksbundle.notebook.function.node_argument_function import node_argument_function


@node_argument_function
def read_csv(csv_path: str, schema: StructType = None, options: dict = None):
    def wrapper(container: ContainerInterface):
        logger: Logger = container.get("databricksbundle.logger")
        logger.info(f"Reading CSV from `{csv_path}` with options: {options}")

        spark: SparkSession = container.get(SparkSession)

        data_frame_reader = spark.read.format("csv")

        if schema:
            data_frame_reader = data_frame_reader.schema(schema)

        if options:
            data_frame_reader = data_frame_reader.options(**options)

        return data_frame_reader.load(csv_path)

    return wrapper
