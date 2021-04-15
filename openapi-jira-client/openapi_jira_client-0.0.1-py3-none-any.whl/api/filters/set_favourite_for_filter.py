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

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id_: int,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[Filter, None]]:
    """Add a filter as a favorite for the user.

    **[Permissions](#permissions) required:** Permission to access Jira, however, the user can only favorite:

     *  filters owned by the user.
     *  filters shared with a group that the user is a member of.
     *  filters shared with a private project that the user has *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for.
     *  filters shared with a public project.
     *  filters shared with the public."""

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
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id_: int,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[Filter, None]]:
    """Add a filter as a favorite for the user.

    **[Permissions](#permissions) required:** Permission to access Jira, however, the user can only favorite:

     *  filters owned by the user.
     *  filters shared with a group that the user is a member of.
     *  filters shared with a private project that the user has *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for.
     *  filters shared with a public project.
     *  filters shared with the public."""

    return (
        await asyncio_detailed(
            client=client,
            id_=id_,
            expand=expand,
        )
    ).parsed
