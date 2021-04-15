from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.error_collection import ErrorCollection
from ...models.get_dashboards_paginated_order_by import GetDashboardsPaginatedOrderBy
from ...models.page_bean_dashboard import PageBeanDashboard
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    dashboard_name: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    owner: Union[Unset, str] = UNSET,
    groupname: Union[Unset, str] = UNSET,
    project_id: Union[Unset, int] = UNSET,
    order_by: Union[Unset, GetDashboardsPaginatedOrderBy] = GetDashboardsPaginatedOrderBy.NAME,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/dashboard/search".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_order_by: Union[Unset, str] = UNSET
    if not isinstance(order_by, Unset):
        json_order_by = order_by.value

    params: Dict[str, Any] = {
        "dashboardName": dashboard_name,
        "accountId": account_id,
        "owner": owner,
        "groupname": groupname,
        "projectId": project_id,
        "orderBy": json_order_by,
        "startAt": start_at,
        "maxResults": max_results,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[ErrorCollection, PageBeanDashboard]]:
    if response.status_code == 200:
        response_200 = PageBeanDashboard.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorCollection.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = ErrorCollection.from_dict(response.json())

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ErrorCollection, PageBeanDashboard]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    dashboard_name: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    owner: Union[Unset, str] = UNSET,
    groupname: Union[Unset, str] = UNSET,
    project_id: Union[Unset, int] = UNSET,
    order_by: Union[Unset, GetDashboardsPaginatedOrderBy] = GetDashboardsPaginatedOrderBy.NAME,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorCollection, PageBeanDashboard]]:
    kwargs = _get_kwargs(
        client=client,
        dashboard_name=dashboard_name,
        account_id=account_id,
        owner=owner,
        groupname=groupname,
        project_id=project_id,
        order_by=order_by,
        start_at=start_at,
        max_results=max_results,
        expand=expand,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    dashboard_name: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    owner: Union[Unset, str] = UNSET,
    groupname: Union[Unset, str] = UNSET,
    project_id: Union[Unset, int] = UNSET,
    order_by: Union[Unset, GetDashboardsPaginatedOrderBy] = GetDashboardsPaginatedOrderBy.NAME,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorCollection, PageBeanDashboard]]:
    """Returns a [paginated](#pagination) list of dashboards. This operation is similar to [Get dashboards](#api-rest-api-3-dashboard-get) except that the results can be refined to include dashboards that have specific attributes. For example, dashboards with a particular name. When multiple attributes are specified only filters matching all attributes are returned.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** The following dashboards that match the query parameters are returned:

     *  Dashboards owned by the user. Not returned for anonymous users.
     *  Dashboards shared with a group that the user is a member of. Not returned for anonymous users.
     *  Dashboards shared with a private project that the user can browse. Not returned for anonymous users.
     *  Dashboards shared with a public project.
     *  Dashboards shared with the public."""

    return sync_detailed(
        client=client,
        dashboard_name=dashboard_name,
        account_id=account_id,
        owner=owner,
        groupname=groupname,
        project_id=project_id,
        order_by=order_by,
        start_at=start_at,
        max_results=max_results,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    dashboard_name: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    owner: Union[Unset, str] = UNSET,
    groupname: Union[Unset, str] = UNSET,
    project_id: Union[Unset, int] = UNSET,
    order_by: Union[Unset, GetDashboardsPaginatedOrderBy] = GetDashboardsPaginatedOrderBy.NAME,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorCollection, PageBeanDashboard]]:
    kwargs = _get_kwargs(
        client=client,
        dashboard_name=dashboard_name,
        account_id=account_id,
        owner=owner,
        groupname=groupname,
        project_id=project_id,
        order_by=order_by,
        start_at=start_at,
        max_results=max_results,
        expand=expand,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    dashboard_name: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    owner: Union[Unset, str] = UNSET,
    groupname: Union[Unset, str] = UNSET,
    project_id: Union[Unset, int] = UNSET,
    order_by: Union[Unset, GetDashboardsPaginatedOrderBy] = GetDashboardsPaginatedOrderBy.NAME,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorCollection, PageBeanDashboard]]:
    """Returns a [paginated](#pagination) list of dashboards. This operation is similar to [Get dashboards](#api-rest-api-3-dashboard-get) except that the results can be refined to include dashboards that have specific attributes. For example, dashboards with a particular name. When multiple attributes are specified only filters matching all attributes are returned.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** The following dashboards that match the query parameters are returned:

     *  Dashboards owned by the user. Not returned for anonymous users.
     *  Dashboards shared with a group that the user is a member of. Not returned for anonymous users.
     *  Dashboards shared with a private project that the user can browse. Not returned for anonymous users.
     *  Dashboards shared with a public project.
     *  Dashboards shared with the public."""

    return (
        await asyncio_detailed(
            client=client,
            dashboard_name=dashboard_name,
            account_id=account_id,
            owner=owner,
            groupname=groupname,
            project_id=project_id,
            order_by=order_by,
            start_at=start_at,
            max_results=max_results,
            expand=expand,
        )
    ).parsed
