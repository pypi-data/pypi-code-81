# cohort_analysis/decorators
# provides custom decorators to modify the behaviour of functions or methods

import functools

from .exceptions import CohortAnalysisException

from typing import Callable


def check_attributes_are_set(self):

    """
    check_attributes_are_set

    RAISES:
        CohortAnalysisException

        if either of the attributes .clickstream or .cohorts
        are not set on the input (and tells you which ones aren't set)

    """

    clickstream_missing = self.clickstream is None
    cohorts_missing = self.cohorts is None

    if clickstream_missing:
        if cohorts_missing:
            raise CohortAnalysisException(
                """
                The clickstream and cohorts attributes (DataFrames) need to be set
                on this instance of the CohortMetrics object.
                """
            )
        raise CohortAnalysisException(
            """
            The clickstream attribute (DataFrame) needs to be set on this instance
            of the CohortMetrics object
            """
        )

    if cohorts_missing:  # only reach this if .clickstream was set
        raise CohortAnalysisException(
            """
            The cohorts attribute (DataFrame) needs to be set on this instance
            of the CohortMetrics object
            """
        )


def check_attributes(method: Callable) -> Callable:

    """
    check_attributes

    Decorator. Returns a modified version of the input method that
    invokes check_attributes_are_set before invoking the input method

    """

    @functools.wraps(method)  # don't overwrite the method's docstring
    def decorated_method(self, *args, **kwargs):
        check_attributes_are_set(self)
        output = method(self, *args, **kwargs)
        return output

    return decorated_method  # return the souped-up method we just defined
