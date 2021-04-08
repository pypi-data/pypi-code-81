"""
This Reader retrives a list of Proposals from Decidim.
"""
from typing import List

from pydecidim.api.decidim_connector import DecidimConnector
from pydecidim.api.participatory_space_name_enum import ParticipatorySpaceNameEnum
from pydecidim.api.participatory_space_reader import ParticipatorySpaceReader
from pydecidim.model.elemental_type_element import ElementalTypeElement
# Path to the query schema
from pydecidim.model.proposal import Proposal

QUERY_PATH = 'pydecidim/queries/proposals.graphql'


class ProposalsReader(ParticipatorySpaceReader):
    """
    This reader retrieves list of Proposals from Decidim.
    """

    def __init__(self, decidim_connector: DecidimConnector,
                 participatory_space_name: ParticipatorySpaceNameEnum,
                 base_path="."):
        """

        :param decidim_connector: An instance of a DecidimConnector class.
        :param base_path: The base path to the schema directory.
        """
        super().__init__(decidim_connector, participatory_space_name, base_path + "/" + QUERY_PATH)

    def execute(self, participatory_process_id: str) -> List[str]:
        """
        Send the query to the API and extract a list of proposals ids from a participatory space.
        :param participatory_process_id: The participatory process id.
        :return: A list of proposals ids.
        """

        response: dict = super().process_query_from_file({
            'id': ElementalTypeElement(participatory_process_id),
            'PARTICIPATORY_SPACE_NAME': ElementalTypeElement(super().participatory_space_name.value)
        })

        proposals_id: List[Proposal] = []
        for component in response[super().participatory_space_name.value]['components']:
            for proposal_dict in component['proposals']['edges']:
                proposal_id: str = proposal_dict['node']['id']
                proposals_id.append(proposal_id)
        return proposals_id
