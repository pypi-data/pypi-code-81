def flatten_filters(filters: dict) -> tuple:
    """

    :param filters:
    :param default_filters:
    :return:
    """
    new_filters = filters
    flattened_filters = flatten_filter(filters=new_filters)
    return flattened_filters


def flatten_filter(filters, list_string='filters', operator_string='item'):
    """Flattens nested pyparser syntax into a single layer

    :param filters:
    :param list_string:
    :param operator_string: string key of the pyparser operator
    :return: flatted list of lists of base operators
    """
    flattened_filter = list()
    operator = filters[operator_string].lower()
    for idx, i in enumerate(filters[list_string]):
        new_filters = i
        if isinstance(i.get(list_string), list):
            new_filters = flatten_filter(filters=i, list_string=list_string, operator_string=operator_string)
        flattened_filter = unify_sets(existing=flattened_filter, new=new_filters, operator=operator)
    return flattened_filter


def unify_sets(existing, new, operator):
    """Join two sets of statements based on boolean operator

    :param existing: List of existing statements
    :param new: New statements to add to the set
    :param operator: boolean operator and, or, not
    :return: combined set of sets based on boolean operation
    """
    import itertools
    unified = []
    if isinstance(new, dict):
        new = [new]
    if not isinstance(new[0], list):
        new = [new]
    if not existing and operator in ['and', 'or']:
        unified = new
    elif operator == 'or':
        unified = existing + new
    elif operator == 'and':
        if existing:
            for a, b in itertools.product(existing, new):
                unified.append([*a, *b])
        else:
            unified.append(new)
    elif operator == 'not':
        pass
        # for s in new:
        #     subset = []
        #     for x in s:
        #         x['not'] = bool(-x.get('not', False))
        #         subset = unify_sets(existing=subset, new=x, operator='or')
        #     unified = unify_sets(existing=unified, new=subset, operator='and')
    return unified


def generate_filter_query_sets(flattened_filters, features, default_filters: dict, default_input: dict,
                               definition_features: dict):
    """

    :param flattened_filters:
    :param features:
    :return:
    """
    query_sets, filter_features = [], dict()
    for idx, filter_set in enumerate(flattened_filters):
        set_features, skip = define_set_features(filter_set=filter_set)
        filter_features.update(set_features)
        query_set = []
        for feature, filters in set_features.items():
            ast = trim_feature_input(
                feature=features[feature], set_filters=set_features[feature],
                default_input=default_input, default_filters=default_filters,
                feature_input=definition_features[feature]['input']
            )
            query_set.append(ast)
        if not skip:
            query_sets.append(query_set)
    return query_sets, filter_features


def define_set_features(filter_set):
    """Processes flattened filter groups into a set of features

    :param filter_set: flattened list of filters
    :return: tuple of a dict of features and attributes and a flag to skip this particular filter group
    """
    features = dict()
    skip = False
    for f in filter_set:
        if skip:
            continue
        if f['feature_id'] not in features.keys():
            features[f['feature_id']] = dict()
        if f['attribute'] not in features[f['feature_id']].keys():
            features[f['feature_id']][f['attribute']] = {'not': f.get('not', False), 'value': f['value']}
    return features, skip


def trim_feature_input(feature: dict, set_filters: dict, default_filters: dict, feature_input: dict,
                       default_input: dict) -> tuple:
    """Remove all unnecessary query input from the query_ast

    :param feature: feature dict
    :param variables: dict of variables used for string formatting
    :param default_variables:
    :param feature_input:
    :param prefix:
    :return: feature dict with cleaned query_ast
    """
    from copy import deepcopy
    ast = deepcopy(feature['query_ast'])

    for query_input in feature['inputs']:
        if all(query_input['name'] not in i.keys() for i in
               [set_filters, default_input, default_filters, feature_input]):
            v = None
        elif any(query_input['name'] in i.keys() for i in [set_filters, default_filters]):
            v = set_filters[query_input['name']]['value'] if query_input['name'] in set_filters else default_filters[
                query_input['name']]
        else:
            v = feature_input[query_input['name']] if query_input['name'] in feature_input else default_input[
                query_input['name']]
        ast = update_feature_input(ast=ast, v=v, query_input=query_input)

    return ast


def update_feature_input(ast, v, query_input):
    new_val = v
    if query_input['is_literal']:
        if isinstance(v, str):
            new_val = {'literal': v}
        elif isinstance(v, list):
            new_val = [{'literal': i} for i in v]
    for i in query_input['locations']:
        if not query_input['is_literal']:
            new_val = i['value'].replace('{' + query_input['name'] + '}', v)
        ast = set_tree_value(
            json=ast, locations=i['location'],
            val=new_val, target_index=i['level'] - 1 if i['wrapped_literal'] else i['level']
        )
    return ast


def set_value(val, **kwargs):
    """ Convenience function to set value for set_tree_value

    :param val: value to return
    :param kwargs: all other values
    :return: the value provided
    """
    return val


def set_tree_value(json, locations, target_index, current_index=0, replace_func=set_value, val=None):
    """ Set the

    :param json: dictionary
    :param locations: dictionary of the paths containing the location of a target value
    :param replace_func: function to apply when setting value receives val and json
    :param val: value to set
    :param target_index: location from the start of the tree where the replacement function should be applied
    :param current_index: current location in the tree
    :return: dictionary with the newly assigned values.
    """
    if locations and current_index < target_index and (isinstance(json, dict) or isinstance(json, list)):
        for k, v in locations.items():
            if k.isdigit():
                k = int(k)
            v = set_tree_value(json=json[k], locations=v, val=val, replace_func=replace_func,
                               target_index=target_index, current_index=current_index + 1)
            json[k] = v
        return json
    elif current_index == target_index:
        return val
    else:
        raise Exception("Invalid Location / Index")


def replace_string(json, old, new, **kwargs):
    return json.replace(old, new)
