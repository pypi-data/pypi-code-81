from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.share_permission import SharePermission
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id_: int,
    permission_id: int,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/filter/{id}/permission/{permissionId}".format(
        client.base_url, id=id_, permissionId=permission_id
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, SharePermission]]:
    if response.status_code == 200:
        response_200 = SharePermission.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, SharePermission]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    id_: int,
    permission_id: int,
) -> Response[Union[None, SharePermission]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        permission_id=permission_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id_: int,
    permission_id: int,
) -> Optional[Union[None, SharePermission]]:
    """Returns a share permission for a filter. A filter can be shared with groups, projects, all logged-in users, or the public. Sharing with all logged-in users or the public is known as a global share permission.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None, however, a share permission is only returned for:

     *  filters owned by the user.
     *  filters shared with a group that the user is a member of.
     *  filters shared with a private project that the user has *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for.
     *  filters shared with a public project.
     *  filters shared with the public."""

    return sync_detailed(
        client=client,
        id_=id_,
        permission_id=permission_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id_: int,
    permission_id: int,
) -> Response[Union[None, SharePermission]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        permission_id=permission_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id_: int,
    permission_id: int,
) -> Optional[Union[None, SharePermission]]:
    """Returns a share permission for a filter. A filter can be shared with groups, projects, all logged-in users, or the public. Sharing with all logged-in users or the public is known as a global share permission.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None, however, a share permission is only returned for:

     *  filters owned by the user.
     *  filters shared with a group that the user is a member of.
     *  filters shared with a private project that the user has *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for.
     *  filters shared with a public project.
     *  filters shared with the public."""

    return (
        await asyncio_detailed(
            client=client,
            id_=id_,
            permission_id=permission_id,
        )
    ).parsed
