"""This module implements the Aug class."""
import time
import uuid

from rook.logger import logger
from rook.processor.error import Error
from rook.processor.namespaces.container_namespace import ContainerNamespace
from rook.processor.namespaces.stack_namespace import StackNamespace
from rook.processor.namespaces.python_utils_namespace import PythonUtilsNamespace
from rook.processor.namespaces.trace_namespace import TraceNamespace
from rook.processor.namespaces.process_state_namespace import ProcessStateNamespace
from rook.user_warnings import UserWarnings

from rook.exceptions import RookRuleMaxExecutionTimeReached, RookRuleRateLimited
from rook.augs.aug_rate_limiter import AugRateLimiter


class Aug(object):
    """The Aug class is the skeleton that holds together all the components that define a modification to the application.

    This class brings together the following elements:
    - location - specifies when to run the modification.
    - extractor - specifies attributes to extract from the application's state before evaluating the modification.
    - condition - specifies an optional filter as to when to run the modification.
    - action - specifies the modification to preform.
    """

    def __init__(self, aug_id, extractor, condition, action, max_aug_execution_time=0, rate_limits=None):
        """Build an Aug object from the individual elements."""
        self.aug_id = aug_id
        self._extractor = extractor
        self._condition = condition
        self._action = action
        self._max_aug_time = max_aug_execution_time
        self._enabled = True

        if rate_limits:
            self._rate_limiter = AugRateLimiter(rate_limits[0], rate_limits[1])
        else:
            self._rate_limiter = AugRateLimiter(None, None)

    def execute(self, frame_namespace, extracted, output):
        """Called by the trigger service to run the extractor, condition and action."""
        if not self._enabled:
            return

        now = time.time()
        limit_key = None
        executed = False

        try:
            if self._extractor:
                self._extractor.execute(frame_namespace, extracted)

            store = ContainerNamespace({})

            namespace = ContainerNamespace({
                'frame': frame_namespace,
                'stack': StackNamespace(frame_namespace),
                'extracted': ContainerNamespace(extracted),
                'store': store,
                'temp': ContainerNamespace({}),
                'python': PythonUtilsNamespace(),
                'utils': PythonUtilsNamespace(),
                'trace': TraceNamespace(),
                'state': ProcessStateNamespace(),
            })

            # TODO - cleanup rate limit
            if not self._condition or self._condition.evaluate(namespace, extracted):
                limit_key = self._rate_limiter.allow(now)

                if limit_key is None:
                    UserWarnings.send_warning(Error(exc=RookRuleRateLimited()))
                    return

                executed = True
                msg_id = uuid.uuid4().hex

                logger.info("Executing aug-\t%s (msg ID %s)", self.aug_id, msg_id)
                self._action.execute(self.aug_id, msg_id, namespace, output)
        finally:
            if executed:
                duration = time.time() - now

                if 0 < self._max_aug_time < duration * 1000:
                    UserWarnings.set_error(Error(exc=RookRuleMaxExecutionTimeReached()))
                    self._enabled = False

                if limit_key:
                    self._rate_limiter.record(limit_key, duration)
