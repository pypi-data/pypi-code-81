from pprint import pprint

from django import forms
from django.test import TestCase, tag
from edc_constants.constants import STUDY_DEFINED_TIMEPOINT
from edc_utils import get_utcnow
from edc_visit_schedule.constants import DAY1
from edc_visit_tracking.constants import SCHEDULED

from mocca_lists.models import ClinicServices
from mocca_subject.forms.subject_visit_form import SubjectVisitFormValidator

from ..mocca_test_case_mixin import MoccaTestCaseMixin


class TestSubjectVisit(MoccaTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_screening = self.get_subject_screening(report_datetime=get_utcnow())
        self.subject_consent = self.get_subject_consent(
            subject_screening=self.subject_screening
        )

    @tag("v")
    def test_baseline_subject_visit_form(self):
        appointment = self.get_appointment(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code=DAY1,
            visit_code_sequence=0,
            reason=SCHEDULED,
        )
        clinic_services = ClinicServices.objects.filter(name=STUDY_DEFINED_TIMEPOINT)
        cleaned_data = dict(
            appointment=appointment,
            report_datetime=appointment.appt_datetime,
            clinic_services=clinic_services,
            reason=SCHEDULED,
        )
        form_validator = SubjectVisitFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except forms.ValidationError:
            pass
        pprint(form_validator._errors)
        self.assertNotIn("health_services", form_validator._errors)
