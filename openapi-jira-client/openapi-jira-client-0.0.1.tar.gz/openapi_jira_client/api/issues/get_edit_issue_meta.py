from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.issue_update_metadata import IssueUpdateMetadata
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    override_screen_security: Union[Unset, bool] = False,
    override_editable_flag: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}/editmeta".format(client.base_url, issueIdOrKey=issue_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "overrideScreenSecurity": override_screen_security,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[IssueUpdateMetadata, None]]:
    if response.status_code == 200:
        response_200 = IssueUpdateMetadata.from_dict(response.json())

        return response_200
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


def _build_response(*, response: httpx.Response) -> Response[Union[IssueUpdateMetadata, None]]:
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
    override_screen_security: Union[Unset, bool] = False,
    override_editable_flag: Union[Unset, bool] = False,
) -> Response[Union[IssueUpdateMetadata, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        override_screen_security=override_screen_security,
        override_editable_flag=override_editable_flag,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    override_screen_security: Union[Unset, bool] = False,
    override_editable_flag: Union[Unset, bool] = False,
) -> Optional[Union[IssueUpdateMetadata, None]]:
    """Returns the edit screen fields for an issue that are visible to and editable by the user. Use the information to populate the requests in [Edit issue](#api-rest-api-3-issue-issueIdOrKey-put).

    Connect app users with admin permissions (from user permissions and app scopes) can return additional details using:

     *  `overrideScreenSecurity` Returns hidden fields.
     *  `overrideEditableFlag` Returns uneditable fields. For example, where an issue has a workflow status of closed none of its fields are editable.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.

    Note: For any fields to be editable the user must have the *Edit issues* [project permission](https://confluence.atlassian.com/x/yodKLg) for the issue."""

    return sync_detailed(
        client=client,
        issue_id_or_key=issue_id_or_key,
        override_screen_security=override_screen_security,
        override_editable_flag=override_editable_flag,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    override_screen_security: Union[Unset, bool] = False,
    override_editable_flag: Union[Unset, bool] = False,
) -> Response[Union[IssueUpdateMetadata, None]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        override_screen_security=override_screen_security,
        override_editable_flag=override_editable_flag,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    override_screen_security: Union[Unset, bool] = False,
    override_editable_flag: Union[Unset, bool] = False,
) -> Optional[Union[IssueUpdateMetadata, None]]:
    """Returns the edit screen fields for an issue that are visible to and editable by the user. Use the information to populate the requests in [Edit issue](#api-rest-api-3-issue-issueIdOrKey-put).

    Connect app users with admin permissions (from user permissions and app scopes) can return additional details using:

     *  `overrideScreenSecurity` Returns hidden fields.
     *  `overrideEditableFlag` Returns uneditable fields. For example, where an issue has a workflow status of closed none of its fields are editable.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.

    Note: For any fields to be editable the user must have the *Edit issues* [project permission](https://confluence.atlassian.com/x/yodKLg) for the issue."""

    return (
        await asyncio_detailed(
            client=client,
            issue_id_or_key=issue_id_or_key,
            override_screen_security=override_screen_security,
            override_editable_flag=override_editable_flag,
        )
    ).parsed
