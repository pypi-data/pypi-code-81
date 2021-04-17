import requests
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
from typing import Optional

class API:
    API_BASE_ENDPOINT = 'https://api.upbit.com/v1'

    access_key: str
    secret_key: str

    def __init__(self, access_key: str, secret_key: str):
        self.access_key = access_key
        self.secret_key = secret_key

    def call_api(self, method: str, path: str, data: Optional[dict] = None, token: bool = False):
        headers = None
        params = None

        if data != None:
            data = dict({key: value for key, value in data.items() if value != None})

        if token:
            payload = {
                'access_key': self.access_key,
                'nonce': str(uuid.uuid4())
            }

            if data:
                querystring = urlencode(data).encode()
                m = hashlib.sha512()
                m.update(querystring)
                query_hash = m.hexdigest()
                payload['query_hash'] = query_hash
                payload['query_hash_alg'] = 'SHA512'

            jwt_token = jwt.encode(payload, self.secret_key)
            headers = {"Authorization": 'Bearer ' + jwt_token.decode('utf-8')}

        if method == 'get':
            params = data
            data = None

        response = requests.request(method, self.API_BASE_ENDPOINT + path, headers=headers, params=params, data=data)

        response_json = response.json()

        if response.status_code >= 400:
            error = response_json['error']
            raise APIError(error)

        return response_json

class APIError(Exception):
    pass
