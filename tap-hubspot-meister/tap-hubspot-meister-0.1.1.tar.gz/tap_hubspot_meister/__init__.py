#!/usr/bin/env python3
import json
import os
import sys

import singer
from hubspot import HubSpot

from discover import discover
from sync import sync

REQUIRED_CONFIG_KEYS = ["redirect_uri", "start_date"]


LOGGER = singer.get_logger()


def do_discover():
    LOGGER.info("Starting discover")
    catalog = discover()
    json.dump(catalog.to_dict(), sys.stdout, indent=2)
    LOGGER.info("Finished discover")


@singer.utils.handle_top_exception(LOGGER)
def main():

    parsed_args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

    state = {}
    if parsed_args.state:
        state = parsed_args.state

    config = parsed_args.config
    if config.get("hapikey") is not None:
        client = HubSpot(api_key=config["hapikey"])
    else:
        client = HubSpot()
        tokens = client.auth.oauth.default_api.create_token(
            grant_type="refresh_token",
            redirect_uri="http://example.com",
            client_id=os.environ["CLIENT_ID"],
            client_secret=os.environ["CLIENT_SECRET"],
            refresh_token=os.environ["REFRESH_TOKEN"],
        )
        client.access_token = tokens.access_token
        os.environ["REFRESH_TOKEN"] = tokens.refresh_token

    if parsed_args.discover:
        do_discover()
    elif parsed_args.catalog:
        sync(client=client, config=config, catalog=parsed_args.catalog, state=state)


if __name__ == "__main__":
    main()
