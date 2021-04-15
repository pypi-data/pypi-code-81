import datetime
from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.audit_records import AuditRecords
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 1000,
    filter_: Union[Unset, str] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/auditing/record".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_from_: Union[Unset, str] = UNSET
    if not isinstance(from_, Unset):
        json_from_ = from_.isoformat()

    json_to: Union[Unset, str] = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat()

    params: Dict[str, Any] = {
        "offset": offset,
        "limit": limit,
        "filter": filter_,
        "from": json_from_,
        "to": json_to,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[AuditRecords, None]]:
    if response.status_code == 200:
        response_200 = AuditRecords.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 403:
        response_403 = None

        return response_403
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[AuditRecords, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 1000,
    filter_: Union[Unset, str] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Response[Union[AuditRecords, None]]:
    kwargs = _get_kwargs(
        client=client,
        offset=offset,
        limit=limit,
        filter_=filter_,
        from_=from_,
        to=to,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 1000,
    filter_: Union[Unset, str] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Optional[Union[AuditRecords, None]]:
    """Returns a list of audit records. The list can be filtered to include items:

     *  containing a string in at least one field. For example, providing *up* will return all audit records where one or more fields contains words such as *update*.
     *  created on or after a date and time.
     *  created or or before a date and time.
     *  created during a time period.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        offset=offset,
        limit=limit,
        filter_=filter_,
        from_=from_,
        to=to,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 1000,
    filter_: Union[Unset, str] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Response[Union[AuditRecords, None]]:
    kwargs = _get_kwargs(
        client=client,
        offset=offset,
        limit=limit,
        filter_=filter_,
        from_=from_,
        to=to,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 1000,
    filter_: Union[Unset, str] = UNSET,
    from_: Union[Unset, datetime.datetime] = UNSET,
    to: Union[Unset, datetime.datetime] = UNSET,
) -> Optional[Union[AuditRecords, None]]:
    """Returns a list of audit records. The list can be filtered to include items:

     *  containing a string in at least one field. For example, providing *up* will return all audit records where one or more fields contains words such as *update*.
     *  created on or after a date and time.
     *  created or or before a date and time.
     *  created during a time period.

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            offset=offset,
            limit=limit,
            filter_=filter_,
            from_=from_,
            to=to,
        )
    ).parsed
