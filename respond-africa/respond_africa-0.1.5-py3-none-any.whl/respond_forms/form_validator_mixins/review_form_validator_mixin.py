from edc_constants.constants import NO
from edc_form_validators import FormValidator


class ReviewFormValidatorMixin(FormValidator):
    def validate_care_delivery(self) -> None:
        self.required_if(NO, field="care_delivery", field_required="care_delivery_other")
