from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.permission_scheme import PermissionScheme
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: PermissionScheme,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/permissionscheme".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "expand": expand,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, PermissionScheme]]:
    if response.status_code == 201:
        response_201 = PermissionScheme.from_dict(response.json())

        return response_201
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = None

        return response_403
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, PermissionScheme]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: PermissionScheme,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[None, PermissionScheme]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        expand=expand,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: PermissionScheme,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[None, PermissionScheme]]:
    """Creates a new permission scheme. You can create a permission scheme with or without defining a set of permission grants.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        json_body=json_body,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: PermissionScheme,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[None, PermissionScheme]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        expand=expand,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: PermissionScheme,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[None, PermissionScheme]]:
    """Creates a new permission scheme. You can create a permission scheme with or without defining a set of permission grants.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            expand=expand,
        )
    ).parsed
