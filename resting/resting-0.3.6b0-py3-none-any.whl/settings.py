import importlib
import os

__all__ = [
    'settings'
]

DEFAULT_SETTINGS = {
    'API_VERSION':  1,
    'HATEOAS_PARSERS': [
        'resting.hateoas.SimpleLinksParser',
        'resting.hateoas.SimpleUrlParser'
    ],

    'EXCEPTION_MODULES':  [
        'resting.exceptions'
    ],
    'USER_AGENT': None,

    'CLIENT_CLASS': 'resting.client.JsonClient',
    'CLIENT_KWARGS': {},
    'PAGINATOR_CLASS': 'resting.paginators.HeaderPaginator',
    'LIST_ITER_ALL': False
}

IMPORTABLE = [
    'HATEOAS_PARSERS',
    'CLIENT_CLASS',
    'PAGINATOR_CLASS'
]


class Settings:

    _user_settings = {}
    _defaults = {}

    def __init__(self,  user_settings=None):
        self._user_settings = user_settings or {}
        self._defaults = DEFAULT_SETTINGS

    @property
    def user_settings(self):
        return self.user_settings

    @user_settings.setter
    def user_settings(self, sett):
        self._user_settings = dict((key.upper(), val) for key, val in sett.items())

    def __getattr__(self, attr):
        if attr in ['_defaults', '_user_settings']:
            return getattr(self, attr)

        defined_attr = '__DEFINED_{}'.format(attr.upper())

        if attr not in self._defaults:
            raise AttributeError("Setting '{}' does not exists".format(attr))
        attr = attr.upper()
        try:
            if os.getenv(attr, None):
                value = os.getenv(attr)
            else:
                value = self._user_settings[attr]
        except KeyError:

            value = self._defaults[attr]

        if attr in IMPORTABLE:
            value = self._import(value)

        setattr(self, defined_attr, value)
        return value

    def _import(self, value):
        if not value:
            return

        if isinstance(value, (tuple, list)):
            return [self._import_single(line) for line in value]
        else:
            return self._import_single(value)

    def _import_single(self, value):
        module, klazz = value.rsplit('.', 1)
        try:
            return getattr(importlib.import_module(module), klazz)
        except ImportError as e:
            msg = "Could not import driver {}.{}, got error: {}".format(
                module, klazz, str(e)
            )
            raise ImportError(msg)

settings = Settings()
