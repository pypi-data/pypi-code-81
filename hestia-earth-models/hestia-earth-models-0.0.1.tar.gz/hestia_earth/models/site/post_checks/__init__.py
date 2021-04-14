from os.path import dirname, abspath
import sys
from .measurement_value import run as measurement_value

CURRENT_DIR = dirname(abspath(__file__)) + '/'
sys.path.append(CURRENT_DIR)
MODELS = [
    measurement_value
]


def run(site: dict):
    return list(map(lambda model: model(site), MODELS))
