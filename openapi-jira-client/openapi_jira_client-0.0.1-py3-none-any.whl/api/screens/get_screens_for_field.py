from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.page_bean_screen_with_tab import PageBeanScreenWithTab
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    field_id: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 100,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/field/{fieldId}/screens".format(client.base_url, fieldId=field_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "startAt": start_at,
        "maxResults": max_results,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, PageBeanScreenWithTab]]:
    if response.status_code == 200:
        response_200 = PageBeanScreenWithTab.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = None

        return response_403
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, PageBeanScreenWithTab]]:
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
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 100,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[None, PageBeanScreenWithTab]]:
    kwargs = _get_kwargs(
        client=client,
        field_id=field_id,
        start_at=start_at,
        max_results=max_results,
        expand=expand,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    field_id: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 100,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[None, PageBeanScreenWithTab]]:
    """Returns a [paginated](#pagination) list of the screens a field is used in.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        field_id=field_id,
        start_at=start_at,
        max_results=max_results,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    field_id: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 100,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[None, PageBeanScreenWithTab]]:
    kwargs = _get_kwargs(
        client=client,
        field_id=field_id,
        start_at=start_at,
        max_results=max_results,
        expand=expand,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    field_id: str,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 100,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[None, PageBeanScreenWithTab]]:
    """Returns a [paginated](#pagination) list of the screens a field is used in.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            field_id=field_id,
            start_at=start_at,
            max_results=max_results,
            expand=expand,
        )
    ).parsed
