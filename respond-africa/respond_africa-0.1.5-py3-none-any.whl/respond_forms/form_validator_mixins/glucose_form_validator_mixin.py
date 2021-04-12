from edc_constants.constants import YES
from edc_form_validators import FormValidator


class GlucoseFormValidatorMixin(FormValidator):
    def validate_glucose_test(self):
        self.required_if(YES, field="glucose_performed", field_required="glucose_date")
        self.required_if(YES, field="glucose_performed", field_required="glucose_fasted")
        self.required_if(YES, field="glucose_performed", field_required="glucose")
        self.required_if(YES, field="glucose_performed", field_required="glucose_quantifier")
        self.applicable_if(YES, field="glucose_performed", field_applicable="glucose_units")
