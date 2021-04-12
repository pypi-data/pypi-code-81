from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from respond_forms.form_validator_mixins import (
    CrfFormValidatorMixin,
    ResultFormValidatorMixin,
)
from respond_forms.utils import (
    raise_if_baseline,
    raise_if_clinical_review_does_not_exist,
)

from ..models import ViralLoadResult


class ViralLoadResultFormValidator(
    ResultFormValidatorMixin, CrfFormValidatorMixin, FormValidator
):
    def clean(self):
        if self.cleaned_data.get("subject_visit"):
            raise_if_baseline(self.cleaned_data.get("subject_visit"))
            raise_if_clinical_review_does_not_exist(self.cleaned_data.get("subject_visit"))
        self.validate_drawn_date_by_dx_date("hiv", "HIV infection")


class ViralLoadResultForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ViralLoadResultFormValidator

    class Meta:
        model = ViralLoadResult
        fields = "__all__"
