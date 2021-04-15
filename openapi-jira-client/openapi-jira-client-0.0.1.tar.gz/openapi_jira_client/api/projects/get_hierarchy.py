from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.project_issue_type_hierarchy import ProjectIssueTypeHierarchy
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    project_id: int,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/project/{projectId}/hierarchy".format(client.base_url, projectId=project_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, ProjectIssueTypeHierarchy]]:
    if response.status_code == 200:
        response_200 = ProjectIssueTypeHierarchy.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[None, ProjectIssueTypeHierarchy]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    project_id: int,
) -> Response[Union[None, ProjectIssueTypeHierarchy]]:
    kwargs = _get_kwargs(
        client=client,
        project_id=project_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_id: int,
) -> Optional[Union[None, ProjectIssueTypeHierarchy]]:
    """Get the issue type hierarchy for a next-gen project.

    The issue type hierarchy for a project consists of:

     *  *Epic* at level 1 (optional).
     *  One or more issue types at level 0 such as *Story*, *Task*, or *Bug*. Where the issue type *Epic* is defined, these issue types are used to break down the content of an epic.
     *  *Subtask* at level -1 (optional). This issue type enables level 0 issue types to be broken down into components. Issues based on a level -1 issue type must have a parent issue.

    **[Permissions](#permissions) required:** *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project."""

    return sync_detailed(
        client=client,
        project_id=project_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id: int,
) -> Response[Union[None, ProjectIssueTypeHierarchy]]:
    kwargs = _get_kwargs(
        client=client,
        project_id=project_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id: int,
) -> Optional[Union[None, ProjectIssueTypeHierarchy]]:
    """Get the issue type hierarchy for a next-gen project.

    The issue type hierarchy for a project consists of:

     *  *Epic* at level 1 (optional).
     *  One or more issue types at level 0 such as *Story*, *Task*, or *Bug*. Where the issue type *Epic* is defined, these issue types are used to break down the content of an epic.
     *  *Subtask* at level -1 (optional). This issue type enables level 0 issue types to be broken down into components. Issues based on a level -1 issue type must have a parent issue.

    **[Permissions](#permissions) required:** *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project."""

    return (
        await asyncio_detailed(
            client=client,
            project_id=project_id,
        )
    ).parsed
