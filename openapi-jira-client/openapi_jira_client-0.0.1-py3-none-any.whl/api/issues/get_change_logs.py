from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.page_bean_changelog import PageBeanChangelog
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 100,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}/changelog".format(client.base_url, issueIdOrKey=issue_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "startAt": start_at,
        "maxResults": max_results,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, PageBeanChangelog]]:
    if response.status_code == 200:
        response_200 = PageBeanChangelog.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, PageBeanChangelog]]:
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
    max_results: Union[Unset, int] = 100,
) -> Response[Union[None, PageBeanChangelog]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        start_at=start_at,
        max_results=max_results,
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
    max_results: Union[Unset, int] = 100,
) -> Optional[Union[None, PageBeanChangelog]]:
    """Returns a [paginated](#pagination) list of all changelogs for an issue sorted by date, starting from the oldest.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return sync_detailed(
        client=client,
        issue_id_or_key=issue_id_or_key,
        start_at=start_at,
        max_results=max_results,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 100,
) -> Response[Union[None, PageBeanChangelog]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        start_at=start_at,
        max_results=max_results,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 100,
) -> Optional[Union[None, PageBeanChangelog]]:
    """Returns a [paginated](#pagination) list of all changelogs for an issue sorted by date, starting from the oldest.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return (
        await asyncio_detailed(
            client=client,
            issue_id_or_key=issue_id_or_key,
            start_at=start_at,
            max_results=max_results,
        )
    ).parsed
