from functools import lru_cache

from werkzeug.utils import cached_property
from . import config


class OARepoSearchState:
    def __init__(self, app):
        self.app = app

    @cached_property
    def supported_languages(self):
        return self.app.config.get("OAREPO_SEARCH_SUPPORTED_LANGUAGES", [])

    @cached_property
    def search_fields(self):
        return self.app.config.get("OAREPO_SEARCH_FIELDS", {})

    @lru_cache(maxsize=20)
    def get_fields(self, endpoint_name: str):
        return self.search_fields.get(endpoint_name, [])


class OARepoSearch(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.init_config(app)
        _state = OARepoSearchState(app)
        app.extensions['oarepo-search'] = _state
        # app_loaded.connect(_state.app_loaded)

    def init_config(self, app):
        for k in dir(config):
            if k.startswith('OAREPO_SEARCH_'):
                app.config.setdefault(k, getattr(config, k))
