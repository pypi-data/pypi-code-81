import os
from typing import Callable, Union, Mapping

from .extended_environ import extended_environ
from .configuration_injector import _ConfigurationInjector


def configuration(*, prefix: str, source: Mapping[str, str]) -> Callable[[type], type]:
    return lambda cls: _ConfigurationInjector.inject_class(cls, prefix, source)


def environment_configuration(
    target_class: type = None, *, prefix: str = "", include_dot_env_file: bool = True
) -> Union[Callable[[type], type], type]:

    source = extended_environ if include_dot_env_file else os.environ
    if target_class:  # decorator used without parentheses
        return configuration(prefix=prefix, source=source)(target_class)
    else:
        return configuration(prefix=prefix, source=source)
