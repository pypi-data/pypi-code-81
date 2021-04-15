from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.error_collection import ErrorCollection
from ...models.get_workflow_transition_rule_configurations_types_item import (
    GetWorkflowTransitionRuleConfigurationsTypesItem,
)
from ...models.page_bean_workflow_transition_rules import PageBeanWorkflowTransitionRules
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 10,
    types: List[GetWorkflowTransitionRuleConfigurationsTypesItem],
    keys: Union[Unset, List[str]] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/workflow/rule/config".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_types = []
    for types_item_data in types:
        types_item = types_item_data.value

        json_types.append(types_item)

    json_keys: Union[Unset, List[str]] = UNSET
    if not isinstance(keys, Unset):
        json_keys = keys

    params: Dict[str, Any] = {
        "startAt": start_at,
        "maxResults": max_results,
        "types": json_types,
        "keys": json_keys,
        "expand": expand,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[ErrorCollection, None, PageBeanWorkflowTransitionRules]]:
    if response.status_code == 200:
        response_200 = PageBeanWorkflowTransitionRules.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorCollection.from_dict(response.json())

        return response_400
    if response.status_code == 403:
        response_403 = ErrorCollection.from_dict(response.json())

        return response_403
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[ErrorCollection, None, PageBeanWorkflowTransitionRules]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 10,
    types: List[GetWorkflowTransitionRuleConfigurationsTypesItem],
    keys: Union[Unset, List[str]] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorCollection, None, PageBeanWorkflowTransitionRules]]:
    kwargs = _get_kwargs(
        client=client,
        start_at=start_at,
        max_results=max_results,
        types=types,
        keys=keys,
        expand=expand,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 10,
    types: List[GetWorkflowTransitionRuleConfigurationsTypesItem],
    keys: Union[Unset, List[str]] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorCollection, None, PageBeanWorkflowTransitionRules]]:
    """Returns a [paginated](#pagination) list of workflows with transition rules. The workflows can be filtered to return only those containing workflow transition rules:

     *  of one or more transition rule types, such as [workflow post functions](https://developer.atlassian.com/cloud/jira/platform/modules/workflow-post-function/).
     *  matching one or more transition rule keys.

    Only workflows containing transition rules created by the calling Connect app are returned. However, if a workflow is returned all transition rules that match the filters are returned for that workflow.

    Due to server-side optimizations, workflows with an empty list of rules may be returned; these workflows can be ignored.

    **[Permissions](#permissions) required:** Only Connect apps can use this operation."""

    return sync_detailed(
        client=client,
        start_at=start_at,
        max_results=max_results,
        types=types,
        keys=keys,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 10,
    types: List[GetWorkflowTransitionRuleConfigurationsTypesItem],
    keys: Union[Unset, List[str]] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorCollection, None, PageBeanWorkflowTransitionRules]]:
    kwargs = _get_kwargs(
        client=client,
        start_at=start_at,
        max_results=max_results,
        types=types,
        keys=keys,
        expand=expand,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 10,
    types: List[GetWorkflowTransitionRuleConfigurationsTypesItem],
    keys: Union[Unset, List[str]] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorCollection, None, PageBeanWorkflowTransitionRules]]:
    """Returns a [paginated](#pagination) list of workflows with transition rules. The workflows can be filtered to return only those containing workflow transition rules:

     *  of one or more transition rule types, such as [workflow post functions](https://developer.atlassian.com/cloud/jira/platform/modules/workflow-post-function/).
     *  matching one or more transition rule keys.

    Only workflows containing transition rules created by the calling Connect app are returned. However, if a workflow is returned all transition rules that match the filters are returned for that workflow.

    Due to server-side optimizations, workflows with an empty list of rules may be returned; these workflows can be ignored.

    **[Permissions](#permissions) required:** Only Connect apps can use this operation."""

    return (
        await asyncio_detailed(
            client=client,
            start_at=start_at,
            max_results=max_results,
            types=types,
            keys=keys,
            expand=expand,
        )
    ).parsed
