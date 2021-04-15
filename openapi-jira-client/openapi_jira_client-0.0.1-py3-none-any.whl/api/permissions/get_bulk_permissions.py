from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.bulk_permission_grants import BulkPermissionGrants
from ...models.bulk_permissions_request_bean import BulkPermissionsRequestBean
from ...models.error_collection import ErrorCollection
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: BulkPermissionsRequestBean,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/permissions/check".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[BulkPermissionGrants, ErrorCollection]]:
    if response.status_code == 200:
        response_200 = BulkPermissionGrants.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorCollection.from_dict(response.json())

        return response_400
    if response.status_code == 403:
        response_403 = ErrorCollection.from_dict(response.json())

        return response_403
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[BulkPermissionGrants, ErrorCollection]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: BulkPermissionsRequestBean,
) -> Response[Union[BulkPermissionGrants, ErrorCollection]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: BulkPermissionsRequestBean,
) -> Optional[Union[BulkPermissionGrants, ErrorCollection]]:
    """Returns:

     *  for a list of global permissions, the global permissions granted to a user.
     *  for a list of project permissions and lists of projects and issues, for each project permission a list of the projects and issues a user can access or manipulate.

    If no account ID is provided, the operation returns details for the logged in user.

    Note that:

     *  Invalid project and issue IDs are ignored.
     *  A maximum of 1000 projects and 1000 issues can be checked.
     *  Null values in `globalPermissions`, `projectPermissions`, `projectPermissions.projects`, and `projectPermissions.issues` are ignored.
     *  Empty strings in `projectPermissions.permissions` are ignored.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg) to check the permissions for other users, otherwise none. However, Connect apps can make a call from the app server to the product to obtain permission details for any user, without admin permission. This Connect app ability doesn't apply to calls made using AP.request() in a browser."""

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: BulkPermissionsRequestBean,
) -> Response[Union[BulkPermissionGrants, ErrorCollection]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: BulkPermissionsRequestBean,
) -> Optional[Union[BulkPermissionGrants, ErrorCollection]]:
    """Returns:

     *  for a list of global permissions, the global permissions granted to a user.
     *  for a list of project permissions and lists of projects and issues, for each project permission a list of the projects and issues a user can access or manipulate.

    If no account ID is provided, the operation returns details for the logged in user.

    Note that:

     *  Invalid project and issue IDs are ignored.
     *  A maximum of 1000 projects and 1000 issues can be checked.
     *  Null values in `globalPermissions`, `projectPermissions`, `projectPermissions.projects`, and `projectPermissions.issues` are ignored.
     *  Empty strings in `projectPermissions.permissions` are ignored.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg) to check the permissions for other users, otherwise none. However, Connect apps can make a call from the app server to the product to obtain permission details for any user, without admin permission. This Connect app ability doesn't apply to calls made using AP.request() in a browser."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
