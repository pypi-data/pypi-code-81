from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.error_collection import ErrorCollection
from ...models.page_bean_workflow import PageBeanWorkflow
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    workflow_name: Union[Unset, List[str]] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/workflow/search".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_workflow_name: Union[Unset, List[str]] = UNSET
    if not isinstance(workflow_name, Unset):
        json_workflow_name = workflow_name

    params: Dict[str, Any] = {
        "startAt": start_at,
        "maxResults": max_results,
        "workflowName": json_workflow_name,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[ErrorCollection, None, PageBeanWorkflow]]:
    if response.status_code == 200:
        response_200 = PageBeanWorkflow.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = ErrorCollection.from_dict(response.json())

        return response_403
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ErrorCollection, None, PageBeanWorkflow]]:
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
    workflow_name: Union[Unset, List[str]] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorCollection, None, PageBeanWorkflow]]:
    kwargs = _get_kwargs(
        client=client,
        start_at=start_at,
        max_results=max_results,
        workflow_name=workflow_name,
        expand=expand,
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
    workflow_name: Union[Unset, List[str]] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorCollection, None, PageBeanWorkflow]]:
    """Returns a [paginated](#pagination) list of published classic workflows. When workflow names are specified, details of those workflows are returned. Otherwise, all published classic workflows are returned.

    This operation does not return next-gen workflows.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        start_at=start_at,
        max_results=max_results,
        workflow_name=workflow_name,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    workflow_name: Union[Unset, List[str]] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorCollection, None, PageBeanWorkflow]]:
    kwargs = _get_kwargs(
        client=client,
        start_at=start_at,
        max_results=max_results,
        workflow_name=workflow_name,
        expand=expand,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    workflow_name: Union[Unset, List[str]] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorCollection, None, PageBeanWorkflow]]:
    """Returns a [paginated](#pagination) list of published classic workflows. When workflow names are specified, details of those workflows are returned. Otherwise, all published classic workflows are returned.

    This operation does not return next-gen workflows.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            start_at=start_at,
            max_results=max_results,
            workflow_name=workflow_name,
            expand=expand,
        )
    ).parsed
