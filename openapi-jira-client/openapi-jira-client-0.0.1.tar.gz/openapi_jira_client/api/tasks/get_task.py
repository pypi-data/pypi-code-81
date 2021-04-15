from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.task_progress_bean_object import TaskProgressBeanObject
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    task_id: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/task/{taskId}".format(client.base_url, taskId=task_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, TaskProgressBeanObject]]:
    if response.status_code == 200:
        response_200 = TaskProgressBeanObject.from_dict(response.json())

        return response_200
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


def _build_response(*, response: httpx.Response) -> Response[Union[None, TaskProgressBeanObject]]:
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
) -> Response[Union[None, TaskProgressBeanObject]]:
    kwargs = _get_kwargs(
        client=client,
        task_id=task_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    task_id: str,
) -> Optional[Union[None, TaskProgressBeanObject]]:
    """Returns the status of a [long-running asynchronous task](#async).

    When a task has finished, this operation returns the JSON blob applicable to the task. See the documentation of the operation that created the task for details. Task details are not permanently retained. As of September 2019, details are retained for 14 days although this period may change without notice.

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
) -> Response[Union[None, TaskProgressBeanObject]]:
    kwargs = _get_kwargs(
        client=client,
        task_id=task_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    task_id: str,
) -> Optional[Union[None, TaskProgressBeanObject]]:
    """Returns the status of a [long-running asynchronous task](#async).

    When a task has finished, this operation returns the JSON blob applicable to the task. See the documentation of the operation that created the task for details. Task details are not permanently retained. As of September 2019, details are retained for 14 days although this period may change without notice.

    **[Permissions](#permissions) required:** either of:

     *  *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg).
     *  Creator of the task."""

    return (
        await asyncio_detailed(
            client=client,
            task_id=task_id,
        )
    ).parsed
