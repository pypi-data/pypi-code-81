import abc
import logging
import warnings
from abc import ABC

import numpy as np
import pandas as pd
from numpy.linalg import LinAlgError
from pandas import DataFrame

from py_pal.complexity import ALL_CLASSES, UnderDeterminedEquation

LOGGER = logging.getLogger(__name__)


class Estimator(ABC):
    """
    Base ``Estimator`` class which provides functionality to transform statistics collected by the ``Tracer``
    to `pandas.DataFrame` objects, ways to aggregate opcode statistics per function call and fit the
    ``Complexity`` classes.
    """

    def __init__(self, tracer, per_line=False):
        self.tracer = tracer
        self.per_line = per_line

    @property
    def calls(self):
        call_statistics = self.tracer.get_call_stats()
        data_frame = DataFrame(
            columns=[
                Columns.CALL_ID, Columns.FUNCTION_ID, Columns.FILE, Columns.FUNCTION_LINE, Columns.FUNCTION_NAME,
                Columns.ARGS_NAMES, Columns.ARGS_PROXY, Columns.KWARGS_NAMES, Columns.KWARGS_PROXY,
                Columns.VARARGS_NAMES, Columns.VARARGS_PROXY, Columns.VARKW_NAMES, Columns.VARKW_PROXY,
            ],
            data=call_statistics
        )

        # Remove columns if arguments are not present
        data_frame.dropna(axis=1, how='all', inplace=True)
        LOGGER.debug(len(data_frame))
        return data_frame

    @property
    def opcodes(self):
        opcode_statistics = self.tracer.get_opcode_stats()
        if opcode_statistics.size == 0:
            # Opcode statistics can be empty if no opcode executions are traced
            return DataFrame(columns=[Columns.CALL_ID, Columns.LINE, Columns.OPCODE_WEIGHT])

        data_frame = DataFrame(
            columns=[Columns.CALL_ID, Columns.LINE, Columns.OPCODE_WEIGHT],
            data=opcode_statistics,
        )
        LOGGER.debug(len(data_frame))
        return data_frame

    # Data transformation
    def aggregate_opcodes_per_target(self, target):
        # Sum opcode weights and map them to their respective calls.
        opcodes = self.opcodes
        # if Columns.CALL_ID not in opcodes:
        #    return DataFrame()

        opcode_sum = opcodes.groupby(target)[Columns.OPCODE_WEIGHT].agg(OpcodeWeight=np.sum).reset_index()

        calls = self.calls
        # if any(map(lambda x: x not in target, calls)):
        #    return DataFrame()

        if opcodes.empty or calls.empty:
            return DataFrame()

        data_frame = pd.merge(calls, opcode_sum, on=Columns.CALL_ID)

        # Clean
        data_frame.drop_duplicates(inplace=True)
        return data_frame

    @staticmethod
    def normalize_column(data_frame):
        _min = data_frame.min()
        _max = data_frame.max()
        return data_frame.apply(lambda x: (x - _min) / (_max - _min)), _max - _min

    def group_opcodes_by_call(self, data, group_by, result_columns):
        for _, data_frame in data.groupby(group_by, sort=False):
            slice = DataFrame.copy(data_frame)
            filename = slice[Columns.FILE].values[0]
            line = slice[Columns.LINE if self.per_line else Columns.FUNCTION_LINE].values[0]
            function = slice[Columns.FUNCTION_NAME].values[0]
            if Columns.ARGS_NAMES in slice:
                arg_names = slice[Columns.ARGS_NAMES].values[0]
            else:
                arg_names = None

            # Normalize opcode weights for least squares
            normalized_col, scale = self.normalize_column(slice[Columns.OPCODE_WEIGHT])
            slice[Columns.NORM_OPCODE_WEIGHT] = normalized_col

            if all(map(lambda x: x in slice, result_columns)):
                data_frame_out = slice[result_columns]
            else:
                data_frame_out = DataFrame()
            yield filename, line, function, arg_names, data_frame_out, scale

    @property
    def iterator(self):
        if self.per_line:
            aggregated_opcodes = self.aggregate_opcodes_per_target([Columns.CALL_ID, Columns.LINE])
            if aggregated_opcodes.empty:
                raise StopIteration()
            return self.group_opcodes_by_call(
                aggregated_opcodes,
                [Columns.FUNCTION_ID, Columns.LINE],
                [Columns.ARGS_PROXY, Columns.NORM_OPCODE_WEIGHT, Columns.LINE]
            )
        aggregated_opcodes = self.aggregate_opcodes_per_target(Columns.CALL_ID)
        if aggregated_opcodes.empty:
            raise StopIteration()
        return self.group_opcodes_by_call(
            aggregated_opcodes,
            [Columns.FUNCTION_ID],
            [Columns.ARGS_PROXY, Columns.NORM_OPCODE_WEIGHT]
        )

    @staticmethod
    def infer_complexity(data_frame, arg_column):
        """
        Derive the big O complexity class.

        :param arg_column: Argument column to use as x-axis.
        :param data_frame: Time series-like data.
                            x-axis: argument size
                            y-axis: executed opcodes
        :return: Best fitting complexity class
        """
        best_class = None
        best_residuals = np.inf
        fitted = {}

        for class_ in ALL_CLASSES:
            inst = class_()
            residuals = inst.fit(
                data_frame[arg_column].values.astype(float),
                data_frame[Columns.NORM_OPCODE_WEIGHT].values.astype(float)
            )
            fitted[inst] = residuals

            if residuals < best_residuals - 1e-6:
                best_residuals = residuals
                best_class = inst

        return best_class

    def analyze(self):
        LOGGER.info('%s(per_line=%s)', self.__class__.__name__, self.per_line)

        try:
            for filename, function_line, function, arg_names, data_frame, scale in self.iterator:
                LOGGER.debug("%s: %s", function, len(data_frame))

                for arg_names, complexity, data_points in self.infer_complexity_per_argument(data_frame, arg_names):
                    yield filename, function_line, function, arg_names, complexity, len(data_points), data_points, scale

        except StopIteration:
            warnings.warn("Empty opcode statistics, how did you do that?", UserWarning)

    @abc.abstractmethod
    def infer_complexity_per_argument(self, data_frame, arg_names):
        raise NotImplementedError()

    def export(self):
        data_frame = DataFrame(
            self.analyze(),
            columns=[Columns.FILE, Columns.FUNCTION_LINE, Columns.FUNCTION_NAME, Columns.ARG_DEP, Columns.COMPLEXITY,
                     Columns.DATA_POINTS, Columns.TRACING_DATA, Columns.NORM_OPCODE_SCALE]
        )

        # Ouput order
        cols = [Columns.FUNCTION_NAME, Columns.ARG_DEP, Columns.COMPLEXITY, Columns.FUNCTION_LINE, Columns.FILE,
                Columns.DATA_POINTS, Columns.TRACING_DATA, Columns.NORM_OPCODE_SCALE]
        return data_frame[cols]


