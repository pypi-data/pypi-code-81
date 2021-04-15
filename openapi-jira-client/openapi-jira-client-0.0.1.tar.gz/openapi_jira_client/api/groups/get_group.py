from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.group import Group
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    groupname: str,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/group".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "groupname": groupname,
        "expand": expand,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Group, None]]:
    if response.status_code == 200:
        response_200 = Group.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Group, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    groupname: str,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[Group, None]]:
    kwargs = _get_kwargs(
        client=client,
        groupname=groupname,
        expand=expand,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    groupname: str,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[Group, None]]:
    """This operation is deprecated, use [`group/member`](#api-rest-api-3-group-member-get).

    Returns all users in a group.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        groupname=groupname,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    groupname: str,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[Group, None]]:
    kwargs = _get_kwargs(
        client=client,
        groupname=groupname,
        expand=expand,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    groupname: str,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[Group, None]]:
    """This operation is deprecated, use [`group/member`](#api-rest-api-3-group-member-get).

    Returns all users in a group.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            groupname=groupname,
            expand=expand,
        )
    ).parsed
