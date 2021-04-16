from hestia_earth.models.log import logger


def _run(impact: dict):
    practices = impact.get('cycle', {}).get('practices', [])
    value = next((p for p in practices if p.get('term').get('@id') == 'irrigated'), None) is not None
    logger.info('value=%s', value)
    return value


def _should_run(impact: dict):
    practices = impact.get('cycle', {}).get('practices', [])
    should_run = len(practices) > 0
    logger.info('should_run=%s', should_run)
    return should_run


def run(impact: dict): return _run(impact) if _should_run(impact) else False
