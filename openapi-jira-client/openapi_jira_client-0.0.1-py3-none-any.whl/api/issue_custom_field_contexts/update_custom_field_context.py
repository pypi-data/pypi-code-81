from typing import Any, Dict

import httpx

from ...client import AuthenticatedClient
from ...models.custom_field_context_update_details import CustomFieldContextUpdateDetails
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    field_id: str,
    context_id: int,
    json_body: CustomFieldContextUpdateDetails,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/field/{fieldId}/context/{contextId}".format(
        client.base_url, fieldId=field_id, contextId=context_id
    )

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
    context_id: int,
    json_body: CustomFieldContextUpdateDetails,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        field_id=field_id,
        context_id=context_id,
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
    context_id: int,
    json_body: CustomFieldContextUpdateDetails,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        field_id=field_id,
        context_id=context_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)
