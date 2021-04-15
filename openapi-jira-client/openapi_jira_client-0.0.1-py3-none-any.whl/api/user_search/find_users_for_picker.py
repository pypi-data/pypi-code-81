from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.found_users import FoundUsers
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    query: str,
    max_results: Union[Unset, int] = 50,
    show_avatar: Union[Unset, bool] = False,
    exclude: Union[Unset, List[str]] = UNSET,
    exclude_account_ids: Union[Unset, List[str]] = UNSET,
    avatar_size: Union[Unset, str] = UNSET,
    exclude_connect_users: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/user/picker".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_exclude: Union[Unset, List[str]] = UNSET
    if not isinstance(exclude, Unset):
        json_exclude = exclude

    json_exclude_account_ids: Union[Unset, List[str]] = UNSET
    if not isinstance(exclude_account_ids, Unset):
        json_exclude_account_ids = exclude_account_ids

    params: Dict[str, Any] = {
        "query": query,
        "maxResults": max_results,
        "showAvatar": show_avatar,
        "exclude": json_exclude,
        "excludeAccountIds": json_exclude_account_ids,
        "avatarSize": avatar_size,
        "excludeConnectUsers": exclude_connect_users,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[FoundUsers, None]]:
    if response.status_code == 200:
        response_200 = FoundUsers.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[FoundUsers, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    query: str,
    max_results: Union[Unset, int] = 50,
    show_avatar: Union[Unset, bool] = False,
    exclude: Union[Unset, List[str]] = UNSET,
    exclude_account_ids: Union[Unset, List[str]] = UNSET,
    avatar_size: Union[Unset, str] = UNSET,
    exclude_connect_users: Union[Unset, bool] = False,
) -> Response[Union[FoundUsers, None]]:
    kwargs = _get_kwargs(
        client=client,
        query=query,
        max_results=max_results,
        show_avatar=show_avatar,
        exclude=exclude,
        exclude_account_ids=exclude_account_ids,
        avatar_size=avatar_size,
        exclude_connect_users=exclude_connect_users,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    query: str,
    max_results: Union[Unset, int] = 50,
    show_avatar: Union[Unset, bool] = False,
    exclude: Union[Unset, List[str]] = UNSET,
    exclude_account_ids: Union[Unset, List[str]] = UNSET,
    avatar_size: Union[Unset, str] = UNSET,
    exclude_connect_users: Union[Unset, bool] = False,
) -> Optional[Union[FoundUsers, None]]:
    """Returns a list of users whose attributes match the query term. The returned object includes the `html` field where the matched query term is highlighted with the HTML strong tag. A list of account IDs can be provided to exclude users from the results.

    This operation takes the users in the range defined by `maxResults`, up to the thousandth user, and then returns only the users from that range that match the query term. This means the operation usually returns fewer users than specified in `maxResults`. To get all the users who match the query term, use [Get all users](#api-rest-api-3-users-search-get) and filter the records in your code.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Browse users and groups* [global permission](https://confluence.atlassian.com/x/x4dKLg). Anonymous calls and calls by users without the required permission return search results for an exact name match only."""

    return sync_detailed(
        client=client,
        query=query,
        max_results=max_results,
        show_avatar=show_avatar,
        exclude=exclude,
        exclude_account_ids=exclude_account_ids,
        avatar_size=avatar_size,
        exclude_connect_users=exclude_connect_users,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    query: str,
    max_results: Union[Unset, int] = 50,
    show_avatar: Union[Unset, bool] = False,
    exclude: Union[Unset, List[str]] = UNSET,
    exclude_account_ids: Union[Unset, List[str]] = UNSET,
    avatar_size: Union[Unset, str] = UNSET,
    exclude_connect_users: Union[Unset, bool] = False,
) -> Response[Union[FoundUsers, None]]:
    kwargs = _get_kwargs(
        client=client,
        query=query,
        max_results=max_results,
        show_avatar=show_avatar,
        exclude=exclude,
        exclude_account_ids=exclude_account_ids,
        avatar_size=avatar_size,
        exclude_connect_users=exclude_connect_users,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    query: str,
    max_results: Union[Unset, int] = 50,
    show_avatar: Union[Unset, bool] = False,
    exclude: Union[Unset, List[str]] = UNSET,
    exclude_account_ids: Union[Unset, List[str]] = UNSET,
    avatar_size: Union[Unset, str] = UNSET,
    exclude_connect_users: Union[Unset, bool] = False,
) -> Optional[Union[FoundUsers, None]]:
    """Returns a list of users whose attributes match the query term. The returned object includes the `html` field where the matched query term is highlighted with the HTML strong tag. A list of account IDs can be provided to exclude users from the results.

    This operation takes the users in the range defined by `maxResults`, up to the thousandth user, and then returns only the users from that range that match the query term. This means the operation usually returns fewer users than specified in `maxResults`. To get all the users who match the query term, use [Get all users](#api-rest-api-3-users-search-get) and filter the records in your code.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Browse users and groups* [global permission](https://confluence.atlassian.com/x/x4dKLg). Anonymous calls and calls by users without the required permission return search results for an exact name match only."""

    return (
        await asyncio_detailed(
            client=client,
            query=query,
            max_results=max_results,
            show_avatar=show_avatar,
            exclude=exclude,
            exclude_account_ids=exclude_account_ids,
            avatar_size=avatar_size,
            exclude_connect_users=exclude_connect_users,
        )
    ).parsed
