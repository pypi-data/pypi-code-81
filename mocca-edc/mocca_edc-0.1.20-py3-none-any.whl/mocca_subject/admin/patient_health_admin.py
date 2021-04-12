from django.contrib import admin
from django.utils.html import format_html
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf.admin import crf_status_fieldset_tuple
from edc_form_label.form_label_modeladmin_mixin import FormLabelModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin

from ..admin_site import mocca_subject_admin
from ..forms import PatientHealthForm
from ..models import PatientHealth
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(PatientHealth, site=mocca_subject_admin)
class PatientHealthAdmin(CrfModelAdminMixin, FormLabelModelAdminMixin, SimpleHistoryAdmin):
    form = PatientHealthForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "PHQ-9",
            {
                "description": format_html(
                    "<h3>Over the last 2 weeks, how often have you been bothered "
                    "by any of the following?</h3>"
                ),
                "fields": (
                    "ph9interst",
                    "ph9feel",
                    "ph9troubl",
                    "ph9tired",
                    "ph9appetit",
                    "ph9badabt",
                    "ph9concen",
                    "ph9moving",
                    "ph9though",
                    "ph9functio",
                ),
            },
        ),
        crf_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "crf_status": admin.VERTICAL,
        "ph9appetit": admin.VERTICAL,
        "ph9badabt": admin.VERTICAL,
        "ph9concen": admin.VERTICAL,
        "ph9feel": admin.VERTICAL,
        "ph9functio": admin.VERTICAL,
        "ph9interst": admin.VERTICAL,
        "ph9moving": admin.VERTICAL,
        "ph9tired": admin.VERTICAL,
        "ph9troubl": admin.VERTICAL,
        "ph9though": admin.VERTICAL,
    }
