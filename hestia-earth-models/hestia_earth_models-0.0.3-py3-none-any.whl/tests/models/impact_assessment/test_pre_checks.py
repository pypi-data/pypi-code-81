import unittest
from unittest.mock import patch

from hestia_earth.models.impact_assessment.pre_checks import run

class_path = 'hestia_earth.models.impact_assessment.pre_checks'


class TestPreChecks(unittest.TestCase):
    @patch(f"{class_path}._run_in_serie", return_value={})
    def test_run(self, mock_run_in_serie):
        run({})
        mock_run_in_serie.assert_called_once
