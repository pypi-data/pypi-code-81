import json
from json import JSONDecoder

import redis
from typing import Type, Optional

from fastbot.core import DataStore
from fastbot.json import JSONEncoder


class RedisDataStore(DataStore):
    def __init__(self, json_encoder: Optional[Type[JSONDecoder]] = JSONEncoder, **kwargs):
        self.client = redis.Redis(**kwargs)
        self.json_encoder = json_encoder

    def get(self, session_key) -> dict:
        return json.loads(self.client.get(session_key), cls=self.json_encoder) \
            if self.client.exists(session_key) else {}

    def update(self, session_key, **state):
        return self.client.set(session_key, json.dumps(state, cls=self.json_encoder))

    def remove(self, session_key):
        self.client.delete(session_key)
