from pollination_dsl.alias import InputAlias
from queenbee.io.common import IOAliasHandler


"""Alias for yes/no inputs about whether to filter design days."""
filter_des_days_input = [
    InputAlias.any(
        name='filter_des_days',
        description='A boolean to note whether the ddy file should be filtered to only '
        'include 99.6 and 0.4 design days (True) or all design days in the ddy file '
        'should be used (False).',
        default=True,
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python',
                module='pollination_handlers.inputs.bool_options',
                function='filter_des_days_to_str'
            )
        ]
    )
]


"""Alias for yes/no inputs about whether to use multipliers."""
use_multiplier_input = [
    InputAlias.any(
        name='use_multiplier',
        description='If True, the multipliers on each Building Stories will be '
        'passed along to the generated Honeybee Room objects, indicating the '
        'simulation will be run once for each unique room and then results '
        'will be multiplied. If False, full geometry objects will be written '
        'for each and every story in the building such that all resulting '
        'multipliers will be 1. (Default: False).',
        default=False,
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python',
                module='pollination_handlers.inputs.bool_options',
                function='use_multiplier_to_str'
            )
        ]
    )
]


"""Alias for yes/no inputs about whether a building is residential."""
is_residential_input = [
    InputAlias.any(
        name='is_residential',
        description='A boolean to note whether the model represents a residential '
        'or nonresidential building.',
        default=False,
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python',
                module='pollination_handlers.inputs.bool_options',
                function='is_residential_to_str'
            )
        ]
    )
]


"""Alias for yes/no inputs about whether a comfort map should be for SET."""
write_set_map_input = [
    InputAlias.any(
        name='write_set_map',
        description='A boolean to note whether the output temperature CSV should '
        'record Operative Temperature or Standard Effective Temperature (SET). '
        'SET is relatively intense to compute and so only recording Operative '
        'Temperature can greatly reduce run time, particularly when air speeds '
        'are low. However, SET accounts for all 6 PMV model inputs and so is a '
        'more representative "feels-like" temperature for the PMV model.',
        default=False,
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python',
                module='pollination_handlers.inputs.bool_options',
                function='write_set_map_to_str'
            )
        ]
    )
]
