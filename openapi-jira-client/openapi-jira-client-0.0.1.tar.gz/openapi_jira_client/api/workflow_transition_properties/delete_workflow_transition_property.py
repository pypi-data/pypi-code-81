from typing import Any, Dict, Union

import httpx

from ...client import AuthenticatedClient
from ...models.delete_workflow_transition_property_workflow_mode import DeleteWorkflowTransitionPropertyWorkflowMode
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    transition_id: int,
    key: str,
    workflow_name: str,
    workflow_mode: Union[Unset, DeleteWorkflowTransitionPropertyWorkflowMode] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/workflow/transitions/{transitionId}/properties".format(
        client.base_url, transitionId=transition_id
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_workflow_mode: Union[Unset, str] = UNSET
    if not isinstance(workflow_mode, Unset):
        json_workflow_mode = workflow_mode.value

    params: Dict[str, Any] = {
        "key": key,
        "workflowName": workflow_name,
        "workflowMode": json_workflow_mode,
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
    transition_id: int,
    key: str,
    workflow_name: str,
    workflow_mode: Union[Unset, DeleteWorkflowTransitionPropertyWorkflowMode] = UNSET,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        transition_id=transition_id,
        key=key,
        workflow_name=workflow_name,
        workflow_mode=workflow_mode,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    transition_id: int,
    key: str,
    workflow_name: str,
    workflow_mode: Union[Unset, DeleteWorkflowTransitionPropertyWorkflowMode] = UNSET,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        transition_id=transition_id,
        key=key,
        workflow_name=workflow_name,
        workflow_mode=workflow_mode,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)
