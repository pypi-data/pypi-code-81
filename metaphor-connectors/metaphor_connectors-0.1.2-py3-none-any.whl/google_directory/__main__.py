import argparse
import json
import logging

from .extractor import GoogleDirectoryExtractor, GoogleDirectoryRunConfig

logging.basicConfig(
    format="%(asctime)s %(levelname)s - %(message)s", level=logging.INFO
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google directory connector")
    parser.add_argument("token", help="Path to the token file")
    args = parser.parse_args()

    extractor = GoogleDirectoryExtractor()
    config = json.load(open(args.token))
    extractor.run(config=config)
