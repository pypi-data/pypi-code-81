import json
import logging
import os
from pathlib import Path
import re
from typing import List, Union

import numpy as np
import pandas as pd
import requests

import arthurai.util as arthur_util
from arthurai.common.exceptions import InternalValueError, UserTypeError, UserValueError, InternalTypeError

logger = logging.getLogger(__name__)

def retrieve_parquet_files(directory_path: str):
    """Checks whether a given directory and its subdirectories contain parquet files,
    if so this will return a list of the files

    :param directory_path:    local path to check files types

    :return: List of paths for parquet files that are found
    """
    parquet_files = []
    for path, subdir, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.parquet'):
                parquet_files.append(Path(os.path.join(path, file)))
    return parquet_files


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """

    @staticmethod
    def convert_value(obj):
        """Converts the given object from a numpy data type to a python data type, if the object is already a
        python data type it is returned

        :param obj: object to convert
        :return: python data type version of the object
        """
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32,
                              np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        elif isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        elif isinstance(obj, float) and np.isnan(obj):
            return None
        return obj


def standardize_pd_obj(data: Union[pd.DataFrame, pd.Series], dropna: bool, replacedatetime: bool) -> Union[pd.DataFrame, pd.Series]:
    """Standardize pandas object for nans and datetimes.
    
    Standardization includes casting correct type for int columns that are float due to nans and 
    for converting datetime objects into isoformatted strings.

    :param data: the pandas data to standardize
    :param dropna: if True, drop nans from numeric date columns
    :param dropna: if True, replace timestamps with isoformatted strings

    :return: the standardized pandas data
    :raise: TypeError: timestamp is not of type `datetime.datetime`
    :raise: ValueError: timestamp is not timezone aware and no location data is provided to remedy
    """
    
    def standardize_pd_series(series: pd.Series) -> pd.Series:
        series = series.replace([np.inf, -np.inf], np.nan)
        nans_present = series.isnull().values.any()
        if dropna:
            series = series.dropna()

        # handle case where int column has nans and therefore is incorrectly seen as float column
        if re.search("float*", series.dtype.name, flags=re.I) and nans_present:
            valid_series = series.dropna()
            if len(valid_series) > 0 and np.array_equal(valid_series, valid_series.astype(int)):
                return series.astype(pd.Int64Dtype())

        # check to make sure datetimes are timezone aware
        elif re.search("(datetime|timestamp).*", series.dtype.name, flags=re.I) or arthur_util.is_string_date(series.values[0]): # TODO: remove is_date and first conditional below when deprecating string support @ https://arthurai.atlassian.net/jira/software/projects/CR/boards/11?selectedIssue=CR-10
            if arthur_util.is_string_date(series.values[0]):
                logger.warning(
                    f"DEPRECATION WARNING: Your feature <{series.name}> providing timestamps starting with <{series.values[0]}> is of type `str` and is assumed to be in UTC format. `timezone` information will be ignored. `str` types will be deprecated. Please use timeaware `datetime.datetime` timestamps and use arthurai.util.format_timestamp if needed, e.g. `format_timestamp(datetime.strptime('2020-01-01 01:01:01', '%Y-%m-%d %H:%M:%S'), 'US/Eastern')`.",
                )
            formatted_series = series.apply(arthur_util.format_timestamp)
            if replacedatetime:
                return formatted_series

        return series

    if isinstance(data, pd.Series):
        return standardize_pd_series(data)
    elif isinstance(data, pd.DataFrame):
        if dropna:
            raise InternalValueError(f"Cannot use dropna={dropna} with data argument as pd.DataFrame.")
        df = data.copy()
        for column in df.columns:
            df[column] = standardize_pd_series(df[column])
        return df
    else:
        raise InternalTypeError("Cannot standardize object that is not pd.DataFrame or pd.Series.")