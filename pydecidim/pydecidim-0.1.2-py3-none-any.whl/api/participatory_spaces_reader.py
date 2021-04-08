"""
This Reader retrives a full Proposal information.
"""
from typing import List

from pydecidim.api.decidim_connector import DecidimConnector
from pydecidim.api.participatory_space_name_enum import ParticipatorySpaceNameEnum
from pydecidim.api.participatory_space_reader import ParticipatorySpaceReader
# Path to the query schema
from pydecidim.model.elemental_type_element import ElementalTypeElement
from pydecidim.model.participatory_process_filter import ParticipatorySpaceFilter
from pydecidim.model.participatory_process_sort import ParticipatorySpaceSort

QUERY_PATH = 'pydecidim/queries/participatory_spaces.graphql'


class ParticipatorySpacesReader(ParticipatorySpaceReader):
    """
    This reader retrieves a Proposal from Decidim.
    """

    def __init__(self, decidim_connector: DecidimConnector,
                 participatory_space_name: ParticipatorySpaceNameEnum,
                 base_path="."):
        """

        :param decidim_connector: An instance of a DecidimConnector class.
        :param base_path: The base path to the schema directory.
        """
        super().__init__(decidim_connector, participatory_space_name, base_path + "/" + QUERY_PATH)

    def execute(self) -> List[str]:
        """
        Send the query to the API and extract a list of participatory processes.
        :return: A list of participatory processes ids.
        """

        component_filter: ParticipatorySpaceFilter = ParticipatorySpaceFilter()
        component_sort: ParticipatorySpaceSort = ParticipatorySpaceSort()
        response: dict = super().process_query_from_file({'filter': component_filter,
                                                          'order': component_sort,
                                                          'PARTICIPATORY_SPACE_NAME':
                                                              ElementalTypeElement(
                                                                  super().participatory_space_name.value)
                                                          })

        participatory_processes: List[str] = []
        for participatory_process_dict in response[super().participatory_space_name.value]:
            participatory_process_id: str = participatory_process_dict['id']
            participatory_processes.append(participatory_process_id)
        return participatory_processes
