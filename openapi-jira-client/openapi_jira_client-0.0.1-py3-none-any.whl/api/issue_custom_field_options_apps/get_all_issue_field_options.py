from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.page_bean_issue_field_option import PageBeanIssueFieldOption
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    field_key: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/field/{fieldKey}/option".format(client.base_url, fieldKey=field_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "startAt": start_at,
        "maxResults": max_results,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, PageBeanIssueFieldOption]]:
    if response.status_code == 200:
        response_200 = PageBeanIssueFieldOption.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 403:
        response_403 = None

        return response_403
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, PageBeanIssueFieldOption]]:
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
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Response[Union[None, PageBeanIssueFieldOption]]:
    kwargs = _get_kwargs(
        client=client,
        field_key=field_key,
        start_at=start_at,
        max_results=max_results,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    field_key: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Optional[Union[None, PageBeanIssueFieldOption]]:
    """Returns a [paginated](#pagination) list of all the options of a select list issue field. A select list issue field is a type of [issue field](https://developer.atlassian.com/cloud/jira/platform/modules/issue-field/) that enables a user to select a value from a list of options.

    Note that this operation **only works for issue field select list options added by Connect apps**, it cannot be used with issue field select list options created in Jira or using operations from the [Issue custom field options](#api-group-Issue-custom-field-options) resource.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg). Jira permissions are not required for the app providing the field."""

    return sync_detailed(
        client=client,
        field_key=field_key,
        start_at=start_at,
        max_results=max_results,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    field_key: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Response[Union[None, PageBeanIssueFieldOption]]:
    kwargs = _get_kwargs(
        client=client,
        field_key=field_key,
        start_at=start_at,
        max_results=max_results,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    field_key: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Optional[Union[None, PageBeanIssueFieldOption]]:
    """Returns a [paginated](#pagination) list of all the options of a select list issue field. A select list issue field is a type of [issue field](https://developer.atlassian.com/cloud/jira/platform/modules/issue-field/) that enables a user to select a value from a list of options.

    Note that this operation **only works for issue field select list options added by Connect apps**, it cannot be used with issue field select list options created in Jira or using operations from the [Issue custom field options](#api-group-Issue-custom-field-options) resource.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg). Jira permissions are not required for the app providing the field."""

    return (
        await asyncio_detailed(
            client=client,
            field_key=field_key,
            start_at=start_at,
            max_results=max_results,
        )
    ).parsed
