from copy import deepcopy
from datetime import datetime
import pathlib
import os
import PySimpleGUI as sg
from typing import Optional, Union, Callable
from .uploader import Uploader, utils
from .layout import create_layout
from .__version__ import __version__
from . import config, auth
from loguru import logger
import sys


class App:
    def __init__(
        self,
        key: Optional[Union[str, bytes]],
        title: str = f"Google Cloud Storage Uploader - {__version__}",
        with_authentication: bool = True,
        with_service_account: bool = True,
        with_bucket_id: bool = True,
        with_password: bool = False,
        with_checkboxes: bool = False,
        dry_run: bool = False,
        service_account_path: pathlib.Path = config.service_account_path,
        client_secrets_path: pathlib.Path = config.client_secrets_path,
        user_credentials_path: pathlib.Path = config.get_user_credentials_path(),
        log_file_path: pathlib.Path = config.get_log_file_path(),
        icon: Optional[pathlib.Path] = config.get_icon_path(),
        prefix: Optional[Union[str, Callable[[], str]]] = None,
    ) -> None:

        logger.info(f"Starting app (version {__version__})")

        self.last_updated = datetime.now()
        self.key = key
        self.dry_run = dry_run
        self.service_account_path = pathlib.Path(service_account_path)
        self.client_secrets_path = pathlib.Path(client_secrets_path)
        self.user_credentials_path = pathlib.Path(user_credentials_path)
        self.log_file_path = log_file_path
        self._prefix = prefix

        default_bucket = auth.default_bucket_from_service_account_file(
            self.service_account_path
        )
        self.default_bucket = default_bucket if default_bucket is not None else ""
        self.window = sg.Window(
            title,
            create_layout(
                with_bucket_id,
                with_authentication,
                with_service_account,
                with_checkboxes,
                with_password,
                default_bucket=default_bucket,
            ),
            icon=icon,  # Yes, icon is needed here!
        )
        # Hack to remove icon from title bar, but is needed above on macos!
        if sys.platform == "darwin" and icon is not None:
            self.window.set_icon(None)

    @property
    def prefix(self):
        if self._prefix is None:
            return ""
        if callable(self._prefix):
            return self._prefix()
        return self._prefix

    def callback(self, stats):
        if stats.complete:
            self.window.write_event_value("UPLOADER-DONE", deepcopy(stats))
            return

        # Update progress at a lower rate
        now = datetime.now()
        if (now - self.last_updated).seconds > 0.3:
            self.last_updated = now
            self.window.write_event_value("UPLOADER-PROGRESS", deepcopy(stats))

    def update_progress(self, stats):

        perc = (
            int(100 * (stats.bytes_so_far / stats.total_bytes))
            if stats.total_bytes
            else 0
        )
        self.window["PROGRESS"].update(stats.bytes_so_far, stats.total_bytes, True)

        self.window["PROGRESS-TEXT"].update(
            f"{utils.display_bytes(stats.bytes_so_far)} of "
            f"{utils.display_bytes(stats.total_bytes)} ({perc}%)",
        )

        msg = [
            f"Uploaded: {stats.num_uploaded} of {stats.num_files} files",
            f"Skipped: {stats.num_skipped}",
            f"Errors: {stats.num_errors}",
            f"Elapsed time: {utils.display_time(stats.elapsed_time)}",
        ]

        if stats.complete:
            msg.append("Status: Inactive")
            self.window["START"].update(disabled=False)
            self.window["STOP"].update(disabled=True)
            self.window["AUTH"].update(disabled=False)
        else:
            msg.append("Status: Active")

        self.window["STATS"].update("\n".join(msg))

    def clear_status(self):
        self.window["STATS"].update("")
        self.window["PROGRESS-TEXT"].update("")
        self.window["PROGRESS"].update(0, 100, True)

    def display_error(self, msg=None):
        msg = "View the log file for details" if msg is None else msg
        msg = f"Error occurred:\n{msg}"
        self.window["FEEDBACK"].update(msg)
        self.clear_status()

    def run(self):

        uploader = None

        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                if uploader is not None:
                    uploader.stop()
                break

            if event == "START":
                logger.info("Action: New upload started")

                # If SA file provided, use that over user credentials
                if os.path.isfile(values.get("SA-FILE", "")):
                    user_credentials_path = None
                    sa_file = values.get("SA-FILE")
                else:
                    user_credentials_path = self.user_credentials_path
                    sa_file = self.service_account_path
                if values.get("PW"):
                    key = auth.key_from_password(values.get("PW"), self.key)
                else:
                    key = self.key

                try:
                    uploader = Uploader(
                        bucket_id=(
                            values.get("BUCKET")
                            if values.get("BUCKET")
                            else self.default_bucket
                        ),
                        service_account_file=sa_file,
                        user_credentials_path=user_credentials_path,
                        key=key,
                        client_secrets_path=self.client_secrets_path,
                        dry_run=self.dry_run,
                        prefix=(
                            datetime.utcnow().isoformat()
                            if values.get("DATETIME-PREFIX")
                            else self.prefix
                        ),
                        delete_files_after_upload=values.get("DELETE", False),
                    )
                    uploader.start(
                        [
                            pathlib.Path(_)
                            for _ in values["PATHS"].split(sg.BROWSE_FILES_DELIMITER)
                        ],
                        self.callback,
                    )
                    self.last_updated = datetime.now()
                    dt = self.last_updated.strftime("%d, %b at %T")
                    self.window["FEEDBACK"].update(f"Upload started on {dt}")
                    self.window["START"].update(disabled=True)
                    self.window["STOP"].update(disabled=False)
                    self.window["AUTH"].update(disabled=True)
                    self.window["PROGRESS"].update(0, 100, True)
                except ValueError as e:
                    logger.exception("Value error during startup")
                    self.display_error(msg=e)
                    continue
                except Exception:
                    logger.exception("Uploader raised exception on startup")
                    self.display_error()
                    continue

            elif event == "STOP" and uploader is not None:
                logger.info("Action: stop current upload")
                self.window["STOP"].update(disabled=True)
                uploader.stop()
                self.window["FEEDBACK"].update("Stopping transfer...")

            elif event == "AUTH":
                logger.info("Action: execute user authentication")
                Uploader.run_oauth_flow(
                    self.user_credentials_path,
                    self.client_secrets_path,
                    self.key,
                )

            elif event == "VIEW-LOG":
                logger.info("Action: View log file")
                try:
                    utils.open(self.log_file_path)
                except Exception as e:
                    logger.exception(f"Failed to open {self.log_file_path}")
                    self.window["FEEDBACK"].update(e)
                    pass
            elif event == "UPLOADER-PROGRESS":
                self.update_progress(values.get("UPLOADER-PROGRESS"))
            elif event == "UPLOADER-DONE":
                self.update_progress(values.get("UPLOADER-DONE"))
                self.window["FEEDBACK"].update("")

        self.window.close()
