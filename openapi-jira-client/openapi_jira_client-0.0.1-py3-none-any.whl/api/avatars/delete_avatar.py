from typing import Any, Dict

import httpx

from ...client import AuthenticatedClient
from ...models.delete_avatar_type import DeleteAvatarType
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    type_: DeleteAvatarType,
    owning_object_id: str,
    id_: int,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/universal_avatar/type/{type}/owner/{owningObjectId}/avatar/{id}".format(
        client.base_url, type=type_, owningObjectId=owning_object_id, id=id_
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _build_response(*, response: httpx.Response) -> Response[None]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    type_: DeleteAvatarType,
    owning_object_id: str,
    id_: int,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        type_=type_,
        owning_object_id=owning_object_id,
        id_=id_,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    type_: DeleteAvatarType,
    owning_object_id: str,
    id_: int,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        type_=type_,
        owning_object_id=owning_object_id,
        id_=id_,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)
