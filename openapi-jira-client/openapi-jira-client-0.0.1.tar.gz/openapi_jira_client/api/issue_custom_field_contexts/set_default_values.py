from typing import Any, Dict

import httpx

from ...client import AuthenticatedClient
from ...models.custom_field_context_default_value_update import CustomFieldContextDefaultValueUpdate
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    field_id: str,
    json_body: CustomFieldContextDefaultValueUpdate,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/field/{fieldId}/context/defaultValue".format(client.base_url, fieldId=field_id)

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
    field_id: str,
    json_body: CustomFieldContextDefaultValueUpdate,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        field_id=field_id,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    field_id: str,
    json_body: CustomFieldContextDefaultValueUpdate,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        field_id=field_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)
