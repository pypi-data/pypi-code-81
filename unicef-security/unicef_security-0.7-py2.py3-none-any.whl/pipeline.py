from social_core.pipeline import social_auth
from social_core.pipeline.user import USER_FIELDS

from .config import UNICEF_EMAIL


def social_details(backend, details, response, *args, **kwargs):
    r = social_auth.social_details(backend, details, response, *args, **kwargs)
    r['details']['idp'] = response.get('idp')
    if not r['details'].get('email'):
        if not response.get('email'):
            r['details']['email'] = response["signInNames.emailAddress"]
        else:
            r['details']['email'] = response.get('email')
    email = r['details'].get('email')
    if isinstance(email, str):
        r['details']['email'] = email.lower()
    return r


def get_username(strategy, details, backend, user=None, *args, **kwargs):
    return {'username': details.get('email')}


def create_unicef_user(strategy, details, backend, user=None, *args, **kwargs):
    """Overrides create_user, to create only UNICEF users"""
    if user:
        return {'is_new': False}

    fields = dict((name, kwargs.get(name, details.get(name)))
                  for name in backend.setting('USER_FIELDS', USER_FIELDS))
    if not (fields and details.get('email', '').endswith(UNICEF_EMAIL)):
        return

    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }
