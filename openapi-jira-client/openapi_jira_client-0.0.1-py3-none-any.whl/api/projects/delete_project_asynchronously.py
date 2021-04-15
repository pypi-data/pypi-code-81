from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.task_progress_bean_object import TaskProgressBeanObject
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/project/{projectIdOrKey}/delete".format(client.base_url, projectIdOrKey=project_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, TaskProgressBeanObject]]:
    if response.status_code == 303:
        response_303 = TaskProgressBeanObject.from_dict(response.json())

        return response_303
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
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
    project_id_or_key: str,
) -> Response[Union[None, TaskProgressBeanObject]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
) -> Optional[Union[None, TaskProgressBeanObject]]:
    """Deletes a project asynchronously.

    This operation is:

     *  transactional, that is, if part of the delete fails the project is not deleted.
     *  [asynchronous](#async). Follow the `location` link in the response to determine the status of the task and use [Get task](#api-rest-api-3-task-taskId-get) to obtain subsequent updates.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        project_id_or_key=project_id_or_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
) -> Response[Union[None, TaskProgressBeanObject]]:
    kwargs = _get_kwargs(
        client=client,
        project_id_or_key=project_id_or_key,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id_or_key: str,
) -> Optional[Union[None, TaskProgressBeanObject]]:
    """Deletes a project asynchronously.

    This operation is:

     *  transactional, that is, if part of the delete fails the project is not deleted.
     *  [asynchronous](#async). Follow the `location` link in the response to determine the status of the task and use [Get task](#api-rest-api-3-task-taskId-get) to obtain subsequent updates.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            project_id_or_key=project_id_or_key,
        )
    ).parsed
