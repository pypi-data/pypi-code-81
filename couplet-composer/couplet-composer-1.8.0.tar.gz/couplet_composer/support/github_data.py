# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module contains type GitHubData for creating the
downloading assets from GitHub.
"""

from collections import namedtuple


# The type 'GitHubData' represents the data to retrieve
# repository data from GitHub.
GitHubData = namedtuple("GitHubData", [
    "owner",
    "name",
    "tag_name",
    "asset_name"
])
