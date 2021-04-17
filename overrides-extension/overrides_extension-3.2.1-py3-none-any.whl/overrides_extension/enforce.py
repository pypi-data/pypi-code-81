#
#  Copyright 2019-2021 Mikko Korpela & Eugene Mozharovsky
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

from abc import ABCMeta
from typing import Any, Dict, Tuple


class EnforceOverridesMeta(ABCMeta):
    OVERRIDE_ERROR = "Method `%s` overrides but does not have `@override` decorator"
    FINALIZED_ERROR = "Method `%s` is finalized in `%s`, it cannot be overridden"

    def __new__(
        cls,
        name: str,
        bases: Tuple[type, ...],
        namespace: Dict[str, Any],
        **kwargs: Any
    ) -> type:
        obj = super().__new__(cls, name, bases, namespace, **kwargs)

        for item_name, item_value in namespace.items():
            # Actually checking the direct parent should be enough,
            # otherwise the error would have emerged during the parent class checking
            if item_name.startswith("__"):
                continue

            value = cls.handle_special_value(item_value)
            is_override = getattr(value, "__override__", False)
            for base in bases:
                base_class_method = getattr(base, item_name, False)
                if not base_class_method or not callable(base_class_method):
                    continue

                # `__finalized__` is added by `@final` decorator
                is_finalized = getattr(base_class_method, "__finalized__", False)

                # check if `@override` decorator added
                assert is_override, cls.OVERRIDE_ERROR % item_name
                # check if current method is not finalized
                assert not is_finalized, cls.FINALIZED_ERROR % (base_class_method, base)

        return obj

    @staticmethod
    def handle_special_value(value: Any) -> Any:
        if isinstance(value, (classmethod, staticmethod)):
            value = value.__get__(None, dict)
        elif isinstance(value, property):
            value = value.fget
        return value


# pylint: disable=too-few-public-methods
class EnforceOverrides(metaclass=EnforceOverridesMeta):
    """Use this as the parent class for your custom classes"""
