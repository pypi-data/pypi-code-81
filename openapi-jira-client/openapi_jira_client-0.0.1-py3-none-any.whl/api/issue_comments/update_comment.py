from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.comment import Comment
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    id_: str,
    json_body: Comment,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}/comment/{id}".format(
        client.base_url, issueIdOrKey=issue_id_or_key, id=id_
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "expand": expand,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Comment, None]]:
    if response.status_code == 200:
        response_200 = Comment.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[Comment, None]]:
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
    id_: str,
    json_body: Comment,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[Comment, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        id_=id_,
        json_body=json_body,
        expand=expand,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    id_: str,
    json_body: Comment,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[Comment, None]]:
    """Updates a comment.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue containing the comment is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.
     *  *Edit all comments*[ project permission](https://confluence.atlassian.com/x/yodKLg) to update any comment or *Edit own comments* to update comment created by the user.
     *  If the comment has visibility restrictions, the user belongs to the group or has the role visibility is restricted to."""

    return sync_detailed(
        client=client,
        issue_id_or_key=issue_id_or_key,
        id_=id_,
        json_body=json_body,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    id_: str,
    json_body: Comment,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[Comment, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        id_=id_,
        json_body=json_body,
        expand=expand,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    id_: str,
    json_body: Comment,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[Comment, None]]:
    """Updates a comment.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue containing the comment is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.
     *  *Edit all comments*[ project permission](https://confluence.atlassian.com/x/yodKLg) to update any comment or *Edit own comments* to update comment created by the user.
     *  If the comment has visibility restrictions, the user belongs to the group or has the role visibility is restricted to."""

    return (
        await asyncio_detailed(
            client=client,
            issue_id_or_key=issue_id_or_key,
            id_=id_,
            json_body=json_body,
            expand=expand,
        )
    ).parsed
