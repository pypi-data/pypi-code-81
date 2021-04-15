from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.auto_complete_suggestions import AutoCompleteSuggestions
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    field_name: Union[Unset, str] = UNSET,
    field_value: Union[Unset, str] = UNSET,
    predicate_name: Union[Unset, str] = UNSET,
    predicate_value: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/jql/autocompletedata/suggestions".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "fieldName": field_name,
        "fieldValue": field_value,
        "predicateName": predicate_name,
        "predicateValue": predicate_value,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[AutoCompleteSuggestions, None]]:
    if response.status_code == 200:
        response_200 = AutoCompleteSuggestions.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[AutoCompleteSuggestions, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    field_name: Union[Unset, str] = UNSET,
    field_value: Union[Unset, str] = UNSET,
    predicate_name: Union[Unset, str] = UNSET,
    predicate_value: Union[Unset, str] = UNSET,
) -> Response[Union[AutoCompleteSuggestions, None]]:
    kwargs = _get_kwargs(
        client=client,
        field_name=field_name,
        field_value=field_value,
        predicate_name=predicate_name,
        predicate_value=predicate_value,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    field_name: Union[Unset, str] = UNSET,
    field_value: Union[Unset, str] = UNSET,
    predicate_name: Union[Unset, str] = UNSET,
    predicate_value: Union[Unset, str] = UNSET,
) -> Optional[Union[AutoCompleteSuggestions, None]]:
    """Returns the JQL search auto complete suggestions for a field.

    Suggestions can be obtained by providing:

     *  `fieldName` to get a list of all values for the field.
     *  `fieldName` and `fieldValue` to get a list of values containing the text in `fieldValue`.
     *  `fieldName` and `predicateName` to get a list of all predicate values for the field.
     *  `fieldName`, `predicateName`, and `predicateValue` to get a list of predicate values containing the text in `predicateValue`.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None."""

    return sync_detailed(
        client=client,
        field_name=field_name,
        field_value=field_value,
        predicate_name=predicate_name,
        predicate_value=predicate_value,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    field_name: Union[Unset, str] = UNSET,
    field_value: Union[Unset, str] = UNSET,
    predicate_name: Union[Unset, str] = UNSET,
    predicate_value: Union[Unset, str] = UNSET,
) -> Response[Union[AutoCompleteSuggestions, None]]:
    kwargs = _get_kwargs(
        client=client,
        field_name=field_name,
        field_value=field_value,
        predicate_name=predicate_name,
        predicate_value=predicate_value,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    field_name: Union[Unset, str] = UNSET,
    field_value: Union[Unset, str] = UNSET,
    predicate_name: Union[Unset, str] = UNSET,
    predicate_value: Union[Unset, str] = UNSET,
) -> Optional[Union[AutoCompleteSuggestions, None]]:
    """Returns the JQL search auto complete suggestions for a field.

    Suggestions can be obtained by providing:

     *  `fieldName` to get a list of all values for the field.
     *  `fieldName` and `fieldValue` to get a list of values containing the text in `fieldValue`.
     *  `fieldName` and `predicateName` to get a list of all predicate values for the field.
     *  `fieldName`, `predicateName`, and `predicateValue` to get a list of predicate values containing the text in `predicateValue`.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None."""

    return (
        await asyncio_detailed(
            client=client,
            field_name=field_name,
            field_value=field_value,
            predicate_name=predicate_name,
            predicate_value=predicate_value,
        )
    ).parsed
