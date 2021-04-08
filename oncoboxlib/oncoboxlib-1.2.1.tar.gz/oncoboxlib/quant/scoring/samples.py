import csv
from copy import copy
from pathlib import PosixPath, Path
from typing import Tuple, List, Union, IO, Optional

import pandas as pd
from scipy.stats import gmean

from oncoboxlib.common.math.stat import quantile_normalization


def get_samples_columns_type(
        samples: pd.DataFrame,
        norms_included: bool
) -> Tuple[List[str], List[str]]:
    """
    Splits samples to cases and norms and returns columns names of each.

    Parameters
    ----------
    samples : set of cases and norms
    norms_included : whether norms are included in the samples or not

    Returns
    -------
    norms: Names of norm columns
    cases: Names of case columns.
    """
    if not norms_included:
        return list(), list(samples.columns)

    norms = list()
    cases = list()

    for col in samples.columns:
        col_lower = col.lower()

        is_norm = 'norm' in col_lower
        is_case = ('case' in col_lower) or ('tumor' in col_lower) or ('tumour' in col_lower)

        if is_norm and is_case:
            raise ValueError('Column "{}" has ambiguous name.'.format(col))
        elif not is_norm and not is_case:
            raise ValueError('Column "{}" is neither norm nor case.'.format(col))

        if is_norm:
            norms.append(col)
        else:
            cases.append(col)

    return norms, cases


def calc_cnr(
        samples: pd.DataFrame,
        norm_columns: List[str],
        norm_averaging: str = 'gmean'
) -> pd.DataFrame:

    """
    Calculates case-to-norm ratio.
    """
    norms = samples[norm_columns]
    if norm_averaging == 'mean':
        mean_norm = norms.mean(axis=1)
    elif norm_averaging == 'gmean':
        mean_norm = gmean(norms.values, axis=1)
    else:
        raise ValueError(
            'Wrong norm averaging "{}". "mean" or "gmean" supported'.format(norm_averaging))

    return samples.div(mean_norm, axis=0)


def add_external_norms(
        cases: pd.DataFrame,
        norms: pd.DataFrame,
        sample_format: str
) -> Tuple[pd.DataFrame, List[str]]:

    if cases.index.has_duplicates:
        raise ValueError("Cases has duplicate genes.")

    if not isinstance(norms, pd.DataFrame):
        raise ValueError('External norms must be DataFrame instance.')

    if not norms.empty:

        if not norms.index.name == 'SYMBOL':
            raise ValueError('Norms must have first column with name "SYMBOL" that contains genes names.')

        if norms.index.has_duplicates:
            raise ValueError("Norms has duplicate genes.")

        cases = cases.join(norms, how='inner')

        # to cope with zeros
        if sample_format == 'ngs counts':
            cases += 1
        elif sample_format == 'microarray expression':
            # do nothing; we suppose there is no zeros in norms
            pass
        else:
            raise ValueError('Unsupported sample_format "{}". "ngs counts" or "microarray expression'.format(
                sample_format))

        cases = quantile_normalization(cases)

    return cases, norms.columns.to_list()


def get_df_from_text_file(
        file_: Union[str, PosixPath, IO],
        delimiters: str = '\t,; ',
        converters: Optional[dict] = None,
        index_col: Optional[Union[str, int]] = None,
        has_headers: bool = True
) -> pd.DataFrame:

    as_path = False
    if isinstance(file_, (str, PosixPath)):
        file_ = open(file_, 'rb')
        as_path = True

    sniffer = csv.Sniffer()
    file_.seek(0)
    data = file_.readline()
    if not isinstance(data, str):
        data = data.decode('utf-8')
    dialect = sniffer.sniff(data, delimiters=delimiters)
    file_.seek(0)

    params = {'delimiter': dialect.delimiter, 'float_precision': 'high'}

    if converters is not None:
        params.update({'converters': converters})

    if index_col is not None:
        params.update({'index_col': index_col})

    if not has_headers:
        params['header'] = None

    df = pd.read_csv(file_, **params)

    if as_path:
        file_.close()

    return df


def load_samples(
        samples_path: Union[str, PosixPath],
        norms_path: Optional[Union[str, PosixPath]] = None,
        samples_format: Optional[str] = 'ngs counts'
) -> Tuple[pd.DataFrame, List[str], List[str]]:

    samples_path = Path(samples_path)
    if not samples_path.exists():
        raise ValueError(f'File path not found: {samples_path}')

    samples = get_df_from_text_file(samples_path, index_col='SYMBOL')

    norms = None
    if norms_path is not None:
        norms_path = Path(norms_path)
        if not norms_path.exists():
            raise ValueError(f'File path not found: {norms_path}')

        norms = get_df_from_text_file(norms_path, index_col='SYMBOL')

    if norms is None:
        norm_columns, case_columns = get_samples_columns_type(samples, norms_included=True)
    else:
        case_columns = copy(samples.columns)
        samples, norm_columns = add_external_norms(samples, norms, samples_format)

    return samples, case_columns, norm_columns
