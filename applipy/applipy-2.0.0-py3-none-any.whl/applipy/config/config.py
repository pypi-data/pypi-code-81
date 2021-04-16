import typing as T
from .protocol import ConfigProtocol
from collections.abc import Mapping


class Config(Mapping):

    _providers: T.List[ConfigProtocol]
    _config: T.Dict[str, T.Any]
    _keys: T.Set[str]

    def __init__(self, config: T.Dict[str, T.Any], protocols: T.Optional[T.List[ConfigProtocol]] = None,
                 *, _normalize=True) -> None:
        self._providers = [] if protocols is None else protocols
        self._config = self._build_config(config) if _normalize else config
        self._keys = self._build_keys(config, [])

    def __getitem__(self, key) -> T.Optional[T.Any]:
        parts = key.split('.')

        value = self._config
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                raise KeyError(key)
        if value is None:
            raise KeyError(key)

        if isinstance(value, str):
            idx = value.find(':')
            scheme, other = value[:idx], value[idx + 1:]
            if len(other) > 0:
                maybe_value = self._get_value_from_provider(scheme, other)
                if maybe_value is not None:
                    value = maybe_value
        elif isinstance(value, dict):
            value = Config(value, self._providers, _normalize=False)

        return value

    def __iter__(self):
        yield from self._keys

    def __len__(self):
        return len(self._keys)

    @property
    def protocols(self) -> T.List[ConfigProtocol]:
        return self._providers

    def addProtocol(self, protocol: ConfigProtocol) -> None:
        self._providers.append(protocol)

    def _build_config(self, config):
        new_config = {}
        for k, v in config.items():
            parts = k.split('.')
            sub_config = new_config
            for part in parts[:-1]:
                if part not in sub_config:
                    sub_config[part] = {}
                sub_config = sub_config[part]

            if isinstance(v, dict):
                v = self._build_config(v)
            elif isinstance(v, list):
                v = self._build_config_list(v)

            sub_config[parts[-1]] = v

        return new_config

    def _build_config_list(self, config_list):
        result = []
        for v in config_list:
            if isinstance(v, dict):
                result.append(Config(v, self._providers))
            elif isinstance(v, list):
                result.append(self._build_config_list(v))
            else:
                result.append(v)

        return result

    def _build_keys(self, config, parts):
        keys = set()
        for k, v in config.items():
            new_parts = parts + [k]
            if isinstance(v, dict):
                keys.update(self._build_keys(v, new_parts))
            else:
                keys.add('.'.join(new_parts))

        return keys

    def _get_value_from_provider(self, protocol: str, key: str) -> T.Optional[T.Any]:
        for provider in self._providers:
            r = provider.provide_for(protocol, key)
            if r is not None:
                return r
        return None
