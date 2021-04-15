from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.avatar import Avatar
from ...models.store_avatar_type import StoreAvatarType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    type_: StoreAvatarType,
    entity_id: str,
    x: Union[Unset, int] = 0,
    y: Union[Unset, int] = 0,
    size: int,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/universal_avatar/type/{type}/owner/{entityId}".format(
        client.base_url, type=type_, entityId=entity_id
    )

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
    type_: StoreAvatarType,
    entity_id: str,
    x: Union[Unset, int] = 0,
    y: Union[Unset, int] = 0,
    size: int,
) -> Response[Union[Avatar, None]]:
    kwargs = _get_kwargs(
        client=client,
        type_=type_,
        entity_id=entity_id,
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
    type_: StoreAvatarType,
    entity_id: str,
    x: Union[Unset, int] = 0,
    y: Union[Unset, int] = 0,
    size: int,
) -> Optional[Union[Avatar, None]]:
    """Loads a custom avatar for a project or issue type.

    Specify the avatar's local file location in the body of the request. Also, include the following headers:

     *  `X-Atlassian-Token: no-check` To prevent XSRF protection blocking the request, for more information see [Special Headers](#special-request-headers).
     *  `Content-Type: image/image type` Valid image types are JPEG, GIF, or PNG.

    For example:
    `curl --request POST `

    `--user email@example.com:<api_token> `

    `--header 'X-Atlassian-Token: no-check' `

    `--header 'Content-Type: image/< image_type>' `

    `--data-binary \"<@/path/to/file/with/your/avatar>\" `

    `--url 'https://your-domain.atlassian.net/rest/api/3/universal_avatar/type/{type}/owner/{entityId}'`

    The avatar is cropped to a square. If no crop parameters are specified, the square originates at the top left of the image. The length of the square's sides is set to the smaller of the height or width of the image.

    The cropped image is then used to create avatars of 16x16, 24x24, 32x32, and 48x48 in size.

    After creating the avatar use:

     *  [Update issue type](#api-rest-api-3-issuetype-id-put) to set it as the issue type's displayed avatar.
     *  [Set project avatar](#api-rest-api-3-project-projectIdOrKey-avatar-put) to set it as the project's displayed avatar.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        type_=type_,
        entity_id=entity_id,
        x=x,
        y=y,
        size=size,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    type_: StoreAvatarType,
    entity_id: str,
    x: Union[Unset, int] = 0,
    y: Union[Unset, int] = 0,
    size: int,
) -> Response[Union[Avatar, None]]:
    kwargs = _get_kwargs(
        client=client,
        type_=type_,
        entity_id=entity_id,
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
    type_: StoreAvatarType,
    entity_id: str,
    x: Union[Unset, int] = 0,
    y: Union[Unset, int] = 0,
    size: int,
) -> Optional[Union[Avatar, None]]:
    """Loads a custom avatar for a project or issue type.

    Specify the avatar's local file location in the body of the request. Also, include the following headers:

     *  `X-Atlassian-Token: no-check` To prevent XSRF protection blocking the request, for more information see [Special Headers](#special-request-headers).
     *  `Content-Type: image/image type` Valid image types are JPEG, GIF, or PNG.

    For example:
    `curl --request POST `

    `--user email@example.com:<api_token> `

    `--header 'X-Atlassian-Token: no-check' `

    `--header 'Content-Type: image/< image_type>' `

    `--data-binary \"<@/path/to/file/with/your/avatar>\" `

    `--url 'https://your-domain.atlassian.net/rest/api/3/universal_avatar/type/{type}/owner/{entityId}'`

    The avatar is cropped to a square. If no crop parameters are specified, the square originates at the top left of the image. The length of the square's sides is set to the smaller of the height or width of the image.

    The cropped image is then used to create avatars of 16x16, 24x24, 32x32, and 48x48 in size.

    After creating the avatar use:

     *  [Update issue type](#api-rest-api-3-issuetype-id-put) to set it as the issue type's displayed avatar.
     *  [Set project avatar](#api-rest-api-3-project-projectIdOrKey-avatar-put) to set it as the project's displayed avatar.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            type_=type_,
            entity_id=entity_id,
            x=x,
            y=y,
            size=size,
        )
    ).parsed
