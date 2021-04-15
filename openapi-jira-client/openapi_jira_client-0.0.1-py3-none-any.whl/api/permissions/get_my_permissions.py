from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.error_collection import ErrorCollection
from ...models.permissions import Permissions
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    project_key: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    issue_key: Union[Unset, str] = UNSET,
    issue_id: Union[Unset, str] = UNSET,
    permissions: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, str] = UNSET,
    project_configuration_uuid: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/mypermissions".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "projectKey": project_key,
        "projectId": project_id,
        "issueKey": issue_key,
        "issueId": issue_id,
        "permissions": permissions,
        "projectUuid": project_uuid,
        "projectConfigurationUuid": project_configuration_uuid,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[ErrorCollection, Permissions]]:
    if response.status_code == 200:
        response_200 = Permissions.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorCollection.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = ErrorCollection.from_dict(response.json())

        return response_401
    if response.status_code == 404:
        response_404 = ErrorCollection.from_dict(response.json())

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ErrorCollection, Permissions]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    project_key: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    issue_key: Union[Unset, str] = UNSET,
    issue_id: Union[Unset, str] = UNSET,
    permissions: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, str] = UNSET,
    project_configuration_uuid: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorCollection, Permissions]]:
    kwargs = _get_kwargs(
        client=client,
        project_key=project_key,
        project_id=project_id,
        issue_key=issue_key,
        issue_id=issue_id,
        permissions=permissions,
        project_uuid=project_uuid,
        project_configuration_uuid=project_configuration_uuid,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_key: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    issue_key: Union[Unset, str] = UNSET,
    issue_id: Union[Unset, str] = UNSET,
    permissions: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, str] = UNSET,
    project_configuration_uuid: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorCollection, Permissions]]:
    """Returns a list of permissions indicating which permissions the user has. Details of the user's permissions can be obtained in a global, project, or issue context.

    The user is reported as having a project permission:

     *  in the global context, if the user has the project permission in any project.
     *  for a project, where the project permission is determined using issue data, if the user meets the permission's criteria for any issue in the project. Otherwise, if the user has the project permission in the project.
     *  for an issue, where a project permission is determined using issue data, if the user has the permission in the issue. Otherwise, if the user has the project permission in the project containing the issue.

    This means that users may be shown as having an issue permission (such as EDIT\_ISSUES) in the global context or a project context but may not have the permission for any or all issues. For example, if Reporters have the EDIT\_ISSUES permission a user would be shown as having this permission in the global context or the context of a project, because any user can be a reporter. However, if they are not the user who reported the issue queried they would not have EDIT\_ISSUES permission for that issue.

    Global permissions are unaffected by context.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None."""

    return sync_detailed(
        client=client,
        project_key=project_key,
        project_id=project_id,
        issue_key=issue_key,
        issue_id=issue_id,
        permissions=permissions,
        project_uuid=project_uuid,
        project_configuration_uuid=project_configuration_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_key: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    issue_key: Union[Unset, str] = UNSET,
    issue_id: Union[Unset, str] = UNSET,
    permissions: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, str] = UNSET,
    project_configuration_uuid: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorCollection, Permissions]]:
    kwargs = _get_kwargs(
        client=client,
        project_key=project_key,
        project_id=project_id,
        issue_key=issue_key,
        issue_id=issue_id,
        permissions=permissions,
        project_uuid=project_uuid,
        project_configuration_uuid=project_configuration_uuid,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_key: Union[Unset, str] = UNSET,
    project_id: Union[Unset, str] = UNSET,
    issue_key: Union[Unset, str] = UNSET,
    issue_id: Union[Unset, str] = UNSET,
    permissions: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, str] = UNSET,
    project_configuration_uuid: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorCollection, Permissions]]:
    """Returns a list of permissions indicating which permissions the user has. Details of the user's permissions can be obtained in a global, project, or issue context.

    The user is reported as having a project permission:

     *  in the global context, if the user has the project permission in any project.
     *  for a project, where the project permission is determined using issue data, if the user meets the permission's criteria for any issue in the project. Otherwise, if the user has the project permission in the project.
     *  for an issue, where a project permission is determined using issue data, if the user has the permission in the issue. Otherwise, if the user has the project permission in the project containing the issue.

    This means that users may be shown as having an issue permission (such as EDIT\_ISSUES) in the global context or a project context but may not have the permission for any or all issues. For example, if Reporters have the EDIT\_ISSUES permission a user would be shown as having this permission in the global context or the context of a project, because any user can be a reporter. However, if they are not the user who reported the issue queried they would not have EDIT\_ISSUES permission for that issue.

    Global permissions are unaffected by context.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** None."""

    return (
        await asyncio_detailed(
            client=client,
            project_key=project_key,
            project_id=project_id,
            issue_key=issue_key,
            issue_id=issue_id,
            permissions=permissions,
            project_uuid=project_uuid,
            project_configuration_uuid=project_configuration_uuid,
        )
    ).parsed
