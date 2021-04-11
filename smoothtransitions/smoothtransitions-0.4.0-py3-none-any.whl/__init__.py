import logging
import logging.config
import os

import yaml

dirname = os.path.dirname(__file__)

with open(f"{dirname}/logger_config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
