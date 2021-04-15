from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.page_bean_user import PageBeanUser
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 10,
    username: Union[Unset, List[str]] = UNSET,
    key: Union[Unset, List[str]] = UNSET,
    account_id: List[str],
) -> Dict[str, Any]:
    url = "{}/rest/api/3/user/bulk".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_username: Union[Unset, List[str]] = UNSET
    if not isinstance(username, Unset):
        json_username = username

    json_key: Union[Unset, List[str]] = UNSET
    if not isinstance(key, Unset):
        json_key = key

    json_account_id = account_id

    params: Dict[str, Any] = {
        "startAt": start_at,
        "maxResults": max_results,
        "username": json_username,
        "key": json_key,
        "accountId": json_account_id,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, PageBeanUser]]:
    if response.status_code == 200:
        response_200 = PageBeanUser.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, PageBeanUser]]:
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
    account_id: List[str],
) -> Response[Union[None, PageBeanUser]]:
    kwargs = _get_kwargs(
        client=client,
        start_at=start_at,
        max_results=max_results,
        username=username,
        key=key,
        account_id=account_id,
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
    account_id: List[str],
) -> Optional[Union[None, PageBeanUser]]:
    """Returns a [paginated](#pagination) list of the users specified by one or more account IDs.

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return sync_detailed(
        client=client,
        start_at=start_at,
        max_results=max_results,
        username=username,
        key=key,
        account_id=account_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 10,
    username: Union[Unset, List[str]] = UNSET,
    key: Union[Unset, List[str]] = UNSET,
    account_id: List[str],
) -> Response[Union[None, PageBeanUser]]:
    kwargs = _get_kwargs(
        client=client,
        start_at=start_at,
        max_results=max_results,
        username=username,
        key=key,
        account_id=account_id,
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
    account_id: List[str],
) -> Optional[Union[None, PageBeanUser]]:
    """Returns a [paginated](#pagination) list of the users specified by one or more account IDs.

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return (
        await asyncio_detailed(
            client=client,
            start_at=start_at,
            max_results=max_results,
            username=username,
            key=key,
            account_id=account_id,
        )
    ).parsed
