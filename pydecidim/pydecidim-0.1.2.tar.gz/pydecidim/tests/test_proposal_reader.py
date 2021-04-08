import unittest

from pydecidim.api.decidim_connector import DecidimConnector
from pydecidim.api.participatory_space_name_enum import ParticipatorySpaceNameEnum
from pydecidim.api.proposal_reader import ProposalReader
from pydecidim.model.proposal import Proposal

QUERY_PATH = "https://www.decidim.barcelona/api"


class ProposalReaderTest(unittest.TestCase):
    def test_execute_not_exists(self):
        decidim_connector: DecidimConnector = DecidimConnector(QUERY_PATH)
        reader: ProposalReader = ProposalReader(decidim_connector, base_path="../..",
                                                participatory_space_name=ParticipatorySpaceNameEnum.PARTICIPATORY_PROCESS)
        # We use the participatory process #48 on Decidim.org api and the Proposal #12040
        proposal: Proposal = reader.execute("48", "1")
        self.assertIsNone(proposal)

    def test_execute(self):
        decidim_connector: DecidimConnector = DecidimConnector(QUERY_PATH)
        reader: ProposalReader = ProposalReader(decidim_connector, base_path="../..",
                                                participatory_space_name=ParticipatorySpaceNameEnum.PARTICIPATORY_PROCESS)
        # We use the participatory process #5 on Decidim.org api and the Proposal #10953
        proposal: Proposal = reader.execute("5", "10953")
        self.assertIsInstance(proposal, Proposal)


if __name__ == '__main__':
    unittest.main()
