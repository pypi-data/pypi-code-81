from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.worklog import Worklog
from ...models.worklog_ids_request_bean import WorklogIdsRequestBean
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: WorklogIdsRequestBean,
    expand: Union[Unset, str] = "",
) -> Dict[str, Any]:
    url = "{}/rest/api/3/worklog/list".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[List[Worklog], None]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Worklog.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[List[Worklog], None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: WorklogIdsRequestBean,
    expand: Union[Unset, str] = "",
) -> Response[Union[List[Worklog], None]]:
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
    json_body: WorklogIdsRequestBean,
    expand: Union[Unset, str] = "",
) -> Optional[Union[List[Worklog], None]]:
    """Returns worklog details for a list of worklog IDs.

    The returned list of worklogs is limited to 1000 items.

    **[Permissions](#permissions) required:** Permission to access Jira, however, worklogs are only returned where either of the following is true:

     *  the worklog is set as *Viewable by All Users*.
     *  the user is a member of a project role or group with permission to view the worklog."""

    return sync_detailed(
        client=client,
        json_body=json_body,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: WorklogIdsRequestBean,
    expand: Union[Unset, str] = "",
) -> Response[Union[List[Worklog], None]]:
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
    json_body: WorklogIdsRequestBean,
    expand: Union[Unset, str] = "",
) -> Optional[Union[List[Worklog], None]]:
    """Returns worklog details for a list of worklog IDs.

    The returned list of worklogs is limited to 1000 items.

    **[Permissions](#permissions) required:** Permission to access Jira, however, worklogs are only returned where either of the following is true:

     *  the worklog is set as *Viewable by All Users*.
     *  the user is a member of a project role or group with permission to view the worklog."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            expand=expand,
        )
    ).parsed
