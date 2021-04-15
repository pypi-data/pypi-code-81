from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.project_avatars import ProjectAvatars
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/project/{projectIdOrKey}/avatars".format(client.base_url, projectIdOrKey=project_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, ProjectAvatars]]:
    if response.status_code == 200:
        response_200 = ProjectAvatars.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, ProjectAvatars]]:
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
) -> Response[Union[None, ProjectAvatars]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
) -> Optional[Union[None, ProjectAvatars]]:
    """Returns all project avatars, grouped by system and custom avatars.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project."""

    return sync_detailed(
        client=client,
        project_id_or_key=project_id_or_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
) -> Response[Union[None, ProjectAvatars]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
) -> Optional[Union[None, ProjectAvatars]]:
    """Returns all project avatars, grouped by system and custom avatars.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project."""

    return (
        await asyncio_detailed(
            client=client,
            project_id_or_key=project_id_or_key,
        )
    ).parsed
