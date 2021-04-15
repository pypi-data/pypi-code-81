from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.operation_message import OperationMessage
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    addon_key: str,
    property_key: str,
    json_body: None,
) -> Dict[str, Any]:
    url = "{}/rest/atlassian-connect/1/addons/{addonKey}/properties/{propertyKey}".format(
        client.base_url, addonKey=addon_key, propertyKey=property_key
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = None

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[OperationMessage]:
    if response.status_code == 200:
        response_200 = OperationMessage.from_dict(response.json())

        return response_200
    if response.status_code == 201:
        response_201 = OperationMessage.from_dict(response.json())

        return response_201
    if response.status_code == 400:
        response_400 = OperationMessage.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = OperationMessage.from_dict(response.json())

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[OperationMessage]:
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
    property_key: str,
    json_body: None,
) -> Response[OperationMessage]:
    kwargs = _get_kwargs(
        client=client,
        addon_key=addon_key,
        property_key=property_key,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    addon_key: str,
    property_key: str,
    json_body: None,
) -> Optional[OperationMessage]:
    """Sets the value of an app's property. Use this resource to store custom data for your app.

    The value of the request body must be a [valid](http://tools.ietf.org/html/rfc4627), non-empty JSON blob. The maximum length is 32768 characters.

    **[Permissions](#permissions) required:** Only a Connect app whose key matches `addonKey` can make this request."""

    return sync_detailed(
        client=client,
        addon_key=addon_key,
        property_key=property_key,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    addon_key: str,
    property_key: str,
    json_body: None,
) -> Response[OperationMessage]:
    kwargs = _get_kwargs(
        client=client,
        addon_key=addon_key,
        property_key=property_key,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    addon_key: str,
    property_key: str,
    json_body: None,
) -> Optional[OperationMessage]:
    """Sets the value of an app's property. Use this resource to store custom data for your app.

    The value of the request body must be a [valid](http://tools.ietf.org/html/rfc4627), non-empty JSON blob. The maximum length is 32768 characters.

    **[Permissions](#permissions) required:** Only a Connect app whose key matches `addonKey` can make this request."""

    return (
        await asyncio_detailed(
            client=client,
            addon_key=addon_key,
            property_key=property_key,
            json_body=json_body,
        )
    ).parsed
