from typing import Any, Dict, Union

import httpx

from ...client import AuthenticatedClient
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id_: int,
    workflow_name: str,
    update_draft_if_needed: Union[Unset, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/workflowscheme/{id}/workflow".format(client.base_url, id=id_)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "workflowName": workflow_name,
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


def _build_response(*, response: httpx.Response) -> Response[None]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    id_: int,
    workflow_name: str,
    update_draft_if_needed: Union[Unset, bool] = UNSET,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        workflow_name=workflow_name,
        update_draft_if_needed=update_draft_if_needed,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id_: int,
    workflow_name: str,
    update_draft_if_needed: Union[Unset, bool] = UNSET,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        workflow_name=workflow_name,
        update_draft_if_needed=update_draft_if_needed,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)
