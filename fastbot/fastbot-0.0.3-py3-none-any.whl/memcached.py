import json

from pymemcache.client import base

from fastbot.core import DataStore


class MemcacheDataStore(DataStore):
    def __init__(self, host=None, port=None, json_encoder=None, **kwargs):
        self.client = base.Client((host, port))
        self.json_encoder = json_encoder

    def get(self, session_key) -> dict:
        _body = self.client.get(session_key)
        return json.loads(_body, cls=self.json_encoder) if _body else {}

    def update(self, session_key, **state):
        return self.client.set(session_key, json.dumps(state, cls=self.json_encoder))

    def remove(self, session_key):
        self.client.delete(session_key)
