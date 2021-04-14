from edc_crf.admin import CrfStatusModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin
from edc_model_admin.dashboard import (
    ModelAdminCrfDashboardMixin,
    ModelAdminSubjectDashboardMixin,
)


class ModelAdminMixin(ModelAdminSubjectDashboardMixin):
    pass


class CrfModelAdminMixin(CrfStatusModelAdminMixin, ModelAdminCrfDashboardMixin):

    pass


class CrfModelAdmin(ModelAdminCrfDashboardMixin, SimpleHistoryAdmin):

    pass
