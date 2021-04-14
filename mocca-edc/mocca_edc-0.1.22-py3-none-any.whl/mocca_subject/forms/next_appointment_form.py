import pdb

from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator
from respond_forms.form_validator_mixins import CrfFormValidatorMixin
from respond_forms.utils import raise_if_clinical_review_does_not_exist

from mocca_consent.models import SubjectConsent

from ..models import NextAppointment, SubjectVisit


class NextAppointmentValidator(CrfFormValidatorMixin, FormValidator):
    def clean(self):
        raise_if_clinical_review_does_not_exist(self.cleaned_data.get("subject_visit"))
        self.date_not_before(
            "report_datetime",
            "appt_date",
            convert_to_date=True,
        )

    @property
    def clinic_type(self):
        return SubjectConsent.objects.get(
            subject_identifier=self.subject_identifier
        ).clinic_type


class NextAppointmentForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = NextAppointmentValidator

    def __init__(self, *args, **kwargs):
        try:
            appt_date = SubjectVisit.objects.get(
                id=kwargs.get("initial").get("subject_visit")
            ).appointment.next.appt_datetime
        except AttributeError:
            pass
        else:
            kwargs["initial"].update(appt_date=appt_date)
        super().__init__(*args, **kwargs)

    class Meta:
        model = NextAppointment
        fields = "__all__"
