from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.created_issue import CreatedIssue
from ...models.error_collection import ErrorCollection
from ...models.issue_update_details import IssueUpdateDetails
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: IssueUpdateDetails,
    update_history: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "updateHistory": update_history,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[CreatedIssue, ErrorCollection]]:
    if response.status_code == 201:
        response_201 = CreatedIssue.from_dict(response.json())

        return response_201
    if response.status_code == 400:
        response_400 = ErrorCollection.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = ErrorCollection.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = ErrorCollection.from_dict(response.json())

        return response_403
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[CreatedIssue, ErrorCollection]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: IssueUpdateDetails,
    update_history: Union[Unset, bool] = False,
) -> Response[Union[CreatedIssue, ErrorCollection]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        update_history=update_history,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: IssueUpdateDetails,
    update_history: Union[Unset, bool] = False,
) -> Optional[Union[CreatedIssue, ErrorCollection]]:
    """Creates an issue or, where the option to create subtasks is enabled in Jira, a subtask. A transition may be applied, to move the issue or subtask to a workflow step other than the default start step, and issue properties set.

    The content of the issue or subtask is defined using `update` and `fields`. The fields that can be set in the issue or subtask are determined using the [ Get create issue metadata](#api-rest-api-3-issue-createmeta-get). These are the same fields that appear on the issue's create screen. Note that the `description`, `environment`, and any `textarea` type custom fields (multi-line text fields) take Atlassian Document Format content. Single line custom fields (`textfield`) accept a string and don't handle Atlassian Document Format content.

    Creating a subtask differs from creating an issue as follows:

     *  `issueType` must be set to a subtask issue type (use [ Get create issue metadata](#api-rest-api-3-issue-createmeta-get) to find subtask issue types).
     *  `parent` must contain the ID or key of the parent issue.

    In a next-gen project any issue may be made a child providing that the parent and child are members of the same project. In a classic project the parent field is only valid for subtasks.

    **[Permissions](#permissions) required:** *Browse projects* and *Create issues* [project permissions](https://confluence.atlassian.com/x/yodKLg) for the project in which the issue or subtask is created."""

    return sync_detailed(
        client=client,
        json_body=json_body,
        update_history=update_history,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: IssueUpdateDetails,
    update_history: Union[Unset, bool] = False,
) -> Response[Union[CreatedIssue, ErrorCollection]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        update_history=update_history,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: IssueUpdateDetails,
    update_history: Union[Unset, bool] = False,
) -> Optional[Union[CreatedIssue, ErrorCollection]]:
    """Creates an issue or, where the option to create subtasks is enabled in Jira, a subtask. A transition may be applied, to move the issue or subtask to a workflow step other than the default start step, and issue properties set.

    The content of the issue or subtask is defined using `update` and `fields`. The fields that can be set in the issue or subtask are determined using the [ Get create issue metadata](#api-rest-api-3-issue-createmeta-get). These are the same fields that appear on the issue's create screen. Note that the `description`, `environment`, and any `textarea` type custom fields (multi-line text fields) take Atlassian Document Format content. Single line custom fields (`textfield`) accept a string and don't handle Atlassian Document Format content.

    Creating a subtask differs from creating an issue as follows:

     *  `issueType` must be set to a subtask issue type (use [ Get create issue metadata](#api-rest-api-3-issue-createmeta-get) to find subtask issue types).
     *  `parent` must contain the ID or key of the parent issue.

    In a next-gen project any issue may be made a child providing that the parent and child are members of the same project. In a classic project the parent field is only valid for subtasks.

    **[Permissions](#permissions) required:** *Browse projects* and *Create issues* [project permissions](https://confluence.atlassian.com/x/yodKLg) for the project in which the issue or subtask is created."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            update_history=update_history,
        )
    ).parsed
