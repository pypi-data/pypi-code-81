#! /usr/bin/env python3
import json
import sys
from argparse import ArgumentParser, RawTextHelpFormatter

import elg

C = elg.Catalog()


def main():

    actions_explained = """\
    ELG action to execute. Run with -h for action-specific options.
    info: Get detailed information for a specific item in the catalog.
    install: Install a specific resource (NOT IMPLEMENTED YET!)
    search: Search the ELG catalog.
    run: Run a specific LT."""

    ap = ArgumentParser(formatter_class=RawTextHelpFormatter)
    ap.add_argument("action", help=actions_explained, choices=["search", "install", "info", "run"])
    action = ap.parse_args(sys.argv[1:2]).action
    ap = ArgumentParser(prog="%s %s" % (sys.argv[0], action))

    if action in ["install", "info"]:
        ap.add_argument("id", help="Resource ID")

    elif action == "search":
        # To do:
        #
        # 1. do we need both explicit resource specification and function,
        #    or can resource type be inferred from function?
        # 2. we need to specify possible values for the various arguments with
        #    the help function.
        ap.add_argument("search_term", nargs="*", help="Search term.")
        ap.add_argument("--resource", "-r", help="Resource type")
        ap.add_argument("--lang", "-l", help="Language(s)", default="")
        ap.add_argument("--function", "-f", help="Functionality")
        ap.add_argument("--license", "-L", help="License terms")

    elif action == "run":
        ap.add_argument("id", help="Id of the LT")
        ap.add_argument("--authentication_file", "-t", help="Path to the authentication file")
        ap.add_argument("--data_file", "-f", help="Path to the data file")

    else:
        raise ValueError("action not recognize")

    opts = ap.parse_args(sys.argv[2:])
    if action == "install":
        print("Not yet implemented", file=sys.stdout)
        sys.exit(1)
        pass

    elif action == "info":
        e = elg.Entity.from_id(opts.id)
        print(e)

    elif action == "search":
        if len(opts.search_term) > 0:
            search = " ".join(['"%s"' % t for t in opts.search_term])
        else:
            search = None

        C.interactive_search(
            resource=opts.resource, languages=opts.lang, function=opts.function, search=search, license=opts.license
        )

    elif action == "run":
        lt = elg.Technology(opts.id, opts.authentication_file)
        result, status_code = lt(opts.data_file)
        if status_code == 200:
            print(result)
        else:
            print(f"Error {status_code}")


if __name__ == "__main__":
    main()
