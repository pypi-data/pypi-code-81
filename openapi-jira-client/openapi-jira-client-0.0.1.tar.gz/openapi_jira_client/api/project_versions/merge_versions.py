from typing import Any, Dict

import httpx

from ...client import AuthenticatedClient
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id_: str,
    move_issues_to: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/version/{id}/mergeto/{moveIssuesTo}".format(
        client.base_url, id=id_, moveIssuesTo=move_issues_to
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
    id_: str,
    move_issues_to: str,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        move_issues_to=move_issues_to,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id_: str,
    move_issues_to: str,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        move_issues_to=move_issues_to,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)
