from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.avatars import Avatars
from ...models.get_avatars_type import GetAvatarsType
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    type_: GetAvatarsType,
    entity_id: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/universal_avatar/type/{type}/owner/{entityId}".format(
        client.base_url, type=type_, entityId=entity_id
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Avatars, None]]:
    if response.status_code == 200:
        response_200 = Avatars.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Avatars, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    type_: GetAvatarsType,
    entity_id: str,
) -> Response[Union[Avatars, None]]:
    kwargs = _get_kwargs(
        client=client,
        type_=type_,
        entity_id=entity_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    type_: GetAvatarsType,
    entity_id: str,
) -> Optional[Union[Avatars, None]]:
    """Returns the system and custom avatars for a project or issue type.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  for custom project avatars, *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project the avatar belongs to.
     *  for custom issue type avatars, *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for at least one project the issue type is used in.
     *  for system avatars, none."""

    return sync_detailed(
        client=client,
        type_=type_,
        entity_id=entity_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    type_: GetAvatarsType,
    entity_id: str,
) -> Response[Union[Avatars, None]]:
    kwargs = _get_kwargs(
        client=client,
        type_=type_,
        entity_id=entity_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    type_: GetAvatarsType,
    entity_id: str,
) -> Optional[Union[Avatars, None]]:
    """Returns the system and custom avatars for a project or issue type.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  for custom project avatars, *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project the avatar belongs to.
     *  for custom issue type avatars, *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for at least one project the issue type is used in.
     *  for system avatars, none."""

    return (
        await asyncio_detailed(
            client=client,
            type_=type_,
            entity_id=entity_id,
        )
    ).parsed
