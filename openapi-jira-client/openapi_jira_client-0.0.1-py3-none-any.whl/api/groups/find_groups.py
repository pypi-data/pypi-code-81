from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.found_groups import FoundGroups
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    account_id: Union[Unset, str] = UNSET,
    query: Union[Unset, str] = UNSET,
    exclude: Union[Unset, List[str]] = UNSET,
    max_results: Union[Unset, int] = UNSET,
    user_name: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/groups/picker".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_exclude: Union[Unset, List[str]] = UNSET
    if not isinstance(exclude, Unset):
        json_exclude = exclude

    params: Dict[str, Any] = {
        "accountId": account_id,
        "query": query,
        "exclude": json_exclude,
        "maxResults": max_results,
        "userName": user_name,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[FoundGroups]:
    if response.status_code == 200:
        response_200 = FoundGroups.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[FoundGroups]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    account_id: Union[Unset, str] = UNSET,
    query: Union[Unset, str] = UNSET,
    exclude: Union[Unset, List[str]] = UNSET,
    max_results: Union[Unset, int] = UNSET,
    user_name: Union[Unset, str] = UNSET,
) -> Response[FoundGroups]:
    kwargs = _get_kwargs(
        client=client,
        account_id=account_id,
        query=query,
        exclude=exclude,
        max_results=max_results,
        user_name=user_name,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    account_id: Union[Unset, str] = UNSET,
    query: Union[Unset, str] = UNSET,
    exclude: Union[Unset, List[str]] = UNSET,
    max_results: Union[Unset, int] = UNSET,
    user_name: Union[Unset, str] = UNSET,
) -> Optional[FoundGroups]:
    """Returns a list of groups whose names contain a query string. A list of group names can be provided to exclude groups from the results.

    The primary use case for this resource is to populate a group picker suggestions list. To this end, the returned object includes the `html` field where the matched query term is highlighted in the group name with the HTML strong tag. Also, the groups list is wrapped in a response object that contains a header for use in the picker, specifically *Showing X of Y matching groups*.

    The list returns with the groups sorted. If no groups match the list criteria, an empty list is returned.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg). Anonymous calls and calls by users without the required permission return an empty list."""

    return sync_detailed(
        client=client,
        account_id=account_id,
        query=query,
        exclude=exclude,
        max_results=max_results,
        user_name=user_name,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    account_id: Union[Unset, str] = UNSET,
    query: Union[Unset, str] = UNSET,
    exclude: Union[Unset, List[str]] = UNSET,
    max_results: Union[Unset, int] = UNSET,
    user_name: Union[Unset, str] = UNSET,
) -> Response[FoundGroups]:
    kwargs = _get_kwargs(
        client=client,
        account_id=account_id,
        query=query,
        exclude=exclude,
        max_results=max_results,
        user_name=user_name,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    account_id: Union[Unset, str] = UNSET,
    query: Union[Unset, str] = UNSET,
    exclude: Union[Unset, List[str]] = UNSET,
    max_results: Union[Unset, int] = UNSET,
    user_name: Union[Unset, str] = UNSET,
) -> Optional[FoundGroups]:
    """Returns a list of groups whose names contain a query string. A list of group names can be provided to exclude groups from the results.

    The primary use case for this resource is to populate a group picker suggestions list. To this end, the returned object includes the `html` field where the matched query term is highlighted in the group name with the HTML strong tag. Also, the groups list is wrapped in a response object that contains a header for use in the picker, specifically *Showing X of Y matching groups*.

    The list returns with the groups sorted. If no groups match the list criteria, an empty list is returned.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg). Anonymous calls and calls by users without the required permission return an empty list."""

    return (
        await asyncio_detailed(
            client=client,
            account_id=account_id,
            query=query,
            exclude=exclude,
            max_results=max_results,
            user_name=user_name,
        )
    ).parsed
