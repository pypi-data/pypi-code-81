from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.issue_comment_list_request_bean import IssueCommentListRequestBean
from ...models.page_bean_comment import PageBeanComment
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: IssueCommentListRequestBean,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/comment/list".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, PageBeanComment]]:
    if response.status_code == 200:
        response_200 = PageBeanComment.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, PageBeanComment]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: IssueCommentListRequestBean,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[None, PageBeanComment]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        expand=expand,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: IssueCommentListRequestBean,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[None, PageBeanComment]]:
    """Returns a [paginated](#pagination) list of just the comments for a list of comments specified by comment IDs.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** Comments are returned where the user:

     *  has *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project containing the comment.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.
     *  If the comment has visibility restrictions, belongs to the group or has the role visibility is restricted to."""

    return sync_detailed(
        client=client,
        json_body=json_body,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: IssueCommentListRequestBean,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[None, PageBeanComment]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        expand=expand,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: IssueCommentListRequestBean,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[None, PageBeanComment]]:
    """Returns a [paginated](#pagination) list of just the comments for a list of comments specified by comment IDs.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** Comments are returned where the user:

     *  has *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project containing the comment.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.
     *  If the comment has visibility restrictions, belongs to the group or has the role visibility is restricted to."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            expand=expand,
        )
    ).parsed
