from dataclasses import dataclass
import logging
import os

import boto3

class SecretManager:
    _secrets = {}

    def __init__(self):
        self._client = boto3.client('secretsmanager')

    def get(self, name) -> str:
        return self._get_secret_value(name)

    def _get_secret_value(self, name) -> str:
        if name not in os.environ:
            return None
        if not name in self._secrets:
            self._secrets[name] = self._get_secret_from_ssm(os.environ.get(name))
        return self._secrets.get(name)

    def _get_secret_from_ssm(self, arn) -> str:
        response = self._client.get_secret_value(SecretId=arn)
        response_value = response.get('SecretString')
        return response_value