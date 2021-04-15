from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.project_role_details import ProjectRoleDetails
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    current_member: Union[Unset, bool] = False,
    exclude_connect_addons: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/project/{projectIdOrKey}/roledetails".format(client.base_url, projectIdOrKey=project_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "currentMember": current_member,
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[List[ProjectRoleDetails], None]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ProjectRoleDetails.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[List[ProjectRoleDetails], None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    current_member: Union[Unset, bool] = False,
    exclude_connect_addons: Union[Unset, bool] = False,
) -> Response[Union[List[ProjectRoleDetails], None]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        current_member=current_member,
        exclude_connect_addons=exclude_connect_addons,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    current_member: Union[Unset, bool] = False,
    exclude_connect_addons: Union[Unset, bool] = False,
) -> Optional[Union[List[ProjectRoleDetails], None]]:
    """Returns all [project roles](https://confluence.atlassian.com/x/3odKLg) and the details for each role. Note that the list of project roles is common to all projects.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg) or *Administer projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project."""

    return sync_detailed(
        client=client,
        project_id_or_key=project_id_or_key,
        current_member=current_member,
        exclude_connect_addons=exclude_connect_addons,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    current_member: Union[Unset, bool] = False,
    exclude_connect_addons: Union[Unset, bool] = False,
) -> Response[Union[List[ProjectRoleDetails], None]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        current_member=current_member,
        exclude_connect_addons=exclude_connect_addons,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    current_member: Union[Unset, bool] = False,
    exclude_connect_addons: Union[Unset, bool] = False,
) -> Optional[Union[List[ProjectRoleDetails], None]]:
    """Returns all [project roles](https://confluence.atlassian.com/x/3odKLg) and the details for each role. Note that the list of project roles is common to all projects.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg) or *Administer projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project."""

    return (
        await asyncio_detailed(
            client=client,
            project_id_or_key=project_id_or_key,
            current_member=current_member,
            exclude_connect_addons=exclude_connect_addons,
        )
    ).parsed
