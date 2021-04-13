from datetime import datetime
import logging
from typing import Dict, List, Any, Optional, Union

from dateutil.parser import parse, ParserError
import pytz

from arthurai.common.exceptions import UserTypeError, UserValueError

logger = logging.getLogger(__name__)

"""
Only client facing utils should live in this funciton. If a util  is used for a specific package and not client facing
it should be added to that packages util.py file.
"""


def format_timestamps(inferences: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Checks list of json inferences to ensure their timestamps have been converted to ISO8601 conventions.

    :param inferences: Input to `send_inferences()` function.

    :return: updated list of json inferences with ISO8601 formatted timestamps
    :raise: TypeError: timestamp is not of type `datetime.datetime`
    :raise: ValueError: timestamp is not timezone aware and no location data is provided to remedy
    """
    # TODO: deprecate support for strings and delete conditional @ https://arthurai.atlassian.net/jira/software/projects/CR/boards/11?selectedIssue=CR-10
    if len(inferences) > 0 and (
        is_string_date(inferences[0].get("inference_timestamp"))
        or is_string_date(inferences[0].get("ground_truth_timestamp"))
    ):
        date_to_log = inferences[0].get("inference_timestamp") or inferences[0].get(
            "ground_truth_timestamp"
        )
        logger.warning(
            f"DEPRECATION WARNING: Your provided timestamps starting with: {date_to_log} is of type `str` and is assumed to be in UTC format. Timezone information will be ignored. `str` types will be deprecated. Please use timeaware `datetime.datetime` timestamps and use `arthurai.util.format_timestamp` if needed, e.g. `format_timestamp(datetime.strptime('2020-01-01 01:01:01', '%Y-%m-%d %H:%M:%S'), 'US/Eastern')`.",
        )

    for inf in inferences:
        for timestamp_key in ["inference_timestamp", "ground_truth_timestamp"]:
            if timestamp_key in inf:
                inf[timestamp_key] = format_timestamp(inf[timestamp_key])
    return inferences


def format_timestamp(
    timestamp: Union[datetime, str], location: Optional[str] = None
) -> str:
    """Check if timestamp is time aware and convert to ISO8601 conventioned string.

    This helper function converts datetime objects into timezone aware ISO8601 strings, which is necessary when sending JSON to Arthur's backend.
    If `timestamp` argument is timezone aware, no `location` needs to be provided; otherwise, a string pytz `location` like "US/Eastern"
    needs to be provided to establish timezone.
    String `timestamp` are supported for backwards compatability and for simplicity are assumed to already be in UTC format, but string support
    will be deprecated.

    :param timestamp: timestamp to format
    :param location: pytz location as string

    :return: ISO8601 formatted timestamp
    :raise: TypeError: timestamp is not of type `datetime.datetime`
    :raise: ValueError: timestamp is not timezone aware and no location data is provided to remedy
    """

    # TODO: deprecate support for strings and delete conditional @ https://arthurai.atlassian.net/jira/software/projects/CR/boards/11?selectedIssue=CR-10
    if isinstance(timestamp, str):
        if timestamp[-1] != "Z":
            return timestamp + "Z"
        return timestamp

    if not (location is None or isinstance(location, str)):
        raise UserTypeError(f"`location` must be valid pytz string like 'US/Eastern' or None type")

    localization = pytz.timezone(location) if location else None

    if not isinstance(timestamp, datetime):
        raise UserTypeError(
            f"`timestamp` {timestamp} must be of type `datetime.datetime`, not {type(timestamp)}."
        )

    if not (
        timestamp.tzinfo is not None
        and timestamp.tzinfo.utcoffset(timestamp) is not None
    ):
        if localization:
            return (
                localization.localize(timestamp).astimezone(pytz.utc).isoformat()[:-6]
                + "Z"
            )  # convert to utc, log warning if converting from non-utc to utc
        else:
            raise UserValueError(
                f"`timestamp` {timestamp} is not timezone aware, please supply pytz `timezone` string to make timestamp timezone aware, e.g. `format_timestamp(datetime.datetime(2021, 1, 1), 'US/Eastern')`."
            )
    return timestamp.astimezone(pytz.utc).isoformat()[:-6] + "Z"


# TODO: deprecate support for strings and delete method @ https://arthurai.atlassian.net/jira/software/projects/CR/boards/11?selectedIssue=CR-10
def is_string_date(string: Any, fuzzy=False) -> bool:
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    if not isinstance(string, str) or string.isdigit():
        return False
    try:
        parse(string, fuzzy=fuzzy)
    except ParserError:
        return False
    else:
        return True
