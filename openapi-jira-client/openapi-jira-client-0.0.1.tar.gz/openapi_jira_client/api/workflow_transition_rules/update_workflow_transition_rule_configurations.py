from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.error_collection import ErrorCollection
from ...models.workflow_transition_rules_update import WorkflowTransitionRulesUpdate
from ...models.workflow_transition_rules_update_errors import WorkflowTransitionRulesUpdateErrors
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: WorkflowTransitionRulesUpdate,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/workflow/rule/config".format(client.base_url)

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


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[ErrorCollection, WorkflowTransitionRulesUpdateErrors]]:
    if response.status_code == 200:
        response_200 = WorkflowTransitionRulesUpdateErrors.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorCollection.from_dict(response.json())

        return response_400
    if response.status_code == 403:
        response_403 = ErrorCollection.from_dict(response.json())

        return response_403
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[ErrorCollection, WorkflowTransitionRulesUpdateErrors]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: WorkflowTransitionRulesUpdate,
) -> Response[Union[ErrorCollection, WorkflowTransitionRulesUpdateErrors]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: WorkflowTransitionRulesUpdate,
) -> Optional[Union[ErrorCollection, WorkflowTransitionRulesUpdateErrors]]:
    """Updates configuration of workflow transition rules. The following rule types are supported:

     *  [post functions](https://developer.atlassian.com/cloud/jira/platform/modules/workflow-post-function/)
     *  [conditions](https://developer.atlassian.com/cloud/jira/platform/modules/workflow-condition/)
     *  [validators](https://developer.atlassian.com/cloud/jira/platform/modules/workflow-validator/)

    Only rules created by the calling Connect app can be updated.

    **[Permissions](#permissions) required:** Only Connect apps can use this operation."""

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: WorkflowTransitionRulesUpdate,
) -> Response[Union[ErrorCollection, WorkflowTransitionRulesUpdateErrors]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: WorkflowTransitionRulesUpdate,
) -> Optional[Union[ErrorCollection, WorkflowTransitionRulesUpdateErrors]]:
    """Updates configuration of workflow transition rules. The following rule types are supported:

     *  [post functions](https://developer.atlassian.com/cloud/jira/platform/modules/workflow-post-function/)
     *  [conditions](https://developer.atlassian.com/cloud/jira/platform/modules/workflow-condition/)
     *  [validators](https://developer.atlassian.com/cloud/jira/platform/modules/workflow-validator/)

    Only rules created by the calling Connect app can be updated.

    **[Permissions](#permissions) required:** Only Connect apps can use this operation."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
