"""
This Reader retrives a full Proposal information.
"""
from pydecidim.api.decidim_connector import DecidimConnector
from pydecidim.api.participatory_space_name_enum import ParticipatorySpaceNameEnum
from pydecidim.api.participatory_space_reader import ParticipatorySpaceReader
from pydecidim.model.elemental_type_element import ElementalTypeElement
# Path to the query schema
from pydecidim.model.proposal import Proposal
from pydecidim.model.translated_field import TranslatedField

QUERY_PATH = 'pydecidim/queries/proposal.graphql'


class ProposalReader(ParticipatorySpaceReader):
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

    def execute(self, participatory_process_id: str, proposal_id: str) -> Proposal or None:
        """
        Send the query to the API and extract a list of proposals ids from a participatory space.
        :param participatory_process_id: The participatory process id.
        :param proposal_id: The proposal id.
        :return: A list of proposals ids, or None if the proposal doesn't exists.
        """

        response: dict = super().process_query_from_file(
            {
                'ID_PARTICIPATORY_PROCESS': ElementalTypeElement(participatory_process_id),
                'ID_PROPOSAL': ElementalTypeElement(proposal_id),
                'PARTICIPATORY_SPACE_NAME': ElementalTypeElement(super().participatory_space_name.value)
            })

        proposals = response[super().participatory_space_name.value]['components']
        proposals = [comment for comment in proposals if comment['proposal'] is not None]
        for proposal in proposals:
            proposal_dict = proposal['proposal']
            if proposal_dict is not None:
                title: TranslatedField = TranslatedField.parse_from_gql(proposal_dict['title']['translations'])
                body: TranslatedField = TranslatedField.parse_from_gql(proposal_dict['body']['translations'])
                has_comments: bool = proposal_dict['hasComments']
                vote_count: int = proposal_dict['voteCount']
                created_at: str = proposal_dict['createdAt']
                total_comments_count: int = proposal_dict['totalCommentsCount']
                accept_new_comments: bool = proposal_dict['acceptsNewComments']
                user_allowed_to_comment: bool = proposal_dict['userAllowedToComment']
                comments_id_list = proposal_dict['comments']

                comments_id = []
                for comment_id in comments_id_list:
                    comments_id.append(comment_id['id'])

                new_proposal = Proposal(proposal_id,
                                        total_comments_count,
                                        title,
                                        created_at,
                                        body,
                                        vote_count,
                                        has_comments,
                                        comments_id,
                                        accept_new_comments,
                                        user_allowed_to_comment)

                return new_proposal

        return None
