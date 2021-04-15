import pdb
from typing import Optional

from django import forms
from django.conf import settings
from edc_form_validators import FormValidator
from edc_utils import convert_php_dateformat

from respond_models.diagnoses import Diagnoses, InitialReviewRequired


class ResultFormValidatorMixin(FormValidator):
    def validate_test_date_by_dx_date(
        self, prefix: str, dx_msg_label: str, test_date_fld: Optional[str] = None
    ) -> None:
        return self.validate_drawn_date_by_dx_date(
            prefix=prefix, dx_msg_label=dx_msg_label, drawn_date_fld=test_date_fld
        )

    def validate_drawn_date_by_dx_date(
        self, prefix: str, dx_msg_label: str, drawn_date_fld: Optional[str] = None
    ):
        drawn_date_fld = drawn_date_fld or "drawn_date"
        dx = Diagnoses(
            subject_visit=self.cleaned_data.get("subject_visit"),
            lte=True,
            limit_to_single_condition_prefix=prefix,
        )
        try:
            dx_date = dx.get_dx_date(prefix)
        except InitialReviewRequired:
            dx_date = None
        if not dx_date:
            raise forms.ValidationError(
                f"A {dx_msg_label} diagnosis has not been reported for this subject."
            )
        else:
            if dx_date > self.cleaned_data.get(drawn_date_fld):
                formatted_date = dx_date.strftime(
                    convert_php_dateformat(settings.SHORT_DATE_FORMAT)
                )
                raise forms.ValidationError(
                    {
                        "drawn_date": (
                            "Invalid. Subject was diagnosed with "
                            f"{dx_msg_label} on {formatted_date}."
                        )
                    }
                )
