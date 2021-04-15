from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.page_bean_user_details import PageBeanUserDetails
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    groupname: str,
    include_inactive_users: Union[Unset, bool] = False,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/group/member".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "groupname": groupname,
        "includeInactiveUsers": include_inactive_users,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, PageBeanUserDetails]]:
    if response.status_code == 200:
        response_200 = PageBeanUserDetails.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[None, PageBeanUserDetails]]:
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
    include_inactive_users: Union[Unset, bool] = False,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Response[Union[None, PageBeanUserDetails]]:
    kwargs = _get_kwargs(
        client=client,
        groupname=groupname,
        include_inactive_users=include_inactive_users,
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
    groupname: str,
    include_inactive_users: Union[Unset, bool] = False,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Optional[Union[None, PageBeanUserDetails]]:
    """Returns a [paginated](#pagination) list of all users in a group.

    Note that users are ordered by username, however the username is not returned in the results due to privacy reasons.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        groupname=groupname,
        include_inactive_users=include_inactive_users,
        start_at=start_at,
        max_results=max_results,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    groupname: str,
    include_inactive_users: Union[Unset, bool] = False,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Response[Union[None, PageBeanUserDetails]]:
    kwargs = _get_kwargs(
        client=client,
        groupname=groupname,
        include_inactive_users=include_inactive_users,
        start_at=start_at,
        max_results=max_results,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    groupname: str,
    include_inactive_users: Union[Unset, bool] = False,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Optional[Union[None, PageBeanUserDetails]]:
    """Returns a [paginated](#pagination) list of all users in a group.

    Note that users are ordered by username, however the username is not returned in the results due to privacy reasons.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            groupname=groupname,
            include_inactive_users=include_inactive_users,
            start_at=start_at,
            max_results=max_results,
        )
    ).parsed
