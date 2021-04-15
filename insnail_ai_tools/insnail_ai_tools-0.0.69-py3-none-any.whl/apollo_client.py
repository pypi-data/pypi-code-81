from typing import Any

import requests


class ApolloClient:
    def __init__(
        self,
        app_id: str,
        cluster: str = "default",
        config_server_url: str = "http://localhost:8090",
        env: str = "DEV",
        ip: str = None,
        timeout: int = 30,
        cycle_time: int = 300,
        cache_file_path: str = None,
        authorization: str = None,
    ):
        self.app_id = app_id
        self.cluster = cluster
        self.config_server_url = config_server_url
        self.env = env
        self.ip = ip
        self.timeout = timeout
        self.cycle_time = cycle_time
        self.cache_file_path = cache_file_path
        self.authorization = authorization

        self._cache = {}

    def get_value(
        self, key: str, default_val: str = None, namespace: str = "application"
    ) -> Any:
        """
        get the configuration value
        :param key:
        :param default_val:
        :param namespace:
        :return:
        """
        if namespace in self._cache:
            return self._cache[namespace].get(key, default_val)
        return default_val

    def get_config(self, namespace: str = "application") -> dict:
        url = f"{self.config_server_url}/configfiles/json/{self.app_id}/{self.cluster}/{namespace}?ip={self.ip}"
        rp = requests.get(url)
        if rp.status_code == 200:
            return rp.json()
        else:
            return {}

    def cache_config(self, namespace: str = "application"):
        data = self.get_config(namespace)
        self._cache[namespace] = data


# APOLLO_APP_ID = "ai-comm-center"
# APOLLO_SERVER_URL = "http://10.0.0.176:8080"
# ac = ApolloClient(APOLLO_APP_ID, config_server_url=APOLLO_SERVER_URL)
