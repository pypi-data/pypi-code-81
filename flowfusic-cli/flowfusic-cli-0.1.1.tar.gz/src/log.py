import logging
import sys

logger = logging.getLogger("flowfusic_logger")


def configure_logger(verbose: bool = False) -> None:
    """
    Function configuring the logger for the whole application

    Args:
        verbose (bool): Boolean flag controlling the verbosity of the logger. True if
            DEBUG looger is on, resulting in more extensive logging. Default is False.

    Returns:

    """

    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(format="%(message)s", level=log_level, stream=sys.stdout)
