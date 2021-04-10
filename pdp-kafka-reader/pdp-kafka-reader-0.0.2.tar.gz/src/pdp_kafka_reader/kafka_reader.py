from typing import Any, Dict, Optional

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.column import Column, _to_java_column


class KafkaReader:
    def __init__(self, spark: SparkSession):
        self._spark = spark

    def read(self, options: Dict[str, Any], topic: Optional[str] = None) -> DataFrame:
        """
        Read data from kafka using kafka options. If you define topic argument,
        it will override `subscribe` option in `options` dictionary.
        """
        if topic:
            options["subscribe"] = topic
        return self._spark.read.format("kafka").options(**options).load()


class KafkaAvroReader(KafkaReader):
    def read_avro(
        self,
        options: Dict[str, Any],
        schema: str,
        topic: Optional[str] = None,
    ) -> DataFrame:
        """
        Read messages from kafka and deserialize `value` column into `avro`.
        """
        df = self.read(options, topic)
        df = df.withColumn("avro", self._from_avro("value", schema)).drop("value")
        return df

    def _from_avro(self, column: str, schema: str):
        sc = self._spark.sparkContext
        avro = sc._jvm.org.apache.spark.sql.avro
        f = getattr(getattr(avro, "package$"), "MODULE$").from_avro
        return Column(f(_to_java_column(column), schema))


if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path

    from pdp_kafka_reader.transform import to_hive_format

    parser = argparse.ArgumentParser(
        prog="Kafka Avro export",
        description="Read messages from Kafka, deserialize Avro and export them into CSV.",
    )
    parser.add_argument(
        "-k",
        "--kafka-options",
        type=Path,
        required=True,
        help="Config file with Kafka options in JSON format",
    )
    parser.add_argument(
        "-s",
        "--schema",
        type=Path,
        required=True,
        help="Avro schema in JSON format",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        required=True,
        help="Output file where messages will be stored in JSON format",
    )
    parser.add_argument(
        "-t",
        "--topic",
        type=str,
        required=False,
        default=None,
        help="Kafka topic to read from",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        required=False,
        default=None,
        help="Maximum number of messages collected to driver",
    )
    args = parser.parse_args()

    with args.kafka_options.open("rb") as fp:
        kafka_options = json.load(fp)

    with args.schema.open("r") as fp:
        avro_schema = fp.read()

    spark = SparkSession.builder.appName("COCZ-KafkaReader").getOrCreate()

    reader = KafkaAvroReader(spark)
    df = reader.read_avro(kafka_options, avro_schema, args.topic)
    df = to_hive_format(df)
    df = df.toPandas()
    df.to_csv(args.output, index=False)
