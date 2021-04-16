from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from respond_forms.form_validator_mixins import (
    CrfFormValidatorMixin,
    DrugRefillFormValidatorMixin,
)

from ..models import DrugRefillHiv


class DrugRefillHivFormValidator(
    DrugRefillFormValidatorMixin, CrfFormValidatorMixin, FormValidator
):
    pass


class DrugRefillHivForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = DrugRefillHivFormValidator

    class Meta:
        model = DrugRefillHiv
        fields = "__all__"
