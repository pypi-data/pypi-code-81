from typing import Any, Dict, List, Union

import httpx

from ...client import AuthenticatedClient
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    fields: Union[Unset, List[str]] = UNSET,
    fields_by_keys: Union[Unset, bool] = False,
    expand: Union[Unset, str] = UNSET,
    properties: Union[Unset, List[str]] = UNSET,
    update_history: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}".format(client.base_url, issueIdOrKey=issue_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_fields: Union[Unset, List[str]] = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    json_properties: Union[Unset, List[str]] = UNSET
    if not isinstance(properties, Unset):
        json_properties = properties

    params: Dict[str, Any] = {
        "fields": json_fields,
        "fieldsByKeys": fields_by_keys,
        "expand": expand,
        "properties": json_properties,
        "updateHistory": update_history,
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
    issue_id_or_key: str,
    fields: Union[Unset, List[str]] = UNSET,
    fields_by_keys: Union[Unset, bool] = False,
    expand: Union[Unset, str] = UNSET,
    properties: Union[Unset, List[str]] = UNSET,
    update_history: Union[Unset, bool] = False,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        fields=fields,
        fields_by_keys=fields_by_keys,
        expand=expand,
        properties=properties,
        update_history=update_history,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    fields: Union[Unset, List[str]] = UNSET,
    fields_by_keys: Union[Unset, bool] = False,
    expand: Union[Unset, str] = UNSET,
    properties: Union[Unset, List[str]] = UNSET,
    update_history: Union[Unset, bool] = False,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        fields=fields,
        fields_by_keys=fields_by_keys,
        expand=expand,
        properties=properties,
        update_history=update_history,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)
