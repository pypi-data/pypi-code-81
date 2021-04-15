from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.task_progress_bean_remove_option_from_issues_result import TaskProgressBeanRemoveOptionFromIssuesResult
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    field_key: str,
    option_id: int,
    replace_with: Union[Unset, int] = UNSET,
    jql: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/field/{fieldKey}/option/{optionId}/issue".format(
        client.base_url, fieldKey=field_key, optionId=option_id
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "replaceWith": replace_with,
        "jql": jql,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, TaskProgressBeanRemoveOptionFromIssuesResult]]:
    if response.status_code == 303:
        response_303 = TaskProgressBeanRemoveOptionFromIssuesResult.from_dict(response.json())

        return response_303
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, TaskProgressBeanRemoveOptionFromIssuesResult]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    field_key: str,
    option_id: int,
    replace_with: Union[Unset, int] = UNSET,
    jql: Union[Unset, str] = UNSET,
) -> Response[Union[None, TaskProgressBeanRemoveOptionFromIssuesResult]]:
    kwargs = _get_kwargs(
        client=client,
        field_key=field_key,
        option_id=option_id,
        replace_with=replace_with,
        jql=jql,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    field_key: str,
    option_id: int,
    replace_with: Union[Unset, int] = UNSET,
    jql: Union[Unset, str] = UNSET,
) -> Optional[Union[None, TaskProgressBeanRemoveOptionFromIssuesResult]]:
    """Deselects an issue-field select-list option from all issues where it is selected. A different option can be selected to replace the deselected option. The update can also be limited to a smaller set of issues by using a JQL query.

    This is an [asynchronous operation](#async). The response object contains a link to the long-running task.

    Note that this operation **only works for issue field select list options added by Connect apps**, it cannot be used with issue field select list options created in Jira or using operations from the [Issue custom field options](#api-group-Issue-custom-field-options) resource.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg). Jira permissions are not required for the app providing the field."""

    return sync_detailed(
        client=client,
        field_key=field_key,
        option_id=option_id,
        replace_with=replace_with,
        jql=jql,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    field_key: str,
    option_id: int,
    replace_with: Union[Unset, int] = UNSET,
    jql: Union[Unset, str] = UNSET,
) -> Response[Union[None, TaskProgressBeanRemoveOptionFromIssuesResult]]:
    kwargs = _get_kwargs(
        client=client,
        field_key=field_key,
        option_id=option_id,
        replace_with=replace_with,
        jql=jql,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    field_key: str,
    option_id: int,
    replace_with: Union[Unset, int] = UNSET,
    jql: Union[Unset, str] = UNSET,
) -> Optional[Union[None, TaskProgressBeanRemoveOptionFromIssuesResult]]:
    """Deselects an issue-field select-list option from all issues where it is selected. A different option can be selected to replace the deselected option. The update can also be limited to a smaller set of issues by using a JQL query.

    This is an [asynchronous operation](#async). The response object contains a link to the long-running task.

    Note that this operation **only works for issue field select list options added by Connect apps**, it cannot be used with issue field select list options created in Jira or using operations from the [Issue custom field options](#api-group-Issue-custom-field-options) resource.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg). Jira permissions are not required for the app providing the field."""

    return (
        await asyncio_detailed(
            client=client,
            field_key=field_key,
            option_id=option_id,
            replace_with=replace_with,
            jql=jql,
        )
    ).parsed
