from django import forms
from edc_action_item.forms.action_item_form_mixin import ActionItemFormMixin
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator
from respond_forms.form_validator_mixins import (
    CrfFormValidatorMixin,
    HivInitialReviewFormValidatorMixin,
)

from ..models import HivInitialReview


class HivInitialReviewFormValidator(
    HivInitialReviewFormValidatorMixin,
    CrfFormValidatorMixin,
    FormValidator,
):
    def match_screening_clinic_or_raise(self):
        pass


class HivInitialReviewForm(
    CrfModelFormMixin,
    ActionItemFormMixin,
    forms.ModelForm,
):
    form_validator_cls = HivInitialReviewFormValidator

    class Meta:
        model = HivInitialReview
        fields = "__all__"
