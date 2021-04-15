import unittest
from unittest.mock import patch
import json
from tests.utils import fixtures_path

from hestia_earth.models.cycle.dataCompleteness.cropResidue import run

class_path = 'hestia_earth.models.cycle.dataCompleteness.cropResidue'
fixtures_folder = f"{fixtures_path}/cycle/dataCompleteness"


class TestCropResidue(unittest.TestCase):
    @patch(f"{class_path}.find_node")
    def test_run(self, mock_find_node):
        with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
            cycle = json.load(f)

        mock_find_node.return_value = [{'@id': 'aboveGroundCropResidueRemoved'}]
        self.assertEqual(run(cycle), True)

        mock_find_node.return_value = [{'@id': 'unknown-term'}]
        self.assertEqual(run(cycle), False)
