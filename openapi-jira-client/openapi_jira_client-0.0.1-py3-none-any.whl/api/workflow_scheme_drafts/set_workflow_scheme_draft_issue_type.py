from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.issue_type_workflow_mapping import IssueTypeWorkflowMapping
from ...models.workflow_scheme import WorkflowScheme
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id_: int,
    issue_type: str,
    json_body: IssueTypeWorkflowMapping,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/workflowscheme/{id}/draft/issuetype/{issueType}".format(
        client.base_url, id=id_, issueType=issue_type
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, WorkflowScheme]]:
    if response.status_code == 200:
        response_200 = WorkflowScheme.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
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


def _build_response(*, response: httpx.Response) -> Response[Union[None, WorkflowScheme]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    id_: int,
    issue_type: str,
    json_body: IssueTypeWorkflowMapping,
) -> Response[Union[None, WorkflowScheme]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        issue_type=issue_type,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id_: int,
    issue_type: str,
    json_body: IssueTypeWorkflowMapping,
) -> Optional[Union[None, WorkflowScheme]]:
    """Sets the workflow for an issue type in a workflow scheme's draft.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        id_=id_,
        issue_type=issue_type,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id_: int,
    issue_type: str,
    json_body: IssueTypeWorkflowMapping,
) -> Response[Union[None, WorkflowScheme]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        issue_type=issue_type,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id_: int,
    issue_type: str,
    json_body: IssueTypeWorkflowMapping,
) -> Optional[Union[None, WorkflowScheme]]:
    """Sets the workflow for an issue type in a workflow scheme's draft.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            id_=id_,
            issue_type=issue_type,
            json_body=json_body,
        )
    ).parsed
