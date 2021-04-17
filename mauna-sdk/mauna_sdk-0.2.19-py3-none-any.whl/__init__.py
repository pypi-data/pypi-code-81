from gql.client import Client
from gql.transport.aiohttp import AIOHTTPTransport
from . import config, utils, token_cache


def Mauna(api_key, developer_id):
    """
    Get the graphql client instance
    """
    cache = token_cache.TokenCache(developer_id, api_key)
    jwt_token = cache.read()
    if not jwt_token:
        exchange_token, nonce = utils.create_exchange_token(api_key)
        auth_data = utils.request_jwt(developer_id, exchange_token)
        jwt_token = utils.decrypt_jwt(auth_data, api_key, nonce)
        cache.write(jwt_token)

    transport = AIOHTTPTransport(url=config.API_ENDPOINT, headers={"Authorization": f"Bearer {jwt_token}"})
    return Client(transport=transport, fetch_schema_from_transport=True)

