from functools import reduce
from hestia_earth.utils.model import find_primary_product, find_term_match
from hestia_earth.utils.tools import safe_parse_float

from hestia_earth.models.log import logger
from hestia_earth.models.utils import _average
from hestia_earth.models.utils.product import _new_product
from hestia_earth.models.utils.cycle import _is_term_type_incomplete
from hestia_earth.models.ipcc2006Tier1.aboveGroundCropResidueTotal import TERM_ID as TOTAL_TERM_ID
from . import aboveGroundCropResidueBurnt
from hestia_earth.models.ipcc2006Tier1.residue import residueBurnt
from . import aboveGroundCropResidueIncorporated
from hestia_earth.models.ipcc2006Tier1.residue import residueIncorporated
from . import aboveGroundCropResidueLeftOnField
from . import aboveGroundCropResidueRemoved
from hestia_earth.models.ipcc2006Tier1.residue import residueRemoved

MODELS = [
    {'term': aboveGroundCropResidueRemoved, 'practice': residueRemoved},
    {'term': aboveGroundCropResidueIncorporated, 'practice': residueIncorporated},
    {'term': aboveGroundCropResidueBurnt, 'practice': residueBurnt}
]
REMAINING_MODEL = aboveGroundCropResidueLeftOnField


def _get_practice_value(term_id: str, cycle: dict) -> float:
    value = find_term_match(cycle.get('practices', []), term_id).get('value')
    return safe_parse_float(value) / 100


def _product(term_id: str, value: float):
    logger.info('term=%s, value=%s', term_id, value)
    product = _new_product(term_id)
    product['value'] = [value]
    return product


def _should_run_model(model, cycle: dict, primary_product: dict):
    term_id = model.get('term').TERM_ID
    practice_value = _get_practice_value(model.get('practice').TERM_ID, cycle)
    should_run = practice_value is not None \
        and model.get('term').should_run(cycle, primary_product) \
        and find_term_match(cycle.get('products', []), term_id, None) is None
    logger.info('term=%s, should_run=%s', term_id, should_run)
    return should_run, practice_value


def _run_model(model, cycle: dict, primary_product: dict, total_value: float, products: list):
    should_run, practice_value = _should_run_model(model, cycle, primary_product)
    return model.get('term').run(cycle, primary_product, total_value, practice_value, products) if should_run else None


def _model_value(model, products: list):
    values = find_term_match(products, model.TERM_ID).get('value', [])
    return _average(values) if len(values) > 0 else 0


def _run(cycle: dict, total_values: list):
    products = cycle.get('products', [])
    primary_product = find_primary_product(cycle)
    total_value = _average(total_values)
    # first, calculate the remaining value available after applying all user-uploaded data
    remaining_value = reduce(
        lambda prev, model: prev - _model_value(model.get('term'), products),
        MODELS + [{'term': REMAINING_MODEL}],
        total_value
    )

    values = []
    # then run every model in order up to the remaining value
    for model in MODELS:
        term_id = model.get('term').TERM_ID
        value = _run_model(model, cycle, primary_product, total_value, values)
        logger.debug('term=%s, value=%s', term_id, value)
        if remaining_value > 0 and value is not None and value > 0:
            value = value if value < remaining_value else remaining_value
            values.extend([_product(term_id, value)])
            remaining_value = remaining_value - value
            if remaining_value == 0:
                logger.debug('no more residue, stopping')
                break

    return values + [
        # whatever remains is "left on field"
        _product(REMAINING_MODEL.TERM_ID, remaining_value)
    ] if remaining_value > 0 else values


def _should_run(cycle: dict):
    total_values = find_term_match(cycle.get('products', []), TOTAL_TERM_ID).get('value', [])
    should_run = len(total_values) > 0 and _is_term_type_incomplete(cycle, TOTAL_TERM_ID)
    logger.info('should_run=%s', should_run)
    return should_run, total_values


def run(cycle: dict):
    should_run, total_values = _should_run(cycle)
    return _run(cycle, total_values) if should_run else []
