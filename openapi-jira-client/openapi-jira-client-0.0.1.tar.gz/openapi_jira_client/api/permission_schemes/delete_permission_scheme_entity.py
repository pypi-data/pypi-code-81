from typing import Any, Dict

import httpx

from ...client import AuthenticatedClient
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    scheme_id: int,
    permission_id: int,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/permissionscheme/{schemeId}/permission/{permissionId}".format(
        client.base_url, schemeId=scheme_id, permissionId=permission_id
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
    scheme_id: int,
    permission_id: int,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        scheme_id=scheme_id,
        permission_id=permission_id,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    scheme_id: int,
    permission_id: int,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        scheme_id=scheme_id,
        permission_id=permission_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)
