import argparse
import logging

from .extractor import PostgresqlExtractor, PostgresqlRunConfig

logging.basicConfig(
    format="%(asctime)s %(levelname)s - %(message)s", level=logging.INFO
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PostgreSQL metadata extractor")
    for parameter in PostgresqlRunConfig.parameters():
        parser.add_argument(parameter, metavar=parameter, type=str, help=parameter)
    parser.add_argument(
        "--redshift",
        dest="redshift",
        default=False,
        action="store_true",
        help="targeting redshift, default is postgresql",
    )
    parser.add_argument(
        "--port",
        dest="port",
        action="store",
        type=int,
        default=5432,
        help="database port, default postgresql 5432, for redshift use 5439",
    )
    args = parser.parse_args()

    extractor = PostgresqlExtractor()
    extractor.run(config=PostgresqlRunConfig.build(vars(args)))
