from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.application_role import ApplicationRole
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    key: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/applicationrole/{key}".format(client.base_url, key=key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[ApplicationRole, None]]:
    if response.status_code == 200:
        response_200 = ApplicationRole.from_dict(response.json())

        return response_200
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


def _build_response(*, response: httpx.Response) -> Response[Union[ApplicationRole, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    key: str,
) -> Response[Union[ApplicationRole, None]]:
    kwargs = _get_kwargs(
        client=client,
        key=key,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    key: str,
) -> Optional[Union[ApplicationRole, None]]:
    """Returns an application role.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        key=key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    key: str,
) -> Response[Union[ApplicationRole, None]]:
    kwargs = _get_kwargs(
        client=client,
        key=key,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    key: str,
) -> Optional[Union[ApplicationRole, None]]:
    """Returns an application role.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            key=key,
        )
    ).parsed
