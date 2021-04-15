from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.filter import Filter
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    expand: Union[Unset, str] = UNSET,
    include_favourites: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/filter/my".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "expand": expand,
        "includeFavourites": include_favourites,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[List[Filter], None]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Filter.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[List[Filter], None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    expand: Union[Unset, str] = UNSET,
    include_favourites: Union[Unset, bool] = False,
) -> Response[Union[List[Filter], None]]:
    kwargs = _get_kwargs(
        client=client,
        expand=expand,
        include_favourites=include_favourites,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    expand: Union[Unset, str] = UNSET,
    include_favourites: Union[Unset, bool] = False,
) -> Optional[Union[List[Filter], None]]:
    """Returns the filters owned by the user. If `includeFavourites` is `true`, the user's visible favorite filters are also returned.

    **[Permissions](#permissions) required:** Permission to access Jira, however, a favorite filters is only visible to the user where the filter is:

     *  owned by the user.
     *  shared with a group that the user is a member of.
     *  shared with a private project that the user has *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for.
     *  shared with a public project.
     *  shared with the public.

    For example, if the user favorites a public filter that is subsequently made private that filter is not returned by this operation."""

    return sync_detailed(
        client=client,
        expand=expand,
        include_favourites=include_favourites,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    expand: Union[Unset, str] = UNSET,
    include_favourites: Union[Unset, bool] = False,
) -> Response[Union[List[Filter], None]]:
    kwargs = _get_kwargs(
        client=client,
        expand=expand,
        include_favourites=include_favourites,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    expand: Union[Unset, str] = UNSET,
    include_favourites: Union[Unset, bool] = False,
) -> Optional[Union[List[Filter], None]]:
    """Returns the filters owned by the user. If `includeFavourites` is `true`, the user's visible favorite filters are also returned.

    **[Permissions](#permissions) required:** Permission to access Jira, however, a favorite filters is only visible to the user where the filter is:

     *  owned by the user.
     *  shared with a group that the user is a member of.
     *  shared with a private project that the user has *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for.
     *  shared with a public project.
     *  shared with the public.

    For example, if the user favorites a public filter that is subsequently made private that filter is not returned by this operation."""

    return (
        await asyncio_detailed(
            client=client,
            expand=expand,
            include_favourites=include_favourites,
        )
    ).parsed
