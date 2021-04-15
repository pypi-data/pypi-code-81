from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.application_property import ApplicationProperty
from ...models.simple_application_property_bean import SimpleApplicationPropertyBean
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    id_: str,
    json_body: SimpleApplicationPropertyBean,
) -> Dict[str, Any]:
    url = "{}/rest/api/3/application-properties/{id}".format(client.base_url, id=id_)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[ApplicationProperty, None]]:
    if response.status_code == 200:
        response_200 = ApplicationProperty.from_dict(response.json())

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


def _build_response(*, response: httpx.Response) -> Response[Union[ApplicationProperty, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    id_: str,
    json_body: SimpleApplicationPropertyBean,
) -> Response[Union[ApplicationProperty, None]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        json_body=json_body,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id_: str,
    json_body: SimpleApplicationPropertyBean,
) -> Optional[Union[ApplicationProperty, None]]:
    """Changes the value of an application property. For example, you can change the value of the `jira.clone.prefix` from its default value of *CLONE -* to *Clone -* if you prefer sentence case capitalization. Editable properties are described below along with their default values.

    #### Advanced settings ####

    The advanced settings below are also accessible in [Jira](https://confluence.atlassian.com/x/vYXKM).

    | Key | Description | Default value |
    | -- | -- | -- |
    | `jira.clone.prefix` | The string of text prefixed to the title of a cloned issue. | `CLONE -` |
    | `jira.date.picker.java.format` | The date format for the Java (server-side) generated dates. This must be the same as the `jira.date.picker.javascript.format` format setting. | `d/MMM/yy` |
    | `jira.date.picker.javascript.format` | The date format for the JavaScript (client-side) generated dates. This must be the same as the `jira.date.picker.java.format` format setting. | `%e/%b/%y` |
    | `jira.date.time.picker.java.format` | The date format for the Java (server-side) generated date times. This must be the same as the `jira.date.time.picker.javascript.format` format setting. | `dd/MMM/yy h:mm a` |
    | `jira.date.time.picker.javascript.format` | The date format for the JavaScript (client-side) generated date times. This must be the same as the `jira.date.time.picker.java.format` format setting. | `%e/%b/%y %I:%M %p` |
    | `jira.issue.actions.order` | The default order of actions (such as *Comments* or *Change history*) displayed on the issue view. | `asc` |
    | `jira.table.cols.subtasks` | The columns to show while viewing subtask issues in a table. For example, a list of subtasks on an issue. | `issuetype, status, assignee, progress` |
    | `jira.view.issue.links.sort.order` | The sort order of the list of issue links on the issue view. | `type, status, priority` |
    | `jira.comment.collapsing.minimum.hidden` | The minimum number of comments required for comment collapsing to occur. A value of `0` disables comment collapsing. | `4` |
    | `jira.newsletter.tip.delay.days` | The number of days before a prompt to sign up to the Jira Insiders newsletter is shown. A value of `-1` disables this feature. | `7` |


    #### Look and feel ####

    The settings listed below adjust the [look and feel](https://confluence.atlassian.com/x/VwCLLg).

    | Key | Description | Default value |
    | -- | -- | -- |
    | `jira.lf.date.time` | The [ time format](https://docs.oracle.com/javase/6/docs/api/index.html?java/text/SimpleDateFormat.html). | `h:mm a` |
    | `jira.lf.date.day` | The [ day format](https://docs.oracle.com/javase/6/docs/api/index.html?java/text/SimpleDateFormat.html). | `EEEE h:mm a` |
    | `jira.lf.date.complete` | The [ date and time format](https://docs.oracle.com/javase/6/docs/api/index.html?java/text/SimpleDateFormat.html). | `dd/MMM/yy h:mm a` |
    | `jira.lf.date.dmy` | The [ date format](https://docs.oracle.com/javase/6/docs/api/index.html?java/text/SimpleDateFormat.html). | `dd/MMM/yy` |
    | `jira.date.time.picker.use.iso8061` | When enabled, sets Monday as the first day of the week in the date picker, as specified by the ISO8601 standard. | `false` |
    | `jira.lf.logo.url` | The URL of the logo image file. | `/images/icon-jira-logo.png` |
    | `jira.lf.logo.show.application.title` | Controls the visibility of the application title on the sidebar. | `false` |
    | `jira.lf.favicon.url` | The URL of the favicon. | `/favicon.ico` |
    | `jira.lf.favicon.hires.url` | The URL of the high-resolution favicon. | `/images/64jira.png` |
    | `jira.lf.top.adg3.bgcolour` | The background color of the sidebar. | `#0747A6` |
    | `jira.lf.top.adg3.textcolour` | The color of the text and logo of the sidebar. | `#DEEBFF` |
    | `jira.lf.hero.button.base.bg.colour` | The background color of the hero button. | `#3b7fc4` |
    | `jira.title` | The text for the application title. The application title can also be set in *General settings*. | `Jira` |
    | `jira.option.globalsharing` | Whether filters and dashboards can be shared with anyone signed into Jira. | `true` |
    | `xflow.product.suggestions.enabled` | Whether to expose product suggestions for other Atlassian products within Jira. | `true` |


    #### Other settings ####

    | Key | Description | Default value |
    | -- | -- | -- |
    | `jira.issuenav.criteria.autoupdate` | Whether instant updates to search criteria is active. | `true` |


    *Note: Be careful when changing [application properties and advanced settings](https://confluence.atlassian.com/x/vYXKM).*

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return sync_detailed(
        client=client,
        id_=id_,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id_: str,
    json_body: SimpleApplicationPropertyBean,
) -> Response[Union[ApplicationProperty, None]]:
    kwargs = _get_kwargs(
        client=client,
        id_=id_,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id_: str,
    json_body: SimpleApplicationPropertyBean,
) -> Optional[Union[ApplicationProperty, None]]:
    """Changes the value of an application property. For example, you can change the value of the `jira.clone.prefix` from its default value of *CLONE -* to *Clone -* if you prefer sentence case capitalization. Editable properties are described below along with their default values.

    #### Advanced settings ####

    The advanced settings below are also accessible in [Jira](https://confluence.atlassian.com/x/vYXKM).

    | Key | Description | Default value |
    | -- | -- | -- |
    | `jira.clone.prefix` | The string of text prefixed to the title of a cloned issue. | `CLONE -` |
    | `jira.date.picker.java.format` | The date format for the Java (server-side) generated dates. This must be the same as the `jira.date.picker.javascript.format` format setting. | `d/MMM/yy` |
    | `jira.date.picker.javascript.format` | The date format for the JavaScript (client-side) generated dates. This must be the same as the `jira.date.picker.java.format` format setting. | `%e/%b/%y` |
    | `jira.date.time.picker.java.format` | The date format for the Java (server-side) generated date times. This must be the same as the `jira.date.time.picker.javascript.format` format setting. | `dd/MMM/yy h:mm a` |
    | `jira.date.time.picker.javascript.format` | The date format for the JavaScript (client-side) generated date times. This must be the same as the `jira.date.time.picker.java.format` format setting. | `%e/%b/%y %I:%M %p` |
    | `jira.issue.actions.order` | The default order of actions (such as *Comments* or *Change history*) displayed on the issue view. | `asc` |
    | `jira.table.cols.subtasks` | The columns to show while viewing subtask issues in a table. For example, a list of subtasks on an issue. | `issuetype, status, assignee, progress` |
    | `jira.view.issue.links.sort.order` | The sort order of the list of issue links on the issue view. | `type, status, priority` |
    | `jira.comment.collapsing.minimum.hidden` | The minimum number of comments required for comment collapsing to occur. A value of `0` disables comment collapsing. | `4` |
    | `jira.newsletter.tip.delay.days` | The number of days before a prompt to sign up to the Jira Insiders newsletter is shown. A value of `-1` disables this feature. | `7` |


    #### Look and feel ####

    The settings listed below adjust the [look and feel](https://confluence.atlassian.com/x/VwCLLg).

    | Key | Description | Default value |
    | -- | -- | -- |
    | `jira.lf.date.time` | The [ time format](https://docs.oracle.com/javase/6/docs/api/index.html?java/text/SimpleDateFormat.html). | `h:mm a` |
    | `jira.lf.date.day` | The [ day format](https://docs.oracle.com/javase/6/docs/api/index.html?java/text/SimpleDateFormat.html). | `EEEE h:mm a` |
    | `jira.lf.date.complete` | The [ date and time format](https://docs.oracle.com/javase/6/docs/api/index.html?java/text/SimpleDateFormat.html). | `dd/MMM/yy h:mm a` |
    | `jira.lf.date.dmy` | The [ date format](https://docs.oracle.com/javase/6/docs/api/index.html?java/text/SimpleDateFormat.html). | `dd/MMM/yy` |
    | `jira.date.time.picker.use.iso8061` | When enabled, sets Monday as the first day of the week in the date picker, as specified by the ISO8601 standard. | `false` |
    | `jira.lf.logo.url` | The URL of the logo image file. | `/images/icon-jira-logo.png` |
    | `jira.lf.logo.show.application.title` | Controls the visibility of the application title on the sidebar. | `false` |
    | `jira.lf.favicon.url` | The URL of the favicon. | `/favicon.ico` |
    | `jira.lf.favicon.hires.url` | The URL of the high-resolution favicon. | `/images/64jira.png` |
    | `jira.lf.top.adg3.bgcolour` | The background color of the sidebar. | `#0747A6` |
    | `jira.lf.top.adg3.textcolour` | The color of the text and logo of the sidebar. | `#DEEBFF` |
    | `jira.lf.hero.button.base.bg.colour` | The background color of the hero button. | `#3b7fc4` |
    | `jira.title` | The text for the application title. The application title can also be set in *General settings*. | `Jira` |
    | `jira.option.globalsharing` | Whether filters and dashboards can be shared with anyone signed into Jira. | `true` |
    | `xflow.product.suggestions.enabled` | Whether to expose product suggestions for other Atlassian products within Jira. | `true` |


    #### Other settings ####

    | Key | Description | Default value |
    | -- | -- | -- |
    | `jira.issuenav.criteria.autoupdate` | Whether instant updates to search criteria is active. | `true` |


    *Note: Be careful when changing [application properties and advanced settings](https://confluence.atlassian.com/x/vYXKM).*

    **[Permissions](#permissions) required:** *Administer Jira* [global permission](https://confluence.atlassian.com/x/x4dKLg)."""

    return (
        await asyncio_detailed(
            client=client,
            id_=id_,
            json_body=json_body,
        )
    ).parsed
