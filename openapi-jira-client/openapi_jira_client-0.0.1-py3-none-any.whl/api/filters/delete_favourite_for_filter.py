from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.filter import Filter
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id_: int,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/filter/{id}/favourite".format(client.base_url, id=id_)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "expand": expand,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Filter, None]]:
    if response.status_code == 200:
        response_200 = Filter.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Filter, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    id_: int,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[Filter, None]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        expand=expand,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id_: int,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[Filter, None]]:
    """Removes a filter as a favorite for the user. Note that this operation only removes filters visible to the user from the user's favorites list. For example, if the user favorites a public filter that is subsequently made private (and is therefore no longer visible on their favorites list) they cannot remove it from their favorites list.

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return sync_detailed(
        client=client,
        id_=id_,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id_: int,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[Filter, None]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        expand=expand,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id_: int,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[Filter, None]]:
    """Removes a filter as a favorite for the user. Note that this operation only removes filters visible to the user from the user's favorites list. For example, if the user favorites a public filter that is subsequently made private (and is therefore no longer visible on their favorites list) they cannot remove it from their favorites list.

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return (
        await asyncio_detailed(
            client=client,
            id_=id_,
            expand=expand,
        )
    ).parsed
