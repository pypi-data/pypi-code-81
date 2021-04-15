from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.default_share_scope import DefaultShareScope
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: DefaultShareScope,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/filter/defaultShareScope".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[DefaultShareScope, None]]:
    if response.status_code == 200:
        response_200 = DefaultShareScope.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[DefaultShareScope, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: DefaultShareScope,
) -> Response[Union[DefaultShareScope, None]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: DefaultShareScope,
) -> Optional[Union[DefaultShareScope, None]]:
    """Sets the default sharing for new filters and dashboards for a user.

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: DefaultShareScope,
) -> Response[Union[DefaultShareScope, None]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: DefaultShareScope,
) -> Optional[Union[DefaultShareScope, None]]:
    """Sets the default sharing for new filters and dashboards for a user.

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
