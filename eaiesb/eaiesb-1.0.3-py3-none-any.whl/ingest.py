import pyspark
from pyspark.sql.types import IntegerType
from pyspark.sql import SparkSession
import logging
import logging.config
# import transform
# import persist

class Ingest:
    def __init__(self,spark):
        self.spark=spark

    def Ingest(self, csvinput):
        customer_df = self.spark.read.csv(csvinput, header=True)
        return customer_df

    def csv(filePath):
        spark = SparkSession.builder.appName("my first spark app").enableHiveSupport().getOrCreate()
        ingest_process = Ingest(spark)
        df = ingest_process.Ingest(filePath)
        df.show()
        return df

# uncomment everything in this file for testing
# if __name__ == '__main__':
    # df = Ingest.csv("G:\\Akhil\\python-workspace\\output\\retailstore.csv")
    # transformed_df = transform.Transform.drop(df)
    # persisted_df = persist.Persist.save(transformed_df, "G:\\Akhil\\python-workspace\\output\\transformed-retailstore")
