import argparse
import logging

from .extractor import SnowflakeExtractor, SnowflakeRunConfig

logging.basicConfig(
    format="%(asctime)s %(levelname)s - %(message)s", level=logging.INFO
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Snowflake metadata extractor")
    for parameter in SnowflakeRunConfig.parameters():
        parser.add_argument(parameter, metavar=parameter, type=str, help=parameter)
    args = parser.parse_args()

    extractor = SnowflakeExtractor()
    extractor.run(config=SnowflakeRunConfig.build(vars(args)))
