from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.security_scheme import SecurityScheme
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    project_key_or_id: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/project/{projectKeyOrId}/issuesecuritylevelscheme".format(
        client.base_url, projectKeyOrId=project_key_or_id
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, SecurityScheme]]:
    if response.status_code == 200:
        response_200 = SecurityScheme.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[None, SecurityScheme]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    project_key_or_id: str,
) -> Response[Union[None, SecurityScheme]]:
    kwargs = _get_kwargs(
        client=client,
        project_key_or_id=project_key_or_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_key_or_id: str,
) -> Optional[Union[None, SecurityScheme]]:
    """Returns the [issue security scheme](https://confluence.atlassian.com/x/J4lKLg) associated with the project.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg) or the *Administer Projects* [project permission](https://confluence.atlassian.com/x/yodKLg)."""

    return sync_detailed(
        client=client,
        project_key_or_id=project_key_or_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_key_or_id: str,
) -> Response[Union[None, SecurityScheme]]:
    kwargs = _get_kwargs(
        client=client,
        project_key_or_id=project_key_or_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_key_or_id: str,
) -> Optional[Union[None, SecurityScheme]]:
    """Returns the [issue security scheme](https://confluence.atlassian.com/x/J4lKLg) associated with the project.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg) or the *Administer Projects* [project permission](https://confluence.atlassian.com/x/yodKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            project_key_or_id=project_key_or_id,
        )
    ).parsed
