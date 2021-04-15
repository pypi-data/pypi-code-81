from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.get_comments_order_by import GetCommentsOrderBy
from ...models.page_of_comments import PageOfComments
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    order_by: Union[Unset, GetCommentsOrderBy] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}/comment".format(client.base_url, issueIdOrKey=issue_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_order_by: Union[Unset, str] = UNSET
    if not isinstance(order_by, Unset):
        json_order_by = order_by.value

    params: Dict[str, Any] = {
        "startAt": start_at,
        "maxResults": max_results,
        "orderBy": json_order_by,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, PageOfComments]]:
    if response.status_code == 200:
        response_200 = PageOfComments.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, PageOfComments]]:
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
    max_results: Union[Unset, int] = 50,
    order_by: Union[Unset, GetCommentsOrderBy] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[None, PageOfComments]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        start_at=start_at,
        max_results=max_results,
        order_by=order_by,
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
    max_results: Union[Unset, int] = 50,
    order_by: Union[Unset, GetCommentsOrderBy] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[None, PageOfComments]]:
    """Returns all comments for an issue.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** Comments are included in the response where the user has:

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project containing the comment.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.
     *  If the comment has visibility restrictions, belongs to the group or has the role visibility is role visibility is restricted to."""

    return sync_detailed(
        client=client,
        issue_id_or_key=issue_id_or_key,
        start_at=start_at,
        max_results=max_results,
        order_by=order_by,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    order_by: Union[Unset, GetCommentsOrderBy] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[None, PageOfComments]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        start_at=start_at,
        max_results=max_results,
        order_by=order_by,
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
    max_results: Union[Unset, int] = 50,
    order_by: Union[Unset, GetCommentsOrderBy] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[None, PageOfComments]]:
    """Returns all comments for an issue.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** Comments are included in the response where the user has:

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project containing the comment.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.
     *  If the comment has visibility restrictions, belongs to the group or has the role visibility is role visibility is restricted to."""

    return (
        await asyncio_detailed(
            client=client,
            issue_id_or_key=issue_id_or_key,
            start_at=start_at,
            max_results=max_results,
            order_by=order_by,
            expand=expand,
        )
    ).parsed
