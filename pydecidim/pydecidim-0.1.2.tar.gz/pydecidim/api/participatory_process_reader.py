"""
This Reader retrives a list of Participatory processes from Decidim.
"""
from typing import List

from pydecidim.api.abstract_decidim_reader import AbstractDecidimReader
from pydecidim.api.decidim_connector import DecidimConnector
from pydecidim.model.component_interface import ComponentInterface
from pydecidim.model.elemental_type_element import ElementalTypeElement
from pydecidim.model.participatory_process import ParticipatoryProcess
# Path to the query schema
from pydecidim.model.translated_field import TranslatedField

QUERY_PATH = 'pydecidim/queries/participatory_process.graphql'


class ParticipatoryProcessReader(AbstractDecidimReader):
    """
    This reader retrieves list of Participatory processes from Decidim.
    """

    def __init__(self, decidim_connector: DecidimConnector, base_path="."):
        """

        :param decidim_connector: An instance of a DecidimConnector class.
        :param base_path: The base path to the schema directory.
        """
        super().__init__(decidim_connector, base_path + "/" + QUERY_PATH)

    def execute(self, participatory_process_id: str) -> ParticipatoryProcess or None:
        """
        Send the query to the API and extract a list of participatory processes.
        :param participatory_process_id: The participatory process id.
        :return: A list of participatory processes.
        """

        response: dict = super().process_query_from_file({'id': ElementalTypeElement(participatory_process_id)})
        participatory_process_dict = response['participatoryProcess']
        if participatory_process_dict is not None:
            translations: [] = participatory_process_dict['title']['translations']
            components_dict: [dict] = participatory_process_dict['components']
            created_at: str = participatory_process_dict['createdAt']
            components: List[ComponentInterface] = []

            for component in components_dict:
                component_id: str = component['id']
                component_name: TranslatedField = TranslatedField.parse_from_gql(component['name']['translations'])
                component_weight: int = component['weight']
                component_interface: ComponentInterface = ComponentInterface(component_id,
                                                                             component_name,
                                                                             component_weight)
                components.append(component_interface)
            title: TranslatedField = TranslatedField.parse_from_gql(translations)
            participatory_process: ParticipatoryProcess = ParticipatoryProcess(process_id=participatory_process_id,
                                                                               title=title,
                                                                               created_at=created_at,
                                                                               components=components)
            return participatory_process
        else:
            return None
