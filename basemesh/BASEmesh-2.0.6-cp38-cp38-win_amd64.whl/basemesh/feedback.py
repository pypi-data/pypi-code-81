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

"""Helper classes and methods used to provide LRO feedback."""

from types import TracebackType
from typing import Callable, Optional, Type

# Type aliases
FeedbackCallback = Callable[[Optional[float], Optional[str], bool], None]


class Feedback:
    """Generic interface for interacting with long-running functions.

    This class allows functions performing long-running operations
    (aka. LROs, generally anything over 1-2 seconds of blocking time)
    to communicate with their caller.

    The function can share its currents status using the
    Feedback.update() method. For processes of unknown length (such as
    network activity or external programs), you can use the
    Feedback.busy() context manager.

    If your workload supports cancellation, be sure to check the
    Feedback.is_cancelled flag as often as is sensible. It is set when
    the caller requests the termination of the operation.

    The callback function provided as part of the initialiser will be
    passed three positional arguments: a float between 0.0 and 1.0 that
    signifies the progress of the function, a status string, and a
    Boolean flag that shows whether the function flagged itself as busy
    (i.e. working but unable to give progress updates).
    """

    class FeedbackBusyContext:
        """Context manager for unresponsive subtask states.

        This only sets the Feedback.is_busy flag and is provided for
        syntactic sugar. It performs no error handling or suppression
        whatsoever.
        """

        def __init__(self, feedback: 'Feedback',
                     msg: Optional[str] = None) -> None:
            """Create the feedback context.

            Parameters
            ----------
            feedback : Feedback
                The feedback object to modify.
            msg : str, optional
                A status message to broadcast when entering the context
                manager, by default None
            """
            self.feedback = feedback
            self._msg = msg

        def __enter__(self) -> None:
            """Flag the feedback object as busy.

            This is called when the feedback.busy() context handler
            is entered. Does not return a value.
            """
            self.feedback._is_busy = True
            msg = None
            if self._msg is not None:
                msg = self.feedback._prefix + self._msg
            self.feedback._callback(None, msg, True)

        def __exit__(self, exc_type: Type[BaseException],  # type: ignore
                     exc_val: BaseException,
                     exc_traceback: TracebackType) -> bool:
            """Flag the feedback object as no longer busy.

            This performs no error handling whatsoever.

            Parameters
            ----------
            exc_type : Type[BaseException]
                The exception class that was raised
            exc_val : BaseException
                The exception instance raised
            exc_traceback : TracebackType
                Exception traceback

            Returns
            -------
            bool
                Whether the exception should be suppressed
            """
            self.feedback._is_busy = False
            return False

    def __init__(self, callback: FeedbackCallback,
                 prefix: Optional[str] = None) -> None:
        """Set up a new feedback wrapper using the given callback.

        The callback function will be called whenever the status is
        updated, make sure it is very light-weight or rate limited if
        necessary.

        See the docstring of the Feedback class for a list of arguments
        that will be passed.

        Parameters
        ----------
        callback : Callable[Optional[float], Optional[str], bool]
            The callback function to run when the status is updated
        prefix : str, optional
            An optional prefix to use for status messages; reset using
            the Feedback.set_prefix() method, by default None
        """
        self._callback = callback
        self._is_busy = False
        self._is_cancelled = False
        self._prefix = '' if prefix is None else prefix
        self._scaling_span = 1.0
        self._scaling_offset = 0.0

    @property
    def is_busy(self) -> bool:
        """Return whether the task is flagged as busy."""
        return self._is_busy

    @property
    def is_cancelled(self) -> bool:
        """Return whether the task has been cancelled."""
        return self._is_cancelled

    def busy(self, msg: Optional[str] = None) -> 'FeedbackBusyContext':
        """Return a context manager for the FEedback.is_busy flag.

        Use this to flag a part of your LRO as busy, meaning that it is
        working but unable to give progress updates, as may occur while
        waiting for an external executable to exit, or while awaiting
        network traffic.::

            with feedback.busy('Awaiting execution...'):
                # Within this block, the feedback status will
                # always report "busy" and any updates to the
                # progress will be silently ignored.
                subtask.part1()
                # Updating the status message is still permissable
                feedback.update(msg='Almost done...')
                subtask.part2(b)
            feedback.update(1.0, 'Done')

        Parameters
        ----------
        msg : str, optional
            A status message to when the context manager is entered, by
            default None

        Returns
        -------
        FeedbackBusyContext
            A context manager during which the feedback object will be
            flagged as busy

        """
        context = self.FeedbackBusyContext(self, msg)
        return context

    def cancel(self) -> None:
        """Flag the current task as cancelled.

        This informs the function that it should exit gracefully as
        quickly as possible.
        """
        self._is_cancelled = True

    def clear_prefix(self) -> None:
        """Clear the status message prefix."""
        self._prefix = ''

    def clear_scaling(self) -> None:
        """Reset the scaling behaviour."""
        self._scaling_span = 1.0
        self._scaling_offset = 0.0

    @staticmethod
    def scale(value: float, total: float, offset: float = 0.0) -> float:
        """Rescale a given progress value to another range.

        This is mostly used to calculate the total progress of multiple
        sub-tasks, e.g. being 80% finished with a task that is itself
        only half the total workload would mean 40% total progress:

            >>> Feedback.scale(0.8, 0.5)
            0.4

        Parameters
        ----------
        value : float
            The progress of the sub task
        total : float
            How big the sub task is relative to the total job
        offset : float, optional
            An offset to prepend; useful to add the weight of other
            sub tasks that already completed, by default 0.0

        Returns
        -------
        float
            The scaled progress value
        """
        if value < 0.0:
            value = 0.0
        elif value > 1.0:
            value = 1.0
        if total < 0.0:
            total = 0.0
        elif total > 1.0 - offset:
            total = 1.0 - offset
        new_val = offset + value*total
        if new_val < 0.0:
            return 0.0
        if new_val > 1.0:
            return 1.0
        return new_val

    def set_busy(self, is_busy: bool = True) -> None:
        """Set the Feedback.is_busy flag.

        This function is provided for compatibility, it is recommended
        to use the Feedback.busy() context manager instead. See its
        docstring for details.

        Parameters
        ----------
        is_busy : bool, optional
            Whether to flag the feedback object as busy, by default
            True
        """
        self._is_busy = is_busy

    def set_prefix(self, prefix: str) -> None:
        """Set the status message prefix.

        Use Feedback.clear_prefix() to remove the prefix entirely.

        Parameters
        ----------
        prefix : str
            A new prefix to prepend to every status message sent
        """
        self._prefix = prefix

    def set_scaling(self, span: float, offset: float = 0.0) -> None:
        """Set the scaling factor.

        The scaling factor automatically applies the scale() method
        to any status updates.

        Parameters
        ----------
        span : float
            The scaling factor for any progress value passed
        offset : float, optional
            An offset to account for past operations, by default 0.0

        Raises
        ------
        ValueError
            Raised if span is less than 0 or greater than 1
        ValueError
            Raised if offset is less than 0 or greater than 1-span
        """
        if not 0.0 <= span <= 1.0:
            raise ValueError('span must lie within 0.0 and than 1.0')
        if not 0.0 <= offset <= 1.0-span:
            raise ValueError('offset must lie within 0.0 and (1.0 - span)')
        self._scaling_span = span
        self._scaling_offset = offset

    def update(self, value: Optional[float] = None,
               msg: Optional[str] = None) -> None:
        """Push the given status and progress.

        This is the primary endpoint for functions reporting status
        updates to their callers.

        None values mean that the value should not be updated

        Parameters
        ----------
        value : float, optional
            A value from 0 to 1 that reflects the aproximate completion
            status of the operation, by default None
        msg : str, optional
            A status message to push, by default None

        Raises
        ------
        InterruptedError
            Raised if the cancel flag was set
        ValueError
            Raised if value is less than 0 or greater than 1
        """
        if self._is_cancelled:
            self._callback(0.0, 'Operation cancelled', False)
            raise InterruptedError('The operation was cancelled by the user')
        if msg is not None:
            msg = self._prefix + msg
        if value is not None and not self._is_busy:
            if not 0.0 <= value <= 1.0:
                raise ValueError('value must lie within 0.0 and 1.0')
            value = self.scale(value, self._scaling_span, self._scaling_offset)
        self._callback(value, msg, self._is_busy)
