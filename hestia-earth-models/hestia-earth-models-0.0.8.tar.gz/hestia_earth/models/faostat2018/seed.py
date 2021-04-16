from hestia_earth.schema import InputStatsDefinition
from hestia_earth.utils.lookup import get_table_value, download_lookup
from hestia_earth.utils.tools import non_empty_list, safe_parse_float

from hestia_earth.models.log import logger
from hestia_earth.models.utils.input import _new_input
from hestia_earth.models.utils.cycle import _is_term_type_incomplete

TERM_ID = 'seed'


def _run_product(product: dict):
    lookup = download_lookup('crop.csv', True)
    term_id = product.get('term', {}).get('@id', '')
    product_value = product.get('value', [None])[0]

    in_lookup = term_id in list(lookup.termid)
    logger.debug('Found lookup data for Term: %s? %s', term_id, in_lookup)

    if in_lookup and product_value is not None:
        average = safe_parse_float(get_table_value(lookup, 'termid', term_id, 'seed_output_kg_avg'), None)
        sd = safe_parse_float(get_table_value(lookup, 'termid', term_id, 'seed_output_kg_sd'), None)
        if average is not None:
            value = average * product_value
            logger.info('term=%s, value=%s', TERM_ID, value)
            input = _new_input(TERM_ID)
            input['value'] = [value]
            input['statsDefinition'] = InputStatsDefinition.REGIONS.value
            if sd is not None:
                input['sd'] = [sd]
            return input
    return None


def _run(cycle: dict):
    return non_empty_list(map(_run_product, cycle.get('products', [])))


def _should_run(cycle: dict):
    should_run = _is_term_type_incomplete(cycle, TERM_ID)
    logger.info('term=%s, should_run=%s', TERM_ID, should_run)
    return should_run


def run(cycle: dict): return _run(cycle) if _should_run(cycle) else []
