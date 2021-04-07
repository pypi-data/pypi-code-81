import pyspark
from pyspark.sql import SparkSession
import logging
import logging.config

class Transform:
    def __init__(self,spark):
        self.spark=spark

    def drop(df):
        # dropping all the rows which has null values
        transformed_df = df.na.drop()
        transformed_df.show()
        return transformed_df
