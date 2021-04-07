# def inject_feature_dependencies(feature, feature_map) -> dict:
#     """
#
#     :param feature:
#     :param feature_map:
#     :return:
#     """
#     from camtono.parser.clean import set_tree_value
#
#     for dependency in feature.get('dependencies', []):
#         feature['query_ast'], index = set_tree_value(json=feature['query_ast'], locations=dependency['locations'],
#                                                      val=feature_map[dependency['id']]['query_ast'], reverse_index=1)
#         # TODO update input locations
#         feature['inputs'] += dependency['inputs']
#     return feature
#
#
# def update_dependency_inputs(dependency_locations, dependency_inputs):
#     from copy import deepcopy
#     from camtono.parser.clean import set_tree_value
#     for dependency_input in dependency_inputs:
#         location = deepcopy(dependency_locations)
