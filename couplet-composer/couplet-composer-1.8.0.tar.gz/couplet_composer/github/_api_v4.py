# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module contains helper functions for accessing the
version 4 of the GitHub API.
"""

import json
import logging

import requests


def _get_api_endpoint():
    """
    Returns the end point of the version 4 of the GitHub API.
    """
    return "https://api.github.com/graphql"


def make_api_call(query, user_agent, api_token):
    """
    Makes a call to the GitHub GraphQL API using the given query
    and returns the result.

    query -- The GraphQL query that is used in the call.

    user_agent -- The user agent used when accessing the GitHub
    API.

    api_token -- The GitHub API token that is used to access the
    API.
    """
    logging.debug(
        "Making GitHub API call with the following query:\n%s",
        query
    )

    response = requests.post(
        url=_get_api_endpoint(),
        data=json.dumps({"query": query}),
        headers={
            "User-Agent": user_agent,
            "Accept": "application/json",
            "Authorization": "bearer {}".format(api_token)
        })

    logging.debug(
        "The returned value from the API is the following:\n%s",
        response
    )
    logging.debug(
        "The returned JSON data from the API is the following:\n%s",
        response.json()
    )

    return response.json()


def find_release_node(api_response):
    """
    Looks for the wanted release node from the response JSON data
    of the GitHub API and returns the node, if found.

    api_response -- The JSON data got from the GitHub API where
    the node is looked for.
    """
    release_id = api_response["data"]["repository"]["release"]["id"]
    release_edges = api_response["data"]["repository"]["releases"]["edges"]
    release_node = None
    for edge in release_edges:
        node = edge["node"]
        if node is None or node["id"] == "":
            continue
        if node["id"] == release_id:
            release_node = node
    return release_node
