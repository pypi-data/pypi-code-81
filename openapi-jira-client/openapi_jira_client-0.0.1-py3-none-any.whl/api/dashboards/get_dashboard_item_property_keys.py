from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.property_keys import PropertyKeys
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    dashboard_id: str,
    item_id: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/dashboard/{dashboardId}/items/{itemId}/properties".format(
        client.base_url, dashboardId=dashboard_id, itemId=item_id
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, PropertyKeys]]:
    if response.status_code == 200:
        response_200 = PropertyKeys.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, PropertyKeys]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    dashboard_id: str,
    item_id: str,
) -> Response[Union[None, PropertyKeys]]:
    kwargs = _get_kwargs(
        client=client,
        dashboard_id=dashboard_id,
        item_id=item_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    dashboard_id: str,
    item_id: str,
) -> Optional[Union[None, PropertyKeys]]:
    """Returns the keys of all properties for a dashboard item.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** The user must be the owner of the dashboard or be shared the dashboard. Note, users with the *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg) are considered owners of the System dashboard. The System dashboard is considered to be shared with all other users."""

    return sync_detailed(
        client=client,
        dashboard_id=dashboard_id,
        item_id=item_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    dashboard_id: str,
    item_id: str,
) -> Response[Union[None, PropertyKeys]]:
    kwargs = _get_kwargs(
        client=client,
        dashboard_id=dashboard_id,
        item_id=item_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    dashboard_id: str,
    item_id: str,
) -> Optional[Union[None, PropertyKeys]]:
    """Returns the keys of all properties for a dashboard item.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** The user must be the owner of the dashboard or be shared the dashboard. Note, users with the *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg) are considered owners of the System dashboard. The System dashboard is considered to be shared with all other users."""

    return (
        await asyncio_detailed(
            client=client,
            dashboard_id=dashboard_id,
            item_id=item_id,
        )
    ).parsed
