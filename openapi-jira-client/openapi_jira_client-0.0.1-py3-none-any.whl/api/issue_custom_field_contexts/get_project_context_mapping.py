from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.page_bean_custom_field_context_project_mapping import PageBeanCustomFieldContextProjectMapping
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    field_id: str,
    context_id: Union[Unset, List[int]] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/field/{fieldId}/context/projectmapping".format(client.base_url, fieldId=field_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_context_id: Union[Unset, List[int]] = UNSET
    if not isinstance(context_id, Unset):
        json_context_id = context_id

    params: Dict[str, Any] = {
        "contextId": json_context_id,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, PageBeanCustomFieldContextProjectMapping]]:
    if response.status_code == 200:
        response_200 = PageBeanCustomFieldContextProjectMapping.from_dict(response.json())

        return response_200
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


def _build_response(*, response: httpx.Response) -> Response[Union[None, PageBeanCustomFieldContextProjectMapping]]:
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
    context_id: Union[Unset, List[int]] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Response[Union[None, PageBeanCustomFieldContextProjectMapping]]:
    kwargs = _get_kwargs(
        client=client,
        field_id=field_id,
        context_id=context_id,
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
    context_id: Union[Unset, List[int]] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Optional[Union[None, PageBeanCustomFieldContextProjectMapping]]:
    """Returns a [paginated](#pagination) list of context to project mappings for a custom field. The result can be filtered by `contextId`, or otherwise all mappings are returned. Invalid IDs are ignored.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        field_id=field_id,
        context_id=context_id,
        start_at=start_at,
        max_results=max_results,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    field_id: str,
    context_id: Union[Unset, List[int]] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Response[Union[None, PageBeanCustomFieldContextProjectMapping]]:
    kwargs = _get_kwargs(
        client=client,
        field_id=field_id,
        context_id=context_id,
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
    context_id: Union[Unset, List[int]] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
) -> Optional[Union[None, PageBeanCustomFieldContextProjectMapping]]:
    """Returns a [paginated](#pagination) list of context to project mappings for a custom field. The result can be filtered by `contextId`, or otherwise all mappings are returned. Invalid IDs are ignored.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            field_id=field_id,
            context_id=context_id,
            start_at=start_at,
            max_results=max_results,
        )
    ).parsed
