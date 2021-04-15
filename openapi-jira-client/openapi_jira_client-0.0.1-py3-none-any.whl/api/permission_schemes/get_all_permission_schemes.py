from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.permission_schemes import PermissionSchemes
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    expand: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/permissionscheme".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, PermissionSchemes]]:
    if response.status_code == 200:
        response_200 = PermissionSchemes.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, PermissionSchemes]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[None, PermissionSchemes]]:
    kwargs = _get_kwargs(
        client=client,
        expand=expand,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[None, PermissionSchemes]]:
    """Returns all permission schemes.

    ### About permission schemes and grants ###

    A permission scheme is a collection of permission grants. A permission grant consists of a `holder` and a `permission`.

    #### Holder object ####

    The `holder` object contains information about the user or group being granted the permission. For example, the *Administer projects* permission is granted to a group named *Teams in space administrators*. In this case, the type is `\"type\": \"group\"`, and the parameter is the group name, `\"parameter\": \"Teams in space administrators\"`. The `holder` object is defined by the following properties:

     *  `type` Identifies the user or group (see the list of types below).
     *  `parameter` The value of this property depends on the `type`. For example, if the `type` is a group, then you need to specify the group name.

    The following `types` are available. The expected values for the `parameter` are given in parenthesis (some `types` may not have a `parameter`):

     *  `anyone` Grant for anonymous users.
     *  `applicationRole` Grant for users with access to the specified application (application name). See [Update product access settings](https://confluence.atlassian.com/x/3YxjL) for more information.
     *  `assignee` Grant for the user currently assigned to an issue.
     *  `group` Grant for the specified group (group name).
     *  `groupCustomField` Grant for a user in the group selected in the specified custom field (custom field ID).
     *  `projectLead` Grant for a project lead.
     *  `projectRole` Grant for the specified project role (project role ID).
     *  `reporter` Grant for the user who reported the issue.
     *  `sd.customer.portal.only` Jira Service Desk only. Grants customers permission to access the customer portal but not Jira. See [Customizing Jira Service Desk permissions](https://confluence.atlassian.com/x/24dKLg) for more information.
     *  `user` Grant for the specified user (user ID - historically this was the userkey but that is deprecated and the account ID should be used).
     *  `userCustomField` Grant for a user selected in the specified custom field (custom field ID).

    #### Built-in permissions ####

    The [built-in Jira permissions](https://confluence.atlassian.com/x/yodKLg) are listed below. Apps can also define custom permissions. See the [project permission](https://developer.atlassian.com/cloud/jira/platform/modules/project-permission/) and [global permission](https://developer.atlassian.com/cloud/jira/platform/modules/global-permission/) module documentation for more information.

    **Project permissions**

     *  `ADMINISTER_PROJECTS`
     *  `BROWSE_PROJECTS`
     *  `MANAGE_SPRINTS_PERMISSION` (Jira Software only)
     *  `SERVICEDESK_AGENT` (Jira Service Desk only)
     *  `VIEW_DEV_TOOLS` (Jira Software only)
     *  `VIEW_READONLY_WORKFLOW`

    **Issue permissions**

     *  `ASSIGNABLE_USER`
     *  `ASSIGN_ISSUES`
     *  `CLOSE_ISSUES`
     *  `CREATE_ISSUES`
     *  `DELETE_ISSUES`
     *  `EDIT_ISSUES`
     *  `LINK_ISSUES`
     *  `MODIFY_REPORTER`
     *  `MOVE_ISSUES`
     *  `RESOLVE_ISSUES`
     *  `SCHEDULE_ISSUES`
     *  `SET_ISSUE_SECURITY`
     *  `TRANSITION_ISSUES`

    **Voters and watchers permissions**

     *  `MANAGE_WATCHERS`
     *  `VIEW_VOTERS_AND_WATCHERS`

    **Comments permissions**

     *  `ADD_COMMENTS`
     *  `DELETE_ALL_COMMENTS`
     *  `DELETE_OWN_COMMENTS`
     *  `EDIT_ALL_COMMENTS`
     *  `EDIT_OWN_COMMENTS`

    **Attachments permissions**

     *  `CREATE_ATTACHMENTS`
     *  `DELETE_ALL_ATTACHMENTS`
     *  `DELETE_OWN_ATTACHMENTS`

    **Time tracking permissions**

     *  `DELETE_ALL_WORKLOGS`
     *  `DELETE_OWN_WORKLOGS`
     *  `EDIT_ALL_WORKLOGS`
     *  `EDIT_OWN_WORKLOGS`
     *  `WORK_ON_ISSUES`

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return sync_detailed(
        client=client,
        expand=expand,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    expand: Union[Unset, str] = UNSET,
) -> Response[Union[None, PermissionSchemes]]:
    kwargs = _get_kwargs(
        client=client,
        expand=expand,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    expand: Union[Unset, str] = UNSET,
) -> Optional[Union[None, PermissionSchemes]]:
    """Returns all permission schemes.

    ### About permission schemes and grants ###

    A permission scheme is a collection of permission grants. A permission grant consists of a `holder` and a `permission`.

    #### Holder object ####

    The `holder` object contains information about the user or group being granted the permission. For example, the *Administer projects* permission is granted to a group named *Teams in space administrators*. In this case, the type is `\"type\": \"group\"`, and the parameter is the group name, `\"parameter\": \"Teams in space administrators\"`. The `holder` object is defined by the following properties:

     *  `type` Identifies the user or group (see the list of types below).
     *  `parameter` The value of this property depends on the `type`. For example, if the `type` is a group, then you need to specify the group name.

    The following `types` are available. The expected values for the `parameter` are given in parenthesis (some `types` may not have a `parameter`):

     *  `anyone` Grant for anonymous users.
     *  `applicationRole` Grant for users with access to the specified application (application name). See [Update product access settings](https://confluence.atlassian.com/x/3YxjL) for more information.
     *  `assignee` Grant for the user currently assigned to an issue.
     *  `group` Grant for the specified group (group name).
     *  `groupCustomField` Grant for a user in the group selected in the specified custom field (custom field ID).
     *  `projectLead` Grant for a project lead.
     *  `projectRole` Grant for the specified project role (project role ID).
     *  `reporter` Grant for the user who reported the issue.
     *  `sd.customer.portal.only` Jira Service Desk only. Grants customers permission to access the customer portal but not Jira. See [Customizing Jira Service Desk permissions](https://confluence.atlassian.com/x/24dKLg) for more information.
     *  `user` Grant for the specified user (user ID - historically this was the userkey but that is deprecated and the account ID should be used).
     *  `userCustomField` Grant for a user selected in the specified custom field (custom field ID).

    #### Built-in permissions ####

    The [built-in Jira permissions](https://confluence.atlassian.com/x/yodKLg) are listed below. Apps can also define custom permissions. See the [project permission](https://developer.atlassian.com/cloud/jira/platform/modules/project-permission/) and [global permission](https://developer.atlassian.com/cloud/jira/platform/modules/global-permission/) module documentation for more information.

    **Project permissions**

     *  `ADMINISTER_PROJECTS`
     *  `BROWSE_PROJECTS`
     *  `MANAGE_SPRINTS_PERMISSION` (Jira Software only)
     *  `SERVICEDESK_AGENT` (Jira Service Desk only)
     *  `VIEW_DEV_TOOLS` (Jira Software only)
     *  `VIEW_READONLY_WORKFLOW`

    **Issue permissions**

     *  `ASSIGNABLE_USER`
     *  `ASSIGN_ISSUES`
     *  `CLOSE_ISSUES`
     *  `CREATE_ISSUES`
     *  `DELETE_ISSUES`
     *  `EDIT_ISSUES`
     *  `LINK_ISSUES`
     *  `MODIFY_REPORTER`
     *  `MOVE_ISSUES`
     *  `RESOLVE_ISSUES`
     *  `SCHEDULE_ISSUES`
     *  `SET_ISSUE_SECURITY`
     *  `TRANSITION_ISSUES`

    **Voters and watchers permissions**

     *  `MANAGE_WATCHERS`
     *  `VIEW_VOTERS_AND_WATCHERS`

    **Comments permissions**

     *  `ADD_COMMENTS`
     *  `DELETE_ALL_COMMENTS`
     *  `DELETE_OWN_COMMENTS`
     *  `EDIT_ALL_COMMENTS`
     *  `EDIT_OWN_COMMENTS`

    **Attachments permissions**

     *  `CREATE_ATTACHMENTS`
     *  `DELETE_ALL_ATTACHMENTS`
     *  `DELETE_OWN_ATTACHMENTS`

    **Time tracking permissions**

     *  `DELETE_ALL_WORKLOGS`
     *  `DELETE_OWN_WORKLOGS`
     *  `EDIT_ALL_WORKLOGS`
     *  `EDIT_OWN_WORKLOGS`
     *  `WORK_ON_ISSUES`

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return (
        await asyncio_detailed(
            client=client,
            expand=expand,
        )
    ).parsed
