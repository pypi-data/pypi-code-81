from typing import Any, Callable, Dict, Iterable, List, Optional, Union

from d8s_dicts import dict_keys, dict_sort_by_keys, dict_sort_by_values, dict_values


def amb(validation_function: Callable[..., bool], *args: Any) -> Iterable[Any]:
    import itertools

    products = itertools.product(*args)
    for product in products:
        if validation_function(*product):
            yield product


def depth_first_traverse(
    data: Any,
    get_children_function: Callable[[Any], Optional[Iterable]],
    *,
    collect_items_function: Optional[Callable[[Any], Any]] = None
) -> Iterable[Any]:
    """Traverse the data in a depth-first manner.

    The get_children_function specifies how children will be identified from each node of the data.
    The collect_items_function, if provided, allows you to collect items from the data by...
     returning them from the collect_items_function.
    """
    children = get_children_function(data)

    if collect_items_function:
        yield collect_items_function(data)

    if children:
        for child in children:
            yield from depth_first_traverse(child, get_children_function, collect_items_function=collect_items_function)
    elif not children and not collect_items_function:
        yield data


def breadth_first_traverse(
    data: Any,
    get_children_function: Callable[[Any], Optional[Iterable]],
    *,
    collect_items_function: Optional[Callable[[Any], Any]] = None
) -> Iterable[Any]:
    """Traverse the data in a breadth-first manner.

    The get_children_function specifies how children will be identified from each node of the data.
    The collect_items_function, if provided, allows you to collect items from the data by...
     returning them from the collect_items_function.
    """
    container = [data]
    while len(container) > 0:
        node = container.pop(0)
        if collect_items_function:
            yield collect_items_function(node)

        children = get_children_function(node)
        if children:
            container.extend(children)
        elif not children and not collect_items_function:
            yield node


def genetic_algorithm_run(
    data: Iterable[Any],
    scoring_function: Callable[[Any], Union[int, float]],
    selection_function: Callable[[Dict[Any, Union[int, float]]], Iterable[Any]],
    mutation_function: Callable[[Iterable[Any]], Iterable[Any]],
    max_epochs: int,
) -> Dict[Any, Union[int, float]]:
    scored_data = {}
    for __ in range(max_epochs):
        scored_data = dict_sort_by_values({i: scoring_function(i) for i in data}, reverse=True)
        selected_values = selection_function(scored_data)
        data = mutation_function(selected_values)
    return scored_data


def genetic_algorithm_best_mutation_function(
    starting_values: Iterable[Any],
    generations: int,
    scoring_function: Callable[[Any], Union[int, float]],
    mutation_functions: List[Callable[[Any], Any]],
):
    """Find the best mutation function.

    The best function is the one which produces values from the starting values...
     that score the highest (as measured by the scoring_function) after generations.
    """
    import statistics

    results = {}

    # TODO: break this out into a genetic_algorithm function
    for mutation_function in mutation_functions:
        values = starting_values
        for generation in range(generations):
            scores = {i: scoring_function(i) for i in values}
            scores = dict_sort_by_keys(scores)
            # todo: keep track of the score data
            values = [mutation_function(val) for val in values]
        final_scores = scores
        average_score = statistics.mean(dict_values(final_scores))
        results[mutation_function] = average_score

    best_mutation_function = dict_keys(dict_sort_by_values(results, reverse=True))[0]
    return best_mutation_function
