from typing import Any, Dict

import httpx

from ...client import AuthenticatedClient
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    screen_id: int,
    tab_id: int,
    pos: int,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/screens/{screenId}/tabs/{tabId}/move/{pos}".format(
        client.base_url, screenId=screen_id, tabId=tab_id, pos=pos
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
    screen_id: int,
    tab_id: int,
    pos: int,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        screen_id=screen_id,
        tab_id=tab_id,
        pos=pos,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    screen_id: int,
    tab_id: int,
    pos: int,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        screen_id=screen_id,
        tab_id=tab_id,
        pos=pos,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)
