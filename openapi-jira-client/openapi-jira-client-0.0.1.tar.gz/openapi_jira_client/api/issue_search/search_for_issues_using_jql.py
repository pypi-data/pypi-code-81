from typing import Any, Dict, List, Union

import httpx

from ...client import AuthenticatedClient
from ...models.search_for_issues_using_jql_validate_query import SearchForIssuesUsingJqlValidateQuery
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    jql: Union[Unset, str] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    validate_query: Union[Unset, SearchForIssuesUsingJqlValidateQuery] = SearchForIssuesUsingJqlValidateQuery.STRICT,
    fields: Union[Unset, List[str]] = UNSET,
    expand: Union[Unset, str] = UNSET,
    properties: Union[Unset, List[str]] = UNSET,
    fields_by_keys: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/search".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_validate_query: Union[Unset, str] = UNSET
    if not isinstance(validate_query, Unset):
        json_validate_query = validate_query.value

    json_fields: Union[Unset, List[str]] = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    json_properties: Union[Unset, List[str]] = UNSET
    if not isinstance(properties, Unset):
        json_properties = properties

    params: Dict[str, Any] = {
        "jql": jql,
        "startAt": start_at,
        "maxResults": max_results,
        "validateQuery": json_validate_query,
        "fields": json_fields,
        "expand": expand,
        "properties": json_properties,
        "fieldsByKeys": fields_by_keys,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
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
    jql: Union[Unset, str] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    validate_query: Union[Unset, SearchForIssuesUsingJqlValidateQuery] = SearchForIssuesUsingJqlValidateQuery.STRICT,
    fields: Union[Unset, List[str]] = UNSET,
    expand: Union[Unset, str] = UNSET,
    properties: Union[Unset, List[str]] = UNSET,
    fields_by_keys: Union[Unset, bool] = False,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        jql=jql,
        start_at=start_at,
        max_results=max_results,
        validate_query=validate_query,
        fields=fields,
        expand=expand,
        properties=properties,
        fields_by_keys=fields_by_keys,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    jql: Union[Unset, str] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    validate_query: Union[Unset, SearchForIssuesUsingJqlValidateQuery] = SearchForIssuesUsingJqlValidateQuery.STRICT,
    fields: Union[Unset, List[str]] = UNSET,
    expand: Union[Unset, str] = UNSET,
    properties: Union[Unset, List[str]] = UNSET,
    fields_by_keys: Union[Unset, bool] = False,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        jql=jql,
        start_at=start_at,
        max_results=max_results,
        validate_query=validate_query,
        fields=fields,
        expand=expand,
        properties=properties,
        fields_by_keys=fields_by_keys,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)
