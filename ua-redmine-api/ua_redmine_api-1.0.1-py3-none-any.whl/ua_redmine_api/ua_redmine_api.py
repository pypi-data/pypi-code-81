import requests
from requests.auth import HTTPBasicAuth
import json


class RedmineApi():
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def get(self, endpoint):
        response = requests.get(
            f"{self.host}/{endpoint}.json",
            auth=HTTPBasicAuth(self.username, self.password),
        )
        response.raise_for_status()
        return json.loads(response.content)

    def put(self, endpoint, data):

        response = requests.put(
            f"{self.host}/{endpoint}.json",
            auth=HTTPBasicAuth(self.username, self.password),
            json=data,
        )
        response.raise_for_status()
        return json.loads(response.content)

    def post(self, endpoint, data):
        response = requests.post(
            f"{self.host}/{endpoint}.json",
            auth=HTTPBasicAuth(self.username, self.password),
            json=data,
        )

    def delete(self, endpoint):
        response = requests.delete(
            f"{self.host}/{endpoint}.json",
            auth=HTTPBasicAuth(self.username, self.password),
        )
        response.raise_for_status()
        return json.loads(response.content)
