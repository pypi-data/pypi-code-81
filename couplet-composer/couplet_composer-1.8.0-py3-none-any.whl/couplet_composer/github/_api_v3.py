# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""
This support module contains helper functions for accessing the
version 3 of the GitHub API (the REST API).
"""

import logging

import requests


def _get_api_endpoint():
    """
    Returns the end point of the version 3 of the GitHub API (the
    REST API).
    """
    return "https://api.github.com"


def _get_accept_header():
    """
    Returns the default value for the Accept header for the REST
    API calls.
    """
    return "application/vnd.github.v3+json"


def make_api_call(call_path):
    """
    Makes a call to the GitHub REST API using the given path
    appended to the end point and returns the JSON result.

    call_path -- The path that will be appended to the API end
    point.
    """
    logging.debug(
        "Making a GitHub REST API call with the following path:\n%s",
        call_path
    )

    # Redirects which are required for the REST API are enabled
    # by default.
    response = requests.get(
        url="{}{}".format(_get_api_endpoint(), call_path),
        headers={
            "User-Agent": "Couplet Composer",
            "Accept": _get_accept_header()
        }
    )

    logging.debug(
        "The returned value from the REST API is the following:\n%s",
        response
    )
    logging.debug(
        "The returned JSON data from the REST API is the following:\n%s",
        response.json()
    )

    return response.json()


def find_release_asset_id(api_response, name):
    """
    Looks for the wanted release asset node from the response
    JSON data of the GitHub API and returns its ID, if found.

    api_response -- The JSON data got from the GitHub API where
    the node is looked for.

    name -- The name of the release asset.
    """
    asset_id = None
    for node in api_response:
        if node["name"] == name:
            asset_id = node["id"]
    return asset_id
