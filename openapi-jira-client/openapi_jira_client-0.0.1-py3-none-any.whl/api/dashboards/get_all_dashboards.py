from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.error_collection import ErrorCollection
from ...models.get_all_dashboards_filter import GetAllDashboardsFilter
from ...models.page_of_dashboards import PageOfDashboards
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    filter_: Union[Unset, GetAllDashboardsFilter] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 20,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/dashboard".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_filter_: Union[Unset, str] = UNSET
    if not isinstance(filter_, Unset):
        json_filter_ = filter_.value

    params: Dict[str, Any] = {
        "filter": json_filter_,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[ErrorCollection, PageOfDashboards]]:
    if response.status_code == 200:
        response_200 = PageOfDashboards.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorCollection.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = ErrorCollection.from_dict(response.json())

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ErrorCollection, PageOfDashboards]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    filter_: Union[Unset, GetAllDashboardsFilter] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 20,
) -> Response[Union[ErrorCollection, PageOfDashboards]]:
    kwargs = _get_kwargs(
        client=client,
        filter_=filter_,
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
    filter_: Union[Unset, GetAllDashboardsFilter] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 20,
) -> Optional[Union[ErrorCollection, PageOfDashboards]]:
    """Returns a list of dashboards owned by or shared with the user. The list may be filtered to include only favorite or owned dashboards.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None."""

    return sync_detailed(
        client=client,
        filter_=filter_,
        start_at=start_at,
        max_results=max_results,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    filter_: Union[Unset, GetAllDashboardsFilter] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 20,
) -> Response[Union[ErrorCollection, PageOfDashboards]]:
    kwargs = _get_kwargs(
        client=client,
        filter_=filter_,
        start_at=start_at,
        max_results=max_results,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    filter_: Union[Unset, GetAllDashboardsFilter] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 20,
) -> Optional[Union[ErrorCollection, PageOfDashboards]]:
    """Returns a list of dashboards owned by or shared with the user. The list may be filtered to include only favorite or owned dashboards.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None."""

    return (
        await asyncio_detailed(
            client=client,
            filter_=filter_,
            start_at=start_at,
            max_results=max_results,
        )
    ).parsed
