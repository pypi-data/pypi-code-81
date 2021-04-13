from logging import StreamHandler

import jwt
from functools import wraps
from firebase_admin import firestore
from flask import request, abort
from os import getenv
import logging

logger = logging.getLogger("ace_authorize")
handler = StreamHandler()
formatter = logging.Formatter('[%(levelname)s] [%(name)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def authorize(scope):
    def decorator(endpoint_func):
        @wraps(endpoint_func)
        def decorated_function(*args, **kwargs):
            tenant_id = kwargs.get('tenant_id')

            if tenant_id is not None:
                scopes = get_scopes(tenant_id)
            else:
                scopes = get_scopes()

            if scope in scopes:
                return endpoint_func(*args, **kwargs)
            else:
                return abort(403, "NOT ALLOWED")
        return decorated_function
    return decorator


def get_scopes(tenant_id=None):
    # TODO: (cjk) Check for jwt payload in the headers when dealing with requests passed through an api gateway
    # jwt_payload = request.headers.get("X-Apigateway-Api-Userinfo")
    auth_header = request.headers.get("Authorization")

    if auth_header:
        auth_header = auth_header.rpartition(' ')[2]
        decoded_token = jwt.decode(auth_header, options={"verify_signature": False})
        user_roles = decoded_token.get('roles')
        host = getenv("ROLES_HOST")

        if tenant_id == decoded_token.get('firebase').get('tenant'):
            if host:
                roles = get_user_roles()
                scopes = []
                for role in roles:
                    if role['name'] in user_roles:
                        scopes.extend(role["scopes"])
                return scopes
            else:
                logger.error("Failed to retrieve roles. ROLES_HOST is not set.")
                return abort(500, "INTERNAL SERVER ERROR")
        else:
            if host:
                roles = get_platform_roles()
                scopes = []
                for role in roles:
                    if role['name'] in user_roles:
                        scopes.extend(role["scopes"])
                return scopes
            else:
                logger.error("Failed to retrieve roles. ROLES_HOST is not set.")
                return abort(500, "INTERNAL SERVER ERROR")
    return abort(403, "NOT ALLOWED")


def get_user_roles():
    db = firestore.client()
    roles = []

    roles_ref = db.collection(u'userRoles')
    docs = roles_ref.stream()

    for doc in docs:
        roles.append(doc.to_dict())

    return roles


def get_platform_roles():
    db = firestore.client()
    roles = []

    roles_ref = db.collection(u'platformRoles')
    docs = roles_ref.stream()

    for doc in docs:
        roles.append(doc.to_dict())

    return roles
