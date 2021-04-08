import argparse
import json
from typing import List

from duckietown_challenges import dtserver_auth
from .cli_common import ChallengeEnvironment, sprint, wrap_server_operations

__all__ = ["dt_challenges_cli_auth"]


def dt_challenges_cli_auth(args: List[str], environment: ChallengeEnvironment):
    """ [admin only] Queries the authorization profiles. """
    parser = argparse.ArgumentParser(prog=environment.prog)
    parser.add_argument("--cmd", required=True)
    parser.add_argument("--impersonate", default=None)

    parsed = parser.parse_args(args)

    cmd = parsed.cmd

    token = environment.token
    with wrap_server_operations():
        res = dtserver_auth(token=token, cmd=cmd, impersonate=parsed.impersonate)

    results: List[dict] = res["results"]
    sprint(json.dumps(results, indent=2))
    for result in results:
        ok = result["ok"]
        msg = result.get("msg")
        line = result.get("line")
        if msg is None:
            msg = ""
        qr = result.get("query_result")

        sprint("query: %s" % line)
        s = "OK" if ok else "ERR"
        sprint("processed: %s" % s)
        sprint("   result: %s" % qr)
        sprint("message: %s" % msg)
