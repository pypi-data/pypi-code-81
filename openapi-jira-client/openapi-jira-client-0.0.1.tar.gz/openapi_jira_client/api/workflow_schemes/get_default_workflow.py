from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.default_workflow import DefaultWorkflow
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id_: int,
    return_draft_if_exists: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/workflowscheme/{id}/default".format(client.base_url, id=id_)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "returnDraftIfExists": return_draft_if_exists,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[DefaultWorkflow, None]]:
    if response.status_code == 200:
        response_200 = DefaultWorkflow.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[DefaultWorkflow, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    id_: int,
    return_draft_if_exists: Union[Unset, bool] = False,
) -> Response[Union[DefaultWorkflow, None]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        return_draft_if_exists=return_draft_if_exists,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id_: int,
    return_draft_if_exists: Union[Unset, bool] = False,
) -> Optional[Union[DefaultWorkflow, None]]:
    """Returns the default workflow for a workflow scheme. The default workflow is the workflow that is assigned any issue types that have not been mapped to any other workflow. The default workflow has *All Unassigned Issue Types* listed in its issue types for the workflow scheme in Jira.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        id_=id_,
        return_draft_if_exists=return_draft_if_exists,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id_: int,
    return_draft_if_exists: Union[Unset, bool] = False,
) -> Response[Union[DefaultWorkflow, None]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        return_draft_if_exists=return_draft_if_exists,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id_: int,
    return_draft_if_exists: Union[Unset, bool] = False,
) -> Optional[Union[DefaultWorkflow, None]]:
    """Returns the default workflow for a workflow scheme. The default workflow is the workflow that is assigned any issue types that have not been mapped to any other workflow. The default workflow has *All Unassigned Issue Types* listed in its issue types for the workflow scheme in Jira.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            id_=id_,
            return_draft_if_exists=return_draft_if_exists,
        )
    ).parsed
