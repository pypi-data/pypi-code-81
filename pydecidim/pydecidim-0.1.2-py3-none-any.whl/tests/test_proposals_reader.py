import unittest
from typing import List

from pydecidim.api.decidim_connector import DecidimConnector
from pydecidim.api.proposals_reader import ProposalsReader

QUERY_PATH = "https://www.decidim.barcelona/api"


class ProposalsReaderTest(unittest.TestCase):
    def test_execute(self):
        decidim_connector: DecidimConnector = DecidimConnector(QUERY_PATH)
        reader: ProposalsReader = ProposalsReader(decidim_connector, base_path="../..")
        # We use the participatory process #40.
        proposals: List[str] = reader.execute("40")
        self.assertIsInstance(proposals, List)
        if len(proposals) > 0:
            self.assertIsInstance(proposals[0], str)


if __name__ == '__main__':
    unittest.main()
