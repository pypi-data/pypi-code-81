# __init__.py
from .accessors import CohortAnalysisAccessor, CohortMetrics

# as a convenience, we provide cohort_analysis.metrics (an instance of
# cohort_analysis.metrics.CohortMetrics) on import; however the
# crucial .clickstream and .cohorts methods are initially not set.

metrics = CohortMetrics()

# We also provide new pandas.DataFrame methods via pandas_flavor.
# As a convenience, use
#   df1.cohorts.set_clickstream(cohort_analysis.metrics)
# and
#   df2.cohorts.set_cohorts(cohort_analysis.metrics)
# to set the attributes on cohort_analysis.metrics

__version__ = "0.1.2"
