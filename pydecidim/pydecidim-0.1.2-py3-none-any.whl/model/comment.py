from __future__ import annotations

from typing import List

from pydecidim.model.abstract_api_element import AbstractApiElement
from pydecidim.model.author import Author


class Comment(AbstractApiElement):
    """
    Represents a Participatory Process from the Decidim API.
    """

    @staticmethod
    def parse_from_gql(comment_dict: dict) -> Comment:
        """
        Parses a comment from gql to a Comment instance.

        :param comment_dict: The dict with the Comment information.
        :return: A Comment
        """
        pass

    @property
    def accepts_new_comments(self) -> bool:
        return self.__accepts_new_comments

    @property
    def alignment(self) -> int:
        return self.__alignment

    @property
    def already_reported(self) -> bool:
        return self.__already_reported

    @property
    def author(self) -> Author:
        return self.__author

    @property
    def body(self) -> str:
        return self.__body

    @property
    def comments_have_alignment(self) -> bool:
        return self.__comments_have_alignment

    @property
    def comments_have_votes(self) -> bool:
        return self.__comments_have_votes

    @property
    def created_at(self) -> str:
        return self.__created_at

    @property
    def formatted_body(self) -> str:
        return self.__formatted_body

    @property
    def formatted_created_at(self) -> str:
        return self.__formatted_created_at

    @property
    def has_comments(self) -> bool:
        return self.__has_comments

    @property
    def comment_id(self) -> str:
        return self.__comment_id

    @property
    def sgid(self) -> str:
        return self.__comment_sgid

    @property
    def comment_type(self) -> str:
        return self.__comment_type

    @property
    def down_votes(self) -> int:
        return self.__down_votes

    @property
    def up_votes(self) -> int:
        return self.__up_votes

    @property
    def user_allowed_to_comment(self) -> bool:
        return self.__user_allowed_to_comment

    @property
    def total_comments_count(self) -> int:
        return self.__total_comments_count

    @property
    def comments_id(self) -> List[str]:
        return self.__comments_id

    @property
    def up_votes(self) -> int:
        return self.__up_votes

    def __init__(self,
                 accepts_new_comments: bool,
                 alignment: int,
                 already_reported: bool,
                 author: Author,
                 body: str,
                 comments_have_alignment: bool,
                 comments_have_votes: bool,
                 created_at: str,
                 formatted_body: str,
                 formatted_created_at: str,
                 has_comments: bool,
                 comment_id: str,
                 sgid: str,
                 total_comments_count: int,
                 comment_type: str,
                 down_votes: int,
                 up_votes: int,
                 user_allowed_to_comment: bool,
                 comments_id: List[str]) -> None:
        self.__accepts_new_comments: bool = accepts_new_comments
        self.__alignment: int = alignment
        self.__already_reported: bool = already_reported
        self.__author: Author = author
        self.__body: str = body
        self.__comments_have_alignment: bool = comments_have_alignment
        self.__comments_have_votes: bool = comments_have_votes
        self.__created_at: str = created_at
        self.__formatted_body: str = formatted_body
        self.__formatted_created_at: str = formatted_created_at
        self.__has_comments: bool = has_comments
        self.__comment_type: str = comment_type
        self.__comment_id: str = comment_id
        self.__comment_sgid: str = sgid
        self.__total_comments_count: int = total_comments_count
        self.__down_votes: int = down_votes
        self.__up_votes: int = up_votes
        self.__user_allowed_to_comment: bool = user_allowed_to_comment
        self.__comments_id: List[str] = comments_id
