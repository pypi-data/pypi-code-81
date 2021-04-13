from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from respond_forms.form_validator_mixins import (
    CrfFormValidatorMixin,
    DrugRefillFormValidatorMixin,
)

from ..models import DrugRefillDm


class DrugRefillDmFormValidator(
    DrugRefillFormValidatorMixin, CrfFormValidatorMixin, FormValidator
):
    pass


class DrugRefillDmForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = DrugRefillDmFormValidator

    class Meta:
        model = DrugRefillDm
        fields = "__all__"
