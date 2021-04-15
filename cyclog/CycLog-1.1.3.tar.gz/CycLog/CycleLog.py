from itertools import islice
from typing import IO

from .utils import BaseCycleLogger, register_at_exit

__all__ = ["CycleLogger"]


class CycleLogger(BaseCycleLogger):

    """
        A class that handles a logging into a file,
        but also takes care about the max lines in a file.
        So the file will not be that long,
        and the log will only be what you really need to see in case of an error.

        Parameters:
            file_name (``str``):
                The name of the file that this logger will log into.
            include_date(``bool``, *optional*):
                Whether to include date in log message or not.
                By default - True.
            include_time(``bool``, *optional*):
                Whether to include time in log message or not.
                By default - True.
            max_lines (``int``, *optional*):
                Maximum lines in a file, when the file reaches the maximum -
                lines in the beginning will be deleted.
                By default - 500 lines.
            message_format (``str``, *optional*):
                 A format of a log message.
                 By default - [dd/mm/yyyy - {hh:mm}] : log message.
            date_format (``str``, *optional*):
                A format of the date.
                By default - dd/mm/yyyy
            time_format (``str``, *optional*):
                A format of the time.
                By default - hh:mm
            file_mode (``str``, *optional*):
                The mode that the fill will be open in.
                any write-and-read-able python mode is available.
                for example:
                    w+ - opens a new log file for every new run.
                    a+ - appends to an exists file or a new one if there is no such file, recommended.
                By default - a+
    """

    def __init__(
            self,
            *,
            file_name: str,
            include_date: bool = True,
            include_time: bool = True,
            max_lines: int = BaseCycleLogger.MAX_LINES,
            message_format: str = BaseCycleLogger.MESSAGE_FORMAT,
            date_format: str = BaseCycleLogger.DATE_FORMAT,
            time_format: str = BaseCycleLogger.TIME_FORMAT,
            file_mode: str = BaseCycleLogger.FILE_MODE
    ):
        self.message_format = self._set_format_message(message_format, include_date, include_time)
        self.max_lines = max_lines
        self.date_format = date_format
        self.time_format = time_format
        self.file = self.get_file(file_name, file_mode)

    @staticmethod
    def get_file(file_name: str, mode: str) -> IO:
        """
        This functions assigns the file into the files list to close it later,
        and returns the file.

        Returns:
            IO - a log file.
        """
        file = open(file_name, mode, buffering=1)
        file.seek(0)
        CycleLogger.open_files.append(file)
        return file

    def log(self, message: str, **kwargs):
        """
            This function logs into the file.

            Parameters:
                 message (``str``):
                    A message to log.

                kwargs:
                    Additional arguments to pass to MESSAGE_FORMAT
        """
        message = self._format_message(str(message), kwargs)
        lines = self._get_file_lines_count
        if lines >= self.max_lines:
            lines_to_remove = lines - self.max_lines + 1
            self.file.seek(0)
            tuple(islice(self.file, lines_to_remove))
            self.file.truncate(0)
            self.file.write(self.file.read())
        self.file.write(message.rstrip('\n') + '\n')


register_at_exit(CycleLogger)
