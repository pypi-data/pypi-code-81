from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_constants.constants import NO, NOT_APPLICABLE, YES
from edc_lab.constants import EQ
from edc_reportable import MILLIMOLES_PER_LITER
from edc_utils import get_utcnow
from model_bakery import baker

from respond_models.tests.respond_test_case_mixin import RespondModelTestCaseMixin

from ..form_validators import GlucoseFormValidator


class TestGlucose(RespondModelTestCaseMixin, TestCase):
    def test_requirement_at_baseline(self):
        class MyGlucoseFormValidator(GlucoseFormValidator):
            required_at_baseline = False

        subject_visit_baseline = self.get_subject_visit()

        cleaned_data = dict(
            subject_visit=subject_visit_baseline,
            glucose_performed=NO,
        )
        form_validator = MyGlucoseFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(forms.ValidationError) as cm:
            form_validator.validate()
        e = cm.exception
        self.assertEqual(e.message, "This form is not available for completion at baseline.")

    def test_not_required_at_baseline(self):
        class MyGlucoseFormValidator(GlucoseFormValidator):
            required_at_baseline = True

        subject_visit_baseline = self.get_subject_visit()

        cleaned_data = dict(subject_visit=subject_visit_baseline, glucose_performed=NO)
        form_validator = MyGlucoseFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(forms.ValidationError) as cm:
            form_validator.validate()
        e = cm.exception
        self.assertNotEqual(
            e.message, "This form is not available for completion at baseline."
        )

    def test_requires_clinical_initial_review_at_baseline(self):
        class MyGlucoseFormValidator(GlucoseFormValidator):
            required_at_baseline = True

        subject_visit_baseline = self.get_subject_visit()
        cleaned_data = dict(
            subject_visit=subject_visit_baseline,
            glucose_performed=NO,
        )
        form_validator = MyGlucoseFormValidator(cleaned_data=cleaned_data)

        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertEqual(
            cm.exception.message, "Complete the `Clinical Review: Baseline` CRF first."
        )

        baker.make(
            "respond_test_app.clinicalreviewbaseline",
            subject_visit=subject_visit_baseline,
            dm_test=YES,
            dm_dx=YES,
            dm_test_ago="5y",
        )

        try:
            form_validator.validate()
        except ValidationError:
            self.fail("ValidationError unexceptedly raised")

    def test_requires_clinical_review_at_followup(self):
        class MyGlucoseFormValidator(GlucoseFormValidator):
            required_at_baseline = True

        subject_visit_baseline = self.get_subject_visit()
        baker.make(
            "respond_test_app.clinicalreviewbaseline",
            subject_visit=subject_visit_baseline,
            dm_test=YES,
            dm_dx=YES,
            dm_test_ago="5y",
        )

        subject_visit_followup = self.get_next_subject_visit(subject_visit_baseline)
        cleaned_data = dict(
            subject_visit=subject_visit_followup,
            glucose_performed=NO,
        )
        form_validator = MyGlucoseFormValidator(cleaned_data=cleaned_data)

        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        e = cm.exception
        self.assertEqual(e.message, "Complete the `Clinical Review` CRF first.")

        baker.make(
            "respond_test_app.clinicalreview",
            subject_visit=subject_visit_followup,
        )

        try:
            form_validator.validate()
        except ValidationError:
            self.fail("ValidationError unexceptedly raised")

    def test_requires_diagnosis(self):
        class MyGlucoseFormValidator(GlucoseFormValidator):
            required_at_baseline = True
            require_diagnosis = True

        subject_visit_baseline = self.get_subject_visit()
        baker.make(
            "respond_test_app.clinicalreviewbaseline",
            subject_visit=subject_visit_baseline,
            dm_test=YES,
            dm_dx=YES,
            dm_test_ago="5y",
        )
        cleaned_data = dict(
            subject_visit=subject_visit_baseline,
            glucose_performed=NO,
        )
        form_validator = MyGlucoseFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        e = cm.exception
        self.assertEqual(e.message, "Complete the `Diabetes Initial Review` CRF first.")

        baker.make(
            "respond_test_app.dminitialreview",
            subject_visit=subject_visit_baseline,
            dx_date=subject_visit_baseline.report_datetime,
        )

        try:
            form_validator.validate()
        except ValidationError:
            self.fail("ValidationError unexceptedly raised")

    def test_diagnosis_not_required(self):
        class MyGlucoseFormValidator(GlucoseFormValidator):
            required_at_baseline = True
            require_diagnosis = False

        subject_visit_baseline = self.get_subject_visit()
        baker.make(
            "respond_test_app.clinicalreviewbaseline",
            subject_visit=subject_visit_baseline,
            dm_test=YES,
            dm_dx=YES,
            dm_test_ago="5y",
        )
        cleaned_data = dict(
            subject_visit=subject_visit_baseline,
            glucose_performed=NO,
        )
        form_validator = MyGlucoseFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError:
            self.fail("ValidationError unexceptedly raised")

    def test_glucose_result(self):
        class MyGlucoseFormValidator(GlucoseFormValidator):
            required_at_baseline = True
            require_diagnosis = False

        subject_visit_baseline = self.get_subject_visit()
        baker.make(
            "respond_test_app.clinicalreviewbaseline",
            subject_visit=subject_visit_baseline,
            dm_test=YES,
            dm_dx=YES,
            dm_test_ago="5y",
        )
        cleaned_data = dict(
            subject_visit=subject_visit_baseline,
            glucose_performed=YES,
            glucose_units=NOT_APPLICABLE,
        )
        form_validator = MyGlucoseFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("glucose_date", cm.exception.error_dict)

        cleaned_data = dict(
            subject_visit=subject_visit_baseline,
            glucose_performed=YES,
            glucose_date=get_utcnow().date,
            glucose_units=NOT_APPLICABLE,
        )
        form_validator = MyGlucoseFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("glucose_fasted", cm.exception.error_dict)

        cleaned_data = dict(
            subject_visit=subject_visit_baseline,
            glucose_performed=YES,
            glucose_date=get_utcnow().date,
            glucose_fasted=YES,
            glucose_units=NOT_APPLICABLE,
        )
        form_validator = MyGlucoseFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("glucose", cm.exception.error_dict)

        cleaned_data = dict(
            subject_visit=subject_visit_baseline,
            glucose_performed=YES,
            glucose_date=get_utcnow().date,
            glucose_fasted=YES,
            glucose=5.3,
            glucose_units=NOT_APPLICABLE,
        )
        form_validator = MyGlucoseFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("glucose_quantifier", cm.exception.error_dict)

        cleaned_data = dict(
            subject_visit=subject_visit_baseline,
            glucose_performed=YES,
            glucose_date=get_utcnow().date,
            glucose_fasted=YES,
            glucose=5.3,
            glucose_quantifier=EQ,
            glucose_units=NOT_APPLICABLE,
        )
        form_validator = MyGlucoseFormValidator(cleaned_data=cleaned_data)
        with self.assertRaises(ValidationError) as cm:
            form_validator.validate()
        self.assertIn("glucose_units", cm.exception.error_dict)

        cleaned_data = dict(
            subject_visit=subject_visit_baseline,
            glucose_performed=YES,
            glucose_date=get_utcnow().date,
            glucose_fasted=YES,
            glucose=5.3,
            glucose_quantifier=MILLIMOLES_PER_LITER,
        )
        form_validator = MyGlucoseFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError:
            self.fail("ValidationError unexceptedly raised")
