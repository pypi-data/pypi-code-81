from typing import Any, Dict

import httpx

from ...client import AuthenticatedClient
from ...models.delete_and_replace_version_bean import DeleteAndReplaceVersionBean
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id_: str,
    json_body: DeleteAndReplaceVersionBean,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/version/{id}/removeAndSwap".format(client.base_url, id=id_)

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
    id_: str,
    json_body: DeleteAndReplaceVersionBean,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id_: str,
    json_body: DeleteAndReplaceVersionBean,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)
