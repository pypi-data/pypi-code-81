from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.operation_message import OperationMessage
from ...models.property_keys import PropertyKeys
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    addon_key: str,
) -> Dict[str, Any]:
    url = "{}/rest/atlassian-connect/1/addons/{addonKey}/properties".format(client.base_url, addonKey=addon_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[OperationMessage, PropertyKeys]]:
    if response.status_code == 200:
        response_200 = PropertyKeys.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = OperationMessage.from_dict(response.json())

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[OperationMessage, PropertyKeys]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    addon_key: str,
) -> Response[Union[OperationMessage, PropertyKeys]]:
    kwargs = _get_kwargs(
        client=client,
        addon_key=addon_key,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    addon_key: str,
) -> Optional[Union[OperationMessage, PropertyKeys]]:
    """Gets all the properties of an app.

    **[Permissions](#permissions) required:** Only a Connect app whose key matches `addonKey` can make this request."""

    return sync_detailed(
        client=client,
        addon_key=addon_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    addon_key: str,
) -> Response[Union[OperationMessage, PropertyKeys]]:
    kwargs = _get_kwargs(
        client=client,
        addon_key=addon_key,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    addon_key: str,
) -> Optional[Union[OperationMessage, PropertyKeys]]:
    """Gets all the properties of an app.

    **[Permissions](#permissions) required:** Only a Connect app whose key matches `addonKey` can make this request."""

    return (
        await asyncio_detailed(
            client=client,
            addon_key=addon_key,
        )
    ).parsed
