from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.project import Project
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    expand: Union[Unset, str] = UNSET,
    properties: Union[Unset, List[str]] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/project/{projectIdOrKey}".format(client.base_url, projectIdOrKey=project_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_properties: Union[Unset, List[str]] = UNSET
    if not isinstance(properties, Unset):
        json_properties = properties

    params: Dict[str, Any] = {
        "expand": expand,
        "properties": json_properties,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, Project]]:
    if response.status_code == 200:
        response_200 = Project.from_dict(response.json())

        return response_200
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
    expand: Union[Unset, str] = UNSET,
    properties: Union[Unset, List[str]] = UNSET,
) -> Response[Union[None, Project]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        expand=expand,
        properties=properties,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    expand: Union[Unset, str] = UNSET,
    properties: Union[Unset, List[str]] = UNSET,
) -> Optional[Union[None, Project]]:
    """Returns the [project details](https://confluence.atlassian.com/x/ahLpNw) for a project.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project."""

    return sync_detailed(
        client=client,
        project_id_or_key=project_id_or_key,
        expand=expand,
        properties=properties,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    expand: Union[Unset, str] = UNSET,
    properties: Union[Unset, List[str]] = UNSET,
) -> Response[Union[None, Project]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        expand=expand,
        properties=properties,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    expand: Union[Unset, str] = UNSET,
    properties: Union[Unset, List[str]] = UNSET,
) -> Optional[Union[None, Project]]:
    """Returns the [project details](https://confluence.atlassian.com/x/ahLpNw) for a project.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project."""

    return (
        await asyncio_detailed(
            client=client,
            project_id_or_key=project_id_or_key,
            expand=expand,
            properties=properties,
        )
    ).parsed
