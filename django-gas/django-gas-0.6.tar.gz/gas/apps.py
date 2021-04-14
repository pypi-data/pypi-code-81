from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_migrate


class GASConfig(AppConfig):
    name = 'gas'
    verbose_name = _('GAS')

    def ready(self):
        from .sites import site
        super().ready()
        site.autodiscover()
