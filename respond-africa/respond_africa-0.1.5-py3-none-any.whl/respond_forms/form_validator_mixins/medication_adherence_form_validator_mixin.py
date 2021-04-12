from edc_constants.constants import NEVER
from edc_form_validators import FormValidator

from ..utils import raise_if_clinical_review_does_not_exist


class MedicationAdherenceFormValidatorMixin(FormValidator):
    def clean(self):
        super().clean()
        raise_if_clinical_review_does_not_exist(self.cleaned_data.get("subject_visit"))
        self.not_required_if(
            NEVER, field="last_missed_pill", field_required="missed_pill_reason"
        )
        self.m2m_other_specify(
            m2m_field="missed_pill_reason", field_other="other_missed_pill_reason"
        )
