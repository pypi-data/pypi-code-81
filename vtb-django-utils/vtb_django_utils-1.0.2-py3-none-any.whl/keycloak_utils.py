from django.conf import settings
from vtb_http_interaction.keycloak_gateway import KeycloakConfig

keycloak_config = KeycloakConfig(
    server_url=settings.KEY_CLOAK_SERVER_URL,
    client_id=settings.KEY_CLOAK_CLIENT_ID,
    realm_name=settings.KEY_CLOAK_REALM_NAME,
    client_secret_key=settings.KEY_CLOAK_CLIENT_SECRET_KEY
)
