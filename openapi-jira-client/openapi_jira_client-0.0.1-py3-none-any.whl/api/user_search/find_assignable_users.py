from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.user import User
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    query: Union[Unset, str] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    project: Union[Unset, str] = UNSET,
    issue_key: Union[Unset, str] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    action_descriptor_id: Union[Unset, int] = UNSET,
    recommend: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/user/assignable/search".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "query": query,
        "sessionId": session_id,
        "username": username,
        "accountId": account_id,
        "project": project,
        "issueKey": issue_key,
        "startAt": start_at,
        "maxResults": max_results,
        "actionDescriptorId": action_descriptor_id,
        "recommend": recommend,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[List[User], None]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = User.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
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


def _build_response(*, response: httpx.Response) -> Response[Union[List[User], None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    query: Union[Unset, str] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    project: Union[Unset, str] = UNSET,
    issue_key: Union[Unset, str] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    action_descriptor_id: Union[Unset, int] = UNSET,
    recommend: Union[Unset, bool] = False,
) -> Response[Union[List[User], None]]:
    kwargs = _get_kwargs(
        client=client,
        query=query,
        session_id=session_id,
        username=username,
        account_id=account_id,
        project=project,
        issue_key=issue_key,
        start_at=start_at,
        max_results=max_results,
        action_descriptor_id=action_descriptor_id,
        recommend=recommend,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    query: Union[Unset, str] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    project: Union[Unset, str] = UNSET,
    issue_key: Union[Unset, str] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    action_descriptor_id: Union[Unset, int] = UNSET,
    recommend: Union[Unset, bool] = False,
) -> Optional[Union[List[User], None]]:
    """Returns a list of users that can be assigned to an issue. Use this operation to find the list of users who can be assigned to:

     *  a new issue, by providing the `projectKeyOrId`.
     *  an updated issue, by providing the `issueKey`.
     *  to an issue during a transition (workflow action), by providing the `issueKey` and the transition id in `actionDescriptorId`. You can obtain the IDs of an issue's valid transitions using the `transitions` option in the `expand` parameter of [ Get issue](#api-rest-api-3-issue-issueIdOrKey-get).

    In all these cases, you can pass an account ID to determine if a user can be assigned to an issue. The user is returned in the response if they can be assigned to the issue or issue transition.

    This operation takes the users in the range defined by `startAt` and `maxResults`, up to the thousandth user, and then returns only the users from that range that can be assigned the issue. This means the operation usually returns fewer users than specified in `maxResults`. To get all the users who can be assigned the issue, use [Get all users](#api-rest-api-3-users-search-get) and filter the records in your code.

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return sync_detailed(
        client=client,
        query=query,
        session_id=session_id,
        username=username,
        account_id=account_id,
        project=project,
        issue_key=issue_key,
        start_at=start_at,
        max_results=max_results,
        action_descriptor_id=action_descriptor_id,
        recommend=recommend,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    query: Union[Unset, str] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    project: Union[Unset, str] = UNSET,
    issue_key: Union[Unset, str] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    action_descriptor_id: Union[Unset, int] = UNSET,
    recommend: Union[Unset, bool] = False,
) -> Response[Union[List[User], None]]:
    kwargs = _get_kwargs(
        client=client,
        query=query,
        session_id=session_id,
        username=username,
        account_id=account_id,
        project=project,
        issue_key=issue_key,
        start_at=start_at,
        max_results=max_results,
        action_descriptor_id=action_descriptor_id,
        recommend=recommend,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    query: Union[Unset, str] = UNSET,
    session_id: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
    account_id: Union[Unset, str] = UNSET,
    project: Union[Unset, str] = UNSET,
    issue_key: Union[Unset, str] = UNSET,
    start_at: Union[Unset, int] = 0,
    max_results: Union[Unset, int] = 50,
    action_descriptor_id: Union[Unset, int] = UNSET,
    recommend: Union[Unset, bool] = False,
) -> Optional[Union[List[User], None]]:
    """Returns a list of users that can be assigned to an issue. Use this operation to find the list of users who can be assigned to:

     *  a new issue, by providing the `projectKeyOrId`.
     *  an updated issue, by providing the `issueKey`.
     *  to an issue during a transition (workflow action), by providing the `issueKey` and the transition id in `actionDescriptorId`. You can obtain the IDs of an issue's valid transitions using the `transitions` option in the `expand` parameter of [ Get issue](#api-rest-api-3-issue-issueIdOrKey-get).

    In all these cases, you can pass an account ID to determine if a user can be assigned to an issue. The user is returned in the response if they can be assigned to the issue or issue transition.

    This operation takes the users in the range defined by `startAt` and `maxResults`, up to the thousandth user, and then returns only the users from that range that can be assigned the issue. This means the operation usually returns fewer users than specified in `maxResults`. To get all the users who can be assigned the issue, use [Get all users](#api-rest-api-3-users-search-get) and filter the records in your code.

    **[Permissions](#permissions) required:** Permission to access Jira."""

    return (
        await asyncio_detailed(
            client=client,
            query=query,
            session_id=session_id,
            username=username,
            account_id=account_id,
            project=project,
            issue_key=issue_key,
            start_at=start_at,
            max_results=max_results,
            action_descriptor_id=action_descriptor_id,
            recommend=recommend,
        )
    ).parsed
