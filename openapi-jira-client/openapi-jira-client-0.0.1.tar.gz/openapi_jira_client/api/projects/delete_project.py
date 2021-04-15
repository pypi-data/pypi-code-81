from typing import Any, Dict, Union

import httpx

from ...client import AuthenticatedClient
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    enable_undo: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/project/{projectIdOrKey}".format(client.base_url, projectIdOrKey=project_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "enableUndo": enable_undo,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
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
    enable_undo: Union[Unset, bool] = False,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        enable_undo=enable_undo,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    enable_undo: Union[Unset, bool] = False,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        enable_undo=enable_undo,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)
