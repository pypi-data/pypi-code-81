from typing import TYPE_CHECKING, Any, Dict, Optional, Type, get_type_hints

if TYPE_CHECKING:
    from envvarconf import BaseSettings


def get_definition_vars(inherited_class: Any) -> Dict[str, Optional[Type]]:
    vars_definition: Dict[str, Optional[Type]] = {}

    for v, _ in inherited_class.__dict__.items():
        # Skip private and callables
        if not v.startswith("_") and not callable(getattr(inherited_class, v)):
            vars_definition[v] = None

    vars_definition.update(get_type_hints(inherited_class))

    return vars_definition


def get_settings_variables(settings: 'BaseSettings') -> Dict[str, Optional[Type]]:
    annotations = {}
    for inherited_class in reversed(settings.__class__.__mro__):
        if inherited_class != object:
            annotations.update(get_definition_vars(inherited_class))

    return annotations
