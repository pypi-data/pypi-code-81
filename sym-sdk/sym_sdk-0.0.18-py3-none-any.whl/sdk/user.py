"""Representations of Users in both Sym and third parties."""

from abc import ABC, abstractmethod
from typing import Optional


class UserIdentity(ABC):
    """Represents a :class:`~sym.sdk.user.User`'s
    identity in an external system such as Slack or PagerDuty.
    """

    def __str__(self) -> str:
        return f"Identity({self.provider}: {self.user_id})"

    @property
    @abstractmethod
    def provider(self) -> str:
        """The name of the external system providing the identity.

        For example, `:mod:`~sym.sdk.integrations.slack`.
        """

    @property
    @abstractmethod
    def user_id(self) -> str:
        """The :class:`~sym.sdk.user.User`'s identifier in the external system.

        For example, the :class:`~sym.sdk.user.User`'s Slack ID.
        """


class User(ABC):
    """The atomic representation of a user in Sym.

    :class:`~sym.sdk.user.User`s have many :class:`~sym.sdk.user.UserIdentity`,
    which are used for referencing said user in external systems.
    """

    def __str__(self) -> str:
        return f"User({self.username})"

    @property
    @abstractmethod
    def username(self) -> str:
        """The :class:`~sym.sdk.user.User`'s Sym username."""

    @property
    @abstractmethod
    def email(self) -> str:
        """The :class:`~sym.sdk.user.User`'s email."""

    @property
    @abstractmethod
    def first_name(self) -> str:
        """The :class:`~sym.sdk.user.User`'s first name."""

    @property
    @abstractmethod
    def last_name(self) -> str:
        """The :class:`~sym.sdk.user.User`'s last name."""

    @abstractmethod
    def identity(
        self,
        integration_name: Optional[str] = None,
        integration_srn: Optional[str] = None,
    ) -> Optional[UserIdentity]:
        """Retrieves this :class:`~sym.sdk.user.User`'s :class:`~sym.sdk.user.UserIdentity`
        for a particular external system.

        External systems specified by either integration_name or integration_srn.

        Args:
            integration_name: The name of one of Sym's `:mod:`~sym.sdk.integrations`.
            integration_srn: The :class:`~sym.sdk.resource.SRN` of an `Integration <https://docs.symops.com/docs/tf-integration>`_ instance.

        Returns:
            A :class:`~sym.sdk.user.UserIdentity`, or None if no identity is found for the Integration.
        """
