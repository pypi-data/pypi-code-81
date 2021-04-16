"""Triggers for the various steps of a :class:`~sym.sdk.events.Flow`."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict

from sym.sdk.flow import Flow, Run
from sym.sdk.resource import SymResource
from sym.sdk.templates import Template
from sym.sdk.user import User


class Payload(SymResource):
    """The :class:`~sym.sdk.events.Payload` object contains the data of the
    :class:`~sym.sdk.events.Event`.
    """

    @property
    @abstractmethod
    def timestamp(self) -> datetime:
        """A datetime object indicating when the :class:`~sym.sdk.events.Event` was created."""

    @property
    @abstractmethod
    def fields(self) -> Dict[str, Any]:
        """A dict containing the values submitted by the user who created
        the :class:`~sym.sdk.events.Event`
        """

    @property
    @abstractmethod
    def srn(self) -> str:
        """The :class:`~sym.sdk.resource.SRN` of the :class:`~sym.sdk.events.Event` instance."""

    @property
    @abstractmethod
    def user(self) -> User:
        """The :class:`~sym.sdk.user.User` who triggered the :class:`~sym.sdk.events.Event`."""

    @property
    @abstractmethod
    def actors(self) -> Dict[str, User]:
        """A dict mapping :class:`~sym.sdk.events.Event` names to the :class:`~sym.sdk.user.User`
        that created each :class:`~sym.sdk.events.Event`. There will be one entry for each
        :class:`~sym.sdk.events.Event` in the current :class:`~sym.sdk.flow.Run`.

        For example, with a sym:approval :class:`~sym.sdk.flow.Flow` after the "approve"
        :class:`~sym.sdk.events.Event` is received, the actors may look like this::

            {
                "prompt": <User A>,
                "request": <User A>,
                "approve": <User B>
            }
        """

    @property
    @abstractmethod
    def event_name(self) -> str:
        """Returns the name of the :class:`~sym.sdk.events.Event`.

        For example, "approve".
        """


class EventMeta(SymResource, ABC):
    """Contains metadata about an :class:`~sym.sdk.events.Event` instance."""


class Event(ABC):
    """The :class:`~sym.sdk.events.Event` class contains information on an event which has been
    received by Sym, routed to a :class:`~sym.sdk.flow.Run` of a :class:`~sym.sdk.flow.Flow`, and is
    triggering specific user-defined Handlers.

    Each Handler will be invoked with a single argument, which is an instance of this class.
    This :class:`~sym.sdk.events.Event` instance will describe the current execution state,
    and can be used to dynamically alter the behavior and control flow of
    Templates.

    Read more about `Handlers <https://docs.symops.com/docs/handlers>`_.
    """

    @property
    @abstractmethod
    def payload(self) -> Payload:
        """A :class:`~sym.sdk.events.Payload` object, which contains the primary data
        of the :class:`~sym.sdk.events.Event`.
        """

    @property
    @abstractmethod
    def meta(self) -> EventMeta:
        """An :class:`~sym.sdk.events.EventMeta` object, which contains metadata
        about the :class:`~sym.sdk.events.Event` instance.
        """

    @property
    @abstractmethod
    def template(self) -> Template:
        """A :class:`~sym.sdk.templates.Template` object, indicating which
        :class:`~sym.sdk.templates.Template` the current :class:`~sym.sdk.flow.Flow` inherits from.
        """

    @property
    @abstractmethod
    def flow(self) -> Flow:
        """A :class:`~sym.sdk.flow.Flow` object, indicating the :class:`~sym.sdk.flow.Flow` that
        the current :class:`~sym.sdk.flow.Run` is an instance of.
        """

    @property
    @abstractmethod
    def run(self) -> Run:
        """A :class:`~sym.sdk.flow.Run` object, indicating the current
        :class:`~sym.sdk.flow.Run`."""

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the :class:`~sym.sdk.events.Event`."""

    @property
    @abstractmethod
    def actors(self) -> Dict[str, User]:
        """A dict mapping :class:`~sym.sdk.events.Event` names to the :class:`~sym.sdk.user.User`
        that created each :class:`~sym.sdk.events.Event`. There will be one entry for each
        :class:`~sym.sdk.events.Event` in the current :class:`~sym.sdk.flow.Run`.

        For example, with a sym:approval :class:`~sym.sdk.flow.Flow` after the "approve"
        :class:`~sym.sdk.events.Event` is received, the actors may look like this::

            {
                "prompt": <User A>,
                "request": <User A>,
                "approve": <User B>
            }
        """

    @property
    @abstractmethod
    def fields(self) -> Dict[str, Any]:
        """A dict containing the values submitted by the user who created the
        :class:`~sym.sdk.events.Event`.
        """

    @property
    @abstractmethod
    def user(self) -> User:
        """The :class:`~sym.sdk.user.User` who triggered the :class:`~sym.sdk.events.Event`."""
