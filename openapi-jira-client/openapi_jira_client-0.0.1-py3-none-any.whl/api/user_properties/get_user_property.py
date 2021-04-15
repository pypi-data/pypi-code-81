from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.entity_property import EntityProperty
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    property_key: str,
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

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[EntityProperty, None]]:
    if response.status_code == 200:
        response_200 = EntityProperty.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
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


def _build_response(*, response: httpx.Response) -> Response[Union[EntityProperty, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    property_key: str,
    account_id: Union[Unset, str] = UNSET,
    user_key: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[Union[EntityProperty, None]]:
    kwargs = _get_kwargs(
        client=client,
        property_key=property_key,
        account_id=account_id,
        user_key=user_key,
        username=username,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    property_key: str,
    account_id: Union[Unset, str] = UNSET,
    user_key: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Optional[Union[EntityProperty, None]]:
    """Returns the value of a user's property. If no property key is provided [Get user property keys](#api-rest-api-3-user-properties-get) is called.

    Note: This operation does not access the [user properties](https://confluence.atlassian.com/x/8YxjL) created and maintained in Jira.

    **[Permissions](#permissions) required:**

     *  *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg), to get a property from any user.
     *  Access to Jira, to get a property from the calling user's record."""

    return sync_detailed(
        client=client,
        property_key=property_key,
        account_id=account_id,
        user_key=user_key,
        username=username,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    property_key: str,
    account_id: Union[Unset, str] = UNSET,
    user_key: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[Union[EntityProperty, None]]:
    kwargs = _get_kwargs(
        client=client,
        property_key=property_key,
        account_id=account_id,
        user_key=user_key,
        username=username,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    property_key: str,
    account_id: Union[Unset, str] = UNSET,
    user_key: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Optional[Union[EntityProperty, None]]:
    """Returns the value of a user's property. If no property key is provided [Get user property keys](#api-rest-api-3-user-properties-get) is called.

    Note: This operation does not access the [user properties](https://confluence.atlassian.com/x/8YxjL) created and maintained in Jira.

    **[Permissions](#permissions) required:**

     *  *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg), to get a property from any user.
     *  Access to Jira, to get a property from the calling user's record."""

    return (
        await asyncio_detailed(
            client=client,
            property_key=property_key,
            account_id=account_id,
            user_key=user_key,
            username=username,
        )
    ).parsed
