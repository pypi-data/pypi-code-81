from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.converted_jql_queries import ConvertedJQLQueries
from ...models.jql_personal_data_migration_request import JQLPersonalDataMigrationRequest
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: JQLPersonalDataMigrationRequest,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/jql/pdcleaner".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[ConvertedJQLQueries, None]]:
    if response.status_code == 200:
        response_200 = ConvertedJQLQueries.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ConvertedJQLQueries, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: JQLPersonalDataMigrationRequest,
) -> Response[Union[ConvertedJQLQueries, None]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: JQLPersonalDataMigrationRequest,
) -> Optional[Union[ConvertedJQLQueries, None]]:
    """Converts one or more JQL queries with user identifiers (username or user key) to equivalent JQL queries with account IDs.

    You may wish to use this operation if your system stores JQL queries and you want to make them GDPR-compliant. For more information about GDPR-related changes, see the [migration guide](https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-privacy-api-migration-guide/).

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: JQLPersonalDataMigrationRequest,
) -> Response[Union[ConvertedJQLQueries, None]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: JQLPersonalDataMigrationRequest,
) -> Optional[Union[ConvertedJQLQueries, None]]:
    """Converts one or more JQL queries with user identifiers (username or user key) to equivalent JQL queries with account IDs.

    You may wish to use this operation if your system stores JQL queries and you want to make them GDPR-compliant. For more information about GDPR-related changes, see the [migration guide](https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-privacy-api-migration-guide/).

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
