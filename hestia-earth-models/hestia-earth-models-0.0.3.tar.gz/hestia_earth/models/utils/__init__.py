from os.path import dirname, abspath
import sys
import re
from functools import reduce
from statistics import mean

from hestia_earth.utils.api import download_hestia

CURRENT_DIR = dirname(abspath(__file__)) + '/'
sys.path.append(CURRENT_DIR)


def _term_id(term): return term.get('@id') if isinstance(term, dict) else term


def _linked_node(node: dict):
    return {key: node[key] for key in ['@type', '@id', 'name', 'termType', 'units'] if key in node}


def _average(value, default=0): return mean(value) if value is not None and isinstance(value, list) else default


def _is_in_days(date: str):
    return date is not None and re.compile(r'^[\d]{4}\-[\d]{2}\-[\d]{2}').match(date) is not None


def _run_in_serie(data: dict, models: list): return reduce(lambda prev, model: model(prev), models, data)


def _load_calculated_node(node, type: str):
    # TODO: update api to fallback from dataState to original
    try:
        try:
            return download_hestia(node.get('@id'), type, 'recalculated')
        except Exception:
            return download_hestia(node.get('@id'), type, 'gapFilled')
    except Exception:
        return download_hestia(node.get('@id'), type)
