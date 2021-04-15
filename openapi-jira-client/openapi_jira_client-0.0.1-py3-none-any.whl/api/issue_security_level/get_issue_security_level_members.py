from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.page_bean_issue_security_level_member import PageBeanIssueSecurityLevelMember
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_security_scheme_id: int,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    issue_security_level_id: Union[Unset, List[int]] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issuesecurityschemes/{issueSecuritySchemeId}/members".format(
        client.base_url, issueSecuritySchemeId=issue_security_scheme_id
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_issue_security_level_id: Union[Unset, List[int]] = UNSET
    if not isinstance(issue_security_level_id, Unset):
        json_issue_security_level_id = issue_security_level_id

    params: Dict[str, Any] = {
        "startAt": start_at,
        "maxResults": max_results,
        "issueSecurityLevelId": json_issue_security_level_id,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, PageBeanIssueSecurityLevelMember]]:
    if response.status_code == 200:
        response_200 = PageBeanIssueSecurityLevelMember.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[None, PageBeanIssueSecurityLevelMember]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    issue_security_scheme_id: int,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    issue_security_level_id: Union[Unset, List[int]] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[None, PageBeanIssueSecurityLevelMember]]:
    kwargs = _get_kwargs(
        client=client,
        issue_security_scheme_id=issue_security_scheme_id,
        start_at=start_at,
        max_results=max_results,
        issue_security_level_id=issue_security_level_id,
        expand=expand,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    issue_security_scheme_id: int,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    issue_security_level_id: Union[Unset, List[int]] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[None, PageBeanIssueSecurityLevelMember]]:
    """Returns issue security level members.

    Only issue security level members in context of classic projects are returned.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        issue_security_scheme_id=issue_security_scheme_id,
        start_at=start_at,
        max_results=max_results,
        issue_security_level_id=issue_security_level_id,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_security_scheme_id: int,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    issue_security_level_id: Union[Unset, List[int]] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[None, PageBeanIssueSecurityLevelMember]]:
    kwargs = _get_kwargs(
        client=client,
        issue_security_scheme_id=issue_security_scheme_id,
        start_at=start_at,
        max_results=max_results,
        issue_security_level_id=issue_security_level_id,
        expand=expand,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    issue_security_scheme_id: int,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    issue_security_level_id: Union[Unset, List[int]] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[None, PageBeanIssueSecurityLevelMember]]:
    """Returns issue security level members.

    Only issue security level members in context of classic projects are returned.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            issue_security_scheme_id=issue_security_scheme_id,
            start_at=start_at,
            max_results=max_results,
            issue_security_level_id=issue_security_level_id,
            expand=expand,
        )
    ).parsed
