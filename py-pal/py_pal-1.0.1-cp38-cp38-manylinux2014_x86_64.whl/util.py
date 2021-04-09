import argparse
import os
import string
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt

from py_pal.complexity import Complexity
from py_pal.estimator import Columns

VALID_CHARS = "-_.() %s%s" % (string.ascii_letters, string.digits)


def check_positive(value):
    int_value = int(value)
    if int_value <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return int_value


def scale_column(data_frame, scale):
    return data_frame.apply(lambda x: x * scale)


def plot_data_points(data_frame):
    # Add subplot
    plt.cla()

    tracing_data = data_frame[Columns.TRACING_DATA]
    current_axis = plt.gca()
    x_axis = tracing_data.columns[0]
    tracing_data[Columns.NORM_OPCODE_WEIGHT] = scale_column(tracing_data[Columns.NORM_OPCODE_WEIGHT],
                                                            data_frame[Columns.NORM_OPCODE_SCALE])
    tracing_data.plot(
        x=x_axis,
        y=Columns.NORM_OPCODE_WEIGHT,
        kind='scatter',
        title="Function: {}, Args: {}".format(data_frame[Columns.FUNCTION_NAME], data_frame[Columns.ARG_DEP]),
        ax=current_axis,
    )
    x_values = tracing_data[x_axis].to_numpy()
    complexity = data_frame[Columns.COMPLEXITY]
    current_axis.plot(
        x_values,
        scale_column(pd.DataFrame(complexity.compute(x_values)), data_frame[Columns.NORM_OPCODE_SCALE]).values,
        color='red'
    )
    return plt


def save_statistics(data_frame, output_dir, target, format, visualize=False):
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    if visualize:
        save_plots(output_dir, data_frame)

    data_frame[[Columns.TRACING_DATA]] = [
        x if isinstance(x, list) else [tuple(x) for x in x.to_numpy()] for x in data_frame[Columns.TRACING_DATA]
    ]

    filename, ext = os.path.splitext(os.path.basename(target))
    if format == 'csv':
        data_frame.to_csv(Path(output_dir) / "{}.{}".format(filename, 'csv'), sep=";")
    if format == 'html':
        data_frame.to_html(Path(output_dir) / "{}.{}".format(filename, 'html'))
    if format == 'excel':
        data_frame.to_excel(Path(output_dir) / "{}.{}".format(filename, 'xlsx'))
    if format == 'json':
        data_frame.to_json(Path(output_dir) / "{}.{}".format(filename, 'json'))


def save_plots(output_dir, original_df):
    original_df['Plot'] = [""] * len(original_df)
    filtered_df = original_df[[isinstance(x, Complexity) for x in original_df[Columns.COMPLEXITY]]]

    for index, filtered_df in filtered_df.iterrows():
        filename = "{}_{}_{}.png".format(filtered_df[Columns.FUNCTION_NAME], filtered_df[Columns.ARG_DEP], index)
        filename_escaped = escape(filename)
        plot = plot_data_points(filtered_df)
        plot.savefig(
            Path(output_dir) / filename_escaped
        )
        original_df.iloc[index, -1] = Path(output_dir) / filename_escaped


def plot_function_complexity(res, show=True):
    res = res[[isinstance(x, Complexity) for x in res[Columns.COMPLEXITY]]]
    for index, data_frame in res.iterrows():
        plot = plot_data_points(data_frame)
        if show:
            plot.show()
    return res


def escape(filename):
    filename_escaped = ''.join(c for c in filename if c in VALID_CHARS)
    filename_escaped = filename_escaped.replace(' ', '_')
    return filename_escaped
