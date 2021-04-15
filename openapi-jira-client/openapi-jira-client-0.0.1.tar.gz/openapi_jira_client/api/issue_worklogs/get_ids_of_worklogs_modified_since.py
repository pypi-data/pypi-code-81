from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.changed_worklogs import ChangedWorklogs
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    since: Union[Unset, int] = 0,
    expand: Union[Unset, str] = "",
) -> Dict[str, Any]:
    url = "{}/rest/api/3/worklog/updated".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "since": since,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[ChangedWorklogs, None]]:
    if response.status_code == 200:
        response_200 = ChangedWorklogs.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ChangedWorklogs, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    since: Union[Unset, int] = 0,
    expand: Union[Unset, str] = "",
) -> Response[Union[ChangedWorklogs, None]]:
    kwargs = _get_kwargs(
        client=client,
        since=since,
        expand=expand,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    since: Union[Unset, int] = 0,
    expand: Union[Unset, str] = "",
) -> Optional[Union[ChangedWorklogs, None]]:
    """Returns a list of IDs and update timestamps for worklogs updated after a date and time.

    This resource is paginated, with a limit of 1000 worklogs per page. Each page lists worklogs from oldest to youngest. If the number of items in the date range exceeds 1000, `until` indicates the timestamp of the youngest item on the page. Also, `nextPage` provides the URL for the next page of worklogs. The `lastPage` parameter is set to true on the last page of worklogs.

    This resource does not return worklogs updated during the minute preceding the request.

    **[Permissions](#permissions) required:** Permission to access Jira, however, worklogs are only returned where either of the following is true:

     *  the worklog is set as *Viewable by All Users*.
     *  the user is a member of a project role or group with permission to view the worklog."""

    return sync_detailed(
        client=client,
        since=since,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    since: Union[Unset, int] = 0,
    expand: Union[Unset, str] = "",
) -> Response[Union[ChangedWorklogs, None]]:
    kwargs = _get_kwargs(
        client=client,
        since=since,
        expand=expand,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    since: Union[Unset, int] = 0,
    expand: Union[Unset, str] = "",
) -> Optional[Union[ChangedWorklogs, None]]:
    """Returns a list of IDs and update timestamps for worklogs updated after a date and time.

    This resource is paginated, with a limit of 1000 worklogs per page. Each page lists worklogs from oldest to youngest. If the number of items in the date range exceeds 1000, `until` indicates the timestamp of the youngest item on the page. Also, `nextPage` provides the URL for the next page of worklogs. The `lastPage` parameter is set to true on the last page of worklogs.

    This resource does not return worklogs updated during the minute preceding the request.

    **[Permissions](#permissions) required:** Permission to access Jira, however, worklogs are only returned where either of the following is true:

     *  the worklog is set as *Viewable by All Users*.
     *  the user is a member of a project role or group with permission to view the worklog."""

    return (
        await asyncio_detailed(
            client=client,
            since=since,
            expand=expand,
        )
    ).parsed
