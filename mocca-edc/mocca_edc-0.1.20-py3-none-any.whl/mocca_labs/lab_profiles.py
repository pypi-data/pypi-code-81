from django.conf import settings
from edc_lab import LabProfile
from respond_labs.panels import (
    blood_glucose_panel,
    blood_glucose_poc_panel,
    hba1c_panel,
    hba1c_poc_panel,
)

from .panels import chemistry_lipids_panel

subject_lab_profile = LabProfile(
    name="subject_lab_profile", requisition_model=settings.SUBJECT_REQUISITION_MODEL
)

subject_lab_profile.add_panel(blood_glucose_panel)
subject_lab_profile.add_panel(blood_glucose_poc_panel)
subject_lab_profile.add_panel(hba1c_panel)
subject_lab_profile.add_panel(hba1c_poc_panel)
subject_lab_profile.add_panel(chemistry_lipids_panel)
