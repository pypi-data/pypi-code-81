from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.error_collection import ErrorCollection
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    key: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/projectvalidate/key".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "key": key,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[ErrorCollection, None]]:
    if response.status_code == 200:
        response_200 = ErrorCollection.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ErrorCollection, None]]:
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
) -> Response[Union[ErrorCollection, None]]:
    kwargs = _get_kwargs(
        client=client,
        key=key,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    key: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorCollection, None]]:
    """Validates a project key by confirming the key is a valid string and not in use.

    **[Permissions](#permissions) required:** None."""

    return sync_detailed(
        client=client,
        key=key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    key: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorCollection, None]]:
    kwargs = _get_kwargs(
        client=client,
        key=key,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    key: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorCollection, None]]:
    """Validates a project key by confirming the key is a valid string and not in use.

    **[Permissions](#permissions) required:** None."""

    return (
        await asyncio_detailed(
            client=client,
            key=key,
        )
    ).parsed
