from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.error_collection import ErrorCollection
from ...models.jql_queries_to_parse import JqlQueriesToParse
from ...models.parse_jql_queries_validation import ParseJqlQueriesValidation
from ...models.parsed_jql_queries import ParsedJqlQueries
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: JqlQueriesToParse,
    validation: Union[Unset, ParseJqlQueriesValidation] = ParseJqlQueriesValidation.STRICT,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/jql/parse".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_validation: Union[Unset, str] = UNSET
    if not isinstance(validation, Unset):
        json_validation = validation.value

    params: Dict[str, Any] = {
        "validation": json_validation,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[ErrorCollection, None, ParsedJqlQueries]]:
    if response.status_code == 200:
        response_200 = ParsedJqlQueries.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorCollection.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ErrorCollection, None, ParsedJqlQueries]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: JqlQueriesToParse,
    validation: Union[Unset, ParseJqlQueriesValidation] = ParseJqlQueriesValidation.STRICT,
) -> Response[Union[ErrorCollection, None, ParsedJqlQueries]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        validation=validation,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: JqlQueriesToParse,
    validation: Union[Unset, ParseJqlQueriesValidation] = ParseJqlQueriesValidation.STRICT,
) -> Optional[Union[ErrorCollection, None, ParsedJqlQueries]]:
    """Parses and validates JQL queries.

    Validation is performed in context of the current user.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None."""

    return sync_detailed(
        client=client,
        json_body=json_body,
        validation=validation,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: JqlQueriesToParse,
    validation: Union[Unset, ParseJqlQueriesValidation] = ParseJqlQueriesValidation.STRICT,
) -> Response[Union[ErrorCollection, None, ParsedJqlQueries]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        validation=validation,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: JqlQueriesToParse,
    validation: Union[Unset, ParseJqlQueriesValidation] = ParseJqlQueriesValidation.STRICT,
) -> Optional[Union[ErrorCollection, None, ParsedJqlQueries]]:
    """Parses and validates JQL queries.

    Validation is performed in context of the current user.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            validation=validation,
        )
    ).parsed
