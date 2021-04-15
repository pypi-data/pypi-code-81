from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    key: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/mypreferences".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "key": key,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, str]]:
    if response.status_code == 200:
        response_200 = response.json()
        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, str]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    key: str,
) -> Response[Union[None, str]]:
    kwargs = _get_kwargs(
        client=client,
        key=key,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    key: str,
) -> Optional[Union[None, str]]:
    """Returns the value of a preference of the current user.

    Note that these keys are deprecated:

     *  *jira.user.locale* The locale of the user. By default this is not set and the user takes the locale of the instance.
     *  *jira.user.timezone* The time zone of the user. By default this is not set and the user takes the timezone of the instance.

    Use [ Update a user profile](https://developer.atlassian.com/cloud/admin/user-management/rest/#api-users-account-id-manage-profile-patch) from the user management REST API to manage timezone and locale instead.

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return sync_detailed(
        client=client,
        key=key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    key: str,
) -> Response[Union[None, str]]:
    kwargs = _get_kwargs(
        client=client,
        key=key,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    key: str,
) -> Optional[Union[None, str]]:
    """Returns the value of a preference of the current user.

    Note that these keys are deprecated:

     *  *jira.user.locale* The locale of the user. By default this is not set and the user takes the locale of the instance.
     *  *jira.user.timezone* The time zone of the user. By default this is not set and the user takes the timezone of the instance.

    Use [ Update a user profile](https://developer.atlassian.com/cloud/admin/user-management/rest/#api-users-account-id-manage-profile-patch) from the user management REST API to manage timezone and locale instead.

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return (
        await asyncio_detailed(
            client=client,
            key=key,
        )
    ).parsed
