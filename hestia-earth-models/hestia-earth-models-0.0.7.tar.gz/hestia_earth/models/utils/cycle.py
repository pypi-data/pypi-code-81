from hestia_earth.utils.api import download_hestia


def _is_term_type_complete(cycle: dict, term_id: str):
    term = download_hestia(term_id)
    term_type = term.get('termType')
    data_completeness = cycle.get('dataCompleteness', {})
    return term_type in data_completeness and data_completeness[term_type] is True


def _is_term_type_incomplete(cycle: dict, term_id: str):
    term = download_hestia(term_id)
    term_type = term.get('termType')
    data_completeness = cycle.get('dataCompleteness', {})
    return term_type not in data_completeness or data_completeness[term_type] is False
