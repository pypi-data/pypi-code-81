from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.page_bean_project import PageBeanProject
from ...models.search_projects_action import SearchProjectsAction
from ...models.search_projects_order_by import SearchProjectsOrderBy
from ...models.search_projects_status_item import SearchProjectsStatusItem
from ...models.string_list import StringList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    order_by: Union[Unset, SearchProjectsOrderBy] = SearchProjectsOrderBy.KEY,
    query: Union[Unset, str] = UNSET,
    type_key: Union[Unset, str] = UNSET,
    category_id: Union[Unset, int] = UNSET,
    action: Union[Unset, SearchProjectsAction] = SearchProjectsAction.VIEW,
    expand: Union[Unset, str] = UNSET,
    status: Union[Unset, List[SearchProjectsStatusItem]] = UNSET,
    properties: Union[Unset, List[StringList]] = UNSET,
    property_query: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/project/search".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_order_by: Union[Unset, str] = UNSET
    if not isinstance(order_by, Unset):
        json_order_by = order_by.value

    json_action: Union[Unset, str] = UNSET
    if not isinstance(action, Unset):
        json_action = action.value

    json_status: Union[Unset, List[str]] = UNSET
    if not isinstance(status, Unset):
        json_status = []
        for status_item_data in status:
            status_item = status_item_data.value

            json_status.append(status_item)

    json_properties: Union[Unset, List[Dict[str, Any]]] = UNSET
    if not isinstance(properties, Unset):
        json_properties = []
        for properties_item_data in properties:
            properties_item = properties_item_data.to_dict()

            json_properties.append(properties_item)

    params: Dict[str, Any] = {
        "startAt": start_at,
        "maxResults": max_results,
        "orderBy": json_order_by,
        "query": query,
        "typeKey": type_key,
        "categoryId": category_id,
        "action": json_action,
        "expand": expand,
        "status": json_status,
        "properties": json_properties,
        "propertyQuery": property_query,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, PageBeanProject]]:
    if response.status_code == 200:
        response_200 = PageBeanProject.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[None, PageBeanProject]]:
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
    max_results: Union[Unset, int] = 50,
    order_by: Union[Unset, SearchProjectsOrderBy] = SearchProjectsOrderBy.KEY,
    query: Union[Unset, str] = UNSET,
    type_key: Union[Unset, str] = UNSET,
    category_id: Union[Unset, int] = UNSET,
    action: Union[Unset, SearchProjectsAction] = SearchProjectsAction.VIEW,
    expand: Union[Unset, str] = UNSET,
    status: Union[Unset, List[SearchProjectsStatusItem]] = UNSET,
    properties: Union[Unset, List[StringList]] = UNSET,
    property_query: Union[Unset, str] = UNSET,
) -> Response[Union[None, PageBeanProject]]:
    kwargs = _get_kwargs(
        client=client,
        start_at=start_at,
        max_results=max_results,
        order_by=order_by,
        query=query,
        type_key=type_key,
        category_id=category_id,
        action=action,
        expand=expand,
        status=status,
        properties=properties,
        property_query=property_query,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    order_by: Union[Unset, SearchProjectsOrderBy] = SearchProjectsOrderBy.KEY,
    query: Union[Unset, str] = UNSET,
    type_key: Union[Unset, str] = UNSET,
    category_id: Union[Unset, int] = UNSET,
    action: Union[Unset, SearchProjectsAction] = SearchProjectsAction.VIEW,
    expand: Union[Unset, str] = UNSET,
    status: Union[Unset, List[SearchProjectsStatusItem]] = UNSET,
    properties: Union[Unset, List[StringList]] = UNSET,
    property_query: Union[Unset, str] = UNSET,
) -> Optional[Union[None, PageBeanProject]]:
    """Returns a [paginated](#pagination) list of projects visible to the user.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** Projects are returned only where the user has one of:

     *  *Browse Projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project.
     *  *Administer Projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project.
     *  *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        start_at=start_at,
        max_results=max_results,
        order_by=order_by,
        query=query,
        type_key=type_key,
        category_id=category_id,
        action=action,
        expand=expand,
        status=status,
        properties=properties,
        property_query=property_query,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    order_by: Union[Unset, SearchProjectsOrderBy] = SearchProjectsOrderBy.KEY,
    query: Union[Unset, str] = UNSET,
    type_key: Union[Unset, str] = UNSET,
    category_id: Union[Unset, int] = UNSET,
    action: Union[Unset, SearchProjectsAction] = SearchProjectsAction.VIEW,
    expand: Union[Unset, str] = UNSET,
    status: Union[Unset, List[SearchProjectsStatusItem]] = UNSET,
    properties: Union[Unset, List[StringList]] = UNSET,
    property_query: Union[Unset, str] = UNSET,
) -> Response[Union[None, PageBeanProject]]:
    kwargs = _get_kwargs(
        client=client,
        start_at=start_at,
        max_results=max_results,
        order_by=order_by,
        query=query,
        type_key=type_key,
        category_id=category_id,
        action=action,
        expand=expand,
        status=status,
        properties=properties,
        property_query=property_query,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    order_by: Union[Unset, SearchProjectsOrderBy] = SearchProjectsOrderBy.KEY,
    query: Union[Unset, str] = UNSET,
    type_key: Union[Unset, str] = UNSET,
    category_id: Union[Unset, int] = UNSET,
    action: Union[Unset, SearchProjectsAction] = SearchProjectsAction.VIEW,
    expand: Union[Unset, str] = UNSET,
    status: Union[Unset, List[SearchProjectsStatusItem]] = UNSET,
    properties: Union[Unset, List[StringList]] = UNSET,
    property_query: Union[Unset, str] = UNSET,
) -> Optional[Union[None, PageBeanProject]]:
    """Returns a [paginated](#pagination) list of projects visible to the user.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** Projects are returned only where the user has one of:

     *  *Browse Projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project.
     *  *Administer Projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project.
     *  *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            start_at=start_at,
            max_results=max_results,
            order_by=order_by,
            query=query,
            type_key=type_key,
            category_id=category_id,
            action=action,
            expand=expand,
            status=status,
            properties=properties,
            property_query=property_query,
        )
    ).parsed
