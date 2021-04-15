from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.page_bean_user_key import PageBeanUserKey
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    query: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 100,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/user/search/query/key".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "query": query,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, PageBeanUserKey]]:
    if response.status_code == 200:
        response_200 = PageBeanUserKey.from_dict(response.json())

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
    if response.status_code == 408:
        response_408 = None

        return response_408
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, PageBeanUserKey]]:
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
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 100,
) -> Response[Union[None, PageBeanUserKey]]:
    kwargs = _get_kwargs(
        client=client,
        query=query,
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
    query: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 100,
) -> Optional[Union[None, PageBeanUserKey]]:
    """Finds users with a structured query and returns a [paginated](#pagination) list of user keys.

    This operation takes the users in the range defined by `startAt` and `maxResults`, up to the thousandth user, and then returns only the users from that range that match the structured query. This means the operation usually returns fewer users than specified in `maxResults`. To get all the users who match the structured query, use [Get all users](#api-rest-api-3-users-search-get) and filter the records in your code.

    **[Permissions](#permissions) required:** *Browse users and groups* [global permission](https://confluence.atlassian.com/x/x4dKLg).

    The query statements are:

     *  `is assignee of PROJ` Returns the users that are assignees of at least one issue in project *PROJ*.
     *  `is assignee of (PROJ-1, PROJ-2)` Returns users that are assignees on the issues *PROJ-1* or *PROJ-2*.
     *  `is reporter of (PROJ-1, PROJ-2)` Returns users that are reporters on the issues *PROJ-1* or *PROJ-2*.
     *  `is watcher of (PROJ-1, PROJ-2)` Returns users that are watchers on the issues *PROJ-1* or *PROJ-2*.
     *  `is voter of (PROJ-1, PROJ-2)` Returns users that are voters on the issues *PROJ-1* or *PROJ-2*.
     *  `is commenter of (PROJ-1, PROJ-2)` Returns users that have posted a comment on the issues *PROJ-1* or *PROJ-2*.
     *  `is transitioner of (PROJ-1, PROJ-2)` Returns users that have performed a transition on issues *PROJ-1* or *PROJ-2*.
     *  `[propertyKey].entity.property.path is \"property value\"` Returns users with the entity property value.

    The list of issues can be extended as needed, as in *(PROJ-1, PROJ-2, ... PROJ-n)*. Statements can be combined using the `AND` and `OR` operators to form more complex queries. For example:

    `is assignee of PROJ AND [propertyKey].entity.property.path is \"property value\"`"""

    return sync_detailed(
        client=client,
        query=query,
        start_at=start_at,
        max_results=max_results,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    query: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 100,
) -> Response[Union[None, PageBeanUserKey]]:
    kwargs = _get_kwargs(
        client=client,
        query=query,
        start_at=start_at,
        max_results=max_results,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    query: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 100,
) -> Optional[Union[None, PageBeanUserKey]]:
    """Finds users with a structured query and returns a [paginated](#pagination) list of user keys.

    This operation takes the users in the range defined by `startAt` and `maxResults`, up to the thousandth user, and then returns only the users from that range that match the structured query. This means the operation usually returns fewer users than specified in `maxResults`. To get all the users who match the structured query, use [Get all users](#api-rest-api-3-users-search-get) and filter the records in your code.

    **[Permissions](#permissions) required:** *Browse users and groups* [global permission](https://confluence.atlassian.com/x/x4dKLg).

    The query statements are:

     *  `is assignee of PROJ` Returns the users that are assignees of at least one issue in project *PROJ*.
     *  `is assignee of (PROJ-1, PROJ-2)` Returns users that are assignees on the issues *PROJ-1* or *PROJ-2*.
     *  `is reporter of (PROJ-1, PROJ-2)` Returns users that are reporters on the issues *PROJ-1* or *PROJ-2*.
     *  `is watcher of (PROJ-1, PROJ-2)` Returns users that are watchers on the issues *PROJ-1* or *PROJ-2*.
     *  `is voter of (PROJ-1, PROJ-2)` Returns users that are voters on the issues *PROJ-1* or *PROJ-2*.
     *  `is commenter of (PROJ-1, PROJ-2)` Returns users that have posted a comment on the issues *PROJ-1* or *PROJ-2*.
     *  `is transitioner of (PROJ-1, PROJ-2)` Returns users that have performed a transition on issues *PROJ-1* or *PROJ-2*.
     *  `[propertyKey].entity.property.path is \"property value\"` Returns users with the entity property value.

    The list of issues can be extended as needed, as in *(PROJ-1, PROJ-2, ... PROJ-n)*. Statements can be combined using the `AND` and `OR` operators to form more complex queries. For example:

    `is assignee of PROJ AND [propertyKey].entity.property.path is \"property value\"`"""

    return (
        await asyncio_detailed(
            client=client,
            query=query,
            start_at=start_at,
            max_results=max_results,
        )
    ).parsed
