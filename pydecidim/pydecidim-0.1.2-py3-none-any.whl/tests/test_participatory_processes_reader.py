import unittest
from typing import List

from pydecidim.api.abstract_decidim_reader import DecidimConnector
from pydecidim.api.participatory_spaces_reader import ParticipatorySpacesReader

QUERY_PATH = "https://www.decidim.barcelona/api"


class ParticipatoryProcessesReaderTest(unittest.TestCase):
    def test_execute(self):
        decidim_connector: DecidimConnector = DecidimConnector(QUERY_PATH)
        reader: ParticipatorySpacesReader = ParticipatorySpacesReader(decidim_connector, base_path="../..")
        participatory_processes: List[str] = reader.execute()
        self.assertIsInstance(participatory_processes, List)
        if len(participatory_processes) > 0:
            self.assertIsInstance(participatory_processes[0], str)


if __name__ == '__main__':
    unittest.main()
