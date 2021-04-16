import logging
from typing_extensions import Literal
from GuardiPy.helpers import CentraEntity, CentraApiPayload


class User(CentraEntity):
    _path = "/system/user"

    @staticmethod
    def add(
            username: str,
            password: str,
            permission_scheme_ids: Literal["administrator", "guest"],
            two_factor_auth_enabled: bool,
            email: str = None,
            can_access_passwords: bool = False,
            description: str = None,
            is_saml_user: bool = False,
    ) -> CentraApiPayload:
    
        data = {
            "action": "create",
            "username": username,
            "password": password,
            "password_confirm": password,
            "permission_scheme_ids": [permission_scheme_ids],
            "two_factor_auth_enabled": two_factor_auth_enabled,
            "is_saml_user": is_saml_user,
            "can_access_passwords": can_access_passwords,
            "description": description or "",
            "email": email or ""
        }

        payload = CentraApiPayload(path=User._path, method="POST", return_type=User,
                                   data=data, response_pagination=False)
        return payload

    def __init__(self, **kwargs):
        logging.debug("New Attributes found for User")
        for k, v in kwargs:
            logging.debug(f"{k}: {v}")
