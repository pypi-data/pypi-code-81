from django.test import TestCase, tag
from edc_appointment.constants import INCOMPLETE_APPT
from edc_constants.constants import CHOL, DM, HIV, HTN, NOT_APPLICABLE, POS, YES
from edc_visit_tracking.constants import UNSCHEDULED
from model_bakery import baker

from respond_models.diagnoses import (
    ClinicalReviewBaselineRequired,
    Diagnoses,
    InitialReviewRequired,
    MultipleInitialReviewsExist,
)

from .respond_test_case_mixin import RespondModelTestCaseMixin


class TestDiagnoses(RespondModelTestCaseMixin, TestCase):
    def test_diagnoses(self):
        subject_visit_baseline = self.get_subject_visit()

        subject_visit_baseline.save()

        self.assertRaises(
            ClinicalReviewBaselineRequired,
            Diagnoses,
            subject_identifier=subject_visit_baseline.subject_identifier,
        )

        clinical_review_baseline = baker.make(
            "respond_test_app.clinicalreviewbaseline",
            subject_visit=subject_visit_baseline,
            hiv_test=YES,
            hiv_dx=YES,
            hiv_test_ago="5y",
        )
        try:
            diagnoses = Diagnoses(
                subject_identifier=subject_visit_baseline.subject_identifier,
            )
        except ClinicalReviewBaselineRequired:
            self.fail("DiagnosesError unexpectedly raised")

        self.assertEqual(YES, diagnoses.get_dx(HIV))
        self.assertIsNone(diagnoses.get_dx(HTN))
        self.assertIsNone(diagnoses.get_dx(DM))

        clinical_review_baseline.htn_test = YES
        clinical_review_baseline.htn_test_ago = "1y"
        clinical_review_baseline.htn_dx = YES
        clinical_review_baseline.save()

        diagnoses = Diagnoses(
            subject_identifier=subject_visit_baseline.subject_identifier,
        )
        self.assertEqual(YES, diagnoses.get_dx(HIV))
        self.assertEqual(YES, diagnoses.get_dx(HTN))
        self.assertIsNone(diagnoses.get_dx(DM))

        clinical_review_baseline.dm_test = YES
        clinical_review_baseline.dm_test_ago = "1y"
        clinical_review_baseline.dm_dx = YES
        clinical_review_baseline.save()

        diagnoses = Diagnoses(
            subject_identifier=subject_visit_baseline.subject_identifier,
        )
        self.assertEqual(YES, diagnoses.get_dx(HIV))
        self.assertEqual(YES, diagnoses.get_dx(HTN))
        self.assertEqual(YES, diagnoses.get_dx(DM))

    def test_diagnoses_does_not_raise_for_subject_visit(self):
        """ "Note: Source of the exception will be in
        the metadata rule
        """
        try:
            subject_visit_baseline = self.get_subject_visit()
        except ClinicalReviewBaselineRequired:
            self.fail("DiagnosesError unexpectedly raised")

        try:
            subject_visit_baseline.save()
        except ClinicalReviewBaselineRequired:
            self.fail("DiagnosesError unexpectedly raised")

    def test_diagnoses_dates_baseline_raises(self):
        """Assert expects the initial review model instance before
        returning a dx.
        """
        subject_visit_baseline = self.get_subject_visit()

        for prefix in [HIV, DM, HTN, CHOL]:
            prefix = prefix.lower()
            opts = {
                "subject_visit": subject_visit_baseline,
                f"{prefix}_test": POS,
                f"{prefix}_dx": YES,
                f"{prefix}_test_ago": "5y",
            }
            obj = baker.make("respond_test_app.clinicalreviewbaseline", **opts)
            diagnoses = Diagnoses(
                subject_identifier=subject_visit_baseline.subject_identifier,
            )
            self.assertRaises(InitialReviewRequired, diagnoses.get_dx_date, HIV)
            obj.delete()

    def test_diagnoses_dates_baseline(self):
        subject_visit_baseline = self.get_subject_visit()

        clinical_review_baseline = baker.make(
            "respond_test_app.clinicalreviewbaseline",
            subject_visit=subject_visit_baseline,
            hiv_test=POS,
            hiv_dx=YES,
            hiv_test_ago="5y",
        )
        baker.make(
            "respond_test_app.hivinitialreview",
            subject_visit=subject_visit_baseline,
            dx_ago="5y",
            arv_initiation_ago="4y",
        )
        diagnoses = Diagnoses(
            subject_identifier=subject_visit_baseline.subject_identifier,
        )

        self.assertEqual(YES, diagnoses.get_dx(HIV))
        self.assertEqual(
            diagnoses.get_dx_date(HIV),
            clinical_review_baseline.hiv_test_estimated_date,
        )
        self.assertIsNone(diagnoses.get_dx_date(DM))
        self.assertIsNone(diagnoses.get_dx_date(HTN))

        diagnoses = Diagnoses(
            subject_identifier=subject_visit_baseline.subject_identifier,
            report_datetime=subject_visit_baseline.report_datetime,
            lte=True,
        )

        self.assertEqual(YES, diagnoses.get_dx(HIV))
        self.assertEqual(
            diagnoses.get_dx_date(HIV),
            clinical_review_baseline.hiv_test_estimated_date,
        )
        self.assertIsNone(diagnoses.get_dx_date(DM))
        self.assertIsNone(diagnoses.get_dx_date(HTN))

        diagnoses = Diagnoses(
            subject_identifier=subject_visit_baseline.subject_identifier,
            report_datetime=subject_visit_baseline.report_datetime,
            lte=False,
        )

        self.assertEqual(YES, diagnoses.get_dx(HIV))
        self.assertEqual(
            diagnoses.get_dx_date(HIV),
            clinical_review_baseline.hiv_test_estimated_date,
        )
        self.assertIsNone(diagnoses.get_dx_date(DM))
        self.assertIsNone(diagnoses.get_dx_date(HTN))

    def test_diagnoses_dates(self):
        subject_visit_baseline = self.get_subject_visit()

        baker.make(
            "respond_test_app.clinicalreviewbaseline",
            subject_visit=subject_visit_baseline,
            hiv_test=POS,
            hiv_dx=YES,
            hiv_test_ago="5y",
        )

        hiv_initial_review = baker.make(
            "respond_test_app.hivinitialreview",
            subject_visit=subject_visit_baseline,
            dx_ago="5y",
            arv_initiation_ago="4y",
        )

        subject_visit_baseline.appointment.appt_status = INCOMPLETE_APPT
        subject_visit_baseline.appointment.save()
        subject_visit_baseline.appointment.refresh_from_db()
        subject_visit_baseline.refresh_from_db()

        subject_visit = self.get_next_subject_visit(
            subject_visit=subject_visit_baseline, reason=UNSCHEDULED
        )

        baker.make(
            "respond_test_app.clinicalreview",
            subject_visit=subject_visit,
            hiv_test=NOT_APPLICABLE,
            hiv_dx=NOT_APPLICABLE,
            hiv_test_date=None,
            htn_test=YES,
            htn_dx=YES,
            htn_test_date=subject_visit.report_datetime,
        )

        htn_initial_review = baker.make(
            "respond_test_app.htninitialreview",
            subject_visit=subject_visit,
            dx_ago=None,
            dx_date=subject_visit.report_datetime,
        )

        diagnoses = Diagnoses(
            subject_identifier=subject_visit.subject_identifier,
            report_datetime=subject_visit.report_datetime,
            lte=True,
        )
        self.assertIsNotNone(diagnoses.get_dx_date(HIV))
        self.assertEqual(
            diagnoses.get_dx_date(HIV),
            hiv_initial_review.get_best_dx_date().date(),
        )

        self.assertEqual(
            diagnoses.get_dx_date(HTN),
            htn_initial_review.get_best_dx_date().date(),
        )
        self.assertIsNotNone(diagnoses.get_dx_date(HTN))

    def test_diagnoses_dates_baseline2(self):
        subject_visit_baseline = self.get_subject_visit()

        baker.make(
            "respond_test_app.clinicalreviewbaseline",
            subject_visit=subject_visit_baseline,
            hiv_test=POS,
            hiv_dx=YES,
            hiv_test_ago="5y",
        )
        baker.make(
            "respond_test_app.hivinitialreview",
            subject_visit=subject_visit_baseline,
            dx_ago="5y",
            arv_initiation_ago="4y",
        )
        subject_visit_baseline.appointment.appt_status = INCOMPLETE_APPT
        subject_visit_baseline.appointment.save()
        subject_visit_baseline.appointment.refresh_from_db()
        subject_visit_baseline.refresh_from_db()

        subject_visit = self.get_next_subject_visit(
            subject_visit=subject_visit_baseline, reason=UNSCHEDULED
        )

        baker.make(
            "respond_test_app.hivinitialreview",
            subject_visit=subject_visit,
            dx_ago="5y",
            arv_initiation_ago="4y",
        )

        diagnoses = Diagnoses(
            subject_identifier=subject_visit_baseline.subject_identifier,
        )
        self.assertRaises(MultipleInitialReviewsExist, getattr, diagnoses, "initial_reviews")
