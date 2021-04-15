import typing

import marshmallow as ma
from environs import Env as BaseEnv, EnvError


class Env(BaseEnv):
    def __init__(self):
        super().__init__()
        self._is_default_allowed = False

    def allow_default(self):
        self._is_default_allowed = True

    def _get_from_environ(self, key: str, default: typing.Any, *, proxied: bool = False):
        if self._is_default_allowed:
            parsed_key, raw_value, proxied_key = super()._get_from_environ(key, default, proxied=proxied)
        else:
            parsed_key, raw_value, proxied_key = super()._get_from_environ(key, ma.missing, proxied=proxied)
        if raw_value is ma.missing and not self._is_default_allowed:
            raise EnvError(
                'Environment variable "{}" not set. Default value not allowed.'.format(proxied_key or parsed_key))
        return parsed_key, raw_value, proxied_key
