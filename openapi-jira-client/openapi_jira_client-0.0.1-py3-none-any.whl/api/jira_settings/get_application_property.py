from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.application_property import ApplicationProperty
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    key: Union[Unset, str] = UNSET,
    permission_level: Union[Unset, str] = UNSET,
    key_filter: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/application-properties".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "key": key,
        "permissionLevel": permission_level,
        "keyFilter": key_filter,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[List[ApplicationProperty], None]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ApplicationProperty.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[List[ApplicationProperty], None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    key: Union[Unset, str] = UNSET,
    permission_level: Union[Unset, str] = UNSET,
    key_filter: Union[Unset, str] = UNSET,
) -> Response[Union[List[ApplicationProperty], None]]:
    kwargs = _get_kwargs(
        client=client,
        key=key,
        permission_level=permission_level,
        key_filter=key_filter,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    key: Union[Unset, str] = UNSET,
    permission_level: Union[Unset, str] = UNSET,
    key_filter: Union[Unset, str] = UNSET,
) -> Optional[Union[List[ApplicationProperty], None]]:
    """Returns all application properties or an application property.

    If you specify a value for the `key` parameter, then an application property is returned as an object (not in an array). Otherwise, an array of all editable application properties is returned. See [Set application property](#api-rest-api-3-application-properties-id-put) for descriptions of editable properties.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        key=key,
        permission_level=permission_level,
        key_filter=key_filter,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    key: Union[Unset, str] = UNSET,
    permission_level: Union[Unset, str] = UNSET,
    key_filter: Union[Unset, str] = UNSET,
) -> Response[Union[List[ApplicationProperty], None]]:
    kwargs = _get_kwargs(
        client=client,
        key=key,
        permission_level=permission_level,
        key_filter=key_filter,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    key: Union[Unset, str] = UNSET,
    permission_level: Union[Unset, str] = UNSET,
    key_filter: Union[Unset, str] = UNSET,
) -> Optional[Union[List[ApplicationProperty], None]]:
    """Returns all application properties or an application property.

    If you specify a value for the `key` parameter, then an application property is returned as an object (not in an array). Otherwise, an array of all editable application properties is returned. See [Set application property](#api-rest-api-3-application-properties-id-put) for descriptions of editable properties.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            key=key,
            permission_level=permission_level,
            key_filter=key_filter,
        )
    ).parsed
