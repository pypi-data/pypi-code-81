from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.issue_field_option import IssueFieldOption
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    field_key: str,
    option_id: int,
    json_body: IssueFieldOption,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/field/{fieldKey}/option/{optionId}".format(
        client.base_url, fieldKey=field_key, optionId=option_id
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[IssueFieldOption, None]]:
    if response.status_code == 200:
        response_200 = IssueFieldOption.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[IssueFieldOption, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    field_key: str,
    option_id: int,
    json_body: IssueFieldOption,
) -> Response[Union[IssueFieldOption, None]]:
    kwargs = _get_kwargs(
        client=client,
        field_key=field_key,
        option_id=option_id,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    field_key: str,
    option_id: int,
    json_body: IssueFieldOption,
) -> Optional[Union[IssueFieldOption, None]]:
    """Updates or creates an option for a select list issue field. This operation requires that the option ID is provided when creating an option, therefore, the option ID needs to be specified as a path and body parameter. The option ID provided in the path and body must be identical.

    Note that this operation **only works for issue field select list options added by Connect apps**, it cannot be used with issue field select list options created in Jira or using operations from the [Issue custom field options](#api-group-Issue-custom-field-options) resource.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg). Jira permissions are not required for the app providing the field."""

    return sync_detailed(
        client=client,
        field_key=field_key,
        option_id=option_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    field_key: str,
    option_id: int,
    json_body: IssueFieldOption,
) -> Response[Union[IssueFieldOption, None]]:
    kwargs = _get_kwargs(
        client=client,
        field_key=field_key,
        option_id=option_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    field_key: str,
    option_id: int,
    json_body: IssueFieldOption,
) -> Optional[Union[IssueFieldOption, None]]:
    """Updates or creates an option for a select list issue field. This operation requires that the option ID is provided when creating an option, therefore, the option ID needs to be specified as a path and body parameter. The option ID provided in the path and body must be identical.

    Note that this operation **only works for issue field select list options added by Connect apps**, it cannot be used with issue field select list options created in Jira or using operations from the [Issue custom field options](#api-group-Issue-custom-field-options) resource.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg). Jira permissions are not required for the app providing the field."""

    return (
        await asyncio_detailed(
            client=client,
            field_key=field_key,
            option_id=option_id,
            json_body=json_body,
        )
    ).parsed
