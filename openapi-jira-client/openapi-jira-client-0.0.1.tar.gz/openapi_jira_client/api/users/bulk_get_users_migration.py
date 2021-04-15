from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.user_migration_bean import UserMigrationBean
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 10,
    username: Union[Unset, List[str]] = UNSET,
    key: Union[Unset, List[str]] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/user/bulk/migration".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_username: Union[Unset, List[str]] = UNSET
    if not isinstance(username, Unset):
        json_username = username

    json_key: Union[Unset, List[str]] = UNSET
    if not isinstance(key, Unset):
        json_key = key

    params: Dict[str, Any] = {
        "startAt": start_at,
        "maxResults": max_results,
        "username": json_username,
        "key": json_key,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[List[UserMigrationBean], None]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = UserMigrationBean.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[List[UserMigrationBean], None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 10,
    username: Union[Unset, List[str]] = UNSET,
    key: Union[Unset, List[str]] = UNSET,
) -> Response[Union[List[UserMigrationBean], None]]:
    kwargs = _get_kwargs(
        client=client,
        start_at=start_at,
        max_results=max_results,
        username=username,
        key=key,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 10,
    username: Union[Unset, List[str]] = UNSET,
    key: Union[Unset, List[str]] = UNSET,
) -> Optional[Union[List[UserMigrationBean], None]]:
    """Returns the account IDs for the users specified in the `key` or `username` parameters. Note that multiple `key` or `username` parameters can be specified.

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return sync_detailed(
        client=client,
        start_at=start_at,
        max_results=max_results,
        username=username,
        key=key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 10,
    username: Union[Unset, List[str]] = UNSET,
    key: Union[Unset, List[str]] = UNSET,
) -> Response[Union[List[UserMigrationBean], None]]:
    kwargs = _get_kwargs(
        client=client,
        start_at=start_at,
        max_results=max_results,
        username=username,
        key=key,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 10,
    username: Union[Unset, List[str]] = UNSET,
    key: Union[Unset, List[str]] = UNSET,
) -> Optional[Union[List[UserMigrationBean], None]]:
    """Returns the account IDs for the users specified in the `key` or `username` parameters. Note that multiple `key` or `username` parameters can be specified.

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return (
        await asyncio_detailed(
            client=client,
            start_at=start_at,
            max_results=max_results,
            username=username,
            key=key,
        )
    ).parsed
