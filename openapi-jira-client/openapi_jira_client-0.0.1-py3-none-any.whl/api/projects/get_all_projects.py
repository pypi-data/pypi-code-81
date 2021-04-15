from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.project import Project
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    expand: Union[Unset, str] = UNSET,
    recent: Union[Unset, int] = UNSET,
    properties: Union[Unset, List[str]] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/project".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_properties: Union[Unset, List[str]] = UNSET
    if not isinstance(properties, Unset):
        json_properties = properties

    params: Dict[str, Any] = {
        "expand": expand,
        "recent": recent,
        "properties": json_properties,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[List[Project], None]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Project.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[List[Project], None]]:
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
    recent: Union[Unset, int] = UNSET,
    properties: Union[Unset, List[str]] = UNSET,
) -> Response[Union[List[Project], None]]:
    kwargs = _get_kwargs(
        client=client,
        expand=expand,
        recent=recent,
        properties=properties,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    expand: Union[Unset, str] = UNSET,
    recent: Union[Unset, int] = UNSET,
    properties: Union[Unset, List[str]] = UNSET,
) -> Optional[Union[List[Project], None]]:
    """Returns all projects visible to the user. Deprecated, use [ Get projects paginated](#api-rest-api-3-project-search-get) that supports search and pagination.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** Projects are returned only where the user has *Browse Projects* or *Administer projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project."""

    return sync_detailed(
        client=client,
        expand=expand,
        recent=recent,
        properties=properties,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    expand: Union[Unset, str] = UNSET,
    recent: Union[Unset, int] = UNSET,
    properties: Union[Unset, List[str]] = UNSET,
) -> Response[Union[List[Project], None]]:
    kwargs = _get_kwargs(
        client=client,
        expand=expand,
        recent=recent,
        properties=properties,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    expand: Union[Unset, str] = UNSET,
    recent: Union[Unset, int] = UNSET,
    properties: Union[Unset, List[str]] = UNSET,
) -> Optional[Union[List[Project], None]]:
    """Returns all projects visible to the user. Deprecated, use [ Get projects paginated](#api-rest-api-3-project-search-get) that supports search and pagination.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** Projects are returned only where the user has *Browse Projects* or *Administer projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project."""

    return (
        await asyncio_detailed(
            client=client,
            expand=expand,
            recent=recent,
            properties=properties,
        )
    ).parsed
