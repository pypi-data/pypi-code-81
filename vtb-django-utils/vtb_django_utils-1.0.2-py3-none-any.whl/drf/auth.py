"""
Расширения DRF Authentication's для аутентификации пользователей
"""
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from vtb_http_interaction.keycloak_gateway import KeycloakGateway

from vtb_django_utils.backends import prepare_user
from vtb_django_utils.keycloak_utils import keycloak_config


class KeycloakUser:
    """
    Пользователь Keycloak
    """
    id = None
    pk = None
    realm_access = None

    username = ''
    email = ''
    first_name = ''
    last_name = ''

    is_staff = False
    is_active = False
    is_superuser = False

    def __str__(self):
        return 'KeycloakUser'

    @property
    def is_anonymous(self):
        """ anonymous flag """
        return False

    @property
    def is_authenticated(self):
        """ authenticated flag """
        return True

    def get_username(self):
        """ username """
        return self.username


class KeycloakAuthentication(BaseAuthentication):
    """
    Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a
    """
    keyword = 'Bearer'

    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        len_auth = len(auth)

        if len_auth == 1:
            raise exceptions.AuthenticationFailed('Invalid token header. No credentials provided.')

        if len_auth > 2:
            raise exceptions.AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        try:
            token = auth[1].decode()
        except UnicodeError as ex:
            raise exceptions.AuthenticationFailed(
                'Invalid token header. Token string should not contain invalid characters.') from ex

        return _authenticate_credentials(token)

    def authenticate_header(self, request):
        return self.keyword


def _authenticate_credentials(access_token):
    with KeycloakGateway(keycloak_config) as gateway:
        try:
            token_info = gateway.decode_token(token=access_token, key=gateway.public_key)
        except Exception as ex:
            raise exceptions.AuthenticationFailed('Invalid access token.') from ex

        user = KeycloakUser()
        user.username = token_info['sub']
        user.realm_access = token_info.get('realm_access', None)
        user = prepare_user(user, token_info)

        return user, None
