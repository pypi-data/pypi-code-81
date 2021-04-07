"""Defines a base class for interactions. Interactions are the web-socket version of
transactions.
"""
from typing import Generic, Iterable, TypeVar

InputType = TypeVar("InputType")
MessageType = TypeVar("MessageType")


class StopInteraction(Exception):
    """Exception to signal that an interaction wants to stop communicating."""


class InteractionBase(Generic[InputType, MessageType]):
    """Base class for implementing websocket interactions."""

    async def initialize_state(self, data: InputType):
        """Initialize the interaction's state."""
        raise NotImplementedError()

    async def open(self, data: InputType) -> Iterable[MessageType]:
        """Start up the interaction. Initialize state and perform whatever other actions need to
        occur before messages are sent.
        """
        await self.initialize_state(data)
        return []

    async def close(self):
        """Shut down the interaction, close upstream connections"""
        raise NotImplementedError()

    async def send(self, messages: Iterable[MessageType]) -> Iterable[MessageType]:
        """Send messages to the interaction."""
        raise NotImplementedError()

    async def receive(self) -> Iterable[MessageType]:
        """Receive messages from the interaction."""
        raise NotImplementedError()

    @staticmethod
    def error(message: str):
        """Signal that an error occurred and the interaction needs to stop."""
        raise StopInteraction(message)
