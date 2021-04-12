from django.test import TestCase, tag

from respond_models.utils import is_baseline

from .respond_test_case_mixin import RespondModelTestCaseMixin


class TestUtils(RespondModelTestCaseMixin, TestCase):
    def test_is_baseline(self):
        subject_visit_baseline = self.get_subject_visit()
        self.assertTrue(is_baseline(subject_visit_baseline))

        subject_visit_followup = self.get_next_subject_visit(subject_visit_baseline)
        self.assertFalse(is_baseline(subject_visit_followup))
