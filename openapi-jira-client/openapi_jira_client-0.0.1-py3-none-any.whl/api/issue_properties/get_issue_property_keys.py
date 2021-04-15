from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.property_keys import PropertyKeys
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}/properties".format(client.base_url, issueIdOrKey=issue_id_or_key)

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
    issue_id_or_key: str,
) -> Response[Union[None, PropertyKeys]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
) -> Optional[Union[None, PropertyKeys]]:
    """Returns the URLs and keys of an issue's properties.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** Property details are only returned where the user has:

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project containing the issue.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return sync_detailed(
        client=client,
        issue_id_or_key=issue_id_or_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
) -> Response[Union[None, PropertyKeys]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
) -> Optional[Union[None, PropertyKeys]]:
    """Returns the URLs and keys of an issue's properties.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** Property details are only returned where the user has:

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project containing the issue.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return (
        await asyncio_detailed(
            client=client,
            issue_id_or_key=issue_id_or_key,
        )
    ).parsed
