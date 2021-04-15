from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.property_keys import PropertyKeys
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    comment_id: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/comment/{commentId}/properties".format(client.base_url, commentId=comment_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, PropertyKeys]]:
    if response.status_code == 200:
        response_200 = PropertyKeys.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, PropertyKeys]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    comment_id: str,
) -> Response[Union[None, PropertyKeys]]:
    kwargs = _get_kwargs(
        client=client,
        comment_id=comment_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    comment_id: str,
) -> Optional[Union[None, PropertyKeys]]:
    """Returns the keys of all the properties of a comment.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.
     *  If the comment has visibility restrictions, belongs to the group or has the role visibility is restricted to."""

    return sync_detailed(
        client=client,
        comment_id=comment_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    comment_id: str,
) -> Response[Union[None, PropertyKeys]]:
    kwargs = _get_kwargs(
        client=client,
        comment_id=comment_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    comment_id: str,
) -> Optional[Union[None, PropertyKeys]]:
    """Returns the keys of all the properties of a comment.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.
     *  If the comment has visibility restrictions, belongs to the group or has the role visibility is restricted to."""

    return (
        await asyncio_detailed(
            client=client,
            comment_id=comment_id,
        )
    ).parsed
