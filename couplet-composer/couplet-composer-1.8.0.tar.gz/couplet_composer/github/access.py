# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""
This support module contains utility functions for resolving the
values for accessing the GitHub API if they are present.
"""

import logging
import os

from ..support.project_names import get_ode_repository_name


def get_api_access_values(source_root, value_file, user_agent, api_token):
    """
    Resolves the user agent and API token to be used to access
    the version 4 of the GitHub API, if they can be resolved.
    Returns two values, the first of which is the user agent to
    be used and the second the API token.

    source_root -- Path to the directory that is the root of the
    script run.

    value_file -- The pat from arguments to the file from which
    the user agent and API token can be read.

    user_agent -- The user agent given through command line
    arguments that is used when accessing the GitHub API.

    api_token -- The GitHub API token given through command line
    arguments that is used to access the API.
    """
    repository_root = os.path.join(source_root, get_ode_repository_name())
    value_file_path = os.path.join(repository_root, value_file)
    api_file_content = []

    if value_file and os.path.exists(value_file_path):
        logging.debug(
            "Found a file containing the user agent and authorization token "
            "for GitHub API from %s",
            value_file_path
        )
        with open(value_file_path) as api_file:
            api_file_content = [line.strip() for line in api_file.readlines()]
    elif not os.path.exists(value_file_path):
        logging.debug(
            "The file containing the user agent and authorization token for "
            "GitHub API wasn't found from %s",
            value_file_path
        )

    return_user_agent = None
    return_api_token = None

    if api_file_content:
        logging.debug("Adding the user agent and the API token from the file")
        return_user_agent = api_file_content[0]
        return_api_token = api_file_content[1]

    if user_agent:
        logging.debug("Adding the user agent from command line")
        return_user_agent = user_agent

    if api_token:
        logging.debug("Adding the API token from command line")
        return_api_token = api_token

    if return_user_agent and return_api_token:
        logging.info(
            "Using the GraphQL API of GitHub as user agent and access token "
            "are given"
        )
    else:
        logging.info(
            "Using the REST API of GitHub as user agent and access token "
            "aren't given"
        )

    return return_user_agent, return_api_token
