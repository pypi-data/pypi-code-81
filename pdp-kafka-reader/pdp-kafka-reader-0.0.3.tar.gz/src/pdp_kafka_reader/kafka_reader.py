from argparse import Namespace
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


def _export(
    reader: KafkaReader,
    kafka_options: Dict[str, Any],
    args: Namespace,
) -> DataFrame:
    return reader.read(kafka_options, args.topic)


def _export_avro(
    reader: KafkaAvroReader,
    kafka_options: Dict[str, Any],
    args: Namespace,
) -> DataFrame:
    from pdp_kafka_reader.transform import to_hive_format

    with args.schema.open("r") as fp:
        avro_schema = fp.read()

    df = reader.read_avro(kafka_options, avro_schema, args.topic)
    if not args.no_unpack:
        df = to_hive_format(df)
    return df


if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser(
        prog="kafka-reader",
        description="Read and export messages from Kafka",
    )
    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = "command"

    parser_common = argparse.ArgumentParser(add_help=False)
    parser_common.add_argument(
        "-k",
        "--kafka-options",
        type=Path,
        required=True,
        help="Config file with Kafka options in JSON format",
    )
    parser_common.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Output file path",
    )
    parser_common.add_argument(
        "-f",
        "--format",
        choices=["csv", "parquet"],
        required=False,
        default="parquet",
        help="Output format",
    )
    parser_common.add_argument(
        "-t",
        "--topic",
        type=str,
        required=False,
        default=None,
        help="Kafka topic to read data from",
    )
    parser_common.add_argument(
        "-l",
        "--limit",
        type=int,
        required=False,
        default=None,
        help="Maximum number of messages collected to driver",
    )

    # create the parser for the "export" command
    parser_export = subparsers.add_parser(
        "export",
        parents=[parser_common],
        help="Export messages",
    )
    parser_export.set_defaults(func=_export)

    # create the parser for the "export-avro" command
    parser_export_avro = subparsers.add_parser(
        "export-avro",
        parents=[parser_common],
        help="Deserialize and export Avro messages",
    )
    parser_export_avro.set_defaults(func=_export_avro)
    parser_export_avro.add_argument(
        "-s",
        "--schema",
        type=Path,
        required=True,
        help="Avro schema in JSON format",
    )
    parser_export_avro.add_argument(
        "--no-unpack",
        action="store_true",
        default=False,
        help="Do not unpack Avro structures into flat columns",
    )

    args = parser.parse_args()

    with args.kafka_options.open("rb") as fp:
        kafka_options = json.load(fp)

    # fetch data
    spark = SparkSession.builder.appName("COCZ-KafkaReader").getOrCreate()
    reader = KafkaAvroReader(spark)
    df = args.func(reader, kafka_options, args)

    if args.limit:
        df = df.limit(args.limit)

    df.write.format(args.format).option("header", True).save(args.output)
