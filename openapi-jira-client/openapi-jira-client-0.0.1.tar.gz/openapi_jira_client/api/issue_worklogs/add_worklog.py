from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.add_worklog_adjust_estimate import AddWorklogAdjustEstimate
from ...models.worklog import Worklog
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    json_body: Worklog,
    notify_users: Union[Unset, bool] = True,
    adjust_estimate: Union[Unset, AddWorklogAdjustEstimate] = AddWorklogAdjustEstimate.AUTO,
    new_estimate: Union[Unset, str] = UNSET,
    reduce_by: Union[Unset, str] = UNSET,
    expand: Union[Unset, str] = "",
    override_editable_flag: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}/worklog".format(client.base_url, issueIdOrKey=issue_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_adjust_estimate: Union[Unset, str] = UNSET
    if not isinstance(adjust_estimate, Unset):
        json_adjust_estimate = adjust_estimate.value

    params: Dict[str, Any] = {
        "notifyUsers": notify_users,
        "adjustEstimate": json_adjust_estimate,
        "newEstimate": new_estimate,
        "reduceBy": reduce_by,
        "expand": expand,
        "overrideEditableFlag": override_editable_flag,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, Worklog]]:
    if response.status_code == 201:
        response_201 = Worklog.from_dict(response.json())

        return response_201
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


def _build_response(*, response: httpx.Response) -> Response[Union[None, Worklog]]:
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
    json_body: Worklog,
    notify_users: Union[Unset, bool] = True,
    adjust_estimate: Union[Unset, AddWorklogAdjustEstimate] = AddWorklogAdjustEstimate.AUTO,
    new_estimate: Union[Unset, str] = UNSET,
    reduce_by: Union[Unset, str] = UNSET,
    expand: Union[Unset, str] = "",
    override_editable_flag: Union[Unset, bool] = False,
) -> Response[Union[None, Worklog]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        json_body=json_body,
        notify_users=notify_users,
        adjust_estimate=adjust_estimate,
        new_estimate=new_estimate,
        reduce_by=reduce_by,
        expand=expand,
        override_editable_flag=override_editable_flag,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    json_body: Worklog,
    notify_users: Union[Unset, bool] = True,
    adjust_estimate: Union[Unset, AddWorklogAdjustEstimate] = AddWorklogAdjustEstimate.AUTO,
    new_estimate: Union[Unset, str] = UNSET,
    reduce_by: Union[Unset, str] = UNSET,
    expand: Union[Unset, str] = "",
    override_editable_flag: Union[Unset, bool] = False,
) -> Optional[Union[None, Worklog]]:
    """Adds a worklog to an issue.

    Time tracking must be enabled in Jira, otherwise this operation returns an error. For more information, see [Configuring time tracking](https://confluence.atlassian.com/x/qoXKM).

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* and *Work on issues* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return sync_detailed(
        client=client,
        issue_id_or_key=issue_id_or_key,
        json_body=json_body,
        notify_users=notify_users,
        adjust_estimate=adjust_estimate,
        new_estimate=new_estimate,
        reduce_by=reduce_by,
        expand=expand,
        override_editable_flag=override_editable_flag,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    json_body: Worklog,
    notify_users: Union[Unset, bool] = True,
    adjust_estimate: Union[Unset, AddWorklogAdjustEstimate] = AddWorklogAdjustEstimate.AUTO,
    new_estimate: Union[Unset, str] = UNSET,
    reduce_by: Union[Unset, str] = UNSET,
    expand: Union[Unset, str] = "",
    override_editable_flag: Union[Unset, bool] = False,
) -> Response[Union[None, Worklog]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        json_body=json_body,
        notify_users=notify_users,
        adjust_estimate=adjust_estimate,
        new_estimate=new_estimate,
        reduce_by=reduce_by,
        expand=expand,
        override_editable_flag=override_editable_flag,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    json_body: Worklog,
    notify_users: Union[Unset, bool] = True,
    adjust_estimate: Union[Unset, AddWorklogAdjustEstimate] = AddWorklogAdjustEstimate.AUTO,
    new_estimate: Union[Unset, str] = UNSET,
    reduce_by: Union[Unset, str] = UNSET,
    expand: Union[Unset, str] = "",
    override_editable_flag: Union[Unset, bool] = False,
) -> Optional[Union[None, Worklog]]:
    """Adds a worklog to an issue.

    Time tracking must be enabled in Jira, otherwise this operation returns an error. For more information, see [Configuring time tracking](https://confluence.atlassian.com/x/qoXKM).

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* and *Work on issues* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue."""

    return (
        await asyncio_detailed(
            client=client,
            issue_id_or_key=issue_id_or_key,
            json_body=json_body,
            notify_users=notify_users,
            adjust_estimate=adjust_estimate,
            new_estimate=new_estimate,
            reduce_by=reduce_by,
            expand=expand,
            override_editable_flag=override_editable_flag,
        )
    ).parsed
