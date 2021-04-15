from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.avatar import Avatar
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    x: Union[Unset, int] = 0,
    y: Union[Unset, int] = 0,
    size: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/project/{projectIdOrKey}/avatar2".format(client.base_url, projectIdOrKey=project_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "x": x,
        "y": y,
        "size": size,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Avatar, None]]:
    if response.status_code == 201:
        response_201 = Avatar.from_dict(response.json())

        return response_201
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


def _build_response(*, response: httpx.Response) -> Response[Union[Avatar, None]]:
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
    x: Union[Unset, int] = 0,
    y: Union[Unset, int] = 0,
    size: Union[Unset, int] = UNSET,
) -> Response[Union[Avatar, None]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        x=x,
        y=y,
        size=size,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    x: Union[Unset, int] = 0,
    y: Union[Unset, int] = 0,
    size: Union[Unset, int] = UNSET,
) -> Optional[Union[Avatar, None]]:
    """Loads an avatar for a project.

    Specify the avatar's local file location in the body of the request. Also, include the following headers:

     *  `X-Atlassian-Token: no-check` To prevent XSRF protection blocking the request, for more information see [Special Headers](#special-request-headers).
     *  `Content-Type: image/image type` Valid image types are JPEG, GIF, or PNG.

    For example:
    `curl --request POST `

    `--user email@example.com:<api_token> `

    `--header 'X-Atlassian-Token: no-check' `

    `--header 'Content-Type: image/< image_type>' `

    `--data-binary \"<@/path/to/file/with/your/avatar>\" `

    `--url 'https://your-domain.atlassian.net/rest/api/3/project/{projectIdOrKey}/avatar2'`

    The avatar is cropped to a square. If no crop parameters are specified, the square originates at the top left of the image. The length of the square's sides is set to the smaller of the height or width of the image.

    The cropped image is then used to create avatars of 16x16, 24x24, 32x32, and 48x48 in size.

    After creating the avatar use [Set project avatar](#api-rest-api-3-project-projectIdOrKey-avatar-put) to set it as the project's displayed avatar.

    **[Permissions](#permissions) required:** *Administer projects* [project permission](https://confluence.atlassian.com/x/yodKLg)."""

    return sync_detailed(
        client=client,
        project_id_or_key=project_id_or_key,
        x=x,
        y=y,
        size=size,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    x: Union[Unset, int] = 0,
    y: Union[Unset, int] = 0,
    size: Union[Unset, int] = UNSET,
) -> Response[Union[Avatar, None]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
        x=x,
        y=y,
        size=size,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
    x: Union[Unset, int] = 0,
    y: Union[Unset, int] = 0,
    size: Union[Unset, int] = UNSET,
) -> Optional[Union[Avatar, None]]:
    """Loads an avatar for a project.

    Specify the avatar's local file location in the body of the request. Also, include the following headers:

     *  `X-Atlassian-Token: no-check` To prevent XSRF protection blocking the request, for more information see [Special Headers](#special-request-headers).
     *  `Content-Type: image/image type` Valid image types are JPEG, GIF, or PNG.

    For example:
    `curl --request POST `

    `--user email@example.com:<api_token> `

    `--header 'X-Atlassian-Token: no-check' `

    `--header 'Content-Type: image/< image_type>' `

    `--data-binary \"<@/path/to/file/with/your/avatar>\" `

    `--url 'https://your-domain.atlassian.net/rest/api/3/project/{projectIdOrKey}/avatar2'`

    The avatar is cropped to a square. If no crop parameters are specified, the square originates at the top left of the image. The length of the square's sides is set to the smaller of the height or width of the image.

    The cropped image is then used to create avatars of 16x16, 24x24, 32x32, and 48x48 in size.

    After creating the avatar use [Set project avatar](#api-rest-api-3-project-projectIdOrKey-avatar-put) to set it as the project's displayed avatar.

    **[Permissions](#permissions) required:** *Administer projects* [project permission](https://confluence.atlassian.com/x/yodKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            project_id_or_key=project_id_or_key,
            x=x,
            y=y,
            size=size,
        )
    ).parsed
