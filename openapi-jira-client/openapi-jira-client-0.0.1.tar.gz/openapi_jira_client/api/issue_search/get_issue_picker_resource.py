from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.issue_picker_suggestions import IssuePickerSuggestions
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    query: Union[Unset, str] = UNSET,
    current_jql: Union[Unset, str] = UNSET,
    current_issue_key: Union[Unset, str] = UNSET,
    current_project_id: Union[Unset, str] = UNSET,
    show_sub_tasks: Union[Unset, bool] = UNSET,
    show_sub_task_parent: Union[Unset, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/picker".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "query": query,
        "currentJQL": current_jql,
        "currentIssueKey": current_issue_key,
        "currentProjectId": current_project_id,
        "showSubTasks": show_sub_tasks,
        "showSubTaskParent": show_sub_task_parent,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[IssuePickerSuggestions, None]]:
    if response.status_code == 200:
        response_200 = IssuePickerSuggestions.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[IssuePickerSuggestions, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    query: Union[Unset, str] = UNSET,
    current_jql: Union[Unset, str] = UNSET,
    current_issue_key: Union[Unset, str] = UNSET,
    current_project_id: Union[Unset, str] = UNSET,
    show_sub_tasks: Union[Unset, bool] = UNSET,
    show_sub_task_parent: Union[Unset, bool] = UNSET,
) -> Response[Union[IssuePickerSuggestions, None]]:
    kwargs = _get_kwargs(
        client=client,
        query=query,
        current_jql=current_jql,
        current_issue_key=current_issue_key,
        current_project_id=current_project_id,
        show_sub_tasks=show_sub_tasks,
        show_sub_task_parent=show_sub_task_parent,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    query: Union[Unset, str] = UNSET,
    current_jql: Union[Unset, str] = UNSET,
    current_issue_key: Union[Unset, str] = UNSET,
    current_project_id: Union[Unset, str] = UNSET,
    show_sub_tasks: Union[Unset, bool] = UNSET,
    show_sub_task_parent: Union[Unset, bool] = UNSET,
) -> Optional[Union[IssuePickerSuggestions, None]]:
    """Returns lists of issues matching a query string. Use this resource to provide auto-completion suggestions when the user is looking for an issue using a word or string.

    This operation returns two lists:

     *  `History Search` which includes issues from the user's history of created, edited, or viewed issues that contain the string in the `query` parameter.
     *  `Current Search` which includes issues that match the JQL expression in `currentJQL` and contain the string in the `query` parameter.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None."""

    return sync_detailed(
        client=client,
        query=query,
        current_jql=current_jql,
        current_issue_key=current_issue_key,
        current_project_id=current_project_id,
        show_sub_tasks=show_sub_tasks,
        show_sub_task_parent=show_sub_task_parent,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    query: Union[Unset, str] = UNSET,
    current_jql: Union[Unset, str] = UNSET,
    current_issue_key: Union[Unset, str] = UNSET,
    current_project_id: Union[Unset, str] = UNSET,
    show_sub_tasks: Union[Unset, bool] = UNSET,
    show_sub_task_parent: Union[Unset, bool] = UNSET,
) -> Response[Union[IssuePickerSuggestions, None]]:
    kwargs = _get_kwargs(
        client=client,
        query=query,
        current_jql=current_jql,
        current_issue_key=current_issue_key,
        current_project_id=current_project_id,
        show_sub_tasks=show_sub_tasks,
        show_sub_task_parent=show_sub_task_parent,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    query: Union[Unset, str] = UNSET,
    current_jql: Union[Unset, str] = UNSET,
    current_issue_key: Union[Unset, str] = UNSET,
    current_project_id: Union[Unset, str] = UNSET,
    show_sub_tasks: Union[Unset, bool] = UNSET,
    show_sub_task_parent: Union[Unset, bool] = UNSET,
) -> Optional[Union[IssuePickerSuggestions, None]]:
    """Returns lists of issues matching a query string. Use this resource to provide auto-completion suggestions when the user is looking for an issue using a word or string.

    This operation returns two lists:

     *  `History Search` which includes issues from the user's history of created, edited, or viewed issues that contain the string in the `query` parameter.
     *  `Current Search` which includes issues that match the JQL expression in `currentJQL` and contain the string in the `query` parameter.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None."""

    return (
        await asyncio_detailed(
            client=client,
            query=query,
            current_jql=current_jql,
            current_issue_key=current_issue_key,
            current_project_id=current_project_id,
            show_sub_tasks=show_sub_tasks,
            show_sub_task_parent=show_sub_task_parent,
        )
    ).parsed
