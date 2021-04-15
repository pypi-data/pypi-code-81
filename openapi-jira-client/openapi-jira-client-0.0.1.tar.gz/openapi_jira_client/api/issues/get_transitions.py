from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.transitions import Transitions
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    expand: Union[Unset, str] = UNSET,
    transition_id: Union[Unset, str] = UNSET,
    skip_remote_only_condition: Union[Unset, bool] = False,
    include_unavailable_transitions: Union[Unset, bool] = False,
    sort_by_ops_bar_and_status: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/issue/{issueIdOrKey}/transitions".format(client.base_url, issueIdOrKey=issue_id_or_key)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "expand": expand,
        "transitionId": transition_id,
        "skipRemoteOnlyCondition": skip_remote_only_condition,
        "includeUnavailableTransitions": include_unavailable_transitions,
        "sortByOpsBarAndStatus": sort_by_ops_bar_and_status,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, Transitions]]:
    if response.status_code == 200:
        response_200 = Transitions.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, Transitions]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    expand: Union[Unset, str] = UNSET,
    transition_id: Union[Unset, str] = UNSET,
    skip_remote_only_condition: Union[Unset, bool] = False,
    include_unavailable_transitions: Union[Unset, bool] = False,
    sort_by_ops_bar_and_status: Union[Unset, bool] = False,
) -> Response[Union[None, Transitions]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        expand=expand,
        transition_id=transition_id,
        skip_remote_only_condition=skip_remote_only_condition,
        include_unavailable_transitions=include_unavailable_transitions,
        sort_by_ops_bar_and_status=sort_by_ops_bar_and_status,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    expand: Union[Unset, str] = UNSET,
    transition_id: Union[Unset, str] = UNSET,
    skip_remote_only_condition: Union[Unset, bool] = False,
    include_unavailable_transitions: Union[Unset, bool] = False,
    sort_by_ops_bar_and_status: Union[Unset, bool] = False,
) -> Optional[Union[None, Transitions]]:
    """Returns either all transitions or a transition that can be performed by the user on an issue, based on the issue's status.

    Note, if a request is made for a transition that does not exist or cannot be performed on the issue, given its status, the response will return any empty transitions list.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required: A list or transition is returned only when the user has:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.

    However, if the user does not have the *Transition issues* [ project permission](https://confluence.atlassian.com/x/yodKLg) the response will not list any transitions."""

    return sync_detailed(
        client=client,
        issue_id_or_key=issue_id_or_key,
        expand=expand,
        transition_id=transition_id,
        skip_remote_only_condition=skip_remote_only_condition,
        include_unavailable_transitions=include_unavailable_transitions,
        sort_by_ops_bar_and_status=sort_by_ops_bar_and_status,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    expand: Union[Unset, str] = UNSET,
    transition_id: Union[Unset, str] = UNSET,
    skip_remote_only_condition: Union[Unset, bool] = False,
    include_unavailable_transitions: Union[Unset, bool] = False,
    sort_by_ops_bar_and_status: Union[Unset, bool] = False,
) -> Response[Union[None, Transitions]]:
    kwargs = _get_kwargs(
        client=client,
        issue_id_or_key=issue_id_or_key,
        expand=expand,
        transition_id=transition_id,
        skip_remote_only_condition=skip_remote_only_condition,
        include_unavailable_transitions=include_unavailable_transitions,
        sort_by_ops_bar_and_status=sort_by_ops_bar_and_status,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    issue_id_or_key: str,
    expand: Union[Unset, str] = UNSET,
    transition_id: Union[Unset, str] = UNSET,
    skip_remote_only_condition: Union[Unset, bool] = False,
    include_unavailable_transitions: Union[Unset, bool] = False,
    sort_by_ops_bar_and_status: Union[Unset, bool] = False,
) -> Optional[Union[None, Transitions]]:
    """Returns either all transitions or a transition that can be performed by the user on an issue, based on the issue's status.

    Note, if a request is made for a transition that does not exist or cannot be performed on the issue, given its status, the response will return any empty transitions list.

    This operation can be accessed anonymously.

    **[Permissions](#permissions) required: A list or transition is returned only when the user has:**

     *  *Browse projects* [project permission](https://confluence.atlassian.com/x/yodKLg) for the project that the issue is in.
     *  If [issue-level security](https://confluence.atlassian.com/x/J4lKLg) is configured, issue-level security permission to view the issue.

    However, if the user does not have the *Transition issues* [ project permission](https://confluence.atlassian.com/x/yodKLg) the response will not list any transitions."""

    return (
        await asyncio_detailed(
            client=client,
            issue_id_or_key=issue_id_or_key,
            expand=expand,
            transition_id=transition_id,
            skip_remote_only_condition=skip_remote_only_condition,
            include_unavailable_transitions=include_unavailable_transitions,
            sort_by_ops_bar_and_status=sort_by_ops_bar_and_status,
        )
    ).parsed
