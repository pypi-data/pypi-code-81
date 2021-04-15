import re
from collections import OrderedDict
from typing import Dict, Iterable, List

from d8s_dicts import dict_keys, dict_values
from d8s_python import python_ast_parse

from d8s_algorithms import (
    amb,
    breadth_first_traverse,
    depth_first_traverse,
    genetic_algorithm_best_mutation_function,
    genetic_algorithm_run,
)

TEST_DATA_1 = {'a': {'b': 1}, 'c': 2, 'd': 3, 'e': {'f': 4}}
TEST_DATA_2 = '''def test():
    """."""
    x = 10
    if x < 20:
        if x < 10:
            print('here')
        return x
    elif x < 30:
        return x
    else:
        x = x * 10
'''


def _get_children_1(data):
    if isinstance(data, dict):
        return dict_values(data)
    else:
        return None


def _get_children_2(data):
    children = []
    if hasattr(data, 'body'):
        children.extend(data.body)
    if hasattr(data, 'orelse'):
        children.extend(data.orelse)
    return children


def _collect_items_2(data):
    return data.__class__.__name__


def test_amb_docs_1():
    """These examples are taken from https://www.rosettacode.org/wiki/Amb#Python."""
    x = (1, 2, 3)
    y = (7, 6, 4, 5)
    assert list(amb(lambda x, y: x * y == 8, x, y)) == [(2, 4)]

    def match(x, y, z):
        return x * x + y * y == z * z

    data_range = range(1, 11)
    assert list(amb(match, data_range, data_range, data_range)) == [(3, 4, 5), (4, 3, 5), (6, 8, 10), (8, 6, 10)]

    l1 = ["the", "that", "a"]
    l2 = ["frog", "elephant", "thing"]
    l3 = ["walked", "treaded", "grows"]
    l4 = ["slowly", "quickly"]

    def is_match(a, b, c, d):
        return a[-1] == b[0] and b[-1] == c[0] and c[-1] == d[0]

    assert list(amb(is_match, l1, l2, l3, l4)) == [('that', 'thing', 'grows', 'slowly')]


def test_depth_first_traverse_docs_1():
    assert list(depth_first_traverse(TEST_DATA_1, _get_children_1)) == [1, 2, 3, 4]

    result = depth_first_traverse(python_ast_parse(TEST_DATA_2), _get_children_2)
    class_names = [i.__class__.__name__ for i in result]
    assert class_names == ['Expr', 'Assign', 'Expr', 'Return', 'Return', 'Assign']


def test_depth_first_traverse_docs_2():
    # this tests a situation where the function to get children and the collect_items_function (_get_children_1) will return None when given a list
    assert list(depth_first_traverse([1, 2, 3], _get_children_1, collect_items_function=_get_children_1)) == [None]


def test_depth_first_traverse_with_collection_function_docs():
    result = tuple(
        depth_first_traverse(python_ast_parse(TEST_DATA_2), _get_children_2, collect_items_function=_collect_items_2)
    )

    assert result == ('Module', 'FunctionDef', 'Expr', 'Assign', 'If', 'If', 'Expr', 'Return', 'If', 'Return', 'Assign')


def test_breadth_first_traverse_docs_1():
    assert list(breadth_first_traverse(TEST_DATA_1, _get_children_1)) == [2, 3, 1, 4]


def test_breadth_first_traverse_with_collection_function_docs():
    result = tuple(
        breadth_first_traverse(python_ast_parse(TEST_DATA_2), _get_children_2, collect_items_function=_collect_items_2)
    )
    assert result == ('Module', 'FunctionDef', 'Expr', 'Assign', 'If', 'If', 'Return', 'If', 'Expr', 'Return', 'Assign')


def test_genetic_algorithm_best_mutation_function_docs_1():
    def scoring_func(item: str) -> int:
        return item.count('1')

    def mutation_func_1(item: str) -> str:
        item = re.sub('0', '1', item, count=1)
        return item

    def mutation_func_2(item: str) -> str:
        item = re.sub('1', '0', item, count=1)
        return item

    starting_items = ['110', '010', '000', '111', '010']
    mutation_funcs = [mutation_func_1, mutation_func_2]
    result = genetic_algorithm_best_mutation_function(starting_items, 100, scoring_func, mutation_funcs)
    assert result == mutation_func_1


def test_genetic_algorithm_run_docs_1():
    def scoring_func(item: str) -> int:
        return item.count('1')

    def selection_func(data: Dict[str, int]) -> List[str]:
        return dict_keys(data)[:3]

    def mutation_func(items: List[str]) -> Iterable[str]:
        for i in items:
            yield re.sub('0', '10', i, count=1)

    starting_items = ['110', '010', '000', '111', '010']

    result = genetic_algorithm_run(starting_items, scoring_func, selection_func, mutation_func, 100)
    assert result == OrderedDict(
        [
            (
                '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111110',
                101,
            ),
            (
                '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111010',
                100,
            ),
            ('111', 3),
        ]
    )
