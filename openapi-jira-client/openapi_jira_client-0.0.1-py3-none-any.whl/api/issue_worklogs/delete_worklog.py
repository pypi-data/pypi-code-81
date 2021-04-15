from typing import Any, Dict, Union

import httpx

from ...client import AuthenticatedClient
from ...models.delete_worklog_adjust_estimate import DeleteWorklogAdjustEstimate
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    id_: str,
    notify_users: Union[Unset, bool] = True,
    adjust_estimate: Union[Unset, DeleteWorklogAdjustEstimate] = DeleteWorklogAdjustEstimate.AUTO,
    new_estimate: Union[Unset, str] = UNSET,
    increase_by: Union[Unset, str] = UNSET,
    override_editable_flag: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}/worklog/{id}".format(
        client.base_url, issueIdOrKey=issue_id_or_key, id=id_
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_adjust_estimate: Union[Unset, str] = UNSET
    if not isinstance(adjust_estimate, Unset):
        json_adjust_estimate = adjust_estimate.value

    params: Dict[str, Any] = {
        "notifyUsers": notify_users,
        "adjustEstimate": json_adjust_estimate,
        "newEstimate": new_estimate,
        "increaseBy": increase_by,
        "overrideEditableFlag": override_editable_flag,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _build_response(*, response: httpx.Response) -> Response[None]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    id_: str,
    notify_users: Union[Unset, bool] = True,
    adjust_estimate: Union[Unset, DeleteWorklogAdjustEstimate] = DeleteWorklogAdjustEstimate.AUTO,
    new_estimate: Union[Unset, str] = UNSET,
    increase_by: Union[Unset, str] = UNSET,
    override_editable_flag: Union[Unset, bool] = False,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        id_=id_,
        notify_users=notify_users,
        adjust_estimate=adjust_estimate,
        new_estimate=new_estimate,
        increase_by=increase_by,
        override_editable_flag=override_editable_flag,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    id_: str,
    notify_users: Union[Unset, bool] = True,
    adjust_estimate: Union[Unset, DeleteWorklogAdjustEstimate] = DeleteWorklogAdjustEstimate.AUTO,
    new_estimate: Union[Unset, str] = UNSET,
    increase_by: Union[Unset, str] = UNSET,
    override_editable_flag: Union[Unset, bool] = False,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        id_=id_,
        notify_users=notify_users,
        adjust_estimate=adjust_estimate,
        new_estimate=new_estimate,
        increase_by=increase_by,
        override_editable_flag=override_editable_flag,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)
