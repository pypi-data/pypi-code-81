
def get_dict_values(key, dictionary):
    if hasattr(dictionary, 'iteritems'):
        for k, v in dictionary.iteritems():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in get_dict_values(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in get_dict_values(key, d):
                        yield result