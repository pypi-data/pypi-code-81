from datetime import datetime
from typing import IO, List, Dict

import atexit


class BaseCycleLogger:
    open_files: List[IO] = []
    MAX_LINES = 500
    MESSAGE_FORMAT = "[{date} - {time}] : {message}"
    DATE_FORMAT = "%d/%m/%Y"
    TIME_FORMAT = "%H:%M"
    FILE_MODE = "a+"
    file: IO
    message_format: str
    time_format: str
    date_format: str

    def _set_format_message(self, message_format: str, include_date: bool, include_time: bool):
        if message_format == self.MESSAGE_FORMAT:
            if not include_time and not include_date:
                message_format = message_format.replace("[{date} - {time}] : ", "")
            if not include_date:
                message_format = message_format.replace("{date} - ", "")
            elif not include_time:
                message_format = message_format.replace(" - {time}", "")
        return message_format

    @property
    def _date_and_time(self) -> Dict[str, str]:
        """
        This function return formatted date and time.

        Returns:
             dict: formatted date and time
        """
        now = datetime.now()
        return {
            "date": now.strftime(self.date_format),
            "time": now.strftime(self.time_format),
        }

    @property
    def _get_file_lines_count(self) -> int:
        """
        This function returns how many lines in a file.
        Returns:
            int - lines count.
        """
        current_seek = self.file.tell()
        self.file.seek(0)
        count = len(self.file.readlines())
        self.file.seek(current_seek)
        return count

    def _format_message(self, message: str, kwargs) -> str:
        """
        This function return formatted message string.

        Parameters:
             message (``str``):
                A message to log.
            kwargs:
                Additional arguments to pass into MESSAGE_FORMAT

        Returns:
            str - formatted message.
        """
        return self.message_format.format(
            **self._date_and_time, message=message, **kwargs
        )


def register_at_exit(cls):
    @atexit.register
    def close_files():
        """
        function to close any open file.
        """
        for file in cls.open_files:
            file.close()
