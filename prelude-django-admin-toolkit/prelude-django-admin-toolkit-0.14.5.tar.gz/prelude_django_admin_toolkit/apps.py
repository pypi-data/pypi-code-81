from django.contrib.admin.apps import SimpleAdminConfig


class PrlAdminConfig(SimpleAdminConfig):
    """The default AppConfig for admin which does autodiscovery."""

    default_site = 'prelude_django_admin_toolkit.admin.PrlAdmin'

    def ready(self):
        super().ready()
        self.module.autodiscover()
