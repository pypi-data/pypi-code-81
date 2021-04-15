from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.unrestricted_user_email import UnrestrictedUserEmail
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    account_id: List[str],
) -> Dict[str, Any]:
    url = "{}/rest/api/3/user/email/bulk".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_account_id = account_id

    params: Dict[str, Any] = {
        "accountId": json_account_id,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, UnrestrictedUserEmail]]:
    if response.status_code == 200:
        response_200 = UnrestrictedUserEmail.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 503:
        response_503 = None

        return response_503
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, UnrestrictedUserEmail]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    account_id: List[str],
) -> Response[Union[None, UnrestrictedUserEmail]]:
    kwargs = _get_kwargs(
        client=client,
        account_id=account_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    account_id: List[str],
) -> Optional[Union[None, UnrestrictedUserEmail]]:
    """ Returns a user's email address. This API is only available to apps approved by Atlassian, according to these [guidelines](https://community.developer.atlassian.com/t/guidelines-for-requesting-access-to-email-address/27603). """

    return sync_detailed(
        client=client,
        account_id=account_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    account_id: List[str],
) -> Response[Union[None, UnrestrictedUserEmail]]:
    kwargs = _get_kwargs(
        client=client,
        account_id=account_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    account_id: List[str],
) -> Optional[Union[None, UnrestrictedUserEmail]]:
    """ Returns a user's email address. This API is only available to apps approved by Atlassian, according to these [guidelines](https://community.developer.atlassian.com/t/guidelines-for-requesting-access-to-email-address/27603). """

    return (
        await asyncio_detailed(
            client=client,
            account_id=account_id,
        )
    ).parsed
