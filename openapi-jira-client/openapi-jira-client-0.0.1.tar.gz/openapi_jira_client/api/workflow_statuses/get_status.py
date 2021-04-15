from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.status_details import StatusDetails
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id_or_name: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/status/{idOrName}".format(client.base_url, idOrName=id_or_name)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, StatusDetails]]:
    if response.status_code == 200:
        response_200 = StatusDetails.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, StatusDetails]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    id_or_name: str,
) -> Response[Union[None, StatusDetails]]:
    kwargs = _get_kwargs(
        client=client,
        id_or_name=id_or_name,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id_or_name: str,
) -> Optional[Union[None, StatusDetails]]:
    """Returns a status. The status must be associated with a workflow to be returned.

    If a name is used on more than one status, only the status found first is returned. Therefore, identifying the status by its ID may be preferable.

    This operation can be accessed anonymously.

    [Permissions](#permissions) required: None."""

    return sync_detailed(
        client=client,
        id_or_name=id_or_name,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id_or_name: str,
) -> Response[Union[None, StatusDetails]]:
    kwargs = _get_kwargs(
        client=client,
        id_or_name=id_or_name,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id_or_name: str,
) -> Optional[Union[None, StatusDetails]]:
    """Returns a status. The status must be associated with a workflow to be returned.

    If a name is used on more than one status, only the status found first is returned. Therefore, identifying the status by its ID may be preferable.

    This operation can be accessed anonymously.

    [Permissions](#permissions) required: None."""

    return (
        await asyncio_detailed(
            client=client,
            id_or_name=id_or_name,
        )
    ).parsed
