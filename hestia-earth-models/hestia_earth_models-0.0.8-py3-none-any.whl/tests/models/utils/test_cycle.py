import unittest
from unittest.mock import patch
from hestia_earth.schema import TermTermType

from hestia_earth.models.utils.cycle import _is_term_type_complete, _is_term_type_incomplete


class TestCycle(unittest.TestCase):
    @patch('hestia_earth.models.utils.cycle.download_hestia')
    def test_is_term_type_complete(self, mock_download):
        cycle = {'dataCompleteness': {}}

        cycle['dataCompleteness'][TermTermType.CROPRESIDUE.value] = True
        mock_download.return_value = {
            'termType': TermTermType.CROPRESIDUE.value
        }
        self.assertEqual(_is_term_type_complete(cycle, 'termid'), True)

        cycle['dataCompleteness'][TermTermType.CROPRESIDUE.value] = False
        mock_download.return_value = {
            'termType': TermTermType.CROPRESIDUE.value
        }
        self.assertEqual(_is_term_type_complete(cycle, 'termid'), False)

        # termType not in dataCompleteness
        mock_download.return_value = {
            'termType': TermTermType.CROPRESIDUEMANAGEMENT.value
        }
        self.assertEqual(_is_term_type_complete(cycle, 'termid'), False)

    @patch('hestia_earth.models.utils.cycle.download_hestia')
    def test_is_term_type_incomplete(self, mock_download):
        cycle = {'dataCompleteness': {}}

        cycle['dataCompleteness'][TermTermType.CROPRESIDUE.value] = True
        mock_download.return_value = {
            'termType': TermTermType.CROPRESIDUE.value
        }
        self.assertEqual(_is_term_type_incomplete(cycle, 'termid'), False)

        cycle['dataCompleteness'][TermTermType.CROPRESIDUE.value] = False
        mock_download.return_value = {
            'termType': TermTermType.CROPRESIDUE.value
        }
        self.assertEqual(_is_term_type_incomplete(cycle, 'termid'), True)

        # termType not in dataCompleteness
        mock_download.return_value = {
            'termType': TermTermType.CROPRESIDUEMANAGEMENT.value
        }
        self.assertEqual(_is_term_type_incomplete(cycle, 'termid'), True)
