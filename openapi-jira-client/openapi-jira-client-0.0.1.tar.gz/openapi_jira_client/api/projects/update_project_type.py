from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.project import Project
from ...models.update_project_type_new_project_type_key import UpdateProjectTypeNewProjectTypeKey
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    new_project_type_key: UpdateProjectTypeNewProjectTypeKey,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/project/{projectIdOrKey}/type/{newProjectTypeKey}".format(
        client.base_url, projectIdOrKey=project_id_or_key, newProjectTypeKey=new_project_type_key
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, Project]]:
    if response.status_code == 200:
        response_200 = Project.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[None, Project]]:
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
    new_project_type_key: UpdateProjectTypeNewProjectTypeKey,
) -> Response[Union[None, Project]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        new_project_type_key=new_project_type_key,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    new_project_type_key: UpdateProjectTypeNewProjectTypeKey,
) -> Optional[Union[None, Project]]:
    """Deprecated, this feature is no longer supported and no alternatives are available, see [Convert project to a different template or type](https://confluence.atlassian.com/x/yEKeOQ). Updates a [project type](https://confluence.atlassian.com/x/GwiiLQ). The project type can be updated for classic projects only, project type cannot be updated for next-gen projects.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        project_id_or_key=project_id_or_key,
        new_project_type_key=new_project_type_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    new_project_type_key: UpdateProjectTypeNewProjectTypeKey,
) -> Response[Union[None, Project]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        new_project_type_key=new_project_type_key,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    new_project_type_key: UpdateProjectTypeNewProjectTypeKey,
) -> Optional[Union[None, Project]]:
    """Deprecated, this feature is no longer supported and no alternatives are available, see [Convert project to a different template or type](https://confluence.atlassian.com/x/yEKeOQ). Updates a [project type](https://confluence.atlassian.com/x/GwiiLQ). The project type can be updated for classic projects only, project type cannot be updated for next-gen projects.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            project_id_or_key=project_id_or_key,
            new_project_type_key=new_project_type_key,
        )
    ).parsed
