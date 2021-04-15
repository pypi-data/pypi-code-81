from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.page_bean_context_for_project_and_issue_type import PageBeanContextForProjectAndIssueType
from ...models.project_issue_type_mappings import ProjectIssueTypeMappings
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    field_id: str,
    json_body: ProjectIssueTypeMappings,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/field/{fieldId}/context/mapping".format(client.base_url, fieldId=field_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "startAt": start_at,
        "maxResults": max_results,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, PageBeanContextForProjectAndIssueType]]:
    if response.status_code == 200:
        response_200 = PageBeanContextForProjectAndIssueType.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[None, PageBeanContextForProjectAndIssueType]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    field_id: str,
    json_body: ProjectIssueTypeMappings,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Response[Union[None, PageBeanContextForProjectAndIssueType]]:
    kwargs = _get_kwargs(
        client=client,
        field_id=field_id,
        json_body=json_body,
        start_at=start_at,
        max_results=max_results,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    field_id: str,
    json_body: ProjectIssueTypeMappings,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Optional[Union[None, PageBeanContextForProjectAndIssueType]]:
    """Returns a [paginated](#pagination) list of project and issue type mappings and, for each mapping, the ID of a [custom field context](https://confluence.atlassian.com/x/k44fOw) that applies to the project and issue type.

    If there is no custom field context assigned to the project then, if present, the custom field context that applies to all projects is returned if it also applies to the issue type or all issue types. If a custom field context is not found, the returned custom field context ID is `null`.

    Duplicate project and issue type mappings cannot be provided in the request.

    The order of the returned values is the same as provided in the request.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        field_id=field_id,
        json_body=json_body,
        start_at=start_at,
        max_results=max_results,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    field_id: str,
    json_body: ProjectIssueTypeMappings,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Response[Union[None, PageBeanContextForProjectAndIssueType]]:
    kwargs = _get_kwargs(
        client=client,
        field_id=field_id,
        json_body=json_body,
        start_at=start_at,
        max_results=max_results,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    field_id: str,
    json_body: ProjectIssueTypeMappings,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Optional[Union[None, PageBeanContextForProjectAndIssueType]]:
    """Returns a [paginated](#pagination) list of project and issue type mappings and, for each mapping, the ID of a [custom field context](https://confluence.atlassian.com/x/k44fOw) that applies to the project and issue type.

    If there is no custom field context assigned to the project then, if present, the custom field context that applies to all projects is returned if it also applies to the issue type or all issue types. If a custom field context is not found, the returned custom field context ID is `null`.

    Duplicate project and issue type mappings cannot be provided in the request.

    The order of the returned values is the same as provided in the request.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            field_id=field_id,
            json_body=json_body,
            start_at=start_at,
            max_results=max_results,
        )
    ).parsed
