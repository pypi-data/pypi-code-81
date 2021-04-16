from dateutil.relativedelta import relativedelta
from hestia_earth.utils.tools import safe_parse_date

from hestia_earth.models.log import logger
from hestia_earth.models.utils import _is_in_days


def _run(cycle: dict):
    days = -float(cycle.get('cycleDuration'))
    start_date = (safe_parse_date(cycle.get('endDate')) + relativedelta(days=days)).strftime('%Y-%m-%d')
    logger.info('value=%s', start_date)
    return start_date


def _should_run(cycle: dict):
    should_run = _is_in_days(cycle.get('endDate')) \
        and cycle.get('cycleDuration') is not None \
        and cycle.get('startDate') is None
    logger.info('should_run=%s', should_run)
    return should_run


def run(cycle: dict): return {**cycle, 'startDate': _run(cycle)} if _should_run(cycle) else cycle
