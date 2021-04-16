from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from respond_forms.form_validators import (
    GlucoseFormValidator as BaseGlucoseFormValidator,
)

from ..models import Glucose


class GlucoseFormValidator(BaseGlucoseFormValidator):
    required_at_baseline = False


class GlucoseForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = GlucoseFormValidator

    class Meta:
        model = Glucose
        fields = "__all__"
