from typing import Any, Dict

import httpx

from ...client import AuthenticatedClient
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    id_: int,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/project/{projectIdOrKey}/avatar/{id}".format(
        client.base_url, projectIdOrKey=project_id_or_key, id=id_
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
    project_id_or_key: str,
    id_: int,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        id_=id_,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    id_: int,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        id_=id_,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)
