
def bested_dict_get_values(key, dictionary):
    if hasattr(dictionary, 'iteritems'):
        for k, v in dictionary.iteritems():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in bested_dict_get_values(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in bested_dict_get_values(key, d):
                        yield result


def neted_dict_has_key(key, dictionary):

    if hasattr(dictionary, 'iteritems'):
        for k, v in dictionary.iteritems():
            if k == key:
                return True
            if isinstance(v, dict):
                return neted_dict_has_key(key, v)
            elif isinstance(v, list):
                for d in v:
                    if neted_dict_has_key(key, d):
                        return True
    return False