class AllArgumentEstimator(Estimator):
    """
    Complexity ``Estimator`` that treats all arguments as one by averaging out the proxy value of all arguments.
    """

    def infer_complexity_per_argument(self, data_frame, arg_names):
        """View all argument axes together and sort argument proxy value ascending"""
        if Columns.ARGS_PROXY not in data_frame:
            return None, DataFrame()

        args_df = pd.DataFrame(data_frame[Columns.ARGS_PROXY].tolist(), index=data_frame.index)
        args_df['mean'] = args_df.mean(axis=1)
        args_df[Columns.NORM_OPCODE_WEIGHT] = data_frame[Columns.NORM_OPCODE_WEIGHT]

        # Take average of ArgProxy values and opcode weights
        if not args_df.empty:
            args_df = args_df.groupby('mean')[Columns.NORM_OPCODE_WEIGHT].mean().reset_index()
            args_df.sort_values('mean', inplace=True)

        try:
            yield arg_names, self.infer_complexity(args_df, 'mean'), args_df[['mean', Columns.NORM_OPCODE_WEIGHT]]
        except (LinAlgError, UnderDeterminedEquation) as exception:
            yield arg_names, exception.__class__.__name__, []


class SeparateArgumentEstimator(Estimator):
    """
    Voodoo complexity ``Estimator`` that tries to infer complexity for each argument separately.
    Even though the influence of arguments on each other is minimized this may not produce reliable
    results and therefore should be viewed as experimental.
    """

    def analyze_args_separate_ascending(self, data_frame):
        # View separate argument axes and sort argument proxy value ascending
        for column in data_frame:
            if column == Columns.NORM_OPCODE_WEIGHT:
                continue

            # Keep influence of other arguments as low as possible by selecting rows with smallest proxy value
            args_columns = data_frame.columns.to_list()[:-1]
            data_frame = data_frame.sort_values(args_columns)
            data_frame.drop_duplicates([column, Columns.NORM_OPCODE_WEIGHT], keep='first', inplace=True)
            yield self.infer_complexity(data_frame, column), column, data_frame[[column, Columns.NORM_OPCODE_WEIGHT]]

    @staticmethod
    def unpack_tuples(data_frame):
        # Unpack tuples of arguments
        slice = data_frame.copy()
        slice.dropna(subset=[Columns.ARGS_PROXY], inplace=True)
        unpacked_data_frame = pd.DataFrame(zip(*slice[Columns.ARGS_PROXY])).transpose()
        unpacked_data_frame[Columns.NORM_OPCODE_WEIGHT] = slice[Columns.NORM_OPCODE_WEIGHT]
        unpacked_data_frame.dropna(inplace=True, )
        return unpacked_data_frame

    @staticmethod
    def map_arg_names(pos, names):
        if not names:
            return ""
        if isinstance(pos, int):
            return names[pos]
        return list(map(lambda x: names[x], pos))

    def infer_complexity_per_argument(self, data_frame, arg_names):
        warnings.warn("You are using an experimental feature.", UserWarning)

        if Columns.ARGS_PROXY not in data_frame:
            return None, DataFrame()

        args_df = self.unpack_tuples(data_frame)

        arg = 0
        try:
            for best, arg_pos, data_points in self.analyze_args_separate_ascending(args_df):
                yield self.map_arg_names(arg_pos, arg_names), best, data_points
        except (LinAlgError, UnderDeterminedEquation) as exception:
            yield self.map_arg_names(arg, arg_names), exception.__class__.__name__, []
        finally:
            arg += 1


class Columns:
    """Column names for the DataFrame objects used in the ``Estimator`` classes."""
    CALL_ID = 'CallID'
    FILE = 'File'
    FUNCTION_NAME = 'FunctionName'
    ARGS_PROXY = 'ArgsProxy'
    ARGS_NAMES = 'Args'
    KWARGS_PROXY = 'KwargsProxy'
    KWARGS_NAMES = 'Kwargs'
    VARARGS_PROXY = 'VarArgsProxy'
    VARARGS_NAMES = 'VarArgs'
    VARKW_PROXY = 'VarKwProxy'
    VARKW_NAMES = 'VarKw'
    LINE = 'Line'
    FUNCTION_LINE = 'FunctionLine'
    OPCODE_WEIGHT = 'OpcodeWeight'
    NORM_OPCODE_WEIGHT = 'NormOpcodeWeight'
    NORM_OPCODE_SCALE = 'NormOpcodeScale'
    ARG_DEP = 'DependentArgs'
    COMPLEXITY = 'Complexity'
    DATA_POINTS = 'DataPoints'
    TRACING_DATA = 'TracingData'
    FUNCTION_ID = 'FunctionID'
