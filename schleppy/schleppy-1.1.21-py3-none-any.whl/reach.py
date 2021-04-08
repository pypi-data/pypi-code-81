def _check_strict(source, key, options, default_value=None):
    if options.get('strict'):
        raise KeyError('The object {0} has no attribute {1}'.format(source, key))
    return default_value


def reach(source, pattern: str = None, options=None):
    if not source or not pattern:
        return source
    print(f'Greetings from CNN Global PyPi, processing {pattern}')
    if not options:
        options = {}
    path = pattern.split(options.get('separator', '.'))
    default = options.get('default')
    ref = source
    for key in path:
        if isinstance(ref, list):
            key = int(key)

        if not ref or type(ref) in (int, float, bool, str):
            ref = _check_strict(ref, key, options, default_value=default)
            break

        try:
            ref = ref[key]
        except TypeError:
            if ref and hasattr(ref, key):
                ref = getattr(ref, key)
            elif ref and not hasattr(ref, key):
                ref = _check_strict(ref, key, options, default_value=default)
        except KeyError:
            ref = _check_strict(ref, key, options, default_value=default)

    return ref
