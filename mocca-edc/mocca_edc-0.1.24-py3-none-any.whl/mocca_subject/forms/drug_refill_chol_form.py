from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from respond_forms.form_validator_mixins import (
    CrfFormValidatorMixin,
    DrugRefillFormValidatorMixin,
)

from ..models import DrugRefillChol


class DrugRefillCholFormValidator(
    DrugRefillFormValidatorMixin, CrfFormValidatorMixin, FormValidator
):
    pass


class DrugRefillCholForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = DrugRefillCholFormValidator

    class Meta:
        model = DrugRefillChol
        fields = "__all__"
