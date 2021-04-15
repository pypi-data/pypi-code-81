from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.issue_link import IssueLink
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    link_id: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issueLink/{linkId}".format(client.base_url, linkId=link_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[IssueLink, None]]:
    if response.status_code == 200:
        response_200 = IssueLink.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[IssueLink, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    link_id: str,
) -> Response[Union[IssueLink, None]]:
    kwargs = _get_kwargs(
        client=client,
        link_id=link_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    link_id: str,
) -> Optional[Union[IssueLink, None]]:
    """Returns an issue link.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse project* [project permission](https://confluence.atlassian.com/x/yodKLg) for all the projects containing the linked issues.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, permission to view both of the issues."""

    return sync_detailed(
        client=client,
        link_id=link_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    link_id: str,
) -> Response[Union[IssueLink, None]]:
    kwargs = _get_kwargs(
        client=client,
        link_id=link_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    link_id: str,
) -> Optional[Union[IssueLink, None]]:
    """Returns an issue link.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse project* [project permission](https://confluence.atlassian.com/x/yodKLg) for all the projects containing the linked issues.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, permission to view both of the issues."""

    return (
        await asyncio_detailed(
            client=client,
            link_id=link_id,
        )
    ).parsed
