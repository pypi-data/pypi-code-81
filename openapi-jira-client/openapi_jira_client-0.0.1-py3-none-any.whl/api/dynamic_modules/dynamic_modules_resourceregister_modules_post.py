from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.connect_modules import ConnectModules
from ...models.error_message import ErrorMessage
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: ConnectModules,
) -> Dict[str, Any]:
    url = "{}/rest/atlassian-connect/1/app/module/dynamic".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[ErrorMessage, None]]:
    if response.status_code == 200:
        response_200 = None

        return response_200
    if response.status_code == 400:
        response_400 = ErrorMessage.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = ErrorMessage.from_dict(response.json())

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ErrorMessage, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: ConnectModules,
) -> Response[Union[ErrorMessage, None]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: ConnectModules,
) -> Optional[Union[ErrorMessage, None]]:
    """Registers a list of modules.

    **[Permissions](#permissions) required:** Only Connect apps can make this request."""

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: ConnectModules,
) -> Response[Union[ErrorMessage, None]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: ConnectModules,
) -> Optional[Union[ErrorMessage, None]]:
    """Registers a list of modules.

    **[Permissions](#permissions) required:** Only Connect apps can make this request."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
