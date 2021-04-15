from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.analyse_expression_check import AnalyseExpressionCheck
from ...models.error_collection import ErrorCollection
from ...models.jira_expression_for_analysis import JiraExpressionForAnalysis
from ...models.jira_expressions_analysis import JiraExpressionsAnalysis
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: JiraExpressionForAnalysis,
    check: Union[Unset, AnalyseExpressionCheck] = AnalyseExpressionCheck.SYNTAX,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/expression/analyse".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_check: Union[Unset, str] = UNSET
    if not isinstance(check, Unset):
        json_check = check.value

    params: Dict[str, Any] = {
        "check": json_check,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[ErrorCollection, JiraExpressionsAnalysis, None]]:
    if response.status_code == 200:
        response_200 = JiraExpressionsAnalysis.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorCollection.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = ErrorCollection.from_dict(response.json())

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ErrorCollection, JiraExpressionsAnalysis, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: JiraExpressionForAnalysis,
    check: Union[Unset, AnalyseExpressionCheck] = AnalyseExpressionCheck.SYNTAX,
) -> Response[Union[ErrorCollection, JiraExpressionsAnalysis, None]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        check=check,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: JiraExpressionForAnalysis,
    check: Union[Unset, AnalyseExpressionCheck] = AnalyseExpressionCheck.SYNTAX,
) -> Optional[Union[ErrorCollection, JiraExpressionsAnalysis, None]]:
    """Analyses and validates Jira expressions.

    As an experimental feature, this operation can also attempt to type-check the expressions.

    Learn more about Jira expressions in the [documentation](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/).

    **[Permissions](#permissions) required**: None."""

    return sync_detailed(
        client=client,
        json_body=json_body,
        check=check,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: JiraExpressionForAnalysis,
    check: Union[Unset, AnalyseExpressionCheck] = AnalyseExpressionCheck.SYNTAX,
) -> Response[Union[ErrorCollection, JiraExpressionsAnalysis, None]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        check=check,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: JiraExpressionForAnalysis,
    check: Union[Unset, AnalyseExpressionCheck] = AnalyseExpressionCheck.SYNTAX,
) -> Optional[Union[ErrorCollection, JiraExpressionsAnalysis, None]]:
    """Analyses and validates Jira expressions.

    As an experimental feature, this operation can also attempt to type-check the expressions.

    Learn more about Jira expressions in the [documentation](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/).

    **[Permissions](#permissions) required**: None."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            check=check,
        )
    ).parsed
