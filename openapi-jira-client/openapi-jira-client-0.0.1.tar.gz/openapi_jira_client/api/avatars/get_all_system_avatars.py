from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.get_all_system_avatars_type import GetAllSystemAvatarsType
from ...models.system_avatars import SystemAvatars
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    type_: GetAllSystemAvatarsType,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/avatar/{type}/system".format(client.base_url, type=type_)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, SystemAvatars]]:
    if response.status_code == 200:
        response_200 = SystemAvatars.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 500:
        response_500 = None

        return response_500
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, SystemAvatars]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    type_: GetAllSystemAvatarsType,
) -> Response[Union[None, SystemAvatars]]:
    kwargs = _get_kwargs(
        client=client,
        type_=type_,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    type_: GetAllSystemAvatarsType,
) -> Optional[Union[None, SystemAvatars]]:
    """Returns a list of system avatar details by owner type, where the owner types are issue type, project, or user.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None."""

    return sync_detailed(
        client=client,
        type_=type_,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    type_: GetAllSystemAvatarsType,
) -> Response[Union[None, SystemAvatars]]:
    kwargs = _get_kwargs(
        client=client,
        type_=type_,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    type_: GetAllSystemAvatarsType,
) -> Optional[Union[None, SystemAvatars]]:
    """Returns a list of system avatar details by owner type, where the owner types are issue type, project, or user.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None."""

    return (
        await asyncio_detailed(
            client=client,
            type_=type_,
        )
    ).parsed
