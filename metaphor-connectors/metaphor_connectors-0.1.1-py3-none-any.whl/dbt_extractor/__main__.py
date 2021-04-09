import argparse
import logging

from .extractor import DbtExtractor, DbtRunConfig

logging.basicConfig(
    format="%(asctime)s %(levelname)s - %(message)s", level=logging.INFO
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DBT metadata extractor")
    for parameter in DbtRunConfig.parameters():
        parser.add_argument(parameter, metavar=parameter, type=str, help=parameter)
    args = parser.parse_args()

    extractor = DbtExtractor()
    extractor.run(config=DbtRunConfig.build(vars(args)))
