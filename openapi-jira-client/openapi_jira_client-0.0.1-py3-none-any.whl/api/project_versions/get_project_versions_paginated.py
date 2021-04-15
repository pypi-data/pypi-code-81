from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.get_project_versions_paginated_order_by import GetProjectVersionsPaginatedOrderBy
from ...models.page_bean_version import PageBeanVersion
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    order_by: Union[Unset, GetProjectVersionsPaginatedOrderBy] = UNSET,
    query: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/project/{projectIdOrKey}/version".format(client.base_url, projectIdOrKey=project_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_order_by: Union[Unset, str] = UNSET
    if not isinstance(order_by, Unset):
        json_order_by = order_by.value

    params: Dict[str, Any] = {
        "startAt": start_at,
        "maxResults": max_results,
        "orderBy": json_order_by,
        "query": query,
        "status": status,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, PageBeanVersion]]:
    if response.status_code == 200:
        response_200 = PageBeanVersion.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, PageBeanVersion]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    order_by: Union[Unset, GetProjectVersionsPaginatedOrderBy] = UNSET,
    query: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[None, PageBeanVersion]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        start_at=start_at,
        max_results=max_results,
        order_by=order_by,
        query=query,
        status=status,
        expand=expand,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    order_by: Union[Unset, GetProjectVersionsPaginatedOrderBy] = UNSET,
    query: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[None, PageBeanVersion]]:
    """Returns a [paginated](#pagination) list of all versions in a project. See the [Get project versions](#api-rest-api-3-project-projectIdOrKey-versions-get) resource if you want to get a full list of versions without pagination.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Browse Projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project."""

    return sync_detailed(
        client=client,
        project_id_or_key=project_id_or_key,
        start_at=start_at,
        max_results=max_results,
        order_by=order_by,
        query=query,
        status=status,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    order_by: Union[Unset, GetProjectVersionsPaginatedOrderBy] = UNSET,
    query: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[None, PageBeanVersion]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        start_at=start_at,
        max_results=max_results,
        order_by=order_by,
        query=query,
        status=status,
        expand=expand,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    order_by: Union[Unset, GetProjectVersionsPaginatedOrderBy] = UNSET,
    query: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[None, PageBeanVersion]]:
    """Returns a [paginated](#pagination) list of all versions in a project. See the [Get project versions](#api-rest-api-3-project-projectIdOrKey-versions-get) resource if you want to get a full list of versions without pagination.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Browse Projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project."""

    return (
        await asyncio_detailed(
            client=client,
            project_id_or_key=project_id_or_key,
            start_at=start_at,
            max_results=max_results,
            order_by=order_by,
            query=query,
            status=status,
            expand=expand,
        )
    ).parsed
