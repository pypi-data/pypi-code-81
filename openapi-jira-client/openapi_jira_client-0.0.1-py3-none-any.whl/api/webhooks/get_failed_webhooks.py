from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.error_collection import ErrorCollection
from ...models.failed_webhooks import FailedWebhooks
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    max_results: Union[Unset, int] = UNSET,
    after: Union[Unset, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/webhook/failed".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "maxResults": max_results,
        "after": after,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[ErrorCollection, FailedWebhooks]]:
    if response.status_code == 200:
        response_200 = FailedWebhooks.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorCollection.from_dict(response.json())

        return response_400
    if response.status_code == 403:
        response_403 = ErrorCollection.from_dict(response.json())

        return response_403
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ErrorCollection, FailedWebhooks]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    max_results: Union[Unset, int] = UNSET,
    after: Union[Unset, int] = UNSET,
) -> Response[Union[ErrorCollection, FailedWebhooks]]:
    kwargs = _get_kwargs(
        client=client,
        max_results=max_results,
        after=after,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    max_results: Union[Unset, int] = UNSET,
    after: Union[Unset, int] = UNSET,
) -> Optional[Union[ErrorCollection, FailedWebhooks]]:
    """Returns webhooks that have recently failed to be delivered to the requesting app after the maximum number of retries.

    After 72 hours the failure may no longer be returned by this operation.

    The oldest failure is returned first.

    This method uses a cursor-based pagination. To request the next page use the failure time of the last webhook on the list as the `failedAfter` value or use the URL provided in `next`.

    **[Permissions](#permissions) required:** Only [Connect apps](https://developer.atlassian.com/cloud/jira/platform/integrating-with-jira-cloud/#atlassian-connect) can use this operation."""

    return sync_detailed(
        client=client,
        max_results=max_results,
        after=after,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    max_results: Union[Unset, int] = UNSET,
    after: Union[Unset, int] = UNSET,
) -> Response[Union[ErrorCollection, FailedWebhooks]]:
    kwargs = _get_kwargs(
        client=client,
        max_results=max_results,
        after=after,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    max_results: Union[Unset, int] = UNSET,
    after: Union[Unset, int] = UNSET,
) -> Optional[Union[ErrorCollection, FailedWebhooks]]:
    """Returns webhooks that have recently failed to be delivered to the requesting app after the maximum number of retries.

    After 72 hours the failure may no longer be returned by this operation.

    The oldest failure is returned first.

    This method uses a cursor-based pagination. To request the next page use the failure time of the last webhook on the list as the `failedAfter` value or use the URL provided in `next`.

    **[Permissions](#permissions) required:** Only [Connect apps](https://developer.atlassian.com/cloud/jira/platform/integrating-with-jira-cloud/#atlassian-connect) can use this operation."""

    return (
        await asyncio_detailed(
            client=client,
            max_results=max_results,
            after=after,
        )
    ).parsed
