
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


def nested_dict_get_value(key, dictionary):

    if hasattr(dictionary, 'items'):
        for k, v in dictionary.items():
            if k == key:
                return v
            if isinstance(v, dict):
                val= nested_dict_get_value(key, v)
                if val:
                     return val
            elif isinstance(v, list):
                for d in v:
                    val = nested_dict_get_value(key, d)
                    if val:
                        return val

if __name__=="__main__":
    dic={
        'k1': 'v1',
        'k2': 'v2',
        'k3':{
            'k31': 'v31'
        }
    }
    print(nested_dict_has_key('k32', dic))