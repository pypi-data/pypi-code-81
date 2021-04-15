from typing import Any, Dict, Union

import httpx

from ...client import AuthenticatedClient
from ...models.issue_update_details import IssueUpdateDetails
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    json_body: IssueUpdateDetails,
    notify_users: Union[Unset, bool] = True,
    override_screen_security: Union[Unset, bool] = False,
    override_editable_flag: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}".format(client.base_url, issueIdOrKey=issue_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "notifyUsers": notify_users,
        "overrideScreenSecurity": override_screen_security,
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
    json_body: IssueUpdateDetails,
    notify_users: Union[Unset, bool] = True,
    override_screen_security: Union[Unset, bool] = False,
    override_editable_flag: Union[Unset, bool] = False,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        json_body=json_body,
        notify_users=notify_users,
        override_screen_security=override_screen_security,
        override_editable_flag=override_editable_flag,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    json_body: IssueUpdateDetails,
    notify_users: Union[Unset, bool] = True,
    override_screen_security: Union[Unset, bool] = False,
    override_editable_flag: Union[Unset, bool] = False,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        json_body=json_body,
        notify_users=notify_users,
        override_screen_security=override_screen_security,
        override_editable_flag=override_editable_flag,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)
