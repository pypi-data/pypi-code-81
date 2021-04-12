# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module contains functions for downloading
repositories from GitHub.
"""

import os

from ..util import shell

from ._api_v4 import make_api_call


def _checkout_commit(
    path,
    git,
    github_data,
    commit,
    dry_run=None,
    print_debug=None
):
    with shell.pushd(os.path.join(path, github_data.name)):
        shell.call(
            [
                git,
                "checkout",
                "-b",
                "{}_composer_branch".format(commit),
                commit
            ],
            dry_run=dry_run,
            echo=print_debug
        )


def _clone_by_api_v3(
    path,
    git,
    github_data,
    host_system,
    commit=None,
    dry_run=None,
    print_debug=None
):
    """
    Downloads a repository from GitHub using the version 3 of the
    GitHub API (the REST API).

    path -- Path to the directory where the downloaded files are
    put.

    git -- Path to the Git executable from the toolchain.

    github_data -- The object containing the data required to
    download the repository from GitHub.

    host_system -- The system this script is run on.

    commit -- A commit that is checked out after the cloning.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    repository_url = "https://github.com/{owner}/{repo}".format(
        owner=github_data.owner,
        repo=github_data.name
    )

    with shell.pushd(path):
        shell.call(
            [git, "clone", "{}.git".format(repository_url)],
            dry_run=dry_run,
            echo=print_debug
        )

    if commit:
        _checkout_commit(
            path=path,
            git=git,
            github_data=github_data,
            commit=commit,
            dry_run=dry_run,
            print_debug=print_debug
        )

    return os.path.join(path, github_data.name)


def _clone_by_api_v4(
    path,
    git,
    github_data,
    user_agent,
    api_token,
    host_system,
    commit=None,
    dry_run=None,
    print_debug=None
):
    """
    Downloads a repository from GitHub using the version 4 of the
    GitHub API.

    path -- Path to the directory where the downloaded files are
    put.

    git -- Path to the Git executable from the toolchain.

    github_data -- The object containing the data required to
    download the repository from GitHub.

    user_agent -- The user agent used when accessing the GitHub
    API.

    api_token -- The GitHub API token that is used to access the
    API.

    host_system -- The system this script is run on.

    commit -- A commit that is checked out after the cloning.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    graph_ql_call = None
    with open(os.path.join(
        os.path.dirname(__file__),
        "graphql",
        "github_repository.graphql"
    )) as f:
        graph_ql_call = str(f.read()).replace(
            "{OWNER}",
            github_data.owner
        ).replace(
            "{REPOSITORY_NAME}",
            github_data.name
        )
    api_response = make_api_call(
        query=graph_ql_call,
        user_agent=user_agent,
        api_token=api_token
    )
    repository_url = api_response["data"]["repository"]["url"]

    with shell.pushd(path):
        shell.call(
            [git, "clone", "{}.git".format(repository_url)],
            dry_run=dry_run,
            echo=print_debug
        )

    if commit:
        _checkout_commit(
            path=path,
            git=git,
            github_data=github_data,
            commit=commit,
            dry_run=dry_run,
            print_debug=print_debug
        )

    return os.path.join(path, github_data.name)


def clone(
    path,
    git,
    github_data,
    user_agent,
    api_token,
    host_system,
    commit=None,
    dry_run=None,
    print_debug=None
):
    """
    Downloads a repository from GitHub according to repository
    data and returns path to the downloaded repository.

    path -- Path to the directory where the downloaded files are
    put.

    git -- Path to the Git executable from the toolchain.

    github_data -- The object containing the data required to
    download the repository from GitHub.

    user_agent -- The user agent used when accessing the GitHub
    API.

    api_token -- The GitHub API token that is used to access the
    API.

    host_system -- The system this script is run on.

    commit -- A commit that is checked out after the cloning.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    if user_agent and api_token:
        return _clone_by_api_v4(
            path=path,
            git=git,
            github_data=github_data,
            user_agent=user_agent,
            api_token=api_token,
            host_system=host_system,
            dry_run=dry_run,
            print_debug=print_debug
        )
    else:
        return _clone_by_api_v3(
            path=path,
            git=git,
            github_data=github_data,
            host_system=host_system,
            dry_run=dry_run,
            print_debug=print_debug
        )
