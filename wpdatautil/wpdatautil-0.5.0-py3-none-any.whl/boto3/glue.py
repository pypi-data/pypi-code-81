"""boto3 glue client utilities."""
import logging
import time
import timeit
from typing import Any

import boto3

log = logging.getLogger(__name__)

# Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html


def ensure_crawler(**kwargs: Any) -> None:
    """Ensure that the specified AWS Glue crawler exists with the given configuration.

    At minimum the `Name` and `Targets` keyword arguments are required.
    """
    # Use defaults
    assert all(kwargs.get(k) for k in ("Name", "Targets"))
    defaults = {
        "Role": "AWSGlueRole",
        "DatabaseName": kwargs["Name"],
        "SchemaChangePolicy": {"UpdateBehavior": "UPDATE_IN_DATABASE", "DeleteBehavior": "DELETE_FROM_DATABASE"},
        "RecrawlPolicy": {"RecrawlBehavior": "CRAWL_EVERYTHING"},
        "LineageConfiguration": {"CrawlerLineageSettings": "DISABLE"},
    }
    kwargs = {**defaults, **kwargs}

    # Ensure crawler
    client = boto3.client("glue")
    name = kwargs["Name"]
    try:
        response = client.create_crawler(**kwargs)
        log.info(f"Created crawler {name}.")
    except client.exceptions.AlreadyExistsException:
        response = client.update_crawler(**kwargs)
        log.info(f"Updated crawler {name}.")
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200


def run_crawler(crawler: str, *, timeout_minutes: int = 60, retry_seconds: int = 5) -> None:
    """Run the specified AWS Glue crawler, waiting until completion."""
    # Ref: https://stackoverflow.com/a/66072347/
    timeout_seconds = timeout_minutes * 60
    client = boto3.client("glue")
    start_time = timeit.default_timer()
    abort_time = start_time + timeout_seconds

    def wait_until_ready() -> None:
        state_previous = None
        while True:
            response_get = client.get_crawler(Name=crawler)
            state = response_get["Crawler"]["State"]
            if state != state_previous:
                log.info(f"Crawler {crawler} is {state.lower()}.")
                state_previous = state
            if state == "READY":  # Other known states: RUNNING, STOPPING
                return
            if timeit.default_timer() > abort_time:
                raise TimeoutError(f"Failed to crawl {crawler}. The allocated time of {timeout_minutes:,} minutes has elapsed.")
            time.sleep(retry_seconds)

    wait_until_ready()
    response_start = client.start_crawler(Name=crawler)
    assert response_start["ResponseMetadata"]["HTTPStatusCode"] == 200
    log.info(f"Crawling {crawler}.")
    wait_until_ready()
    log.info(f"Crawled {crawler}.")
