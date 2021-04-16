from os.path import dirname, basename, isfile, join, abspath
from importlib import import_module
import sys
import glob
from functools import reduce
from hestia_earth.utils.model import find_primary_product, find_term_match
from hestia_earth.utils.tools import safe_parse_float

from hestia_earth.models.log import logger
from hestia_earth.models.utils.practice import _new_practice

CURRENT_DIR = dirname(abspath(__file__)) + '/'
sys.path.append(CURRENT_DIR)
PKG = 'hestia_earth.models.ipcc2006Tier1.residue'
modules = glob.glob(join(dirname(__file__), '*.py'))
modules = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
modules = [{'key': m, 'module': import_module(f".{m}", package=PKG)} for m in modules]
MODELS = list(filter(lambda m: hasattr(m.get('module'), 'run'), modules))
REMAINING_MODEL = next((m for m in modules if not hasattr(m.get('module'), 'run')), None)


def _practice(term_id: str, value: float):
    logger.info('term=%s, value=%s',  term_id, value)
    practice = _new_practice(term_id)
    practice['value'] = value
    return practice


def _should_run_model(term_id: str, cycle: dict):
    should_run = find_term_match(cycle.get('practices', []), term_id, None) is None
    logger.info('term=%s, should_run=%s', term_id, should_run)
    return should_run


def _run_model(model: dict, cycle: dict, primary_product: dict):
    should_run = _should_run_model(model.get('key'), cycle)
    run = getattr(model.get('module'), 'run')
    return run(cycle, primary_product) if should_run else None


def _model_value(term_id: str, practices: list):
    value = find_term_match(practices, term_id).get('value', 0)
    return safe_parse_float(value, 0)


def run(cycle: dict):
    practices = cycle.get('practices', [])
    primary_product = find_primary_product(cycle)
    # first, calculate the remaining value available after applying all user-uploaded data
    remaining_value = reduce(
        lambda prev, model: prev - _model_value(model.get('key'), practices),
        MODELS + [REMAINING_MODEL],
        100
    )

    values = []
    # then runevery model in order up to the remaining value
    for model in MODELS:
        value = _run_model(model, cycle, primary_product)
        logger.debug('term=%s, value=%s', model.get('key'), value)
        if remaining_value > 0 and value is not None and value > 0:
            value = value if value < remaining_value else remaining_value
            values.extend([_practice(model.get('key'), value)])
            remaining_value = remaining_value - value
            if remaining_value == 0:
                logger.debug('no more residue, stopping')
                break

    return values + [
        # whatever remains is "left on field"
        _practice(REMAINING_MODEL.get('key'), remaining_value)
    ] if remaining_value > 0 else values
