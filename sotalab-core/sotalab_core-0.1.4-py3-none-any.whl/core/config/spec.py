import functools
from abc import ABCMeta, abstractmethod
from typing import Any, List, Union

from ..utils.yaml import CommentedMap, CommentedSeq, TaggedScalar
from .registry import ClassRegistry
from .type_utils import get_full_arg_spec

GenericAlias = type(List)
NoneType = type(None)

__all__ = [
    "ConfigSpec",
    "ScalarConfigSpec",
    "OptionalConfigSpec",
    "TuplesConfigSpec",
    "ListConfigSpec",
    "DictConfigSpec",
    "ClassConfigSpec",
    "FunctionConfigSpec",
]


class ConfigSpec(metaclass=ABCMeta):
    @staticmethod
    def from_type(tp):
        if tp in (int, float, bool, str):
            return ScalarConfigSpec(tp)
        elif isinstance(tp, GenericAlias):
            origin = tp.__origin__
            if origin is list:
                internal_type = tp.__args__[0]
                return ListConfigSpec(internal_type)
            elif origin is Union:
                internal_types = tp.__args__
                if len(internal_types) == 2 and (
                    internal_types[0] is NoneType or internal_types[1] is NoneType
                ):
                    # Optional[T]
                    internal_type = (
                        internal_types[0]
                        if internal_types[0] is not NoneType
                        else internal_types[1]
                    )
                    return OptionalConfigSpec(internal_type)
            elif origin is tuple:
                internal_types = tp.__args__
                return TuplesConfigSpec(internal_types)
            elif origin is dict:
                key_tp, value_tp = tp.__args__
                return DictConfigSpec(key_tp, value_tp)
            else:
                raise NotImplementedError(tp)
        elif tp in ClassRegistry():
            return ClassConfigSpec(tp)
        else:
            raise NotImplementedError(tp)

    @abstractmethod
    def instantiate(self, config):
        ...


class ScalarConfigSpec(ConfigSpec):
    def __init__(self, tp: type):
        self._tp = tp

    def instantiate(self, config: Any):
        return self._tp(config)


class OptionalConfigSpec(ConfigSpec):
    def __init__(self, tp: type):
        self._internal_spec = ConfigSpec.from_type(tp)

    def instantiate(self, config: Any):
        if config is None:
            return None
        else:
            return self._internal_spec.instantiate(config)


class TuplesConfigSpec(ConfigSpec):
    def __init__(self, types: List[type]):
        self._internal_specs = [ConfigSpec.from_type(tp) for tp in types]

    def instantiate(self, config: CommentedSeq):
        assert isinstance(config, CommentedSeq), config
        assert len(config) == len(self._internal_specs), (
            len(config),
            len(self._internal_specs),
        )
        return tuple(
            spec.instantiate(cfg) for spec, cfg in zip(self._internal_specs, config)
        )


class ListConfigSpec(ConfigSpec):
    def __init__(self, internal_type: type):
        self.internal_spec = ConfigSpec.from_type(internal_type)

    def instantiate(self, config: CommentedSeq):
        assert isinstance(config, CommentedSeq), config
        return list(map(lambda x: self.internal_spec.instantiate(x), config))


class DictConfigSpec(ConfigSpec):
    def __init__(self, key_type: type, value_type: type):
        self.key_spec = ConfigSpec.from_type(key_type)
        self.value_spec = ConfigSpec.from_type(value_type)

    def instantiate(self, config: CommentedMap):
        assert isinstance(config, CommentedMap), config
        result = {}
        for k, v in config.items():
            result[self.key_spec.instantiate(k)] = self.value_spec.instantiate(v)
        return result


class ClassConfigSpec(ConfigSpec):
    def __init__(self, cls):
        self._cls = cls

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def get_argument_config_specs(cls):
        specs = {}

        arguments_spec, defaults = get_full_arg_spec(cls)
        for key, tp in arguments_spec.items():
            specs[key] = ConfigSpec.from_type(tp)

        return specs, defaults

    def instantiate(self, config: Union[str, TaggedScalar, CommentedMap]):
        params = {}
        if isinstance(config, str):
            # config is a class name
            cls = ClassRegistry().get(self._cls, config)
            assert cls is not None, f"{self._cls} {config}"
        elif isinstance(config, TaggedScalar):
            # config is a class name
            name = config.value[1:]  # strip off `!`
            cls = ClassRegistry().get(self._cls, name)
            assert cls is not None, f"{self._cls} {name}"
        elif isinstance(config, CommentedMap):
            tag = config.tag
            if tag.value is not None:
                name = tag.value[1:]  # strip off `!`
                cls = ClassRegistry().get(self._cls, name)
                assert cls is not None, f"{self._cls} {name}"
            else:
                cls = self._cls

            specs, defaults = self.get_argument_config_specs(cls)
            for key in config.keys():
                if key not in specs:
                    raise RuntimeError(f"unknown key: {key} ({cls})")
            for key, spec in specs.items():
                if key in config:
                    params[key] = spec.instantiate(config[key])
                elif key in defaults:
                    params[key] = defaults[key]
                else:
                    raise RuntimeError(f"Missing required key: {key} ({cls})")

        else:
            raise NotImplementedError(config, type(config))

        return cls(**params)


class FunctionConfigSpec(ConfigSpec):
    def __init__(self):
        pass
