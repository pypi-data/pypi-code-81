from pollination_dsl.alias import InputAlias
from queenbee.io.common import IOAliasHandler


"""Alias inputs that expect a HBJSON model file as the recipe input."""
hbjson_model_input = [
    # grasshopper Alias
    InputAlias.any(
        name='model',
        description='A Honeybee Model to simulate or the path to a HBJSON file '
        'of a Model. This can also be the path to a HBpkl file, though this is only '
        'recommended for cases where the model is extremely large.',
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python', module='pollination_handlers.inputs.model',
                function='model_to_json'
            ),
            IOAliasHandler(
                language='csharp', module='Pollination.RhinoHandlers',
                function='HBModelToJSON'
            )
        ]
    ),
    # Rhino alias
    InputAlias.linked(
        name='model',
        description='This input links the model to Rhino model.',
        platform=['rhino'],
        handler=[
            IOAliasHandler(
                language='csharp', module='Pollination.RhinoHandlers',
                function='RhinoHBModelToJSON'
            )
        ]
    )
]


"""Alias inputs that expect a DFJSON model file as the recipe input."""
dfjson_model_input = [
    # grasshopper Alias
    InputAlias.any(
        name='model',
        description='A Dragonfly Model object or the path to a DFJSON file.',
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python', module='pollination_handlers.inputs.model',
                function='model_dragonfly_to_json'
            )
        ]
    )
]
