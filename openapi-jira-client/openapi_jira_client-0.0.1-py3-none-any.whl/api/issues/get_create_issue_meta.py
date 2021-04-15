from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.issue_create_metadata import IssueCreateMetadata
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    project_ids: Union[Unset, List[str]] = UNSET,
    project_keys: Union[Unset, List[str]] = UNSET,
    issuetype_ids: Union[Unset, List[str]] = UNSET,
    issuetype_names: Union[Unset, List[str]] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/createmeta".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_project_ids: Union[Unset, List[str]] = UNSET
    if not isinstance(project_ids, Unset):
        json_project_ids = project_ids

    json_project_keys: Union[Unset, List[str]] = UNSET
    if not isinstance(project_keys, Unset):
        json_project_keys = project_keys

    json_issuetype_ids: Union[Unset, List[str]] = UNSET
    if not isinstance(issuetype_ids, Unset):
        json_issuetype_ids = issuetype_ids

    json_issuetype_names: Union[Unset, List[str]] = UNSET
    if not isinstance(issuetype_names, Unset):
        json_issuetype_names = issuetype_names

    params: Dict[str, Any] = {
        "projectIds": json_project_ids,
        "projectKeys": json_project_keys,
        "issuetypeIds": json_issuetype_ids,
        "issuetypeNames": json_issuetype_names,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[IssueCreateMetadata, None]]:
    if response.status_code == 200:
        response_200 = IssueCreateMetadata.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[IssueCreateMetadata, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    project_ids: Union[Unset, List[str]] = UNSET,
    project_keys: Union[Unset, List[str]] = UNSET,
    issuetype_ids: Union[Unset, List[str]] = UNSET,
    issuetype_names: Union[Unset, List[str]] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[IssueCreateMetadata, None]]:
    kwargs = _get_kwargs(
        client=client,
        project_ids=project_ids,
        project_keys=project_keys,
        issuetype_ids=issuetype_ids,
        issuetype_names=issuetype_names,
        expand=expand,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_ids: Union[Unset, List[str]] = UNSET,
    project_keys: Union[Unset, List[str]] = UNSET,
    issuetype_ids: Union[Unset, List[str]] = UNSET,
    issuetype_names: Union[Unset, List[str]] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[IssueCreateMetadata, None]]:
    """Returns details of projects, issue types within projects, and, when requested, the create screen fields for each issue type for the user. Use the information to populate the requests in [ Create issue](#api-rest-api-3-issue-post) and [Create issues](#api-rest-api-3-issue-bulk-post).

    The request can be restricted to specific projects or issue types using the query parameters. The response will contain information for the valid projects, issue types, or project and issue type combinations requested. Note that invalid project, issue type, or project and issue type combinations do not generate errors.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Create issues* [project permission](https://confluence.atlassian.com/x/yodKLg) in the requested projects."""

    return sync_detailed(
        client=client,
        project_ids=project_ids,
        project_keys=project_keys,
        issuetype_ids=issuetype_ids,
        issuetype_names=issuetype_names,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_ids: Union[Unset, List[str]] = UNSET,
    project_keys: Union[Unset, List[str]] = UNSET,
    issuetype_ids: Union[Unset, List[str]] = UNSET,
    issuetype_names: Union[Unset, List[str]] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[IssueCreateMetadata, None]]:
    kwargs = _get_kwargs(
        client=client,
        project_ids=project_ids,
        project_keys=project_keys,
        issuetype_ids=issuetype_ids,
        issuetype_names=issuetype_names,
        expand=expand,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_ids: Union[Unset, List[str]] = UNSET,
    project_keys: Union[Unset, List[str]] = UNSET,
    issuetype_ids: Union[Unset, List[str]] = UNSET,
    issuetype_names: Union[Unset, List[str]] = UNSET,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[IssueCreateMetadata, None]]:
    """Returns details of projects, issue types within projects, and, when requested, the create screen fields for each issue type for the user. Use the information to populate the requests in [ Create issue](#api-rest-api-3-issue-post) and [Create issues](#api-rest-api-3-issue-bulk-post).

    The request can be restricted to specific projects or issue types using the query parameters. The response will contain information for the valid projects, issue types, or project and issue type combinations requested. Note that invalid project, issue type, or project and issue type combinations do not generate errors.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Create issues* [project permission](https://confluence.atlassian.com/x/yodKLg) in the requested projects."""

    return (
        await asyncio_detailed(
            client=client,
            project_ids=project_ids,
            project_keys=project_keys,
            issuetype_ids=issuetype_ids,
            issuetype_names=issuetype_names,
            expand=expand,
        )
    ).parsed
