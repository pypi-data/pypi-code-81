from hestia_earth.models.utils import _linked_node


def _run(cycle: dict): return _linked_node(cycle.get('site'))


def _should_run(cycle: dict):
    site_id = cycle.get('site', {}).get('@id')
    run = site_id is not None
    return run


def run(cycle: dict):
    cycle['site'] = _run(cycle) if _should_run(cycle) else cycle.get('site')
    return cycle
