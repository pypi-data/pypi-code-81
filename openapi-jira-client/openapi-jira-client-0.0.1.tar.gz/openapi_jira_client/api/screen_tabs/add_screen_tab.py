from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.screenable_tab import ScreenableTab
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    screen_id: int,
    json_body: ScreenableTab,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/screens/{screenId}/tabs".format(client.base_url, screenId=screen_id)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, ScreenableTab]]:
    if response.status_code == 200:
        response_200 = ScreenableTab.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, ScreenableTab]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    screen_id: int,
    json_body: ScreenableTab,
) -> Response[Union[None, ScreenableTab]]:
    kwargs = _get_kwargs(
        client=client,
        screen_id=screen_id,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    screen_id: int,
    json_body: ScreenableTab,
) -> Optional[Union[None, ScreenableTab]]:
    """Creates a tab for a screen.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        screen_id=screen_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    screen_id: int,
    json_body: ScreenableTab,
) -> Response[Union[None, ScreenableTab]]:
    kwargs = _get_kwargs(
        client=client,
        screen_id=screen_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    screen_id: int,
    json_body: ScreenableTab,
) -> Optional[Union[None, ScreenableTab]]:
    """Creates a tab for a screen.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            screen_id=screen_id,
            json_body=json_body,
        )
    ).parsed
