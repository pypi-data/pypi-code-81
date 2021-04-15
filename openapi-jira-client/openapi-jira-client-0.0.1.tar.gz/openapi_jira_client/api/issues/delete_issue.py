from typing import Any, Dict, Union

import httpx

from ...client import AuthenticatedClient
from ...models.delete_issue_delete_subtasks import DeleteIssueDeleteSubtasks
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    delete_subtasks: Union[Unset, DeleteIssueDeleteSubtasks] = DeleteIssueDeleteSubtasks.FALSE,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}".format(client.base_url, issueIdOrKey=issue_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_delete_subtasks: Union[Unset, str] = UNSET
    if not isinstance(delete_subtasks, Unset):
        json_delete_subtasks = delete_subtasks.value

    params: Dict[str, Any] = {
        "deleteSubtasks": json_delete_subtasks,
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
    delete_subtasks: Union[Unset, DeleteIssueDeleteSubtasks] = DeleteIssueDeleteSubtasks.FALSE,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        delete_subtasks=delete_subtasks,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    delete_subtasks: Union[Unset, DeleteIssueDeleteSubtasks] = DeleteIssueDeleteSubtasks.FALSE,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        delete_subtasks=delete_subtasks,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)
