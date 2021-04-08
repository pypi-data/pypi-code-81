from schleppy.reach import reach


def transform(source, pattern: dict, options=None):
    if isinstance(source, list):
        results = []
        for item in source:
            results.append(transform(item, pattern, options))

        return results
    if not options:
        options = {}

    result = {}

    for key in pattern:
        path = key.split(options.get('separator', '.'))

        source_path = pattern[key]

        if not isinstance(source_path, str):
            raise ValueError('All mappings must be "(0)" delimited strings'.format(options.get('separator', '.')))

        res = result

        while len(path) > 1:
            segment = path.pop(0)
            if not res.get(segment):
                res[segment] = {}
            res = res[segment]

        segment = path.pop(0)
        res[segment] = reach(source, source_path, options)

    return result
