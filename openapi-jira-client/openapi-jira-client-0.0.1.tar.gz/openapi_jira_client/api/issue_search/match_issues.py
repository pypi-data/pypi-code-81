from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.issue_matches import IssueMatches
from ...models.issues_and_jql_queries import IssuesAndJQLQueries
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: IssuesAndJQLQueries,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/jql/match".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[IssueMatches, None]]:
    if response.status_code == 200:
        response_200 = IssueMatches.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[IssueMatches, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: IssuesAndJQLQueries,
) -> Response[Union[IssueMatches, None]]:
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
    json_body: IssuesAndJQLQueries,
) -> Optional[Union[IssueMatches, None]]:
    """Checks whether one or more issues would be returned by one or more JQL queries.

    **[Permissions](#permissions) required:** None, however, issues are only matched against JQL queries where the user has:

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: IssuesAndJQLQueries,
) -> Response[Union[IssueMatches, None]]:
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
    json_body: IssuesAndJQLQueries,
) -> Optional[Union[IssueMatches, None]]:
    """Checks whether one or more issues would be returned by one or more JQL queries.

    **[Permissions](#permissions) required:** None, however, issues are only matched against JQL queries where the user has:

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
