from django.conf import settings
from django.views.generic import RedirectView


class UNICEFLogoutView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return f'https://{settings.TENANT_B2C_URL}/{settings.TENANT_ID}/{settings.POLICY}/oauth2/v2.0/' \
               f'logout?post_logout_redirect_uri={settings.HOST}{settings.LOGOUT_URL}'
