#!/usr/bin/env python3
"""
The Command Line Interface for
the Codoc SDK.


Mainly used to publish your views to the webapp.
"""
import sys
import os
import fire
import sentry_sdk
import logging


from codoc.service.finder.config import get_config

from codoc.service.finder.views import get_views_in_folder

logger = logging.getLogger(__name__)
NO_API_ERROR = """
API Key is not supplied.
Please set 'CODOC_API_KEY' as an environmental variable

Alternatively consult the documentation at https://codoc.org
"""
UNEXPECTED_ERROR = """
An unexpected error happened.

If you want us to act on this error, then use the `--report_errors` flag :)
"""


class CliHandler:
    """
    The Command Line Interface for
    the Codoc SDK.

    Mainly used to publish your views. For a complete view
    Use `codoc -h` for more information and available flags

    Args:
        path (str): The path to the codoc_views folder
        report_errors (bool): whether to send errors to the codoc dev team
        silent (bool): Whether to display logging messages
        raise_errors (bool): Whether to raise errors or print friendly errors
    """

    def __init__(
        self, path="codoc_views", report_errors=False, silent=False, raise_errors=False
    ):
        self._path = path

        self._raise_errors = raise_errors
        if not silent:
            logging.basicConfig(
                format="%(message)s",
                encoding="utf-8",
                level=logging.INFO,
            )
        self._report_errors = report_errors
        if report_errors:
            _setup_sentry()

    def publish(self, strict_mode: bool = False):
        """
        Publish all graphs in the current package

        Args:
            strict_mode (bool): Whether to terminate if dependency cannot be resolved.

        """

        sys.path.append(os.getcwd())
        try:
            config = get_config(self._path)
        except KeyboardInterrupt:
            return "Manual exit"
        except Exception as e:
            if self._raise_errors:
                raise e
            if self._report_errors:
                sentry_sdk.capture_exception(e)
                sentry_sdk.flush()
            return f"Could not load config ({error_name(e)})"

        logger.info("Starting to bootstrap")
        try:
            try:
                graph = config.bootstrap(strict_mode=strict_mode)
                # TODO
            except TypeError:
                logger.warning(
                    "Please pass kwargs into bootstrap! this will be deprecated soon!"
                )
                graph = config.bootstrap()
        except KeyboardInterrupt:
            return "Manual exit"
        except Exception as e:
            if self._raise_errors:
                raise e
            if self._report_errors:
                sentry_sdk.capture_exception(e)
                sentry_sdk.flush()
            return f"Could not run bootstrap ({error_name(e)})"
        logger.info("Graph loaded")

        api_key = os.getenv("CODOC_API_KEY")
        if not api_key:
            return NO_API_ERROR

        logger.info("Loading views")
        views = get_views_in_folder(self._path)

        resp = []
        for view in views:
            logger.info(f"Publishing {view.label}...")
            try:
                pk = view(graph=graph, api_key=api_key)
            except KeyboardInterrupt:
                return "Manual exit"
            except Exception as e:
                if self._raise_errors:
                    raise e
                error = f"An unexpected error occurred when running `{view.label}` ({error_name(e)})"
                if self._report_errors:
                    sentry_sdk.capture_exception(e)
                    sentry_sdk.flush()
                    return f"{error}\n\nThe error has been reported"
                return f"{error}\n\nRerun with `--report_errors` to report the errors"
            url = get_url_for_graph(pk)
            resp.append(f"'{view.label}' published at:\n{url}")

        return "\n".join(resp)

    def list_views(self):
        """
        returns a list of all the views found.
        """
        views = get_views_in_folder(self._path)
        if not views:
            return "No views found"
        sep = " - "
        return sep + ("\n" + sep).join(v.__name__ for v in views)


def get_url_for_graph(pk: int) -> str:
    return f"https://codoc.org/app/graph/{pk}"


def _main():
    fire.Fire(CliHandler)


if __name__ == "__main__":
    _main()


def error_name(error):
    return str(error) or error.__class__.__name__


def _setup_sentry():
    sentry_sdk.init(
        "https://d4168cc6cb0e44339911e3ede140853e@o522026.ingest.sentry.io/5700616",
    )
