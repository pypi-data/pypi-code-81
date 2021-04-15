from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.user import User
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    account_id: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    key: Union[Unset, str] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/user".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "accountId": account_id,
        "username": username,
        "key": key,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, User]]:
    if response.status_code == 200:
        response_200 = User.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[None, User]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    account_id: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    key: Union[Unset, str] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[None, User]]:
    kwargs = _get_kwargs(
        client=client,
        account_id=account_id,
        username=username,
        key=key,
        expand=expand,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    account_id: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    key: Union[Unset, str] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[None, User]]:
    """Returns a user.

    **[Permissions](#permissions) required:** *Browse users and groups* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        account_id=account_id,
        username=username,
        key=key,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    account_id: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    key: Union[Unset, str] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[None, User]]:
    kwargs = _get_kwargs(
        client=client,
        account_id=account_id,
        username=username,
        key=key,
        expand=expand,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    account_id: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    key: Union[Unset, str] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[None, User]]:
    """Returns a user.

    **[Permissions](#permissions) required:** *Browse users and groups* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            account_id=account_id,
            username=username,
            key=key,
            expand=expand,
        )
    ).parsed
