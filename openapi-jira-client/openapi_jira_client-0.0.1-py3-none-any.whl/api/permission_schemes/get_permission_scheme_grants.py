from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.permission_grants import PermissionGrants
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    scheme_id: int,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/permissionscheme/{schemeId}/permission".format(client.base_url, schemeId=scheme_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, PermissionGrants]]:
    if response.status_code == 200:
        response_200 = PermissionGrants.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, PermissionGrants]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    scheme_id: int,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[None, PermissionGrants]]:
    kwargs = _get_kwargs(
        client=client,
        scheme_id=scheme_id,
        expand=expand,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    scheme_id: int,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[None, PermissionGrants]]:
    """Returns all permission grants for a permission scheme.

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return sync_detailed(
        client=client,
        scheme_id=scheme_id,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    scheme_id: int,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[None, PermissionGrants]]:
    kwargs = _get_kwargs(
        client=client,
        scheme_id=scheme_id,
        expand=expand,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    scheme_id: int,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[None, PermissionGrants]]:
    """Returns all permission grants for a permission scheme.

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return (
        await asyncio_detailed(
            client=client,
            scheme_id=scheme_id,
            expand=expand,
        )
    ).parsed
