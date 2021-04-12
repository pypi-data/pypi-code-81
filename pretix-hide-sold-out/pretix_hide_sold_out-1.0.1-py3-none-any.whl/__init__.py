from django.utils.translation import gettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")

__version__ = "1.0.1"


class PluginApp(PluginConfig):
    name = "pretix_hide_sold_out"
    verbose_name = "Hide sold out events"

    class PretixPluginMeta:
        name = gettext_lazy("Hide sold out events")
        author = "pretix team"
        description = gettext_lazy("Hide sold out events")
        visible = True
        version = __version__
        category = "CUSTOMIZATION"
        compatibility = "pretix>=3.0.0"


default_app_config = "pretix_hide_sold_out.PluginApp"
