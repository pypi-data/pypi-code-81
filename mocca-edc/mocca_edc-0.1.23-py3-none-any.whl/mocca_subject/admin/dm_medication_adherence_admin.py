from django.contrib import admin
from edc_form_label.form_label_modeladmin_mixin import FormLabelModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin
from respond_admin.mixins import MedicationAdherenceAdminMixin

from ..admin_site import mocca_subject_admin
from ..forms import DmMedicationAdherenceForm
from ..models import DmMedicationAdherence
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(DmMedicationAdherence, site=mocca_subject_admin)
class DmMedicationAdherenceAdmin(
    MedicationAdherenceAdminMixin,
    CrfModelAdminMixin,
    FormLabelModelAdminMixin,
    SimpleHistoryAdmin,
):

    form = DmMedicationAdherenceForm
