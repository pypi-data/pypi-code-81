from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.screenable_field import ScreenableField
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    screen_id: int,
    tab_id: int,
    project_key: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/screens/{screenId}/tabs/{tabId}/fields".format(
        client.base_url, screenId=screen_id, tabId=tab_id
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "projectKey": project_key,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[List[ScreenableField], None]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ScreenableField.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
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


def _build_response(*, response: httpx.Response) -> Response[Union[List[ScreenableField], None]]:
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
    tab_id: int,
    project_key: Union[Unset, str] = UNSET,
) -> Response[Union[List[ScreenableField], None]]:
    kwargs = _get_kwargs(
        client=client,
        screen_id=screen_id,
        tab_id=tab_id,
        project_key=project_key,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    screen_id: int,
    tab_id: int,
    project_key: Union[Unset, str] = UNSET,
) -> Optional[Union[List[ScreenableField], None]]:
    """Returns all fields for a screen tab.

    **[Permissions](#permissions) required:**

     *  *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg).
     *  *Administer projects* [project permission](https://confluence.atlassian.com/x/yodKLg) when the project key is specified, providing that the screen is associated with the project through a Screen Scheme and Issue Type Screen Scheme."""

    return sync_detailed(
        client=client,
        screen_id=screen_id,
        tab_id=tab_id,
        project_key=project_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    screen_id: int,
    tab_id: int,
    project_key: Union[Unset, str] = UNSET,
) -> Response[Union[List[ScreenableField], None]]:
    kwargs = _get_kwargs(
        client=client,
        screen_id=screen_id,
        tab_id=tab_id,
        project_key=project_key,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    screen_id: int,
    tab_id: int,
    project_key: Union[Unset, str] = UNSET,
) -> Optional[Union[List[ScreenableField], None]]:
    """Returns all fields for a screen tab.

    **[Permissions](#permissions) required:**

     *  *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg).
     *  *Administer projects* [project permission](https://confluence.atlassian.com/x/yodKLg) when the project key is specified, providing that the screen is associated with the project through a Screen Scheme and Issue Type Screen Scheme."""

    return (
        await asyncio_detailed(
            client=client,
            screen_id=screen_id,
            tab_id=tab_id,
            project_key=project_key,
        )
    ).parsed
