from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.connect_modules import ConnectModules
from ...models.error_message import ErrorMessage
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/rest/atlassian-connect/1/app/module/dynamic".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[ConnectModules, ErrorMessage]]:
    if response.status_code == 200:
        response_200 = ConnectModules.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = ErrorMessage.from_dict(response.json())

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ConnectModules, ErrorMessage]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[Union[ConnectModules, ErrorMessage]]:
    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
) -> Optional[Union[ConnectModules, ErrorMessage]]:
    """Returns all modules registered dynamically by the calling app.

    **[Permissions](#permissions) required:** Only Connect apps can make this request."""

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[Union[ConnectModules, ErrorMessage]]:
    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
) -> Optional[Union[ConnectModules, ErrorMessage]]:
    """Returns all modules registered dynamically by the calling app.

    **[Permissions](#permissions) required:** Only Connect apps can make this request."""

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
