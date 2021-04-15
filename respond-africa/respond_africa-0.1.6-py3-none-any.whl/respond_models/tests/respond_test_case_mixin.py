from dateutil.relativedelta import relativedelta
from django.test import TestCase
from edc_appointment.tests.appointment_test_case_mixin import AppointmentTestCaseMixin
from edc_facility.import_holidays import import_holidays
from edc_utils import get_dob, get_utcnow
from edc_visit_schedule.constants import DAY1
from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED

from respond_test_app.models import SubjectConsent, SubjectVisit
from respond_test_app.visit_schedules import visit_schedule


class RespondModelTestCaseMixin(AppointmentTestCaseMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        import_holidays()

    def setUp(self):
        self.visit_schedule_name = "visit_schedule"
        self.schedule_name = "schedule"

        self.schedule = visit_schedule.schedules.get("schedule")

        self.subject_identifier = "111111111"
        self.subject_identifiers = [
            self.subject_identifier,
            "222222222",
            "333333333",
            "444444444",
        ]
        self.consent_datetime = get_utcnow() - relativedelta(weeks=4)
        dob = get_dob(age_in_years=25, now=self.consent_datetime)
        for subject_identifier in self.subject_identifiers:
            subject_consent = SubjectConsent.objects.create(
                subject_identifier=subject_identifier,
                identity=subject_identifier,
                confirm_identity=subject_identifier,
                consent_datetime=self.consent_datetime,
                dob=dob,
            )
            self.schedule.put_on_schedule(
                subject_identifier=subject_consent.subject_identifier,
                onschedule_datetime=self.consent_datetime,
            )
        self.subject_consent = SubjectConsent.objects.get(
            subject_identifier=self.subject_identifier, dob=dob
        )

    @property
    def subject_visit_model_cls(self):
        return SubjectVisit

    def get_subject_visit(
        self,
        visit_code=None,
        visit_code_sequence=None,
        reason=None,
        appointment=None,
    ):
        reason = reason or SCHEDULED
        if not appointment:
            visit_code = visit_code or DAY1
            visit_code_sequence = 0 if visit_code_sequence is None else visit_code_sequence
            appointment = self.get_appointment(
                subject_identifier=self.subject_consent.subject_identifier,
                visit_code=visit_code,
                visit_code_sequence=visit_code_sequence,
                reason=reason,
            )
        return self.subject_visit_model_cls.objects.create(
            appointment=appointment, reason=reason
        )

    def get_next_subject_visit(
        self,
        subject_visit=None,
        reason=None,
    ):
        visit_code = (
            subject_visit.appointment.visit_code
            if reason == UNSCHEDULED
            else subject_visit.appointment.next.visit_code
        )
        visit_code_sequence = (
            subject_visit.appointment.visit_code_sequence if reason == UNSCHEDULED else 0
        )
        return self.get_subject_visit(
            visit_code=visit_code,
            visit_code_sequence=visit_code_sequence,
            reason=reason,
        )
