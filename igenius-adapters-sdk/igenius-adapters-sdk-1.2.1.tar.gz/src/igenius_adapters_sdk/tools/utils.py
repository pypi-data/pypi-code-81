from itertools import product
from typing import List, Mapping

from igenius_adapters_sdk.entities.numeric_binning import BinningRules
from igenius_adapters_sdk.entities.query import GroupByQuery


def bin_interpolation(query: GroupByQuery, result: List[Mapping]) -> List[Mapping]:
    binset = {}
    for att in query.groups:
        if isinstance(att.function_uri.function_params, BinningRules):
            binset[att.alias] = att.function_uri.function_params.bins
    default = {d.alias: d.default_bin_interpolation for d in query.aggregations}
    fullset = []
    for comb in product(*[[{bins: str(b)} for b in binset[bins]] for bins in binset]):
        partial = {k: v for d in comb for k, v in d.items()}
        match = []
        keep = {}
        for row in result:
            if any(match):
                break
            match.append(True)
            for k in row:
                if k not in partial:
                    keep[k] = row[k]
                    continue
                # the following two lines are related to a postgres issue with None management
                # see https://igenius.atlassian.net/browse/SQD-922?focusedCommentId=57332
                if isinstance(row[k], str):
                    row[k] = row[k].replace("NaN", "None")
                if partial[k] != row[k]:
                    match[-1] = False
                    break
        partial.update(keep if any(match) else default)
        fullset.append(partial)
    return fullset
