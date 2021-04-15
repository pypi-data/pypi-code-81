from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.bulk_custom_field_option_update_request import BulkCustomFieldOptionUpdateRequest
from ...models.custom_field_updated_context_options_list import CustomFieldUpdatedContextOptionsList
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    field_id: str,
    context_id: int,
    json_body: BulkCustomFieldOptionUpdateRequest,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/field/{fieldId}/context/{contextId}/option".format(
        client.base_url, fieldId=field_id, contextId=context_id
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[CustomFieldUpdatedContextOptionsList, None]]:
    if response.status_code == 200:
        response_200 = CustomFieldUpdatedContextOptionsList.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[CustomFieldUpdatedContextOptionsList, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    field_id: str,
    context_id: int,
    json_body: BulkCustomFieldOptionUpdateRequest,
) -> Response[Union[CustomFieldUpdatedContextOptionsList, None]]:
    kwargs = _get_kwargs(
        client=client,
        field_id=field_id,
        context_id=context_id,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    field_id: str,
    context_id: int,
    json_body: BulkCustomFieldOptionUpdateRequest,
) -> Optional[Union[CustomFieldUpdatedContextOptionsList, None]]:
    """Updates the options of a custom field.

    If any of the options are not found, no options are updated. Options where the values in the request match the current values aren't updated and aren't reported in the response.

    Note that this operation **only works for issue field select list options created in Jira or using operations from the [Issue custom field options](#api-group-Issue-custom-field-options) resource**, it cannot be used with issue field select list options created by Connect apps.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        field_id=field_id,
        context_id=context_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    field_id: str,
    context_id: int,
    json_body: BulkCustomFieldOptionUpdateRequest,
) -> Response[Union[CustomFieldUpdatedContextOptionsList, None]]:
    kwargs = _get_kwargs(
        client=client,
        field_id=field_id,
        context_id=context_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    field_id: str,
    context_id: int,
    json_body: BulkCustomFieldOptionUpdateRequest,
) -> Optional[Union[CustomFieldUpdatedContextOptionsList, None]]:
    """Updates the options of a custom field.

    If any of the options are not found, no options are updated. Options where the values in the request match the current values aren't updated and aren't reported in the response.

    Note that this operation **only works for issue field select list options created in Jira or using operations from the [Issue custom field options](#api-group-Issue-custom-field-options) resource**, it cannot be used with issue field select list options created by Connect apps.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            field_id=field_id,
            context_id=context_id,
            json_body=json_body,
        )
    ).parsed
