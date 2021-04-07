import pyspark
from pyspark.sql import SparkSession
import logging
import logging.config

class Persist:
    def __init__(self,spark):
        self.spark=spark

    def save(df, filePath):
        df.coalesce(1).write.option("header", "true").csv(filePath)
        return df
