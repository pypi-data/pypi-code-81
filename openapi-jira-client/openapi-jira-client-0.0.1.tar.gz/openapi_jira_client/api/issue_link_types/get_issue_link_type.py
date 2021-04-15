from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.issue_link_type import IssueLinkType
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_link_type_id: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issueLinkType/{issueLinkTypeId}".format(client.base_url, issueLinkTypeId=issue_link_type_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[IssueLinkType, None]]:
    if response.status_code == 200:
        response_200 = IssueLinkType.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[IssueLinkType, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    issue_link_type_id: str,
) -> Response[Union[IssueLinkType, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_link_type_id=issue_link_type_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    issue_link_type_id: str,
) -> Optional[Union[IssueLinkType, None]]:
    """Returns an issue link type.

    To use this operation, the site must have [issue linking](https://confluence.atlassian.com/x/yoXKM) enabled.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for a project in the site."""

    return sync_detailed(
        client=client,
        issue_link_type_id=issue_link_type_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_link_type_id: str,
) -> Response[Union[IssueLinkType, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_link_type_id=issue_link_type_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    issue_link_type_id: str,
) -> Optional[Union[IssueLinkType, None]]:
    """Returns an issue link type.

    To use this operation, the site must have [issue linking](https://confluence.atlassian.com/x/yoXKM) enabled.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for a project in the site."""

    return (
        await asyncio_detailed(
            client=client,
            issue_link_type_id=issue_link_type_id,
        )
    ).parsed
