from hestia_earth.utils.lookup import get_table_value, download_lookup, column_name

from hestia_earth.models.log import logger


def _is_organic(lookup, term_id: str):
    return get_table_value(lookup, 'termid', term_id, column_name('isOrganic')) == 'organic'


def _run(impact: dict):
    lookup = download_lookup('standardsLabels.csv')
    practices = impact.get('cycle', {}).get('practices', [])
    value = any([_is_organic(lookup, p.get('term').get('@id')) for p in practices])
    logger.info('value=%s', value)
    return value


def _should_run(impact: dict):
    practices = impact.get('cycle', {}).get('practices', [])
    should_run = len(practices) > 0
    logger.info('should_run=%s', should_run)
    return should_run


def run(impact: dict): return _run(impact) if _should_run(impact) else False
