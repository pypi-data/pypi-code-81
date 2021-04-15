from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.workflow_scheme import WorkflowScheme
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id_: int,
    update_draft_if_needed: Union[Unset, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/workflowscheme/{id}/default".format(client.base_url, id=id_)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "updateDraftIfNeeded": update_draft_if_needed,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, WorkflowScheme]]:
    if response.status_code == 200:
        response_200 = WorkflowScheme.from_dict(response.json())

        return response_200
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


def _build_response(*, response: httpx.Response) -> Response[Union[None, WorkflowScheme]]:
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
    update_draft_if_needed: Union[Unset, bool] = UNSET,
) -> Response[Union[None, WorkflowScheme]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        update_draft_if_needed=update_draft_if_needed,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id_: int,
    update_draft_if_needed: Union[Unset, bool] = UNSET,
) -> Optional[Union[None, WorkflowScheme]]:
    """Resets the default workflow for a workflow scheme. That is, the default workflow is set to Jira's system workflow (the *jira* workflow).

    Note that active workflow schemes cannot be edited. If the workflow scheme is active, set `updateDraftIfNeeded` to `true` and a draft workflow scheme is created or updated with the default workflow reset. The draft workflow scheme can be published in Jira.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        id_=id_,
        update_draft_if_needed=update_draft_if_needed,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id_: int,
    update_draft_if_needed: Union[Unset, bool] = UNSET,
) -> Response[Union[None, WorkflowScheme]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        update_draft_if_needed=update_draft_if_needed,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id_: int,
    update_draft_if_needed: Union[Unset, bool] = UNSET,
) -> Optional[Union[None, WorkflowScheme]]:
    """Resets the default workflow for a workflow scheme. That is, the default workflow is set to Jira's system workflow (the *jira* workflow).

    Note that active workflow schemes cannot be edited. If the workflow scheme is active, set `updateDraftIfNeeded` to `true` and a draft workflow scheme is created or updated with the default workflow reset. The draft workflow scheme can be published in Jira.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            id_=id_,
            update_draft_if_needed=update_draft_if_needed,
        )
    ).parsed
