from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.bulk_issue_property_update_request import BulkIssuePropertyUpdateRequest
from ...models.error_collection import ErrorCollection
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    property_key: str,
    json_body: BulkIssuePropertyUpdateRequest,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/properties/{propertyKey}".format(client.base_url, propertyKey=property_key)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[ErrorCollection, None]]:
    if response.status_code == 303:
        response_303 = None

        return response_303
    if response.status_code == 400:
        response_400 = ErrorCollection.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = ErrorCollection.from_dict(response.json())

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ErrorCollection, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    property_key: str,
    json_body: BulkIssuePropertyUpdateRequest,
) -> Response[Union[ErrorCollection, None]]:
    kwargs = _get_kwargs(
        client=client,
        property_key=property_key,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    property_key: str,
    json_body: BulkIssuePropertyUpdateRequest,
) -> Optional[Union[ErrorCollection, None]]:
    """Sets a property value on multiple issues.

    The value set can be a constant or determined by a [Jira expression](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/). Expressions must be computable with constant complexity when applied to a set of issues. Expressions must also comply with the [restrictions](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/#restrictions) that apply to all Jira expressions.

    The issues to be updated can be specified by a filter.

    The filter identifies issues eligible for update using these criteria:

     *  `entityIds` Only issues from this list are eligible.
     *  `currentValue` Only issues with the property set to this value are eligible.
     *  `hasProperty`:

         *  If *true*, only issues with the property are eligible.
         *  If *false*, only issues without the property are eligible.

    If more than one criteria is specified, they are joined with the logical *AND*: only issues that satisfy all criteria are eligible.

    If an invalid combination of criteria is provided, an error is returned. For example, specifying a `currentValue` and `hasProperty` as *false* would not match any issues (because without the property the property cannot have a value).

    The filter is optional. Without the filter all the issues visible to the user and where the user has the EDIT\_ISSUES permission for the issue are considered eligible.

    This operation is:

     *  transactional, either all eligible issues are updated or, when errors occur, none are updated.
     *  [asynchronous](#async). Follow the `location` link in the response to determine the status of the task and use [Get task](#api-rest-api-3-task-taskId-get) to obtain subsequent updates.

    **[Permissions](#permissions) required:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for each project containing issues.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.
     *  *Edit issues* [project permission](https://confluence.atlassian.com/x/yodKLg) for each issue."""

    return sync_detailed(
        client=client,
        property_key=property_key,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    property_key: str,
    json_body: BulkIssuePropertyUpdateRequest,
) -> Response[Union[ErrorCollection, None]]:
    kwargs = _get_kwargs(
        client=client,
        property_key=property_key,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    property_key: str,
    json_body: BulkIssuePropertyUpdateRequest,
) -> Optional[Union[ErrorCollection, None]]:
    """Sets a property value on multiple issues.

    The value set can be a constant or determined by a [Jira expression](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/). Expressions must be computable with constant complexity when applied to a set of issues. Expressions must also comply with the [restrictions](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/#restrictions) that apply to all Jira expressions.

    The issues to be updated can be specified by a filter.

    The filter identifies issues eligible for update using these criteria:

     *  `entityIds` Only issues from this list are eligible.
     *  `currentValue` Only issues with the property set to this value are eligible.
     *  `hasProperty`:

         *  If *true*, only issues with the property are eligible.
         *  If *false*, only issues without the property are eligible.

    If more than one criteria is specified, they are joined with the logical *AND*: only issues that satisfy all criteria are eligible.

    If an invalid combination of criteria is provided, an error is returned. For example, specifying a `currentValue` and `hasProperty` as *false* would not match any issues (because without the property the property cannot have a value).

    The filter is optional. Without the filter all the issues visible to the user and where the user has the EDIT\_ISSUES permission for the issue are considered eligible.

    This operation is:

     *  transactional, either all eligible issues are updated or, when errors occur, none are updated.
     *  [asynchronous](#async). Follow the `location` link in the response to determine the status of the task and use [Get task](#api-rest-api-3-task-taskId-get) to obtain subsequent updates.

    **[Permissions](#permissions) required:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for each project containing issues.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.
     *  *Edit issues* [project permission](https://confluence.atlassian.com/x/yodKLg) for each issue."""

    return (
        await asyncio_detailed(
            client=client,
            property_key=property_key,
            json_body=json_body,
        )
    ).parsed
