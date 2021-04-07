# Third party
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.urlutils import admin_reverse
from django.utils.translation import ugettext_lazy as _

from .settings import ADD_LIST_BUTTON


class DjangocmsPopupToolbar(CMSToolbar):
    def populate(self):

        self.toolbar.add_link_item(
            name=_("Popup list"),
            url=admin_reverse("djangocms_popup_popuppluginmodel_changelist"),
        )


if ADD_LIST_BUTTON:
    # register the toolbar only if setting does not exist or is set to true
    toolbar_pool.register(DjangocmsPopupToolbar)
