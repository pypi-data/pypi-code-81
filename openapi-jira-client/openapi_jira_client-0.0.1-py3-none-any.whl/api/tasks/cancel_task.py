from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    task_id: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/task/{taskId}/cancel".format(client.base_url, taskId=task_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[List[str], None]]:
    if response.status_code == 202:
        response_202 = None

        return response_202
    if response.status_code == 400:
        response_400 = cast(List[str], response.json())

        return response_400
    if response.status_code == 401:
        response_401 = cast(List[str], response.json())

        return response_401
    if response.status_code == 403:
        response_403 = cast(List[str], response.json())

        return response_403
    if response.status_code == 404:
        response_404 = cast(List[str], response.json())

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[List[str], None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    task_id: str,
) -> Response[Union[List[str], None]]:
    kwargs = _get_kwargs(
        client=client,
        task_id=task_id,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    task_id: str,
) -> Optional[Union[List[str], None]]:
    """Cancels a task.

    **[Permissions](#permissions) required:** either of:

     *  *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg).
     *  Creator of the task."""

    return sync_detailed(
        client=client,
        task_id=task_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    task_id: str,
) -> Response[Union[List[str], None]]:
    kwargs = _get_kwargs(
        client=client,
        task_id=task_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    task_id: str,
) -> Optional[Union[List[str], None]]:
    """Cancels a task.

    **[Permissions](#permissions) required:** either of:

     *  *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg).
     *  Creator of the task."""

    return (
        await asyncio_detailed(
            client=client,
            task_id=task_id,
        )
    ).parsed
