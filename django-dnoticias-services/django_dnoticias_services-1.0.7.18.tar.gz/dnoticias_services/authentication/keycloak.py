from uuid import uuid4

from django.conf import settings
from django.contrib.auth import get_backends, get_user_model
from django.core.exceptions import SuspiciousOperation
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from keycloak import KeycloakAdmin, KeycloakOpenID

User = get_user_model()

class BaseKeyCloak(object):
    def __init__(self):
        self.server_url = getattr(settings, "KEYCLOAK_SERVER_URL", "")
        self.admin_realm_name = getattr(settings, "KEYCLOAK_ADMIN_REALM_NAME", "")
        self.user_realm_name = getattr(settings, "KEYCLOAK_USER_REALM_NAME", "") or self.admin_realm_name
        self.username = getattr(settings, "KEYCLOAK_ADMIN_USERNAME", "")
        self.password = getattr(settings, "KEYCLOAK_ADMIN_PASSWORD", "")
        self.client_id = getattr(settings, "KEYCLOAK_CLIENT_ID", "")
        self.client_secret_key = getattr(settings, "KEYCLOAK_CLIENT_SECRET_KEY", "")

        self.keycloak_admin = KeycloakAdmin(
                                server_url=self.server_url,
                                username=self.username,
                                password=self.password,
                                realm_name=self.admin_realm_name,
                                user_realm_name=self.user_realm_name,
                                verify=True
                            )

        self.keycloak_openid = KeycloakOpenID(
                                server_url=self.server_url,
                                client_id=self.client_id,
                                realm_name=self.user_realm_name,
                                client_secret_key=self.client_secret_key,
                                verify=True
                            )

    def get_backend(self):
        backends = get_backends()

        for backend in backends:
            if issubclass(backend.__class__, OIDCAuthenticationBackend):
                return backend

        raise ValueError("No backend that is subclass of OIDCAuthenticationBackend")

class CreateUser(BaseKeyCloak):
    def __call__(self, email):
        user_id_keycloack = self.keycloak_admin.get_user_id(email)
        if user_id_keycloack is None:
            password = uuid4()
            user_id_keycloack = self.keycloak_admin.create_user(
                {
                    "email": email,
                    "username": email,
                    "enabled": True,
                    "emailVerified" : True,
                    "credentials": [
                        {
                            "value": str(password), "type": "password", "temporary": False
                        }
                    ],
                    "realmRoles": ["user_default", ],
                    "attributes": {
                        "is_staff": False
                    }
                }
            )

        user_info = self.keycloak_admin.get_user(user_id_keycloack)

        email = user_info.get('email')

        backend = self.get_backend()
        claims_verified = backend.verify_claims(user_info)
        if not claims_verified:
            msg = 'Claims verification failed'
            raise SuspiciousOperation(msg)

        # email based filtering
        users = backend.filter_users_by_claims(user_info)

        if len(users) == 1:
            return backend.update_user(users[0], user_info)
        elif len(users) > 1:
            # In the rare case that two user accounts have the same email address,
            # bail. Randomly selecting one seems really wrong.
            msg = 'Multiple users returned'
            raise SuspiciousOperation(msg)
        elif backend.get_settings('OIDC_CREATE_USER', True):
            return backend.create_user(user_info)
        
        return None

class UpdatePassword(BaseKeyCloak):
    def __call__(self, email, password):
        user_id_keycloack = self.keycloak_admin.get_user_id(email)
        self.keycloak_admin.set_user_password(user_id=user_id_keycloack, password=password, temporary=False)

class GetToken(BaseKeyCloak):
    def __call__(self, email, password):
        return self.keycloak_openid.token(email, password)

create_user = CreateUser()
update_password = UpdatePassword()
get_token = GetToken()
