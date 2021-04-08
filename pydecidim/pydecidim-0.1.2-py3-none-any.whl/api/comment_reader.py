"""
This Reader retrives a full Proposal information.
"""

from pydecidim.api.abstract_decidim_reader import AbstractDecidimReader
from pydecidim.api.decidim_connector import DecidimConnector
from pydecidim.model.comment import Comment
from pydecidim.model.elemental_type_element import ElementalTypeElement

# Path to the query schema

QUERY_PATH = 'pydecidim/queries/comment.graphql'


class CommentReader(AbstractDecidimReader):
    """
    This reader retrieves a Proposal from Decidim.
    """

    def __init__(self, decidim_connector: DecidimConnector, base_path="."):
        """

        :param decidim_connector: An instance of a DecidimConnector class.
        :param base_path: The base path to the schema directory.
        """
        super().__init__(decidim_connector, base_path + "/" + QUERY_PATH)

    def execute(self, participatory_process_id: str, proposal_id: str, id_comment: str) -> Comment or None:
        """
        Send the query to the API and extract a list of proposals ids from a participatory space.
        :param participatory_process_id: The participatory process id.
        :param proposal_id: The proposal id.
        :param id_comment: The id of the comment to retrieve.
        :return: A list of proposals ids.
        """

        response: dict = super().process_query_from_file(
            {
                'ID_PARTICIPATORY_PROCESS': ElementalTypeElement(participatory_process_id),
                'ID_PROPOSAL': ElementalTypeElement(proposal_id),
                'ID_COMMENT': ElementalTypeElement(id_comment),
            })

        try:
            comment_dict = response['participatoryProcess']['components'][0]['proposal']['comments'][0]
            alignment: int = comment_dict['alignment']
            body: str = comment_dict['body']
            comment_type: str = comment_dict['type']
            created_at: str = comment_dict['createdAt']
            down_votes: int = comment_dict['downVotes']
            up_votes: int = comment_dict['upVotes']
            comments_id_list = comment_dict['comments']

            comments_id = []
            for comment_id in comments_id_list:
                comments_id.append(comment_id['id'])

            new_comment: Comment = Comment(id_comment,
                                           body,
                                           alignment,
                                           created_at,
                                           down_votes,
                                           up_votes,
                                           comment_type,
                                           comments_id)
            return new_comment
        except IndexError:
            return None

