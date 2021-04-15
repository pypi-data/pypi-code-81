import logging.config
from pathlib import Path

import yaml

DIR = Path(__file__).parent.absolute()


def configureLogging():
    """."""
    with open(DIR / 'logging.yaml', 'r') as f:
        log_cfg = yaml.full_load(f)

    logging.config.dictConfig(log_cfg)
