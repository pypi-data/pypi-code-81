from typing import Any, Dict, Union

import httpx

from ...client import AuthenticatedClient
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    property_key: str,
    json_body: None,
    account_id: Union[Unset, str] = UNSET,
    user_key: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/user/properties/{propertyKey}".format(client.base_url, propertyKey=property_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "accountId": account_id,
        "userKey": user_key,
        "username": username,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = None

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _build_response(*, response: httpx.Response) -> Response[None]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    property_key: str,
    json_body: None,
    account_id: Union[Unset, str] = UNSET,
    user_key: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        property_key=property_key,
        json_body=json_body,
        account_id=account_id,
        user_key=user_key,
        username=username,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    property_key: str,
    json_body: None,
    account_id: Union[Unset, str] = UNSET,
    user_key: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        property_key=property_key,
        json_body=json_body,
        account_id=account_id,
        user_key=user_key,
        username=username,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)
