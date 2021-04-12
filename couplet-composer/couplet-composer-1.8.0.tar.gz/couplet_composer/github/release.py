# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module contains functions for downloading release
assets from GitHub.
"""

import os

from ..util import http

from . import _api_v3, _api_v4, tag


def _get_api_v3_streaming_accept_header():
    """
    Returns the default value for the Accept header for the REST
    API calls that should be used for streaming files.
    """
    return "application/octet-stream"


def _download_by_api_v3(
    path,
    github_data,
    host_system,
    dry_run=None,
    print_debug=None
):
    """
    Downloads an asset from GitHub using the version 3 of the
    GitHub API (the REST API).

    path -- Path to the directory where the downloaded files are
    put.

    github_data -- The object containing the data required to
    download the asset from GitHub.

    host_system -- The system this script is run on.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    api_response = _api_v3.make_api_call(
        call_path="/repos/{owner}/{repo}/releases/tags/{tag}".format(
            owner=github_data.owner,
            repo=github_data.name,
            tag=github_data.tag_name
        )
    )
    release_id = api_response["id"]
    asset_list_response = _api_v3.make_api_call(
        call_path="/repos/{owner}/{repo}/releases/{release_id}/assets".format(
            owner=github_data.owner,
            repo=github_data.name,
            release_id=release_id
        )
    )
    asset_id = _api_v3.find_release_asset_id(
        api_response=asset_list_response,
        name=github_data.asset_name
    )
    asset_response = _api_v3.make_api_call(
        call_path="/repos/{owner}/{repo}/releases/assets/{asset_id}".format(
            owner=github_data.owner,
            repo=github_data.name,
            asset_id=asset_id
        )
    )
    dest = os.path.join(path, github_data.asset_name)
    http.stream(
        url=asset_response["url"],
        destination=dest,
        host_system=host_system,
        headers={
            "User-Agent": "Couplet Composer",
            "Accept": _get_api_v3_streaming_accept_header()
        },
        dry_run=dry_run,
        print_debug=print_debug
    )
    return dest


def _download_by_api_v4(
    path,
    github_data,
    user_agent,
    api_token,
    host_system,
    dry_run=None,
    print_debug=None
):
    """
    Downloads an asset from GitHub using the version 4 of the
    GitHub API.

    path -- Path to the directory where the downloaded files are
    put.

    github_data -- The object containing the data required to
    download the asset from GitHub.

    user_agent -- The user agent used when accessing the GitHub
    API.

    api_token -- The GitHub API token that is used to access the
    API.

    host_system -- The system this script is run on.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    graph_ql_call = None
    with open(os.path.join(
        os.path.dirname(__file__),
        "graphql",
        "github_asset.graphql"
    )) as f:
        graph_ql_call = str(f.read()).replace(
            "{OWNER}",
            github_data.owner
        ).replace(
            "{REPOSITORY_NAME}",
            github_data.name
        ).replace(
            "{TAG_NAME}",
            github_data.tag_name
        ).replace(
            "{ASSET_NAME}",
            github_data.asset_name
        )
    api_response = _api_v4.make_api_call(
        query=graph_ql_call,
        user_agent=user_agent,
        api_token=api_token
    )
    release_node = _api_v4.find_release_node(api_response=api_response)
    asset_node = release_node["releaseAssets"]["edges"][0]["node"]
    dest = os.path.join(path, github_data.asset_name)
    http.stream(
        url=asset_node["url"],
        destination=dest,
        host_system=host_system,
        headers={
            "User-Agent": user_agent,
            "Accept": "application/octet-stream"
        },
        dry_run=dry_run,
        print_debug=print_debug
    )
    return dest


def download_tag(
    path,
    git,
    github_data,
    user_agent,
    api_token,
    host_system,
    dry_run=None,
    print_debug=None
):
    """
    Downloads a tag from GitHub according to release data and
    returns path to the downloaded tag.

    path -- Path to the directory where the downloaded files are
    put.

    git -- Path to the Git executable from the toolchain.

    github_data -- The object containing the data required to
    download the tag from GitHub.

    user_agent -- The user agent used when accessing the GitHub
    API.

    api_token -- The GitHub API token that is used to access the
    API.

    host_system -- The system this script is run on.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    return tag.download_release_tag(
        path=path,
        git=git,
        github_data=github_data,
        user_agent=user_agent,
        api_token=api_token,
        host_system=host_system,
        dry_run=dry_run,
        print_debug=print_debug
    )


def download_asset(
    path,
    github_data,
    user_agent,
    api_token,
    host_system,
    dry_run=None,
    print_debug=None
):
    """
    Downloads an asset from GitHub according to release data and
    returns path to the downloaded asset.

    path -- Path to the directory where the downloaded files are
    put.

    github_data -- The object containing the data required to
    download the asset from GitHub.

    user_agent -- The user agent used when accessing the GitHub
    API.

    api_token -- The GitHub API token that is used to access the
    API.

    host_system -- The system this script is run on.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    if user_agent and api_token:
        return _download_by_api_v4(
            path=path,
            github_data=github_data,
            user_agent=user_agent,
            api_token=api_token,
            host_system=host_system,
            dry_run=dry_run,
            print_debug=print_debug
        )
    else:
        return _download_by_api_v3(
            path=path,
            github_data=github_data,
            host_system=host_system,
            dry_run=dry_run,
            print_debug=print_debug
        )
