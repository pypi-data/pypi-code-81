from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.page_bean_custom_field_context_option import PageBeanCustomFieldContextOption
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    field_id: str,
    context_id: int,
    option_id: Union[Unset, int] = UNSET,
    only_options: Union[Unset, bool] = False,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 100,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/field/{fieldId}/context/{contextId}/option".format(
        client.base_url, fieldId=field_id, contextId=context_id
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "optionId": option_id,
        "onlyOptions": only_options,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, PageBeanCustomFieldContextOption]]:
    if response.status_code == 200:
        response_200 = PageBeanCustomFieldContextOption.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[None, PageBeanCustomFieldContextOption]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    field_id: str,
    context_id: int,
    option_id: Union[Unset, int] = UNSET,
    only_options: Union[Unset, bool] = False,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 100,
) -> Response[Union[None, PageBeanCustomFieldContextOption]]:
    kwargs = _get_kwargs(
        client=client,
        field_id=field_id,
        context_id=context_id,
        option_id=option_id,
        only_options=only_options,
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
    field_id: str,
    context_id: int,
    option_id: Union[Unset, int] = UNSET,
    only_options: Union[Unset, bool] = False,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 100,
) -> Optional[Union[None, PageBeanCustomFieldContextOption]]:
    """Returns a [paginated](#pagination) list of all custom field option for a context. Options are returned first then cascading options, in the order they display in Jira.

    This operation works for custom field options created in Jira or the operations from this resource. **To work with issue field select list options created for Connect apps use the [Issue custom field options (apps)](#api-group-issue-custom-field-options--apps-) operations.**

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        field_id=field_id,
        context_id=context_id,
        option_id=option_id,
        only_options=only_options,
        start_at=start_at,
        max_results=max_results,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    field_id: str,
    context_id: int,
    option_id: Union[Unset, int] = UNSET,
    only_options: Union[Unset, bool] = False,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 100,
) -> Response[Union[None, PageBeanCustomFieldContextOption]]:
    kwargs = _get_kwargs(
        client=client,
        field_id=field_id,
        context_id=context_id,
        option_id=option_id,
        only_options=only_options,
        start_at=start_at,
        max_results=max_results,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    field_id: str,
    context_id: int,
    option_id: Union[Unset, int] = UNSET,
    only_options: Union[Unset, bool] = False,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 100,
) -> Optional[Union[None, PageBeanCustomFieldContextOption]]:
    """Returns a [paginated](#pagination) list of all custom field option for a context. Options are returned first then cascading options, in the order they display in Jira.

    This operation works for custom field options created in Jira or the operations from this resource. **To work with issue field select list options created for Connect apps use the [Issue custom field options (apps)](#api-group-issue-custom-field-options--apps-) operations.**

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            field_id=field_id,
            context_id=context_id,
            option_id=option_id,
            only_options=only_options,
            start_at=start_at,
            max_results=max_results,
        )
    ).parsed
