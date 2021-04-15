from typing import Any, Dict

import httpx

from ...client import AuthenticatedClient
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_link_type_id: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issueLinkType/{issueLinkTypeId}".format(client.base_url, issueLinkTypeId=issue_link_type_id)

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
    issue_link_type_id: str,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        issue_link_type_id=issue_link_type_id,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_link_type_id: str,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        issue_link_type_id=issue_link_type_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)
