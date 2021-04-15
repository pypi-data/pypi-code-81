from typing import Any, Dict

import httpx

from ...client import AuthenticatedClient
from ...models.update_screen_scheme_details import UpdateScreenSchemeDetails
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    screen_scheme_id: str,
    json_body: UpdateScreenSchemeDetails,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/screenscheme/{screenSchemeId}".format(client.base_url, screenSchemeId=screen_scheme_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
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
    screen_scheme_id: str,
    json_body: UpdateScreenSchemeDetails,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        screen_scheme_id=screen_scheme_id,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    screen_scheme_id: str,
    json_body: UpdateScreenSchemeDetails,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        screen_scheme_id=screen_scheme_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)
