from django import forms


class InitialReviewFormValidatorMixin:
    def raise_if_both_ago_and_actual_date(self):
        if self.cleaned_data.get("dx_ago") and self.cleaned_data.get("dx_date"):
            raise forms.ValidationError(
                {
                    "dx_ago": (
                        "Date conflict. Do not provide a response "
                        "here if the exact data of diagnosis is available."
                    )
                }
            )
