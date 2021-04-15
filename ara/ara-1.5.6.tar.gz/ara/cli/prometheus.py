# Copyright (c) 2020 The ARA Records Ansible authors
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import logging
import os
import sys
from datetime import datetime, timedelta

from cliff.command import Command

import ara.cli.utils as cli_utils
from ara.cli.base import global_arguments
from ara.clients.utils import get_client

from prometheus_client import start_http_server, Summary

class PlayDelete(Command):
    """ Deletes the specified play and associated resources """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(PlayDelete, self).get_parser(prog_name)
        parser = global_arguments(parser)
        # fmt: off
        # TODO: Arguments
        # fmt: on
        return parser

    def take_action(self, args):
        client = get_client(
            client=args.client,
            endpoint=args.server,
            timeout=args.timeout,
            username=args.username,
            password=args.password,
            verify=False if args.insecure else True,
            run_sql_migrations=False,
        )

        # TODO: Improve client to be better at handling exceptions
        # Get metrics
        # playbooks per ansible version
        # playbooks per controller
        # playbook duration
        # number of playbooks
        # number of plays
        # number of tasks
        # number of results
        # number of hosts

        playbooks = client.get("/api/v1/playbooks", limit=1)["count"]
        plays = client.get("/api/v1/plays", limit=1)["count"]
        hosts = client.get("/api/v1/hosts", limit=1)["count"]
        tasks = client.get("/api/v1/tasks", limit=1)["count"]
        results = client.get("/api/v1/results", limit=1)["count"]
        records = client.get("/api/v1/records", limit=1)["count"]

def main():
    parser = argparse.ArgumentParser()
    

client = get_client(
    client=args.client,
    endpoint=args.server,
    timeout=args.timeout,
    username=args.username,
    password=args.password,
    verify=False if args.insecure else True,
    run_sql_migrations=False,
)


# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)