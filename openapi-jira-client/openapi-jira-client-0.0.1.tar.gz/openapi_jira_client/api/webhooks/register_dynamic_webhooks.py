from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.container_for_registered_webhooks import ContainerForRegisteredWebhooks
from ...models.error_collection import ErrorCollection
from ...models.webhook_registration_details import WebhookRegistrationDetails
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: WebhookRegistrationDetails,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/webhook".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[ContainerForRegisteredWebhooks, ErrorCollection]]:
    if response.status_code == 200:
        response_200 = ContainerForRegisteredWebhooks.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorCollection.from_dict(response.json())

        return response_400
    if response.status_code == 403:
        response_403 = ErrorCollection.from_dict(response.json())

        return response_403
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ContainerForRegisteredWebhooks, ErrorCollection]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: WebhookRegistrationDetails,
) -> Response[Union[ContainerForRegisteredWebhooks, ErrorCollection]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: WebhookRegistrationDetails,
) -> Optional[Union[ContainerForRegisteredWebhooks, ErrorCollection]]:
    """Registers webhooks.

    **[Permissions](#permissions) required:** Only [Connect apps](https://developer.atlassian.com/cloud/jira/platform/integrating-with-jira-cloud/#atlassian-connect) can use this operation."""

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: WebhookRegistrationDetails,
) -> Response[Union[ContainerForRegisteredWebhooks, ErrorCollection]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: WebhookRegistrationDetails,
) -> Optional[Union[ContainerForRegisteredWebhooks, ErrorCollection]]:
    """Registers webhooks.

    **[Permissions](#permissions) required:** Only [Connect apps](https://developer.atlassian.com/cloud/jira/platform/integrating-with-jira-cloud/#atlassian-connect) can use this operation."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
