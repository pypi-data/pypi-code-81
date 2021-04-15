from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.user import User
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    query: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    project_keys: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/user/assignable/multiProjectSearch".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "query": query,
        "username": username,
        "accountId": account_id,
        "projectKeys": project_keys,
        "startAt": start_at,
        "maxResults": max_results,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[List[User], None]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = User.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[List[User], None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    query: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    project_keys: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Response[Union[List[User], None]]:
    kwargs = _get_kwargs(
        client=client,
        query=query,
        username=username,
        account_id=account_id,
        project_keys=project_keys,
        start_at=start_at,
        max_results=max_results,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    query: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    project_keys: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Optional[Union[List[User], None]]:
    """Returns a list of users who can be assigned issues in one or more projects. The list may be restricted to users whose attributes match a string.

    This operation takes the users in the range defined by `startAt` and `maxResults`, up to the thousandth user, and then returns only the users from that range that can be assigned issues in the projects. This means the operation usually returns fewer users than specified in `maxResults`. To get all the users who can be assigned issues in the projects, use [Get all users](#api-rest-api-3-users-search-get) and filter the records in your code.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None."""

    return sync_detailed(
        client=client,
        query=query,
        username=username,
        account_id=account_id,
        project_keys=project_keys,
        start_at=start_at,
        max_results=max_results,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    query: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    project_keys: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Response[Union[List[User], None]]:
    kwargs = _get_kwargs(
        client=client,
        query=query,
        username=username,
        account_id=account_id,
        project_keys=project_keys,
        start_at=start_at,
        max_results=max_results,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    query: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    project_keys: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Optional[Union[List[User], None]]:
    """Returns a list of users who can be assigned issues in one or more projects. The list may be restricted to users whose attributes match a string.

    This operation takes the users in the range defined by `startAt` and `maxResults`, up to the thousandth user, and then returns only the users from that range that can be assigned issues in the projects. This means the operation usually returns fewer users than specified in `maxResults`. To get all the users who can be assigned issues in the projects, use [Get all users](#api-rest-api-3-users-search-get) and filter the records in your code.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None."""

    return (
        await asyncio_detailed(
            client=client,
            query=query,
            username=username,
            account_id=account_id,
            project_keys=project_keys,
            start_at=start_at,
            max_results=max_results,
        )
    ).parsed
