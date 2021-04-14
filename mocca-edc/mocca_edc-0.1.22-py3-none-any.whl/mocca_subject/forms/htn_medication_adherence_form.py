from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_model.widgets import SliderWidget
from respond_forms.form_validator_mixins import (
    CrfFormValidatorMixin,
    MedicationAdherenceFormValidatorMixin,
)

from ..models import HtnMedicationAdherence


class HtnMedicationAdherenceFormValidator(
    MedicationAdherenceFormValidatorMixin,
    CrfFormValidatorMixin,
    FormValidator,
):
    pass


class HtnMedicationAdherenceForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = HtnMedicationAdherenceFormValidator

    visual_score_slider = forms.CharField(
        label="Visual Score", widget=SliderWidget(attrs={"min": 0, "max": 100})
    )

    class Meta:
        model = HtnMedicationAdherence
        fields = "__all__"
