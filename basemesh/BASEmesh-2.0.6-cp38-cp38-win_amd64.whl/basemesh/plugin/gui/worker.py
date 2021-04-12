# A component of the BASEmesh pre-processing toolkit.
# Copyright (C) 2020  ETH Zürich

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Worker objects for long-running operations."""

from collections import deque
from contextlib import redirect_stdout
from typing import Any, Callable, Deque, Iterable, IO, Mapping, Optional
from PyQt5.QtCore import QObject, pyqtSignal
from ...feedback import Feedback


class Worker(QObject):
    """Generic worker task wrapper."""

    done = pyqtSignal(object)  # The return value of the worker
    error = pyqtSignal(object)  # The error raised
    print = pyqtSignal(object)  # The deque containing the printed data
    status = pyqtSignal(object)  # The feedback status tuple

    def __init__(self, target: Callable[..., Any],
                 args: Optional[Iterable[Any]] = None,
                 kwargs: Optional[Mapping[str, Any]] = None) -> None:
        """Initialise the worker for a given callable.

        Parameters
        ----------
        target : Callable[..., Any]
            The callable to run in the worker thread
        args : Iterable[Any], optional
            Any positional arguments to pass to the target callable, by
            default None
        kwargs : Mapping[str, Any], optional
            Any keyword arguments to pass to the target callable, by
            default None
        """
        super().__init__()
        self.args = args if args is not None else ()
        self.feedback = Feedback(self._emit_status)
        self.kwargs = kwargs if kwargs is not None else {}
        self.target = target
        self._queue: Deque[str] = deque()

    def _emit_status(self, progress: Optional[float], msg: Optional[str],
                     busy: bool) -> None:
        """Emit the status signal for this worker.

        Parameters
        ----------
        progress : Optional[float]
            The new progress value, or None to keep unchanged
        msg : Optional[str]
            The new status message, or None to keep unchanged
        busy : bool
            Whether the worker is currently busy
        """
        self.status.emit((progress, msg, busy))

    def cancel(self) -> None:
        """Flag to inform the worker to stop operation."""
        self.feedback.cancel()

    def run(self) -> None:
        """Run the worker's target callable.

        This is the task that will be spun off into another thread.
        """
        # NOTE: This stream technically does not support the IO ABC, but adding
        # all of those methods with NotImplementedErrors just for type
        # strictness seems a bit pointless.
        stream: IO[str] = _WriteOnlyStream(
            self.print, self._queue)  # type: ignore
        with redirect_stdout(stream):
            try:
                value = self.target(self.feedback, *self.args, **self.kwargs)
            except BaseException as err:  # pylint: disable=broad-except
                self.error.emit(err)
                value = None
        self.done.emit(value)


class _WriteOnlyStream:
    """A write-only text stream used to redirect prints to the caller.

    This does not follow the IO[str] type due to missing
    functionality and is only intended for internal use with the
    contextlib.redirect_stdout() context manager.
    """

    def __init__(self, signal: pyqtSignal, output: Deque[str]) -> None:
        """Instantiate a new write-only, cross-thread stream.

        Parameters
        ----------
        signal : pyqtSignal
            The signal to emit when written to
        output : Deque[str]
            An external deque to store writes in
        """
        self._output = output
        self._signal = signal

    def close(self) -> None:
        """Close the stream."""
        self._output.clear()

    def write(self, msg: str) -> int:
        """Write the given string to the stream.

        Parameters
        ----------
        msg : str
            The message to write

        Returns
        -------
        int
            The number of characters written
        """
        self._output.append(msg)
        self._signal.emit(self._output)
        return len(msg)
