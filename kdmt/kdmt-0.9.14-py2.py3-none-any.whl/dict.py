
def nested_dict_get_values(key, dictionary):
    if hasattr(dictionary, 'items'):
        for k, v in dictionary.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in nested_dict_get_values(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in nested_dict_get_values(key, d):
                        yield result


def nested_dict_has_key(key, dictionary):

    if hasattr(dictionary, 'items'):
        for k, v in dictionary.items():
            if k == key:
                return True
            if isinstance(v, dict):
                if nested_dict_has_key(key, v):
                    return True
            elif isinstance(v, list):
                for d in v:
                    if nested_dict_has_key(key, d):
                        return True
