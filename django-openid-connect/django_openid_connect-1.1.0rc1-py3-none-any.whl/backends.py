from django.contrib.auth import get_user_model
from urllib.parse import urlencode

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from social_core.backends.oauth import BaseOAuth2
from django.conf import settings

import logging

logger = logging.getLogger(__name__)


class OpenIdConnect(BaseOAuth2):
    """ OpenID Connect backend """

    name = settings.OPEN_ID_NAME
    EXTRA_DATA = []
    user = None
    ID_KEY = settings.ID_KEY
    ACCESS_TOKEN_METHOD = settings.ACCESS_TOKEN_METHOD
    ID_TOKEN_ISSUER = settings.ID_TOKEN_ISSUER
    OIDC_ENDPOINT = settings.OIDC_ENDPOINT
    AUTHORIZATION_URL = settings.AUTHORIZATION_URL
    ACCESS_TOKEN_URL = settings.ACCESS_TOKEN_URL
    REFRESH_TOKEN_URL = settings.REFRESH_TOKEN_URL
    REDIRECT_STATE = settings.REDIRECT_STATE

    def auth_allowed(self, response, details):
        remote_groups = settings.REMOTE_GROUP_FILTER(response.get(settings.REMOTE_GROUP_KEY, None))
        internal_groups = Group.objects.filter(name__in=remote_groups)

        content_type = ContentType.objects.get(app_label=settings.CONTENT_TYPE_APP_LABEL,
                                               model=settings.CONTENT_TYPE_MODEL)
        login_perm = Permission.objects.get(codename=settings.PERMISSION_MODEL_CODENAME, content_type=content_type)
        for group in internal_groups:
            try:
                group.permissions.get(pk=login_perm.pk)
                logger.info('Login Allowed for group {}'.format(group.name))
                return True
            except ObjectDoesNotExist:
                pass

        logger.info('Login Forbidden. No allowed group for: {}->{}'.format(response.get(settings.ID_KEY),
                                                                           response.get(settings.REMOTE_GROUP_KEY)))
        return False

    def get_user_details(self, response):
        """ Return user details from Open Id account" """
        return settings.GET_USER_DETAILS(response)

    def get_user(self, user_id, **kwargs):
        return get_user_model().objects.get(pk=user_id)

    def user_data(self, access_token, *args, **kwargs):
        """ Load and parse user data from service """
        url = settings.USER_INFO_URL + urlencode({'access_token': access_token})
        result = self.get_json(url)
        return result

    def auth_html(self):
        super(OpenIdConnect, self).auth_html()
