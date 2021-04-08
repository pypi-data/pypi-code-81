from typing import List

from pydecidim.model.abstract_api_element import AbstractApiElement
from pydecidim.model.translated_field import TranslatedField


class Proposal(AbstractApiElement):
    """
    Represents a Participatory Process from the Decidim API.
    """

    @property
    def proposal_id(self) -> str:
        return self.__proposal_id

    @property
    def total_comments_count(self) -> int:
        return self.__total_comments_count

    @property
    def comments_ids(self) -> List[str]:
        return self.__comments_id

    @property
    def title(self) -> TranslatedField:
        return self.__title

    @property
    def created_at(self) -> str:
        return self.__created_at

    @property
    def body(self) -> TranslatedField:
        return self.__body

    @property
    def has_comments(self) -> bool:
        return self.__has_comments

    @property
    def vote_count(self) -> int:
        return self.__vote_count

    @property
    def accept_new_comments(self) -> bool:
        return self.__accept_new_comments

    @property
    def users_allowed_to_comment(self) -> bool:
        return self.__users_allowed_to_comment

    def __init__(self, proposal_id: str,
                 total_comments_count: int,
                 title: TranslatedField,
                 created_at: str,
                 body: TranslatedField,
                 vote_count: int,
                 has_comments: bool,
                 comments_id: List[str],
                 accepts_new_comments: bool,
                 users_allowed_to_comment: bool) -> None:
        self.__proposal_id: str = proposal_id
        self.__total_comments_count: int = total_comments_count
        self.__title: TranslatedField = title
        self.__created_at: str = created_at
        self.__body: TranslatedField = body
        self.__vote_count: int = vote_count
        self.__has_comments: bool = has_comments
        self.__comments_id: List[str] = comments_id
        self.__accept_new_comments: bool = accepts_new_comments
        self.__users_allowed_to_comment: bool = users_allowed_to_comment











