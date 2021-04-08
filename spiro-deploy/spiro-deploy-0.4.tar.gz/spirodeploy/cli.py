#!/usr/bin/env python3
"""
"""
import os
import sys
import argparse
import pprint
import hues
from .client import upload
from .builder import TarballBuilder, git_scanner, fs_scanner


SCANNERS = {
    'git': git_scanner,
    'filesystem': fs_scanner,
    'fs': fs_scanner,
}


def build_argparse(environ=os.environ):
    parser = argparse.ArgumentParser(description="SpiroFS Deployment Client")
    parser.add_argument("project", help="Name of project to deploy to")
    parser.add_argument("deployment", help="Name of specific deployment inside of project to deploy to")
    parser.add_argument("--highstate", action="store_true", dest="highstate", default=True,
            help="Highstate after deployment (default)")
    parser.add_argument("--no-highstate", action="store_false", dest="highstate",
            help="Do not highstate")
    parser.add_argument("--artifact", action="append", metavar="PATH", default=[],
            help="Add the given file/directory into the bundle under _artifacts")
    parser.add_argument("--include-source", type=(lambda v: SCANNERS[v]), default=..., nargs='?',
            help="Include the source as _source, using the specified method, of " + ", ".join(sorted(SCANNERS.keys())))
    parser.add_argument("--token", metavar="TOKEN", default=environ.get("SPIRO_TOKEN", "").strip(),
            help="Token to use to authenticate with the server")
    parser.add_argument("--server", metavar="URL", default=environ.get("SPIRO_URL", "https://salt:4510/").strip(),
            help="URL to POST to, defaults to https://salt:4510/")
    parser.add_argument("--insecure", action="store_false", dest="sslverify",
            help="Do not verify SSL certificates. EXTREMELY UNRECOMMENDED.")
    parser.add_argument("--ssl-cert", dest="sslverify", metavar="FILE",
            help="Key or CA to use for SSL key verification.")
    return parser


def _print_update(data):
    print("")
    print(hues.huestr("== {} ==".format(data['minion'])).bold.colorized, flush=True)
    if data['result'].get('failed'):
        hs = hues.huestr("(No Results)")
        print(hs.red.colorized, flush=True)
        return 1

    print("")
    ret = data['result'].get('ret')
    if isinstance(ret, dict):
        states = sorted(ret.values(), key=lambda s: s.get('__run_num__'))
        for state in states:
            hs = hues.huestr(pprint.pformat(state))
            # FIXME: Only color if isatty
            if not state['result']:
                print(hs.red.colorized, flush=True)
            elif state['changes']:
                print(hs.green.colorized, flush=True)
            else:
                print(hs.blue.colorized, flush=True)
    elif isinstance(ret, list) and len(ret) == 1:
        hs = hues.huestr(ret[0])
        print(hs.red.colorized, flush=True)
    elif ret is None:
        txt = pprint.pformat(data['result'])
        print("(Result)", txt, flush=True)
    else:
        txt = pprint.pformat(ret)
        print(txt, flush=True)
    return data['result'].get('retcode')


def _print_exception(data):
    hs = hues.huestr("Error occurred on server: {}".format(data['msg']))
    print(hs.red.colorized, flush=True)
    return 1


EVENT_PRINTERS = {
    'highstate-update': _print_update,
    'exception': _print_exception,
}


def main(argv=sys.argv[1:]):
    args = build_argparse().parse_args(argv)
    print("Collecting files for {} ({})".format(args.project, args.deployment), flush=True)
    with TarballBuilder() as builder:
        try:
            builder.add_gitcommit()
        except FileNotFoundError:
            print("Warning: No git binary", file=sys.stderr, flush=True)
        if os.path.exists('_salt'):
            builder.add_saltdir('_salt')
        for a in args.artifact:
            builder.add_artifact(a, a)
        if args.include_source is not ...:
            builder.add_source(args.include_source)

    
    print("Uploading to server", flush=True)
    rv = 0
    minions = set()
    reported_minions = set()
    for event, data in upload(
        args.server,
        args.token,
        builder.buffer,
        args.project,
        args.deployment,
        highstate=args.highstate,
        sslverify=args.sslverify
    ):
        if event in EVENT_PRINTERS:
            rv = rv or EVENT_PRINTERS[event](data)
        elif 'msg' in data:
            print(data['msg'], flush=True)
        else:
            print(event, pprint.pformat(data), flush=True)

        if event == 'highstate-start':
            minions |= set(data['minions'])
        elif event == 'highstate-update':
            reported_minions.add(data['minion'])

    print("{} minions reported of {}".format(len(reported_minions), len(minions)))

    missing_minions = minions - reported_minions

    if missing_minions:
        print(
            hues.huestr(
                "Unreported minions: {}".format(', '.join(sorted(missing_minions)))
            ).red.colorized
        )

    return rv
