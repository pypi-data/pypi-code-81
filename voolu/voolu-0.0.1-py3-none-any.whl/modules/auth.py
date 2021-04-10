import httpx
import os

LOOKUP_SERVICE_URL = 'https://discover.dev.voolu.io'


class AuthService:
    def __init__(self):
        self.client = httpx.AsyncClient()

    async def find_replicas(self):
        # r = await self.client.get(LOOKUP_SERVICE_URL + '/replicas')
        # r = r.json()
        # return r['replicas']
        return ['0.0.0.0']

    async def login(self, email, password):
        r = await self.client.post(LOOKUP_SERVICE_URL + '/login', json={'email': email, 'password': password})
        r = r.json()
        return r['token']

    async def create_account(self, email, password):
        r = await self.client.post(LOOKUP_SERVICE_URL + '/create-account', json={'email': email, 'password': password})
        r = r.json()
        return r['token']

    async def get_host_token(self, host_tag):
        with open(os.path.expanduser('~/.voolu/token'), 'r') as f:
            account_token = f.read()

        r = await self.client.post(LOOKUP_SERVICE_URL + '/host-connect', json={'tag': host_tag, 'token': account_token})
        r = r.json()
        if not r['success']:
            return
        return r['host_token']
