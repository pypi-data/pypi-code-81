from __future__ import annotations

from pydecidim.model.abstract_api_element import AbstractApiElement


class Author(AbstractApiElement):
    """
    Represents a Decidim user (Author)

    https://www.decidim.barcelona/api/docs#Author
    """

    @staticmethod
    def parse_from_gql(comment_dict: dict) -> Author:
        """
        Parses a comment from gql to a Comment instance.

        :param comment_dict: The dict with the Comment information.
        :return: A Comment
        """

        return Author(
            comment_dict['avatarUrl'],
            comment_dict['badge'],
            comment_dict['deleted'],
            comment_dict['id'],
            comment_dict['name'],
            comment_dict['nickname'],
            comment_dict['organizationName'],
            comment_dict['profilePath']
        )

    @property
    def avatar_url(self) -> str:
        return self.__avatar_url

    @property
    def badge(self) -> str:
        return self.__badge

    @property
    def deleted(self) -> bool:
        return self.__deleted

    @property
    def author_id(self) -> str:
        return self.__author_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def nickname(self) -> str:
        return self.__nickname

    @property
    def organization_name(self) -> str:
        return self.__organization_name

    @property
    def profile_path(self) -> str:
        return self.__profile_path

    def __init__(self,
                 avatar_url: str,
                 badge: str,
                 deleted: bool,
                 author_id: str,
                 name: str,
                 nickname: str,
                 organization_name: str,
                 profile_path: str) -> None:
        self.__avatar_url: str = avatar_url
        self.__badge: str = badge
        self.__deleted: bool = deleted
        self.__author_id: str = author_id
        self.__name: str = name
        self.__nickname: str = nickname
        self.__organization_name: str = organization_name
        self.__profile_path: str = profile_path
