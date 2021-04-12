import json
import numpy as np
import os

from typing import List, Dict
from teradataml.analytics.valib import *
from teradataml import configure
from teradataml.dataframe.dataframe import DataFrame

configure.val_install_location = os.environ.get("AOA_VAL_DB", "VAL")


class _NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(_NpEncoder, self).default(obj)


def get_reference_ranges(current_statistics, continuous_vars):
    # need to get the min / max for each histogram only.. This can/should be managed at a higher level in the app later
    # so it is consistent across executions of training. VAL will put values out of the range into the extreme buckets
    # so they are still captured and we can deal with these extremes in prometheus also and expand buckets if needed
    if os.path.isfile("artifacts/input/data_stats.json"):
        with open("artifacts/input/data_stats.json") as f:
            data_stats = json.load(f)

            training_stats = dict(data_stats["features"])
            training_stats.update(data_stats["predictors"])

            return {k: (training_stats[k]["statistics"]["min"], training_stats[k]["statistics"]["max"]) for k in continuous_vars}
    else:
        # get min, max from statistics or get xmin,xmax from current_statistics
        ranges = current_statistics.drop(current_statistics.columns.difference(["xcol", "xmin", "xmax"]), 1)
        ranges = ranges.set_index("xcol")
        ranges = ranges.to_dict(orient='index')

        return {k: (v["xmin"], v["xmax"]) for k, v in ranges.items()}


def get_reference_edges(reference_ranges, vars, bins=10):
    # boundaries for multiple columns follows the following format..
    # ["{10, 0, 200000}", "{5, 0, 100}"]

    # boundaries = []
    # for var in vars:
    #     edges = reference_statistics["features"][var]["statistics"]["histogram"]["edges"]
    #     edges_str = ",".join(str(edge) for edge in edges)
    #     boundaries.append("{{ {} }}".format(edges_str))
    #
    # return {"boundaries": boundaries}

    edges = []
    for var in vars:
        min, max = reference_ranges[var]
        edges.append(np.linspace(min, max, bins + 1).tolist())

    return edges


def convert_all_edges_to_val_str(all_edges):
    boundaries = []
    for edges in all_edges:
        edges_str = ",".join(str(edge) for edge in edges)
        boundaries.append("{{ {} }}".format(edges_str))

    return boundaries


def record_stats(df: DataFrame,
                 features: List,
                 predictors: List,
                 categorical: List,
                 category_labels: Dict,
                 category_ordinals: Dict = {},
                 importance: Dict = {}):
    """

    example usage:
        pima = DataFrame("PIMA_TRAIN")

        record_stats(pima,
                   features=["TwoHourSerIns", "Age"],
                   predictors=["HasDiabetes"],
                   categorical=["HasDiabetes"],
                   importance={"Age": 0.9, "TwoHourSerIns": 0.1},
                   category_labels={"HasDiabetes": {0: "false", 1: "true"}})

    :param df:
    :param features:
    :param predictors:
    :param categorical:
    :param category_labels:
    :param category_ordinals:
    :param importance:
    :return:
    """
    if not isinstance(df, DataFrame):
        raise ValueError("We only support teradataml DataFrame currently")

    if not all(k in category_labels for k in categorical):
        raise ValueError("You must specify a category_label for each categorical variable")

    total_rows = df.shape[0]

    continuous_vars = list((set(features) | set(predictors)) - set(categorical))

    reference_edges = []

    if len(continuous_vars) > 0:
        stats = valib.Statistics(data=df, columns=','.join(continuous_vars), stats_options="all")
        stats = stats.result.to_pandas().reset_index()

        reference_ranges = get_reference_ranges(stats, continuous_vars)
        reference_edges = get_reference_edges(reference_ranges, continuous_vars)

        hist = valib.Histogram(data=df, columns=','.join(continuous_vars), boundaries=convert_all_edges_to_val_str(reference_edges))
        hist = hist.result.to_pandas().reset_index()

    if len(categorical) > 0:
        frequencies = valib.Frequency(data=df, columns=','.join(categorical))
        frequencies = frequencies.result.to_pandas().reset_index()

    data_struct = {
        "num_rows": total_rows,
        "features": {},
        "predictors": {}
    }

    def strip_key_x(d: Dict):
        return {k[1:]: v for k, v in d.items()}

    def add_var_metadata(var):
        if var in continuous_vars:
            var_hist = hist[hist.xcol == var].sort_values(by=['xbin'])

            bin_edges = [var_hist.xbeg.tolist()[0]]+var_hist.xend.tolist()
            bin_values = var_hist.xcnt.tolist()

            # Add missing bin_values based on the bin_edges vs reference_edges.
            # VAL doesn't return empty bins
            var_ref_edges = reference_edges[continuous_vars.index(var)]
            if len(bin_edges) < len(var_ref_edges):
                for i, edge in enumerate(var_ref_edges):
                    if edge not in bin_edges:
                        bin_values.insert(i, 0)

            stats_values = stats[stats.xcol == var].drop(["xdb", "xtbl", "xcol"], axis=1).to_dict(orient='records')[0]

            data_struct["features"][var] = {
                "type": "continuous",
                "statistics": strip_key_x(stats_values),
            }
            data_struct["features"][var]["statistics"]["histogram"] = {
                "edges": var_ref_edges,
                "values": bin_values
            }

            if var in importance:
                data_struct["features"][var]["importance"] = importance[var]

        else:
            data_struct["predictors"][var] = {
                "type": "categorical",
                "category_labels": category_labels[var],
                "ordinal": category_ordinals.get(var, False),
                "statistics": {
                    "frequency": frequencies[frequencies.xcol == var][["xval", "xcnt"]].set_index("xval").T.to_dict(orient='records')[0]
                }
            }

            if var in importance:
                data_struct["predictors"][var]["importance"] = importance[var]

    for var in features:
        add_var_metadata(var)

    for var in predictors:
        add_var_metadata(var)

    with open("artifacts/output/data_stats.json", 'w+') as f:
        json.dump(data_struct, f, indent=2, cls=_NpEncoder)

