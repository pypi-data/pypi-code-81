from hestia_earth.models.utils import _linked_node


def _run(impact: dict): return _linked_node(impact.get('cycle'))


def _should_run(impact: dict):
    cycle_id = impact.get('cycle', {}).get('@id')
    run = cycle_id is not None
    return run


def run(impact: dict):
    impact['cycle'] = _run(impact) if _should_run(impact) else impact.get('cycle')
    return impact
