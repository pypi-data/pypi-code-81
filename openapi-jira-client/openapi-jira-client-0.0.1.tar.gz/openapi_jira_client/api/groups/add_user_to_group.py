from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.group import Group
from ...models.update_user_to_group_bean import UpdateUserToGroupBean
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: UpdateUserToGroupBean,
    groupname: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/group/user".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "groupname": groupname,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Group, None]]:
    if response.status_code == 201:
        response_201 = Group.from_dict(response.json())

        return response_201
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
    json_body: UpdateUserToGroupBean,
    groupname: str,
) -> Response[Union[Group, None]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        groupname=groupname,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: UpdateUserToGroupBean,
    groupname: str,
) -> Optional[Union[Group, None]]:
    """Adds a user to a group.

    **[Permissions](#permissions) required:** Site administration (that is, member of the *site-admin* [group](https://confluence.atlassian.com/x/24xjL))."""

    return sync_detailed(
        client=client,
        json_body=json_body,
        groupname=groupname,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: UpdateUserToGroupBean,
    groupname: str,
) -> Response[Union[Group, None]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        groupname=groupname,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: UpdateUserToGroupBean,
    groupname: str,
) -> Optional[Union[Group, None]]:
    """Adds a user to a group.

    **[Permissions](#permissions) required:** Site administration (that is, member of the *site-admin* [group](https://confluence.atlassian.com/x/24xjL))."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            groupname=groupname,
        )
    ).parsed
