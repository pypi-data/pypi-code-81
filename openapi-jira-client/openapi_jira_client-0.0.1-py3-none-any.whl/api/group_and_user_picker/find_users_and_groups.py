from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.find_users_and_groups_avatar_size import FindUsersAndGroupsAvatarSize
from ...models.found_users_and_groups import FoundUsersAndGroups
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    query: str,
    max_results: Union[Unset, int] = 50,
    show_avatar: Union[Unset, bool] = False,
    field_id: Union[Unset, str] = UNSET,
    project_id: Union[Unset, List[str]] = UNSET,
    issue_type_id: Union[Unset, List[str]] = UNSET,
    avatar_size: Union[Unset, FindUsersAndGroupsAvatarSize] = FindUsersAndGroupsAvatarSize.XSMALL,
    case_insensitive: Union[Unset, bool] = False,
    exclude_connect_addons: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/groupuserpicker".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_project_id: Union[Unset, List[str]] = UNSET
    if not isinstance(project_id, Unset):
        json_project_id = project_id

    json_issue_type_id: Union[Unset, List[str]] = UNSET
    if not isinstance(issue_type_id, Unset):
        json_issue_type_id = issue_type_id

    json_avatar_size: Union[Unset, str] = UNSET
    if not isinstance(avatar_size, Unset):
        json_avatar_size = avatar_size.value

    params: Dict[str, Any] = {
        "query": query,
        "maxResults": max_results,
        "showAvatar": show_avatar,
        "fieldId": field_id,
        "projectId": json_project_id,
        "issueTypeId": json_issue_type_id,
        "avatarSize": json_avatar_size,
        "caseInsensitive": case_insensitive,
        "excludeConnectAddons": exclude_connect_addons,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[FoundUsersAndGroups, None]]:
    if response.status_code == 200:
        response_200 = FoundUsersAndGroups.from_dict(response.json())

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
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[FoundUsersAndGroups, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    query: str,
    max_results: Union[Unset, int] = 50,
    show_avatar: Union[Unset, bool] = False,
    field_id: Union[Unset, str] = UNSET,
    project_id: Union[Unset, List[str]] = UNSET,
    issue_type_id: Union[Unset, List[str]] = UNSET,
    avatar_size: Union[Unset, FindUsersAndGroupsAvatarSize] = FindUsersAndGroupsAvatarSize.XSMALL,
    case_insensitive: Union[Unset, bool] = False,
    exclude_connect_addons: Union[Unset, bool] = False,
) -> Response[Union[FoundUsersAndGroups, None]]:
    kwargs = _get_kwargs(
        client=client,
        query=query,
        max_results=max_results,
        show_avatar=show_avatar,
        field_id=field_id,
        project_id=project_id,
        issue_type_id=issue_type_id,
        avatar_size=avatar_size,
        case_insensitive=case_insensitive,
        exclude_connect_addons=exclude_connect_addons,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    query: str,
    max_results: Union[Unset, int] = 50,
    show_avatar: Union[Unset, bool] = False,
    field_id: Union[Unset, str] = UNSET,
    project_id: Union[Unset, List[str]] = UNSET,
    issue_type_id: Union[Unset, List[str]] = UNSET,
    avatar_size: Union[Unset, FindUsersAndGroupsAvatarSize] = FindUsersAndGroupsAvatarSize.XSMALL,
    case_insensitive: Union[Unset, bool] = False,
    exclude_connect_addons: Union[Unset, bool] = False,
) -> Optional[Union[FoundUsersAndGroups, None]]:
    """Returns a list of users and groups matching a string. The string is used:

     *  for users, to find a case-insensitive match with display name and e-mail address. Note that if a user has hidden their email address in their user profile, partial matches of the email address will not find the user. An exact match is required.
     *  for groups, to find a case-sensitive match with group name.

    For example, if the string *tin* is used, records with the display name *Tina*, email address *sarah@tinplatetraining.com*, and the group *accounting* would be returned.

    Optionally, the search can be refined to:

     *  the projects and issue types associated with a custom field, such as a user picker. The search can then be further refined to return only users and groups that have permission to view specific:

         *  projects.
         *  issue types.

        If multiple projects or issue types are specified, they must be a subset of those enabled for the custom field or no results are returned. For example, if a field is enabled for projects A, B, and C then the search could be limited to projects B and C. However, if the search is limited to projects B and D, nothing is returned.
     *  not return Connect app users and groups.
     *  return groups that have a case-insensitive match with the query.

    The primary use case for this resource is to populate a picker field suggestion list with users or groups. To this end, the returned object includes an `html` field for each list. This field highlights the matched query term in the item name with the HTML strong tag. Also, each list is wrapped in a response object that contains a header for use in a picker, specifically *Showing X of Y matching groups*.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Browse users and groups* [global permission](https://confluence.atlassian.com/x/yodKLg)."""

    return sync_detailed(
        client=client,
        query=query,
        max_results=max_results,
        show_avatar=show_avatar,
        field_id=field_id,
        project_id=project_id,
        issue_type_id=issue_type_id,
        avatar_size=avatar_size,
        case_insensitive=case_insensitive,
        exclude_connect_addons=exclude_connect_addons,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    query: str,
    max_results: Union[Unset, int] = 50,
    show_avatar: Union[Unset, bool] = False,
    field_id: Union[Unset, str] = UNSET,
    project_id: Union[Unset, List[str]] = UNSET,
    issue_type_id: Union[Unset, List[str]] = UNSET,
    avatar_size: Union[Unset, FindUsersAndGroupsAvatarSize] = FindUsersAndGroupsAvatarSize.XSMALL,
    case_insensitive: Union[Unset, bool] = False,
    exclude_connect_addons: Union[Unset, bool] = False,
) -> Response[Union[FoundUsersAndGroups, None]]:
    kwargs = _get_kwargs(
        client=client,
        query=query,
        max_results=max_results,
        show_avatar=show_avatar,
        field_id=field_id,
        project_id=project_id,
        issue_type_id=issue_type_id,
        avatar_size=avatar_size,
        case_insensitive=case_insensitive,
        exclude_connect_addons=exclude_connect_addons,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    query: str,
    max_results: Union[Unset, int] = 50,
    show_avatar: Union[Unset, bool] = False,
    field_id: Union[Unset, str] = UNSET,
    project_id: Union[Unset, List[str]] = UNSET,
    issue_type_id: Union[Unset, List[str]] = UNSET,
    avatar_size: Union[Unset, FindUsersAndGroupsAvatarSize] = FindUsersAndGroupsAvatarSize.XSMALL,
    case_insensitive: Union[Unset, bool] = False,
    exclude_connect_addons: Union[Unset, bool] = False,
) -> Optional[Union[FoundUsersAndGroups, None]]:
    """Returns a list of users and groups matching a string. The string is used:

     *  for users, to find a case-insensitive match with display name and e-mail address. Note that if a user has hidden their email address in their user profile, partial matches of the email address will not find the user. An exact match is required.
     *  for groups, to find a case-sensitive match with group name.

    For example, if the string *tin* is used, records with the display name *Tina*, email address *sarah@tinplatetraining.com*, and the group *accounting* would be returned.

    Optionally, the search can be refined to:

     *  the projects and issue types associated with a custom field, such as a user picker. The search can then be further refined to return only users and groups that have permission to view specific:

         *  projects.
         *  issue types.

        If multiple projects or issue types are specified, they must be a subset of those enabled for the custom field or no results are returned. For example, if a field is enabled for projects A, B, and C then the search could be limited to projects B and C. However, if the search is limited to projects B and D, nothing is returned.
     *  not return Connect app users and groups.
     *  return groups that have a case-insensitive match with the query.

    The primary use case for this resource is to populate a picker field suggestion list with users or groups. To this end, the returned object includes an `html` field for each list. This field highlights the matched query term in the item name with the HTML strong tag. Also, each list is wrapped in a response object that contains a header for use in a picker, specifically *Showing X of Y matching groups*.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Browse users and groups* [global permission](https://confluence.atlassian.com/x/yodKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            query=query,
            max_results=max_results,
            show_avatar=show_avatar,
            field_id=field_id,
            project_id=project_id,
            issue_type_id=issue_type_id,
            avatar_size=avatar_size,
            case_insensitive=case_insensitive,
            exclude_connect_addons=exclude_connect_addons,
        )
    ).parsed
