import os
from typing import get_type_hints, Mapping

from .extended_environ import extended_environ
from .utils import type_utils, inspections
from .utils.supported_types import SupportedTypes


class _ConfigurationInjector:
    def __init__(self, target_class: type, prefix: str, source: Mapping[str, str]) -> None:
        self.target_class = target_class
        self.prefix = prefix
        self.source = source

    @staticmethod
    def inject_class(target_class: type, prefix: str, source: Mapping[str, str]) -> type:
        return _ConfigurationInjector(target_class, prefix, source)._get_injected_target_class()

    def _get_injected_target_class(self) -> type:
        for variable_name, variable_type in get_type_hints(self.target_class).items():
            value = self._get_variable_value(variable_name, variable_type)
            setattr(self.target_class, variable_name, value)

        return self.target_class

    def _get_variable_value(self, variable_name: str, variable_type: type) -> SupportedTypes:
        default_value = getattr(self.target_class, variable_name, None)
        lookup_key = self.prefix + variable_name
        value = self.source.get(lookup_key, None)
        if (value or default_value) is None and not type_utils.is_optional(variable_type):
            raise LookupError(self._missing_variable_error_message(lookup_key))
        try:
            return type_utils.cast(value, variable_type) if value is not None else default_value
        except ValueError as e:
            raise ValueError(f"couldn't cast {variable_name} to {variable_type}. input: {value}. message: {e}")

    def _missing_variable_error_message(self, lookup_key: str) -> str:
        if self.source in [os.environ, extended_environ]:
            return f"{lookup_key} is not an environment variable, nor has default value"
        else:
            source_name = inspections.retrieve_name(self.source) or "your source"
            return f"{lookup_key} does not exist in {source_name}, nor has default value"
