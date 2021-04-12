from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from edc_model.widgets import SliderWidget
from respond_forms.form_validator_mixins import (
    CrfFormValidatorMixin,
    MedicationAdherenceFormValidatorMixin,
)

from ..models import CholMedicationAdherence


class CholMedicationAdherenceFormValidator(
    MedicationAdherenceFormValidatorMixin,
    CrfFormValidatorMixin,
    FormValidator,
):
    pass


class CholMedicationAdherenceForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = CholMedicationAdherenceFormValidator

    visual_score_slider = forms.CharField(
        label="Visual Score", widget=SliderWidget(attrs={"min": 0, "max": 100})
    )

    class Meta:
        model = CholMedicationAdherence
        fields = "__all__"
