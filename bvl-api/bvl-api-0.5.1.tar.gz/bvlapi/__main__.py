#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script is run when using `python3 -m bvlapi <|club guid|search query>`.

import sys

from bvlapi.data.teams.get import get_teams
from bvlapi.data.organizations import get_organizations
from bvlapi.guid.club import is_club_guid


def run_script(args):
    """ Main part of script that delegates control to proper handler.
    """
    if len(args) == 0:
        print_help()
    elif is_club_guid(args[0]):
        search_with_guid(args[0])
    else:
        search_with_query(args)


def search_with_guid(guid):
    """ Prints all teams for a single team.
    """
    teams = get_teams(guid)
    if not teams:
        print("no teams found")
        return
    for team in teams:
        print(team.name, ":", team.guid)


def search_with_query(args):
    """ Prints all teams for each team that matches a part of the query.
    """
    found_organizations = []
    for org in get_organizations():
        if any([(a in org.name) for a in args]):
            found_organizations.append(org)
    if not found_organizations:
        print("no clubs found")
        return
    for org in found_organizations:
        search_with_guid(org.guid)
        print("")


def print_help():
    """ Prints instructions on how to use script.
    """
    print("This script is used to list all teams of a club.")
    print("")
    print("You can provide a club GUID:")
    print("")
    print("    $ python3 -m bvlapi BVBL1004")
    print("")
    print("You can also provide one or multiple search terms.")
    print("")
    print("    $ python3 -m bvlapi Antwerp")
    print("")


if __name__ == "__main__":
    run_script([str(arg) for arg in sys.argv[1:]])
