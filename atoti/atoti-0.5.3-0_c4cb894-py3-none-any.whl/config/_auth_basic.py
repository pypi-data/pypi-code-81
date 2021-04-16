from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Collection, Mapping, Optional

from .._deprecation import deprecated
from ._auth import Auth
from ._utils import Configuration

BASIC_AUTH_TYPE = "basic"
ROLE_USER = "ROLE_USER"


@dataclass(frozen=True)
class BasicUser(Configuration):
    """Basic user with roles."""

    name: str
    password: str
    roles: Collection[str] = field(default_factory=list)

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        return create_basic_user(**data)


@deprecated(
    message="Passing basic users in the session configuration is deprecated. Use session.security.basic.create_user() instead."
)
def create_basic_user(
    name: str, password: str, *, roles: Optional[Collection[str]] = None
) -> BasicUser:
    """Create a basic user with roles.

    Args:
        name: The username.
        password: The password of the user.
        roles: The roles given to the user.
            The role ``ROLE_USER``, which is required to access the application, will automatically be added to the passed roles.
    """
    roles = set(roles) if roles is not None else set()
    roles.add(ROLE_USER)
    # Convert back to list so the class is JSON serializable
    return BasicUser(name, password, list(roles))


@dataclass(frozen=True)
class BasicAuthentication(Auth):
    """Basic authentication."""

    _name: str
    users: Collection[BasicUser]
    realm: Optional[str] = None

    @property
    def _type(self):
        return BASIC_AUTH_TYPE

    @classmethod
    def _create(cls, data: Mapping[str, Any]) -> BasicAuthentication:
        """Create the authentication from dictionary."""
        data_dict = dict(data)
        if "users" in data_dict:
            users_data = data_dict.pop("users")
            users = [BasicUser._from_dict(user) for user in users_data]
        else:
            users = []
        return create_basic_authentication(users, **data_dict)


def create_basic_authentication(
    users: Optional[Collection[BasicUser]] = None, *, realm: Optional[str] = None
) -> BasicAuthentication:
    """Create a basic authentication config.

    Basic authentication is the easiest way to get started with security since it only requires defining the users, their password, and their roles.

    Args:
        users (deprecated): The users that can authenticate against the session.
        realm: The realm describing the protected area.
            Different realms can be used to isolate sessions running on the same domain (regardless of the port).
            The realm will also be displayed by the browser when prompting for credentials.
            Defaults to ``f"{session_name} atoti session at {session_id}"``.

    Example:
        >>> python_config = tt.config.create_config(
        ...     authentication=tt.config.create_basic_authentication(
        ...         realm="Example",
        ...     )
        ... )
        >>> yaml_config = '''
        ... authentication:
        ...   basic:
        ...     realm: Example
        ...     users: []
        ... '''

        .. doctest::
            :hide:

            >>> diff_yaml_config_with_python_config(yaml_config, python_config)

    """
    if not users:
        users = []
    return BasicAuthentication("basic", users, realm)
