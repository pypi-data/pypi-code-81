from django.contrib import admin
from edc_model_admin import SimpleHistoryAdmin
from respond_admin.mixins import MedicationAdherenceAdminMixin

from ..admin_site import mocca_subject_admin
from ..forms import CholMedicationAdherenceForm
from ..models import CholMedicationAdherence
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(CholMedicationAdherence, site=mocca_subject_admin)
class CholMedicationAdherenceAdmin(
    MedicationAdherenceAdminMixin,
    CrfModelAdminMixin,
    SimpleHistoryAdmin,
):

    form = CholMedicationAdherenceForm
