from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.page_of_worklogs import PageOfWorklogs
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 1048576,
    started_after: Union[Unset, int] = UNSET,
    expand: Union[Unset, str] = "",
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}/worklog".format(client.base_url, issueIdOrKey=issue_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "startAt": start_at,
        "maxResults": max_results,
        "startedAfter": started_after,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, PageOfWorklogs]]:
    if response.status_code == 200:
        response_200 = PageOfWorklogs.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, PageOfWorklogs]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 1048576,
    started_after: Union[Unset, int] = UNSET,
    expand: Union[Unset, str] = "",
) -> Response[Union[None, PageOfWorklogs]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        start_at=start_at,
        max_results=max_results,
        started_after=started_after,
        expand=expand,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 1048576,
    started_after: Union[Unset, int] = UNSET,
    expand: Union[Unset, str] = "",
) -> Optional[Union[None, PageOfWorklogs]]:
    """Returns worklogs for an issue, starting from the oldest worklog or from the worklog started on or after a date and time.

    Time tracking must be enabled in Jira, otherwise this operation returns an error. For more information, see [Configuring time tracking](https://confluence.atlassian.com/x/qoXKM).

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** Workloads are only returned where the user has:

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.
     *  If the worklog has visibility restrictions, belongs to the group or has the role visibility is restricted to."""

    return sync_detailed(
        client=client,
        issue_id_or_key=issue_id_or_key,
        start_at=start_at,
        max_results=max_results,
        started_after=started_after,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 1048576,
    started_after: Union[Unset, int] = UNSET,
    expand: Union[Unset, str] = "",
) -> Response[Union[None, PageOfWorklogs]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        start_at=start_at,
        max_results=max_results,
        started_after=started_after,
        expand=expand,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 1048576,
    started_after: Union[Unset, int] = UNSET,
    expand: Union[Unset, str] = "",
) -> Optional[Union[None, PageOfWorklogs]]:
    """Returns worklogs for an issue, starting from the oldest worklog or from the worklog started on or after a date and time.

    Time tracking must be enabled in Jira, otherwise this operation returns an error. For more information, see [Configuring time tracking](https://confluence.atlassian.com/x/qoXKM).

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** Workloads are only returned where the user has:

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.
     *  If the worklog has visibility restrictions, belongs to the group or has the role visibility is restricted to."""

    return (
        await asyncio_detailed(
            client=client,
            issue_id_or_key=issue_id_or_key,
            start_at=start_at,
            max_results=max_results,
            started_after=started_after,
            expand=expand,
        )
    ).parsed
