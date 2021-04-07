def generate_derivative(definition: dict, feature_map: dict) -> tuple:
    """Create a derived query ast based on a definition and map of all used features

    :param definition: camtono derivative definition
    :param feature_map:
    :return:
    """
    from camtono.derivatives.filters import flatten_filters, generate_filter_query_sets
    # from camtono.derivatives.dependencies import inject_feature_dependencies
    from camtono.parser.clean import prune_ast
    flattened_filters = flatten_filters(filters=definition.get('filters', dict()))
    complete_feature = {
        k: v for k, v in
        feature_map.items()
    }
    default_filters = {i['attribute']: i['value'] for i in definition.get('default_filters', [])}
    default_input = dict(grain=definition['grain'])
    definition_features = {i['feature_id']: i for i in definition.get('features', [])}
    query_sets, filter_features = generate_filter_query_sets(flattened_filters=flattened_filters, features=feature_map,
                                                             default_filters=default_filters,
                                                             default_input=default_input,
                                                             definition_features=definition_features)
    print('filter_features')
    print(filter_features)
    derived_ast = generate_query_skeleton(query_sets=query_sets, grain=definition['grain'], features=complete_feature,
                                          definition_features=definition_features, filter_features=filter_features)
    return prune_ast(json=derived_ast)


def generate_query_skeleton(query_sets, grain, features, definition_features, filter_features):
    base_query = {'with': [], 'from': [], 'select': [{"value": "base.{grain}".format(grain=grain)}]}
    union = []
    # TODO handle default input
    for idx, query_set in enumerate(query_sets):
        name, sub_ast = generate_filter_statements(idx=idx, query_set=query_set, grain=grain)
        base_query['with'].append({"value": sub_ast, "name": name})
        union.append(
            {"select": [{"value": "{grain}".format(grain=grain)}], "from": [dict(name=name, value=name)]})
    if union:
        base_query['from'].append(dict(value=dict(union_distinct=union), name='base'))
    for idx, feature in enumerate({k for k in definition_features.keys() if k not in filter_features.keys()}):
        sub_ast = generate_feature_statement(idx=idx, feature=features[feature],
                                             feature_input=definition_features[feature].get('input', []), grain=grain)
        if base_query['from']:
            sub_ast = dict(join=sub_ast, using=grain)
        else:
            sub_ast['name'] = 'base'
        base_query['from'].append(sub_ast)

    return base_query


def generate_filter_statements(idx, query_set, grain):
    name = "sub_filter_{}".format(idx)
    sub_ast = {"select": [{"value": "f" + str(idx) + "t0.{grain}".format(grain=grain)}], "from": []}
    for query_idx, query in enumerate(query_set):
        # TODO setting join criteria
        from_ = dict(
            value=query,
            name='f{filter_index}t{query_index}'.format(
                filter_index=idx, query_index=query_idx
            )
        )
        if sub_ast['from']:
            sub_ast['from'].append(dict(join=from_, using='{grain}'.format(grain=grain)))
        else:
            sub_ast['from'].append(from_)
    return name, sub_ast


def generate_feature_statement(idx, feature, feature_input, grain):
    from camtono.derivatives.filters import trim_feature_input
    name = 'sub_feature_{}'.format(idx)
    ast = dict(name=name, value=trim_feature_input(
        feature=feature, set_filters=dict(), default_filters=dict(), feature_input=feature_input,
        default_input=dict(grain=grain)
    ))
    return ast
