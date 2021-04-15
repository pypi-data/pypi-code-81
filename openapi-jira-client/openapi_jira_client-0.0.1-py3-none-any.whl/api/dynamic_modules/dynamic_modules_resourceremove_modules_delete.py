from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.error_message import ErrorMessage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    module_key: Union[Unset, List[str]] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/atlassian-connect/1/app/module/dynamic".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_module_key: Union[Unset, List[str]] = UNSET
    if not isinstance(module_key, Unset):
        json_module_key = module_key

    params: Dict[str, Any] = {
        "moduleKey": json_module_key,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[ErrorMessage, None]]:
    if response.status_code == 204:
        response_204 = None

        return response_204
    if response.status_code == 401:
        response_401 = ErrorMessage.from_dict(response.json())

        return response_401
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ErrorMessage, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    module_key: Union[Unset, List[str]] = UNSET,
) -> Response[Union[ErrorMessage, None]]:
    kwargs = _get_kwargs(
        client=client,
        module_key=module_key,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    module_key: Union[Unset, List[str]] = UNSET,
) -> Optional[Union[ErrorMessage, None]]:
    """Remove all or a list of modules registered by the calling app.

    **[Permissions](#permissions) required:** Only Connect apps can make this request."""

    return sync_detailed(
        client=client,
        module_key=module_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    module_key: Union[Unset, List[str]] = UNSET,
) -> Response[Union[ErrorMessage, None]]:
    kwargs = _get_kwargs(
        client=client,
        module_key=module_key,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    module_key: Union[Unset, List[str]] = UNSET,
) -> Optional[Union[ErrorMessage, None]]:
    """Remove all or a list of modules registered by the calling app.

    **[Permissions](#permissions) required:** Only Connect apps can make this request."""

    return (
        await asyncio_detailed(
            client=client,
            module_key=module_key,
        )
    ).parsed
