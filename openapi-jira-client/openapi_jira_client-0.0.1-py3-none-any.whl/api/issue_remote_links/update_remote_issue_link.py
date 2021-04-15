from typing import Any, Dict

import httpx

from ...client import AuthenticatedClient
from ...models.remote_issue_link_request import RemoteIssueLinkRequest
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    link_id: str,
    json_body: RemoteIssueLinkRequest,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}/remotelink/{linkId}".format(
        client.base_url, issueIdOrKey=issue_id_or_key, linkId=link_id
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
    issue_id_or_key: str,
    link_id: str,
    json_body: RemoteIssueLinkRequest,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        link_id=link_id,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    link_id: str,
    json_body: RemoteIssueLinkRequest,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        link_id=link_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)
