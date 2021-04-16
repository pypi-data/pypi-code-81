import itertools
from operator import itemgetter


def sort(items: list, *keys):
    return sorted(items, key=itemgetter(*keys))


def group_by(items: list, *keys):

    results = []
    for key_values, items_iterator in itertools.groupby(sort(items, *keys), key=itemgetter(*keys)):
        result = dict([x for x in zip(keys, key_values if isinstance(key_values, tuple) else (key_values,))])
        result.update({'items': [x for x in items_iterator]})
        results.append(result)
    return results


def count(items: list, *keys):

    results = []
    for item in group_by(items, *keys):
        result = {key: item[key] for key in keys}
        result.update({'count': len(item['items'])})
        results.append(result)
    return results
