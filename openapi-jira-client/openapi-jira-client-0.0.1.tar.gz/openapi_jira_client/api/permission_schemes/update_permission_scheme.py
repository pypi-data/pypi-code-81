from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.permission_scheme import PermissionScheme
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    scheme_id: int,
    json_body: PermissionScheme,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/permissionscheme/{schemeId}".format(client.base_url, schemeId=scheme_id)

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
    if response.status_code == 200:
        response_200 = PermissionScheme.from_dict(response.json())

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
    scheme_id: int,
    json_body: PermissionScheme,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[None, PermissionScheme]]:
    kwargs = _get_kwargs(
        client=client,
        scheme_id=scheme_id,
        json_body=json_body,
        expand=expand,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    scheme_id: int,
    json_body: PermissionScheme,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[None, PermissionScheme]]:
    """Updates a permission scheme. Below are some important things to note when using this resource:

     *  If a permissions list is present in the request, then it is set in the permission scheme, overwriting *all existing* grants.
     *  If you want to update only the name and description, then do not send a permissions list in the request.
     *  Sending an empty list will remove all permission grants from the permission scheme.

    If you want to add or delete a permission grant instead of updating the whole list, see [Create permission grant](#api-rest-api-3-permissionscheme-schemeId-permission-post) or [Delete permission scheme entity](#api-rest-api-3-permissionscheme-schemeId-permission-permissionId-delete).

    See [About permission schemes and grants](../api-group-permission-schemes/#about-permission-schemes-and-grants) for more details.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        scheme_id=scheme_id,
        json_body=json_body,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    scheme_id: int,
    json_body: PermissionScheme,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[None, PermissionScheme]]:
    kwargs = _get_kwargs(
        client=client,
        scheme_id=scheme_id,
        json_body=json_body,
        expand=expand,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    scheme_id: int,
    json_body: PermissionScheme,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[None, PermissionScheme]]:
    """Updates a permission scheme. Below are some important things to note when using this resource:

     *  If a permissions list is present in the request, then it is set in the permission scheme, overwriting *all existing* grants.
     *  If you want to update only the name and description, then do not send a permissions list in the request.
     *  Sending an empty list will remove all permission grants from the permission scheme.

    If you want to add or delete a permission grant instead of updating the whole list, see [Create permission grant](#api-rest-api-3-permissionscheme-schemeId-permission-post) or [Delete permission scheme entity](#api-rest-api-3-permissionscheme-schemeId-permission-permissionId-delete).

    See [About permission schemes and grants](../api-group-permission-schemes/#about-permission-schemes-and-grants) for more details.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            scheme_id=scheme_id,
            json_body=json_body,
            expand=expand,
        )
    ).parsed
