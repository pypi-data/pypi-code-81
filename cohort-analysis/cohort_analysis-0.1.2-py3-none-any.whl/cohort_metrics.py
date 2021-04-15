# cohort_analysis/cohort_metrics
# provides classes for organising the data

import numpy as np
import pandas as pd

from pandas import DataFrame, Period, Series, Timestamp
from datetime import date

from .decorators import check_attributes
from .exceptions import CohortAnalysisException

from typing import Dict, List, Optional, Tuple, Union


CohortSpecifierType = Optional[Union[str, List[Optional[str]]]]
CohortFilterType = Optional[Dict[str, CohortSpecifierType]]


class CohortMetrics:
    """
    CohortMetrics

    A class for computing activity and retention metrics for different
    cohorts of users

    """

    def __init__(
        self,
        clickstream: Optional[DataFrame] = None,
        cohorts: Optional[DataFrame] = None,
        timezone: str = "UTC",
    ):

        """
        __init__ for CohortMetrics

        Sets the .clickstream and .cohorts metrics (either as DataFrames or None)

        Sets the .filter_logic, .timezone, and .current_timestamp properties

        """

        self.filter_logic = "AND"
        self.timezone = timezone
        self.current_timestamp = Timestamp.now(tz=timezone)

        self.clickstream = None
        self.cohorts = None

        if clickstream is not None:
            if not isinstance(clickstream, DataFrame):
                raise CohortAnalysisException("clickstream must be a DataFrame if set")
            self.set_clickstream(clickstream)

        if cohorts is not None:
            if not isinstance(cohorts, DataFrame):
                raise CohortAnalysisException("cohorts must be a DataFrame if set")
            self.set_cohorts(cohorts)

    def __repr__(self):

        """
        __repr__

        The representation of a CohortMetrics instance should:

        - indicate whether clickstream and cohorts attributes are set
        - if so, provide summary information via the string
          representations of those DataFrames

        """

        classname = self.__class__.__name__  # in case we change the class name!

        no_clickstream = self.clickstream is None
        no_cohorts = self.cohorts is None

        # TO-DO: indicate the timezone and current_timestamp

        if no_clickstream and no_cohorts:
            return f"{classname}(<no clickstream set>, <no cohorts set>)"
        if no_clickstream:
            return f"{classname}(<no clickstream set>, <cohorts DataFrame>)"
        if no_cohorts:
            return f"{classname}(<clickstream DataFrame>, <no cohorts set>)"

        df_representations = zip(
            str(self.clickstream).splitlines(), str(self.cohorts).splitlines()
        )

        separator = "   |   "

        all_lines = [l1 + separator + l2 for l1, l2 in df_representations]

        # TO-DO: handle the (unexpected) case where the DataFrames are so short their
        # string representations don't include a summary line at the end

        # replace the penultimate line with one of appropriate width

        line_widths = [len(l) for l in all_lines[0].split(separator)]

        dummy_str = " "

        penultimate_line = separator.join([f"{dummy_str:<{lw}}" for lw in line_widths])

        all_lines[-2] = penultimate_line

        # replace the final line with an appropriate-width summary

        summ_parts = zip(["CLICKSTREAM: ", "COHORTS: "], all_lines[-1].split(separator))

        summary = [descriptor + shape for descriptor, shape in summ_parts]

        final_line = separator.join(
            [f"{summ:<{lw}}" for summ, lw in zip(summary, line_widths)]
        )

        all_lines[-1] = final_line

        representation = f":: {classname} instance :: \n\n" + "\n".join(all_lines)

        return representation

    def __str__(self):

        """
        __str__

        Wraps the __repr__ method for CohortMetrics

        """

        return self.__repr__()

    def verify_clickstream(self):

        """
        verify_clickstream

        If .clickstream is set, checks that it has the required columns

            user_id, timestamp in self.clickstream.columns

        RAISES:
            CohortAnalysisException - if columns are missing/misnamed

        """

        if self.clickstream is None:
            return  # early return if clickstream not set

        if "user_id" not in self.clickstream.columns:
            raise CohortAnalysisException("clickstream must have user_id column")

        if "timestamp" not in self.clickstream.columns:
            raise CohortAnalysisException("clickstream must have timestamp column")

    def verify_cohorts(self):

        """
        verify_cohorts

        If .cohorts is set, checks that it has the required columns

            user_id, reference_timestamp in self.cohorts.columns

        RAISES:
            CohortAnalysisException - if columns are missing/misnamed

        """

        if self.cohorts is None:
            return  # early return if cohorts not set

        if "user_id" not in self.cohorts.columns:
            raise CohortAnalysisException("cohorts must have user_id column")

        if "reference_timestamp" not in self.cohorts.columns:
            raise CohortAnalysisException(
                "cohorts must have reference_timestamp column"
            )

    def change_current_timestamp(
        self, current_timestamp: Union[str, Timestamp] = "now"
    ):

        """
        change_current_timestamp

        By default, CohortMetrics uses the timestamp at initialisation
        (in the chosen timezone) as its .current_timestamp property.

        This method allows us to change that (e.g. in case working with
        old/checkpointed data, test data with future values etc)

        KEYWORDS:
            current_timestamp = "now" - set the new .current_timestamp
                                        property

            options:
                "now" - set to current timestamp in the set timezone
                "last" - set to last timestamp/reference timestamp
                         contained within the clickstream/cohorts data
                <any pandas Timestamp> - will be localized in or
                                         converted to the set timezone
                <any parseable datetime string> - will be converted to a
                                                  localized Timestamp

        """

        if current_timestamp == "now":

            self.current_timestamp = Timestamp.now(tz=self.timezone)

        elif current_timestamp == "last":

            clickstream, cohorts = self.filter_by_cohorts()

            self.current_timestamp = max(
                [clickstream.timestamp.max(), cohorts.reference_timestamp.max()]
            )

        elif isinstance(current_timestamp, Timestamp):

            if current_timestamp.tz is None:
                self.current_timestamp = current_timestamp.tz_localize(self.timezone)
            else:
                self.current_timestamp = current_timestamp.tz_convert(self.timezone)

        else:
            self.current_timestamp = Timestamp(current_timestamp, tz=self.timezone)

    def change_timezone(self, timezone="UTC"):

        """
        change_timezone

        This method changes the .timezone property and converts

            .current_timestamp property
            .cohorts.reference_timestamp column (if set)
            .clickstream.timestamp column (if set)

        to the new timezone

        KEYWORDS:
            timezone = "UTC" - timezone to change instance to

        """

        self.timezone = timezone

        self.current_timestamp = self.current_timestamp.tz_convert(timezone)

        if self.cohorts is not None:

            self.cohorts.loc[
                :, "reference_timestamp"
            ] = self.cohorts.reference_timestamp.dt.tz_convert(timezone)

        if self.clickstream is not None:

            self.clickstream.loc[
                :, "timestamp"
            ] = self.clickstream.timestamp.dt.tz_convert(timezone)

    def change_filter_logic(self, logic: str):

        """
        change_filter_logic

        Change the filter logic to be used when selecting cohorts

            AND: filtering should identify the intersection of cohorts
            OR:  filtering should identify the union of cohorts
            NOT: filtering should identify the complement of the
                 union of cohorts (everyone not in the union)

        INPUTS:
            logic - any of {"AND", "OR", "NOT"}

        RAISES:
            CohortAnalysisException if an invalid input is given

        """

        supported_logic = ["AND", "OR", "NOT"]

        if logic not in supported_logic:
            raise CohortAnalysisException(f"logic must be one of {supported_logic}")

        self.filter_logic = logic

    def set_clickstream(
        self,
        clickstream: DataFrame,
        timestamp_col: str = "timestamp",
        user_id_col: str = "user_id",
    ):

        """
        set_clickstream

        Sets the clickstream attribute to be a copy of a supplied
        DataFrame with normalised column names

        INPUTS:
            clickstream - DataFrame with columns for user IDs and timestamps

        KEYWORDS:
            timestamp_col = "timestamp"
            user_id_col = "user_id"

            If the DataFrame has different names for these columns,
            that can be indicated using these keywords

        """

        clickstream_copy = clickstream.copy()

        if timestamp_col != "timestamp":
            clickstream_copy.loc[:, "timestamp"] = clickstream.loc[:, timestamp_col]
        elif "timestamp" not in clickstream.columns:
            raise CohortAnalysisException(
                "'timestamp' should be a column of the clickstream DataFrame if timestamp_col not specified"
            )

        if user_id_col != "user_id":
            clickstream_copy.loc[:, "user_id"] = clickstream.loc[:, user_id_col]
        elif "user_id" not in clickstream.columns:
            raise CohortAnalysisException(
                "'user_id' should be a column of the clickstream DataFrame if user_id_col not specified"
            )

        clickstream_copy.loc[:, "timestamp"] = pd.to_datetime(
            clickstream_copy.timestamp, utc=True, errors="coerce"  # force to UTC
        ).dt.tz_convert(
            self.timezone  # convert to the instance timezone
        )

        self.clickstream = clickstream_copy

        self.verify_clickstream()

        self.clickstream = clickstream_copy[["timestamp", "user_id"]]

    def set_cohorts(
        self,
        cohorts: DataFrame,
        user_id_col: str = "user_id",
        reference_timestamp_col: str = "reference_timestamp",
    ):

        """
        set_cohorts

        Sets the cohorts attribute to be a copy of a supplied
        DataFrame with normalised column names

        INPUTS:
            cohorts - a DataFrame with at least a column for user IDs

        KEYWORDS:
            user_id_col = "user_id"
            reference_timestamp_col = "reference_timestamp"

            If the DataFrame has different names for these columns,
            that can be indicated using these keywords

        """

        cohorts_copy = cohorts.copy()

        if user_id_col != "user_id":
            cohorts_copy.loc[:, "user_id"] = cohorts.loc[:, user_id_col]
            cohorts_copy = cohorts_copy.drop(user_id_col, axis="columns")
        elif "user_id" not in cohorts.columns:
            raise CohortAnalysisException(
                "'user_id' should be a column of the cohorts DataFrame if user_id_col not specified"
            )

        if reference_timestamp_col != "reference_timestamp":
            cohorts_copy.loc[:, "reference_timestamp"] = cohorts.loc[
                :, reference_timestamp_col
            ]
            cohorts_copy = cohorts_copy.drop(reference_timestamp_col, axis="columns")
        elif "reference_timestamp" not in cohorts.columns:
            raise CohortAnalysisException(
                "'reference_timestamp' should be a column of the cohorts DataFrame if reference_timestamp_col not specified"
            )

        cohorts_copy.loc[:, "reference_timestamp"] = pd.to_datetime(
            cohorts_copy.reference_timestamp, utc=True, errors="coerce"  # force to UTC
        ).dt.tz_convert(
            self.timezone  # convert to the instance timezone
        )

        self.cohorts = cohorts_copy

        self.verify_cohorts()

    @check_attributes
    def __get_attribute_copies(self) -> Tuple[DataFrame, DataFrame]:

        """
        __get_attribute_copies

        Returns a copy of .clickstream and .cohorts

        OUTPUTS:
            clickstream - DataFrame, a copy of the .clickstream attribute
            cohorts - DataFrame, a copy of the .cohorts attribute

        RAISES:
            CohortAnalysisException - if either attribute not yet set

        """

        # mostly this facilitates type-checking downstream (the @check_attributes
        # decorator isn't acknowledged by mypy, so we ignore that the attributes
        # can at times be None - @check_attributes is guaranteeing they won't be)

        clickstream = self.clickstream.copy()  # type: ignore
        cohorts = self.cohorts.copy()  # type: ignore

        return clickstream, cohorts

    @staticmethod
    def __parse_period(timeframe: str) -> Period:

        """
        __parse_period

        Takes a string indicating a calendar period and parses it,
        creating a pandas Period object. Mostly relies on built-in Period
        functionality with special handling for parsing weeks

        INPUTS:
            timeframe - string indicating period, e.g. as follows:

                    year    - '2019',
                    quarter - '2020Q3',
                    month   - '2020-07',
                    week    - '2020-W-SUN-1'
                    day     - '2020-08-01'

        RAISES:
            CohortAnalysisException - if there was an unresolvable
                                      period parsing error

        OUTPUTS:
            period - corresponding Period object

        """

        if "W" not in timeframe:
            try:
                period = Period(timeframe)
                return period
            except:
                raise CohortAnalysisException(
                    f"Could not parse calendar cohort {timeframe}"
                )

        # only reach here if timeframe indicates weekly cohort

        year, *freq, week_number = timeframe.split("-")

        try:
            period = Period(year, freq="-".join(freq)) + int(week_number) - 1
            return period
        except:
            raise CohortAnalysisException(
                f"Could not parse calendar cohort {timeframe}"
            )

    def __update_mask(
        self, filtered_cohorts: DataFrame, key: str, values: CohortSpecifierType
    ) -> DataFrame:

        """
        __update_mask

        When filtering a cohorts DataFrame according to the contents of
        a cohort filter dictionary, it is necessary to iteratively update
        the mask applied to calculate all users who belong to the chosen
        cohort. This method accomplishes that task.

        The method allows the selection of a calendar-type cohort or else
        a categorical-type cohort (i.e. based either on the column
        reference_timestamp or on any of the other columns), which may be
        combined with other cohort definitions through repeated calls.

        INPUTS:
            filtered_cohorts - DataFrame containing the cohorts data with
                               an appended _MASK column that stores the
                               filter under construction
            key - either the name of a column in the cohorts table or
                  'calendar' to indicate that a calendar-based cohort
                  should be constructed
            value - the corresponding value: None, str, list of str/None

        RAISES:
            CohortAnalysisException - if called with a DataFrame without
                                      a _MASK column, or with a key
                                      that cannot be parsed

        OUTPUTS:
            filtered_cohorts - input DataFrame with _MASK column updated

        """

        columns = filtered_cohorts.columns

        if "_MASK" not in columns:
            raise CohortAnalysisException("Passed dataframe should have _MASK column")

        if isinstance(values, str) or isinstance(values, bool) or (values is None):
            vals = [values]  # wrap single strings into a one-element list
        else:
            vals = values

        current_mask = filtered_cohorts._MASK.copy()

        ### CALENDAR COHORTS

        if (key == "calendar") or (key == "reference_timestamp"):

            timeframes = [
                self.__parse_period(timeframe)
                for timeframe in vals
                if timeframe is not None  # assume reference_timestamp is never missing
            ]

            update_to_mask = current_mask.copy()  # match size
            update_to_mask = False  # set all False initially for internal 'OR' logic

            # because the type of period could vary (e.g. '2018' OR 'Q1 2019'), we
            # have to loop through them and create a PeriodIndex in each case.
            for tf in timeframes:

                mask = filtered_cohorts.reference_timestamp.dt.to_period(tf.freq).eq(tf)
                # as with 'isin(vals)', always use OR logic here
                update_to_mask = update_to_mask | mask

            if self.filter_logic == "AND":
                new_mask = current_mask & update_to_mask
            else:
                new_mask = current_mask | update_to_mask

            filtered_cohorts.loc[:, "_MASK"] = new_mask

            return filtered_cohorts

        ### CATEGORICAL COHORTS

        elif key in columns:  # if key is a column name (other than reference_date)

            mask = filtered_cohorts[key].isin(vals)

            if self.filter_logic == "AND":
                new_mask = current_mask & mask
            else:
                new_mask = current_mask | mask

            filtered_cohorts.loc[:, "_MASK"] = new_mask

            return filtered_cohorts

        # only reach here if key not a column, or 'calendar'
        raise CohortAnalysisException(
            """
            Did not understand cohorts filter dictionary.
            Keys should either be 'calendar' or correspond to columns in
            the cohorts DataFrame.
            """
        )

    def filter_by_cohorts(
        self, cohort: CohortFilterType = None
    ) -> Tuple[DataFrame, DataFrame]:

        """
        filter_by_cohorts

        Returns copies of the clickstream and the cohorts DataFrames
        filtered by any provided cohorts. Filter logic is determined
        by the .filter_logic property, which can be changed using the
        .set_filter_logic method (the default is "AND").

        KEYWORDS:
            cohort = None

                If None (default), a copy of the clickstream and cohorts
                DataFrames are returned, with the clickstream filtered
                only by which user IDs are also present in cohorts.

                If a dictionary of strings, the keys select columns, the
                values select acceptable value of the indicated columns.

                If a dictionary with list-type values, multiple values
                are indicated as acceptable for the corresponding column.

        OUTPUTS:
            filtered_clickstream - DataFrame; clickstream for users in
                                   the identified cohort
            filtered_cohorts - DataFrame; cohorts (user info table) for
                               users in the identified cohort

        """

        filtered_clickstream, filtered_cohorts = self.__get_attribute_copies()

        # first, remove any users with reference_timestamp later
        # than current_timestamp property

        filtered_cohorts = filtered_cohorts.loc[
            filtered_cohorts.reference_timestamp.le(self.current_timestamp)
        ].drop_duplicates()

        # now remove any clicks from the stream with user IDs not in cohorts.user_id
        filtered_clickstream = filtered_clickstream.merge(filtered_cohorts.user_id)

        # next remove any clicks from the stream with timestamps earlier
        # than the associated user's reference timestamp and later than
        # the CohortMetrics instance .current_timestamp property

        comparison = filtered_clickstream.join(
            filtered_cohorts.set_index("user_id").reference_timestamp, on="user_id"
        )

        not_too_early = comparison.timestamp.ge(comparison.reference_timestamp)

        not_too_late = filtered_clickstream.timestamp.le(self.current_timestamp)

        filtered_clickstream = filtered_clickstream.loc[not_too_early & not_too_late]

        # if no further filtering is required, return early:
        if cohort is None:
            return filtered_clickstream, filtered_cohorts

        # otherwise, parse the cohorts dictionary and filter accordingly:

        cohort_columns = (
            filtered_cohorts.columns
        )  # this is for restoring the original columns later

        if self.filter_logic == "AND":
            filtered_cohorts.loc[:, "_MASK"] = True
        else:
            filtered_cohorts.loc[:, "_MASK"] = False

        for key, values in cohort.items():

            filtered_cohorts = self.__update_mask(filtered_cohorts, key, values)

        if self.filter_logic == "NOT":  # in this case we'll have used OR logic so far
            filtered_cohorts.loc[:, "_MASK"] = filtered_cohorts._MASK.ne(True)

        filtered_cohorts = filtered_cohorts.loc[filtered_cohorts._MASK, cohort_columns]

        filtered_clickstream = filtered_clickstream.loc[
            filtered_clickstream.user_id.isin(filtered_cohorts.user_id)
        ]

        return filtered_clickstream, filtered_cohorts

    @staticmethod
    def __offset_cohort_size_timeperiod(
        data_by_period: DataFrame, target_col: str = "cohort_size"
    ) -> DataFrame:

        """
        __offset_cohort_size_timeperiod

        When a cumulative sum has been taken over a numerical Series
        with a period index, the interpretation is that the summed values
        correspond to the *end* of each period. This method allows us to
        offset the index from the values so that they instead correspond
        to the start of the period.

        The method takes an input DataFrame with a Period index and a
        cohort_size column of numerical values and shifts the values
        of that column forwards one period with respect to the index.

        A zero is prepended and the final value is lost.

        INPUTS:
            data_by_period - DataFrame with PeriodIndex

        KEYWORDS:
            target_col = "cohort_size" - column to offset can be changed

        OUTPUTS:
            offset_data - DataFrame with the same PeriodIndex, values of
                          target_col shifted to the successive period

        EXAMPLE:

                BEFORE                      AFTER

                     cohort_size                 cohort_size
            2020-01  1500               2020-01  0
            2020-02  3000               2020-02  1500
            2020-03  4500               2020-03  3000

        """

        offset_data = data_by_period.copy()

        values_at_start = offset_data[target_col].shift(1).fillna(0).astype(int)

        offset_data.loc[:, target_col] = values_at_start

        return offset_data

    @check_attributes
    def active_users_calendar_interval(
        self, cohort: CohortFilterType = None, freq: str = "W-SUN",
    ) -> DataFrame:

        """
        active_users_calendar_interval

        This method takes activity data (optionally filtered by cohort)
        and calculates the number of users active in every fixed-interval
        calendar period, as well as the cohort size by the end of each
        period. All periods between

        KEYWORDS:
            cohort = None - allows filtering by cohort. Optional input is
                            a dictionary: keys identify columns, values
                            may be a string or list of strings indicating
                            accepted values.
                            SEE ALSO: CohortMetrics.filter_cohorts
            freq = "W-SUN" - pandas-convention calendar frequency index
                             (default: calendar weeks concluding Sunday)

        OUTPUTS:
            active_users - DataFrame with columns 'cohort_size' and
                           'n_active', indexed by Period

        """

        clickstream, cohorts = self.filter_by_cohorts(cohort)

        min_ts = min([clickstream.timestamp.min(), cohorts.reference_timestamp.min()])
        max_ts = max([clickstream.timestamp.max(), cohorts.reference_timestamp.max()])

        # generate an index of all periods of type `freq` between the timestamps
        period_index = pd.date_range(start=min_ts, end=max_ts).to_period(freq).unique()

        # compute number of active users in each period from `clickstream`
        clickstream["period"] = clickstream.timestamp.dt.to_period(freq)

        n_active = clickstream.groupby("period").user_id.nunique()

        # compute number of users added to cohort in each period from `cohorts`
        cohorts["period"] = cohorts.reference_timestamp.dt.to_period(freq)

        cohort_size = cohorts.groupby("period").user_id.nunique().cumsum()

        # join active users and cohort size to the pre-computed index

        dummy_index_name = "periods"

        active_users = (
            period_index.rename(dummy_index_name)
            .to_frame()  # needed to support `.join`, creates dummy index column
            .join(cohort_size.rename("cohort_size"))
            .ffill()  # forward fill any periods no users were added to cohort
            .join(n_active.rename("n_active"))
            .fillna(0)  # fill any periods with no activity with 0 active users
            .drop(dummy_index_name, axis=1)  # drop dummy index column
            .astype(int)  # convert to integer
        )

        return active_users

    def dau_calendar_day(
        self, cohort: CohortFilterType = None, cohort_size_at: str = "end"
    ) -> DataFrame:

        """
        dau_calendar_day

        Computes daily active users by calendar day

        KEYWORDS:
            cohort = None - allows filtering by cohort. Optional input is
                            a dictionary: keys identify columns, values
                            may be a string or list of strings indicating
                            accepted values.
                            SEE ALSO: CohortMetrics.filter_cohorts
            cohort_size_at = "end" (either of "start", "end")

        OUTPUTS:
            dau - DataFrame indexed by calendar period with columns

                    cohort_size (either at end or beginning of period)
                    n_active
                    dau - daily active users as a percentage

        """

        if cohort_size_at not in ["start", "end"]:
            raise ValueError(
                f"cohort_size_at={cohort_size_at} invalid; should be 'start' or 'end'"
            )

        dau = self.active_users_calendar_interval(cohort=cohort, freq="D")

        if cohort_size_at == "start":  # offset cohort_size by one day
            dau = self.__offset_cohort_size_timeperiod(dau)

        dau["dau"] = dau.n_active.div(dau.cohort_size).mul(100.0)

        return dau

    def wau_calendar_week(
        self,
        cohort: CohortFilterType = None,
        week_commencing: str = "Monday",
        cohort_size_at: str = "end",
    ) -> DataFrame:

        """
        wau_calendar_week

        Computes weekly active users by calendar week. The user may
        choose the definition of a week (i.e. on what day a week starts)
        and when the cohort size ought to be calculated (start, middle,
        or end of the week).

        KEYWORDS:
            cohort = None - allows filtering by cohort. Optional input is
                            a dictionary: keys identify columns, values
                            may be a string or list of strings indicating
                            accepted values.
                            SEE ALSO: CohortMetrics.filter_cohorts
            week_commencing = "Monday" - definition of a week
            cohort_size_at = "end" (either of "start", "end")

        RAISES:
            ValueError - if week_commencing or cohort_size_at are given
                         non-permitted values

        OUTPUTS:
            wau - DataFrame indexed by calendar period with columns

                    cohort_size (either at end or beginning of period)
                    n_active
                    wau - weekly active users as a percentage

        """

        freq_lookup = {
            "Monday": "W-SUN",
            "Tuesday": "W-MON",
            "Wednesday": "W-TUE",
            "Thursday": "W-WED",
            "Friday": "W-THU",
            "Saturday": "W-FRI",
            "Sunday": "W-SAT",
        }

        freq = freq_lookup.get(week_commencing.title())  # case-insensitive

        if freq is None:
            raise ValueError(
                f"week_commencing={week_commencing} invalid; should be the full name of a week-day"
            )

        if cohort_size_at not in ["start", "end"]:
            raise ValueError(
                f"cohort_size_at={cohort_size_at} invalid; should be 'start' or 'end'"
            )

        wau = self.active_users_calendar_interval(cohort=cohort, freq=freq)

        if cohort_size_at == "start":  # offset cohort_size by one week
            wau = self.__offset_cohort_size_timeperiod(wau)

        wau["wau"] = wau.n_active.div(wau.cohort_size).mul(100.0)

        return wau

    def mau_calendar_month(
        self, cohort: CohortFilterType = None, cohort_size_at: str = "end",
    ) -> DataFrame:

        """
        mau_calendar_month

        Computes weekly active users by calendar week. The user may
        choose when the cohort size ought to be calculated (start
        or end of the month).

        KEYWORDS:
            cohort = None - allows filtering by cohort. Optional input is
                            a dictionary: keys identify columns, values
                            may be a string or list of strings indicating
                            accepted values.
                            SEE ALSO: CohortMetrics.filter_cohorts
            cohort_size_at = "end" (either of "start", "end")

        RAISES:
            ValueError - if cohort_size_at is given
                         non-permitted value

        OUTPUTS:
            mau - DataFrame indexed by calendar period with columns

                    cohort_size (either at end or beginning of period)
                    n_active
                    mau - monthly active users as a percentage

        """

        if cohort_size_at not in ["start", "end"]:
            raise ValueError(
                f"cohort_size_at={cohort_size_at} invalid; should be 'start' or 'end'"
            )

        mau = self.active_users_calendar_interval(cohort=cohort, freq="M")

        if cohort_size_at == "start":  # offset cohort_size by one week
            mau = self.__offset_cohort_size_timeperiod(mau)

        mau["mau"] = mau.n_active.div(mau.cohort_size).mul(100.0)

        return mau

    def qau_calendar_quarter(
        self,
        cohort: CohortFilterType = None,
        year_commencing: str = "January",
        cohort_size_at: str = "end",
    ) -> DataFrame:

        """
        qau_calendar_quarter

        Computes quarterly active users by calendar quarter. The user may
        choose the definition of a year (i.e. in which month the year starts)
        and when the cohort size ought to be calculated (start
        or end of each quarter).

        KEYWORDS:
            cohort = None - allows filtering by cohort. Optional input is
                            a dictionary: keys identify columns, values
                            may be a string or list of strings indicating
                            accepted values.
                            SEE ALSO: CohortMetrics.filter_cohorts
            year_commencing = "January" - definition of a year
            cohort_size_at = "end" (either of "start", "end")

        RAISES:
            ValueError - if year_commencing or cohort_size_at are given
                         non-permitted values

        OUTPUTS:
            qau - DataFrame indexed by calendar period with columns

                    cohort_size (either at end or beginning of period)
                    n_active
                    qau - quarterly active users as a percentage

        """

        freq_lookup = {
            "January": "Q-DEC",
            "February": "Q-JAN",
            "March": "Q-FEB",
            "April": "Q-MAR",
            "May": "Q-APR",
            "June": "Q-MAY",
            "July": "Q-JUN",
            "August": "Q-JUL",
            "September": "Q-AUG",
            "October": "Q-SEPT",
            "November": "Q-OCT",
            "December": "Q-NOV",
        }

        freq = freq_lookup.get(year_commencing.title())  # case-insensitive

        if freq is None:
            raise ValueError(
                f"year_commencing={year_commencing} invalid; should be the full name of a month"
            )

        if cohort_size_at not in ["start", "end"]:
            raise ValueError(
                f"cohort_size_at={cohort_size_at} invalid; should be 'start' or 'end'"
            )

        qau = self.active_users_calendar_interval(cohort=cohort, freq=freq)

        if cohort_size_at == "start":  # offset cohort_size by one quarter
            qau = self.__offset_cohort_size_timeperiod(qau)

        qau["qau"] = qau.n_active.div(qau.cohort_size).mul(100.0)

        return qau

    def yau_calendar_year(
        self,
        cohort: CohortFilterType = None,
        year_commencing: str = "January",
        cohort_size_at: str = "end",
    ) -> DataFrame:

        """
        yau_calendar_year

        Computes yearly active users. The user may
        choose the definition of a year (i.e. in which month the year starts)
        and when the cohort size ought to be calculated (start
        or end of each quarter).

        KEYWORDS:
            cohort = None - allows filtering by cohort. Optional input is
                            a dictionary: keys identify columns, values
                            may be a string or list of strings indicating
                            accepted values.
                            SEE ALSO: CohortMetrics.filter_cohorts
            year_commencing = "January" - definition of a year
            cohort_size_at = "end" (either of "start", "end")

        RAISES:
            ValueError - if year_commencing or cohort_size_at are given
                         non-permitted values

        OUTPUTS:
            yau - DataFrame indexed by calendar period with columns

                    cohort_size (either at end or beginning of period)
                    n_active
                    yau - quarterly active users as a percentage

        """

        freq_lookup = {
            "January": "A-DEC",
            "February": "A-JAN",
            "March": "A-FEB",
            "April": "A-MAR",
            "May": "A-APR",
            "June": "A-MAY",
            "July": "A-JUN",
            "August": "A-JUL",
            "September": "A-AUG",
            "October": "A-SEP",
            "November": "A-OCT",
            "December": "A-NOV",
        }

        freq = freq_lookup.get(year_commencing.title())  # case-insensitive

        if freq is None:
            raise ValueError(
                f"year_commencing={year_commencing} invalid; should be the full name of a month"
            )

        if cohort_size_at not in ["start", "end"]:
            raise ValueError(
                f"cohort_size_at={cohort_size_at} invalid; should be 'start' or 'end'"
            )

        yau = self.active_users_calendar_interval(cohort=cohort, freq=freq)

        if cohort_size_at == "start":  # offset cohort_size by one year
            yau = self.__offset_cohort_size_timeperiod(yau)

        yau["yau"] = yau.n_active.div(yau.cohort_size).mul(100.0)

        return yau

    @check_attributes
    def active_users_rolling_interval(
        self,
        cohort: CohortFilterType = None,
        cohort_size_at: str = "end",
        offset_days: int = 1,
    ) -> DataFrame:

        """
        active_users_rolling_interval

        This method takes activity data (optionally filtered by cohort)
        and calculates the number of users active over rolling interval
        calendar periods

        INPUTS:
         cohort = None - allows filtering by cohort. Optional input is
                                a dictionary: keys identify columns, values
                                may be a string or list of strings indicating
                                accepted values.
                                SEE ALSO: CohortMetrics.filter_cohorts
        cohort_size_at = "end" (either of "start", "end")
        offset_days = number of days in a rolling window. e.g. 7 for weekly

        RAISES:
                ValueError - if cohort_size_at is given a non-permitted value

        OUTPUTS:
            rolling_users - DataFrame of distinct active users
                            and total users over given windows of time.
                            Columns 'cohort_size' and 'n_active',
                            indexed by end dates
        """

        clickstream, cohorts = self.filter_by_cohorts(cohort)

        min_ts = min([clickstream.timestamp.min(), cohorts.reference_timestamp.min()])
        max_ts = max([clickstream.timestamp.max(), cohorts.reference_timestamp.max()])

        # iterate through clickstream
        dates = pd.date_range(start=min_ts, end=max_ts, normalize=True)

        rolling_dates = [(day - pd.DateOffset(days=offset_days), day) for day in dates]

        data: Dict[str, List] = {"end_date": [], "n_active": [], "cohort_size": []}

        for start, end in rolling_dates:

            after_end = end + pd.DateOffset(days=1)

            mask = clickstream.timestamp.ge(start) & clickstream.timestamp.lt(after_end)
            n_active = clickstream.loc[mask].user_id.nunique()

            if cohort_size_at == "end":
                cohort_size = cohorts.reference_timestamp.lt(after_end).sum()
            elif cohort_size_at == "start":
                cohort_size = cohorts.reference_timestamp.lt(start).sum()
            else:
                raise ValueError(
                    f"cohort_size_at={cohort_size_at} invalid; should be 'start' or 'end'"
                )

            data["end_date"].append(end)
            data["n_active"].append(n_active)
            data["cohort_size"].append(cohort_size)

        rolling_users = DataFrame(data).set_index("end_date")

        return rolling_users

    def rolling_wau(
        self, cohort: CohortFilterType = None, cohort_size_at: str = "end"
    ) -> DataFrame:
        """
        rolling_wau

        Takes activity data (optionally filtered by cohort)
        and calculates the percentage of users active
        over rolling calendar weeks

         KEYWORDS:
                cohort = None - allows filtering by cohort. Optional input is
                                a dictionary: keys identify columns, values
                                may be a string or list of strings indicating
                                accepted values.
                                SEE ALSO: CohortMetrics.filter_cohorts
                cohort_size_at = "end" (either of "start", "end")
        RAISES:
                ValueError - if cohort_size_at is given a non-permitted value

            OUTPUTS:
                rolling_weekly_users - percentage of users active over
                                       rolling weeks

        """

        if cohort_size_at not in ["start", "end"]:
            raise ValueError(
                f"cohort_size_at={cohort_size_at} invalid; should be 'start' or 'end'"
            )

        rolling_wau = self.active_users_rolling_interval(
            cohort=cohort, offset_days=7, cohort_size_at=cohort_size_at
        )

        rolling_wau["wau"] = rolling_wau.n_active.div(rolling_wau.cohort_size).mul(
            100.0
        )

        return rolling_wau

    def rolling_mau(
        self, cohort: CohortFilterType = None, cohort_size_at: str = "end"
    ) -> DataFrame:
        """
        rolling_mau

        Takes activity data (optionally filtered by cohort)
        and calculates the percentage of users active
        over rolling calendar months

         KEYWORDS:
                cohort = None - allows filtering by cohort. Optional input is
                                a dictionary: keys identify columns, values
                                may be a string or list of strings indicating
                                accepted values.
                                SEE ALSO: CohortMetrics.filter_cohorts
                cohort_size_at = "end" (either of "start", "end")
        RAISES:
                ValueError - if cohort_size_at is given a non-permitted value

            OUTPUTS:
                rolling_monthly_users - percentage of users active over
                                        rolling months

        """

        if cohort_size_at not in ["start", "end"]:
            raise ValueError(
                f"cohort_size_at={cohort_size_at} invalid; should be 'start' or 'end'"
            )

        rolling_mau = self.active_users_rolling_interval(
            cohort=cohort, offset_days=28, cohort_size_at=cohort_size_at
        )

        rolling_mau["mau"] = rolling_mau.n_active.div(rolling_mau.cohort_size).mul(
            100.0
        )

        return rolling_mau

    def rolling_qau(
        self, cohort: CohortFilterType = None, cohort_size_at: str = "end"
    ) -> DataFrame:
        """
        rolling_qau

        Takes activity data (optionally filtered by cohort)
        and calculates the percentage of users active
        over rolling calendar quarters

         KEYWORDS:
                cohort = None - allows filtering by cohort. Optional input is
                                a dictionary: keys identify columns, values
                                may be a string or list of strings indicating
                                accepted values.
                                SEE ALSO: CohortMetrics.filter_cohorts
                cohort_size_at = "end" (either of "start", "end")
        RAISES:
                ValueError - if cohort_size_at is given a non-permitted value

            OUTPUTS:
                rolling_quarterly_users - percentage of users active over
                                        rolling quarters

        """

        if cohort_size_at not in ["start", "end"]:
            raise ValueError(
                f"cohort_size_at={cohort_size_at} invalid; should be 'start' or 'end'"
            )

        rolling_qau = self.active_users_rolling_interval(
            cohort=cohort, offset_days=91, cohort_size_at=cohort_size_at
        )

        rolling_qau["qau"] = rolling_qau.n_active.div(rolling_qau.cohort_size).mul(
            100.0
        )

        return rolling_qau

    @staticmethod
    def user_activities_by_interval(
        stream_cohorts: DataFrame, interval_in_days: int = 7,
    ) -> DataFrame:

        """
        user_activities_by_interval

        Return a DataFrame indexed by each user_id and valued by a list.
        Each value in the list is the relative active date since the
        reference_timestamp in the given time interval.
        E.g. value of 1 and interval of 7 shows that a user is active
        between day 7 and day 14 since the reference_timestamp, i.e. is
        active in the second week.

        KEYWORDS:
            interval_in_days = 7 - the number of days for a time interval

        INPUTS:
            stream_cohorts - pandas DataFrame of merged clickstream and
                             cohorts on user_id

       OUTPUTS:
            user_activities - pandas DataFrame indexed by user_id and
                              columned by "active_at_interval_list".
                              Value for the column is a list of user's
                              activity in the given time-interval since
                              reference_timestamp

        """

        # get user activities at a given time interval
        clickstream_with_active_intervals = stream_cohorts[
            ["user_id", "timestamp", "reference_timestamp"]
        ].assign(
            active_at_interval=lambda d: d.timestamp.sub(
                d.reference_timestamp
            ).dt.days.floordiv(interval_in_days)
        )

        # group by user_id
        user_activities = (
            clickstream_with_active_intervals.groupby("user_id")
            .active_at_interval.apply(list)
            .to_frame(name="active_at_interval_list")
        )

        return user_activities

    def add_interval_upper_bound(
        self, cohorts: DataFrame, interval_in_days: int = 7
    ) -> DataFrame:

        """
        add_interval_upper_bound

        Adds a column to cohorts data table as the upper bound value
        for calculating user activities with the given time interval. The
        upper bound is calculated as the difference between current timestamp
        and the reference_timestamp.
        The upper bound helps identify inactive record as either "user is
        not active" or "impossible to get activity" at a given time
        interval.

        INPUTS:
            cohorts - filtered cohorts data table

        KEYWORDS:
            interval_in_days = 7 - the number of days for a time interval

        OUTPUTS:
            cohorts_with_upper_bound - cohorts Dataframe with upper bound
                                       for the given interval added

        """

        cohorts_with_upper_bound = cohorts.assign(
            interval_upper_bound=(
                self.current_timestamp - cohorts.reference_timestamp
            ).dt.days.floordiv(interval_in_days)
        )

        return cohorts_with_upper_bound

    @staticmethod
    def filter_by_upper_bound(row: Series) -> Series:

        """
        filter_by_upper_bound

        Function to filter a Series of activity data by the value of maximum
        threshold. Applies a value of 1 where there is activity in this interval
        and otherwise a value of 0 if the interval is below the upper bound
        or NaN if the interval is above the upper bound.

        INPUTS:
            row - pandas Series containing activity data by interval and
                maximum threshold for a user

        OUTPUTS:
            filtered_series - pandas Series indexed by each time interval
                              with value of 1 if there is activity in
                              this interval and otherwise 0 if no activity
                              in this interval or NaN if the interval is
                              greater than the upper bound for the user

        """

        interval_upper_bound = row.interval_upper_bound

        active_counts_at_intervals = row.filter(
            regex=r"^\d+$", axis=0
        )  # select only the interval columns
        intervals = active_counts_at_intervals.index
        counts = active_counts_at_intervals.fillna(0).values

        filtered = np.where(
            intervals > interval_upper_bound,
            np.nan,
            np.where(counts >= 1.0, True, False),
        )
        # when user active interval is outside of upper bound,
        ## fill with np.nan (i.e. not calculable)
        # when user active interval is within the bound
        ## fill with True, if user is active
        ## fill with False, if user is not active

        filtered_series = Series(filtered, index=intervals)

        return filtered_series

    @staticmethod
    def fixed_interval_bincount(row: Series) -> Series:

        """
        fixed_interval_bincount

        Helper function to convert list of time-interval activities to
        activity for each fixed interval.

        INPUTS:
            row - pandas Series containing activity data by time-interval
                  of a given user

        OUTPUTS:
            series - pandas Series of user activity from 0 to largest-
                     possible time-interval. Value=0 means user is
                     inactive at the interval, and Value>=1 means active.

        """

        series = Series(np.bincount(row.active_at_interval_list))

        return series

    def fixed_interval_retention(
        self, cohort: CohortFilterType = None, interval_in_days: int = 7,
    ) -> Series:

        """
        fixed_interval_retention

        Returns a pandas Series of fixed interval retention rates of a
        cohort. With fixed interval, the retention rate at a time-interval
        is calculated as "number of active users" divided by "number of
        users having reached this time-interval"

        KEYWORDS:
            cohort = None - allows filtering by cohort. Optional input is
                            a dictionary: keys identify columns, values
                            may be a string or list of strings indicating
                            accepted values.

            interval_in_days = 7 - the number of days for a time interval

        OUTPUTS:

            cohort_active_rates - pandas Series indexed by time interval
                                  indices and valued by the active rate
                                  at that time interval of a cohort

        """

        clickstream, cohorts = self.filter_by_cohorts(cohort)

        cohorts = self.add_interval_upper_bound(cohorts, interval_in_days)

        merged_stream = clickstream.merge(cohorts, on="user_id", how="inner")

        # 1. convert each user's activities to an array of integers
        ## each integer represents that user is active at that time-interval
        # 2. count user activities from 0 to N time-interval; 0 for no activity
        ## N for the largest interval of the cohort
        # 3. join with cohorts and keep users without any activity
        # 4. filter user's activity by interval_upper_bound
        ## activity status can be: active, non-active and impossible to calculate
        # 5. calculate active rates
        ## at each time-interval: num of active / num of could be active

        cohort_active_rates = (
            self.user_activities_by_interval(merged_stream, interval_in_days)
            .apply(self.fixed_interval_bincount, axis=1)
            .join(cohorts.set_index("user_id"), how="right")
            .apply(self.filter_by_upper_bound, axis=1)
            .pipe(lambda d: d.sum(axis=0).div(d.notna().sum(axis=0)))
        )

        return cohort_active_rates

    @staticmethod
    def unbounded_interval_bincount(row) -> Series:

        """
        unbounded_interval_bincount

        Helper function to convert list of time-interval activities to
        unbounded activity. This is achieved by finding the latest
        active interval for a user and convert all intervals before
        that as active.

        INPUTS:
            row - pandas Series containing activity data by time-interval
                  of a given user

        OUTPUTS:
            series - pandas Series of user activity from 0 to largest-
                     possible time-interval. Value=0 means user is
                     inactive at the interval, and Value>=1 means active.

        """

        series = Series(
            np.bincount(range(0, int(max(row.active_at_interval_list)) + 1))
        )

        return series

    def unbounded_interval_retention(
        self, cohort: CohortFilterType = None, interval_in_days: int = 7,
    ) -> Series:

        """
        unbounded_interval_retention

        Return a pandas Series of unbounded retention rates of a cohort.
        With unbounded retention, the active rate at each time-interval
        is calculated as the "number of active users" divided by "number
         of users available". An user is active at the time-interval
        if it is active in a later time-interval.

        KEYWORDS:
            cohort = None - allows filtering by cohort. Optional input is
                            a dictionary: keys identify columns, values
                            may be a string or list of strings indicating
                            accepted values.

            interval_in_days = 7 - the number of days for a time interval

        OUTPUTS:
            cohort_active_rates - pandas Series indexed by time-interval
                                  indices and valued by the active rate
                                  at that time interval of a cohort

        """

        clickstream, cohorts = self.filter_by_cohorts(cohort)

        cohorts = self.add_interval_upper_bound(cohorts, interval_in_days)

        merged_stream = clickstream.merge(cohorts, on="user_id", how="inner")

        # 1. convert each user's activities to array of integers
        ## each integer represents that user is active at that time-interval
        # 2. count user activities from 0 to N time-interval
        ## if user is active at K interval, all previous intervals are active
        # 3. join with cohorts and keep users without any activity
        # 4. filter user's activity by interval_upper_bound
        ## activity status can be: active, non-active and impossible to calculate
        # 5. calculate active rates
        ## at each time-interval: num of active / num of could be active

        cohort_active_rates = (
            self.user_activities_by_interval(merged_stream, interval_in_days)
            .apply(self.unbounded_interval_bincount, axis=1)
            .join(cohorts.set_index("user_id"), how="right")
            .apply(self.filter_by_upper_bound, axis=1)
            .pipe(lambda d: d.sum(axis=0).div(d.notna().sum(axis=0)))
        )

        return cohort_active_rates

    @staticmethod
    def wmqy_interval_bincount(row) -> Series:

        """
        wmqy_interval_bincount

        Helper function to convert list of time-interval activities to
        wmqy activity. This is achieved by checking if a user has at
        least one activity in each of the bins:
            bin 0: "active at day of reference_timestamp",
            bin 1: "active in the 1st week, besides the 1st day",
            bin 2: "active in the 1st month, besides the 1st week",
            bin 3: "active in the 1st quarter, besides the 1st month",
            bin 4: "active in the 1st year, besides the 1st quarter".

        INPUTS:
            row - pandas Series containing activity data by time-interval
                  of a given user

        OUTPUTS:
            series - pandas Series of user activity from bin0 to bin4.
                     Value=0 means user is inactive at the interval, and
                     Value>=1 means active.

        """

        arr = np.bincount(row.active_at_interval_list)
        slicing = [(0, 1), (1, 2), (2, 5), (5, 14), (14, 53)]
        # indices to slice array,
        # e.g. (2, 5) to get first month activity, besides activity on the first week

        series = Series([1 if (arr[s:e]).any() else 0 for s, e in slicing])

        return series

    def wmqy_interval_retention(
        self, cohort: CohortFilterType = None, interval_in_days: int = 7,
    ) -> Series:

        """
        wmqy_interval_retention

        Return a pandas Series of wmqy retention rates of a cohort.
        WMQY stands for Week, Month, Quarter and Year.
        With WMQY retention, the active rate at each time-interval is
        calculated by ignoring the activies in the previous interval.
        For example, active rate at Month is calculated as the "number of
        active users in the second to fourth week" divided by "number of
        users in the second to fourth week".

        KEYWORDS:
            cohort = None - allows filtering by cohort. Optional input is
                            a dictionary: keys identify columns, values
                            may be a string or list of strings indicating
                            accepted values.

            interval_in_days = 7 - the number of days for a time interval

        OUTPUTS:
            cohort_active_rates - pandas Series indexed by time-interval
                                  indices and valued by the active rate
                                  at that time interval of a cohort

        """

        clickstream, cohorts = self.filter_by_cohorts(cohort)

        # add the activity at reference_timestamp as an activity in clickstream
        tmp = clickstream.append(
            cohorts[["user_id", "reference_timestamp"]].rename(
                {"reference_timestamp": "timestamp"}, axis=1
            )
        )

        merged_stream = tmp.merge(cohorts, on="user_id", how="inner")

        cohort_active_rates = (
            self.user_activities_by_interval(merged_stream, interval_in_days)
            .apply(self.wmqy_interval_bincount, axis=1)
            .join(cohorts.set_index("user_id"))
            .filter(regex=r"[0-9]", axis=1)  # select only the value columns
            .pipe(lambda d: d.sum(axis=0).div(d.shape[0]))
        )

        return cohort_active_rates

    def cohort_retention(
        self,
        retention_type: str,
        retention_cohort: Union[CohortFilterType, List[CohortFilterType]] = None,
        interval_type: str = "week",
        melted_output: bool = False,
        retention_cohort_names: List[str] = [],
    ):

        """
        cohort_retention

        Calculates cohort retention metrics for any number of cohorts. The
        retention metrics can be over either fixed intervals, unbounded
        intervals or custom intervals.

        INPUTS:
            retention_type - string, the type of retention cohort to
                             calculate, any of {"fixed", "unbounded", "wqmy"}

        KEYWORDS:
            retention_cohort = None - allows filtering by multiple cohorts.
                               Optional input is a list of dictionaries: keys
                               identify columns, values may be a string or
                               list of strings indicating accepted values.

            interval_type = "week" - type of time interval used for
                            calculating the retention rates, any of
                            {"day", "week", "month", "quarter", "year"}

            melted_output = False - boolean, set to True to return a melted
                            DataFrame (long format)

            retention_cohort_names = None - list of strings, each string
                                    is the cohort name for the returned
                                    DataFrame

        RAISES:
            CohortAnalysisException - if different length for retention_cohort
                                      and retention_cohort_names

            CohortAnalysisException - if invalid retention_type is provided

            CohortAnalysisException - if invalid interval_type is provided

        OUTPUTS:
            retention_rates - pandas DataFrame of retention rates with
                              given cohort in specified time-intervals

        """

        retentions_mapping = {
            "fixed": self.fixed_interval_retention,
            "unbounded": self.unbounded_interval_retention,
            "wmqy": self.wmqy_interval_retention,
        }

        _intervals_mapping = {
            "day": 1,
            "week": 7,
            "month": 28,
            "quarter": 91,
            "year": 365,
        }

        retention_cohort = (
            retention_cohort
            if isinstance(retention_cohort, list)
            else [retention_cohort]
        )
        if (retention_cohort_names) and (
            len(retention_cohort) != len(retention_cohort_names)
        ):
            raise CohortAnalysisException(
                "retention_cohort_names must have the same length as retention_cohort"
            )

        if retention_type not in retentions_mapping.keys():
            raise CohortAnalysisException(
                "invalid retention_type, permitted types: 'fixed', 'unbounded' and 'wmqy'"
            )

        if interval_type not in _intervals_mapping.keys():
            raise CohortAnalysisException(
                "invalid interval_type, permitted values: 'day', 'week', 'month, 'quarter' and 'year'"
            )

        interval_in_days = _intervals_mapping[interval_type]
        retention_rates = DataFrame()

        for i, cohort in enumerate(retention_cohort):  # type: ignore

            if retention_cohort_names:
                name = retention_cohort_names[i]
            else:
                if cohort is None:
                    name = "cohort"
                else:
                    name = "/".join([f"{k}={v}" for k, v in cohort.items()])

            active_rates = retentions_mapping[retention_type](  # type: ignore
                cohort, interval_in_days
            )

            active_rates.name = name
            retention_rates = pd.concat([retention_rates, active_rates], axis=1)

        # TODO: returns the active rates DataFrame with meaningful indices
        # to show the time-intervals, rather than just integer indices
        if melted_output:
            retention_rates = retention_rates.reset_index().melt(
                id_vars="index", var_name="cohort", value_name="active_rate"
            )

        return retention_rates
