# defines the df.cohorts DataFrame accessor and associated methods

from pandas_flavor import register_dataframe_accessor

from .cohort_metrics import CohortAnalysisException, CohortMetrics


@register_dataframe_accessor("cohorts")
class CohortAnalysisAccessor:

    """
    Register DataFrame.cohorts accessor

    Provides methods that faciliate the setting of particular
    DataFrames as the clickstream or cohorts attributes of a
    cohort_analysis.CohortMetrics instance

    """

    def __init__(self, df):
        self._df = df

    def __repr__(self):
        return "DataFrame.cohorts (accessor for cohort_analysis methods)"

    def __str__(self):
        return self.__repr__()

    def set_as_clickstream(
        self,
        metrics: CohortMetrics,
        timestamp_col: str = "timestamp",
        user_id_col: str = "user_id",
    ):

        """
        Register DataFrame.cohorts.set_as_clickstream

        Sets the clickstream attribute of a supplied CohortMetrics
        instance to be a copy of the DataFrame on which this
        method is called

        INPUTS:
            metrics - a cohort_analysis.metrics.CohortMetrics instance

        KEYWORDS:
            timestamp_col = "timestamp"
            user_id_col = "user_id"

            If the DataFrame has different names for these columns,
            that can be indicated using these keywords

        """

        clickstream = self._df.copy()

        metrics.set_clickstream(
            clickstream, user_id_col=user_id_col, timestamp_col=timestamp_col
        )

    def set_as_cohorts(
        self,
        metrics: CohortMetrics,
        user_id_col: str = "user_id",
        reference_timestamp_col: str = "reference_timestamp",
    ):

        """
        Register DataFrame.cohorts.set_as_cohorts

        Sets the cohorts attribute of a supplied CohortMetrics
        instance to be a copy of the DataFrame on which this
        method is called

        INPUTS:
            metrics - a cohort_analysis.metrics.CohortMetrics instance

        KEYWORDS:
            user_id_col = "user_id"
            reference_timestamp_col = "reference_timestamp"

            If the DataFrame has different names for these columns,
            that can be indicated using these keywords

        """

        cohorts = self._df.copy()

        metrics.set_cohorts(
            cohorts,
            user_id_col=user_id_col,
            reference_timestamp_col=reference_timestamp_col,
        )
