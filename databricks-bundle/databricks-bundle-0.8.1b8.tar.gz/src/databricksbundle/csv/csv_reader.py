from logging import Logger
from injecta.container.ContainerInterface import ContainerInterface
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from databricksbundle.notebook.function.input_decorator_function import input_decorator_function


@input_decorator_function
def read_csv(csv_path: str, schema: StructType = None, options: dict = None):
    def wrapper(container: ContainerInterface):
        logger: Logger = container.get("databricksbundle.logger")
        logger.info(f"Reading CSV from `{csv_path}`", extra=options)

        spark: SparkSession = container.get(SparkSession)

        data_frame_reader = spark.read.format("csv")

        if schema:
            data_frame_reader = data_frame_reader.schema(schema)

        if options:
            data_frame_reader = data_frame_reader.options(**options)

        return data_frame_reader.load(csv_path)

    return wrapper
