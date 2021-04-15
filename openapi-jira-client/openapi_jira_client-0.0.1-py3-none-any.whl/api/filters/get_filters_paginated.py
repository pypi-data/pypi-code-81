from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.error_collection import ErrorCollection
from ...models.get_filters_paginated_order_by import GetFiltersPaginatedOrderBy
from ...models.page_bean_filter_details import PageBeanFilterDetails
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    filter_name: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    owner: Union[Unset, str] = UNSET,
    groupname: Union[Unset, str] = UNSET,
    project_id: Union[Unset, int] = UNSET,
    id_: Union[Unset, List[int]] = UNSET,
    order_by: Union[Unset, GetFiltersPaginatedOrderBy] = GetFiltersPaginatedOrderBy.NAME,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/filter/search".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_id_: Union[Unset, List[int]] = UNSET
    if not isinstance(id_, Unset):
        json_id_ = id_

    json_order_by: Union[Unset, str] = UNSET
    if not isinstance(order_by, Unset):
        json_order_by = order_by.value

    params: Dict[str, Any] = {
        "filterName": filter_name,
        "accountId": account_id,
        "owner": owner,
        "groupname": groupname,
        "projectId": project_id,
        "id": json_id_,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[ErrorCollection, None, PageBeanFilterDetails]]:
    if response.status_code == 200:
        response_200 = PageBeanFilterDetails.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorCollection.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ErrorCollection, None, PageBeanFilterDetails]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    filter_name: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    owner: Union[Unset, str] = UNSET,
    groupname: Union[Unset, str] = UNSET,
    project_id: Union[Unset, int] = UNSET,
    id_: Union[Unset, List[int]] = UNSET,
    order_by: Union[Unset, GetFiltersPaginatedOrderBy] = GetFiltersPaginatedOrderBy.NAME,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorCollection, None, PageBeanFilterDetails]]:
    kwargs = _get_kwargs(
        client=client,
        filter_name=filter_name,
        account_id=account_id,
        owner=owner,
        groupname=groupname,
        project_id=project_id,
        id_=id_,
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
    filter_name: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    owner: Union[Unset, str] = UNSET,
    groupname: Union[Unset, str] = UNSET,
    project_id: Union[Unset, int] = UNSET,
    id_: Union[Unset, List[int]] = UNSET,
    order_by: Union[Unset, GetFiltersPaginatedOrderBy] = GetFiltersPaginatedOrderBy.NAME,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorCollection, None, PageBeanFilterDetails]]:
    """Returns a [paginated](#pagination) list of filters. Use this operation to get:

     *  specific filters, by defining `id` only.
     *  filters that match all of the specified attributes. For example, all filters for a user with a particular word in their name. When multiple attributes are specified only filters matching all attributes are returned.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None, however, only the following filters that match the query parameters are returned:

     *  filters owned by the user.
     *  filters shared with a group that the user is a member of.
     *  filters shared with a private project that the user has *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for.
     *  filters shared with a public project.
     *  filters shared with the public."""

    return sync_detailed(
        client=client,
        filter_name=filter_name,
        account_id=account_id,
        owner=owner,
        groupname=groupname,
        project_id=project_id,
        id_=id_,
        order_by=order_by,
        start_at=start_at,
        max_results=max_results,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    filter_name: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    owner: Union[Unset, str] = UNSET,
    groupname: Union[Unset, str] = UNSET,
    project_id: Union[Unset, int] = UNSET,
    id_: Union[Unset, List[int]] = UNSET,
    order_by: Union[Unset, GetFiltersPaginatedOrderBy] = GetFiltersPaginatedOrderBy.NAME,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorCollection, None, PageBeanFilterDetails]]:
    kwargs = _get_kwargs(
        client=client,
        filter_name=filter_name,
        account_id=account_id,
        owner=owner,
        groupname=groupname,
        project_id=project_id,
        id_=id_,
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
    filter_name: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    owner: Union[Unset, str] = UNSET,
    groupname: Union[Unset, str] = UNSET,
    project_id: Union[Unset, int] = UNSET,
    id_: Union[Unset, List[int]] = UNSET,
    order_by: Union[Unset, GetFiltersPaginatedOrderBy] = GetFiltersPaginatedOrderBy.NAME,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorCollection, None, PageBeanFilterDetails]]:
    """Returns a [paginated](#pagination) list of filters. Use this operation to get:

     *  specific filters, by defining `id` only.
     *  filters that match all of the specified attributes. For example, all filters for a user with a particular word in their name. When multiple attributes are specified only filters matching all attributes are returned.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None, however, only the following filters that match the query parameters are returned:

     *  filters owned by the user.
     *  filters shared with a group that the user is a member of.
     *  filters shared with a private project that the user has *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for.
     *  filters shared with a public project.
     *  filters shared with the public."""

    return (
        await asyncio_detailed(
            client=client,
            filter_name=filter_name,
            account_id=account_id,
            owner=owner,
            groupname=groupname,
            project_id=project_id,
            id_=id_,
            order_by=order_by,
            start_at=start_at,
            max_results=max_results,
            expand=expand,
        )
    ).parsed
