# -*- coding: utf-8 -*-
"""Deal with n-tuple jcamps"""
import numpy as np

from .constants import END_STRING, NTUPLE_HEADER, NTUPLE_PAGE_HEADER, SYMBOL_LIST_NTUPLE
from .utils import InvalidNtupleError, _format_additional_header


def _process_data_dict(
    data_dictionary_key: str, data_dictionary_values: dict, i: int = 0
) -> dict:
    try:
        name = data_dictionary_values["name"].replace(r" *\[.*", "")
    except KeyError:
        name = ""
    try:
        unit = data_dictionary_values["unit"].replace(r".*\[(.*)\].*", "$1")
    except KeyError:
        unit = ""

    try:
        symbol = data_dictionary_values["symbol"]
    except KeyError:
        symbol = data_dictionary_key

    try:
        var_name = data_dictionary_values["name"]
    except KeyError:
        var_name = name if name != "" else data_dictionary_key

    try:
        var_type = data_dictionary_values["type"].upper()
        if var_type not in ["INDEPENDENT", "DEPENDENT"]:
            raise ValueError()
    except ValueError or KeyError:  # pylint:disable=binary-op-exception
        if i == 0:
            var_type = "INDEPENDENT"
        else:
            var_type = "DEPENDENT"

    maximum = np.max(data_dictionary_values["data"])
    minimum = np.min(data_dictionary_values["data"])

    return {
        data_dictionary_key: {
            "data": data_dictionary_values["data"],
            "type": var_type,
            "unit": unit,
            "maximum": maximum,
            "minimum": minimum,
            "symbol": symbol,
            "var_name": var_name,
            "dimension": len(data_dictionary_values["data"]),
            "name": name,
        }
    }


def from_dict(  # pylint:disable=too-many-arguments,too-many-locals
    data_dictionary: dict,
    title: str = "",
    owner: str = "",
    origin: str = "",
    data_type: str = "",
    meta: dict = None,
) -> str:
    """[summary]

    Args:
        data_dictionary (dict): a nested dictionary of form
            {
                'x' : {
                    'data': [],
                    'type': 'INDEPENDENT'
                    'unit': ''
                }
            }
        title (str, optional): Defaults to "".
        owner (str, optional):  Defaults to "".
        origin (str, optional): Defaults to "".
        data_type (str, optional):  Defaults to "".
        meta (dict, optional):  Defaults to None.

    Raises:
        InvalidTupleError: In case x/y keys are missing

    Returns:
        str: [description]
    """
    var_names = []
    units = []
    symbols = []
    var_dims = []
    datas = []
    types = []

    header = NTUPLE_HEADER.format(
        title=title, dataType=data_type, owner=owner, origin=origin
    ) + _format_additional_header(meta)

    for counter, data_dict_tuple in enumerate(data_dictionary.items()):
        data_dictionary_key, data_dictionary_values = data_dict_tuple
        new_data_dict = _process_data_dict(
            data_dictionary_key, data_dictionary_values, counter
        )
        var_names.append(new_data_dict[data_dictionary_key]["var_name"])
        units.append(new_data_dict[data_dictionary_key]["unit"])
        symbols.append(new_data_dict[data_dictionary_key]["symbol"])
        datas.append(new_data_dict[data_dictionary_key]["data"])
        var_dims.append(str(new_data_dict[data_dictionary_key]["dimension"]))
        types.append(new_data_dict[data_dictionary_key]["type"])

    if "x" not in symbols:
        raise InvalidNtupleError("You must have the x symbol in your dictionary")
    if "y" not in symbols:
        raise InvalidNtupleError("You must have the y symbol in your dictionary")
    ntuple_page_header = NTUPLE_PAGE_HEADER.format(
        varName=",".join(var_names),
        symbol=",".join(symbols),
        varType=",".join(types),
        varDim=",".join(var_dims),
        units=",".join(units),
        dataType=data_type,
    )

    peak_table_header = SYMBOL_LIST_NTUPLE.format(symbols="".join(symbols))

    point_lists = []
    for i in range(len(datas[0])):
        sublist = []
        for column in datas:
            sublist.append(str(column[i]))

        point_lists.append("\t".join(sublist))

    jcamp_string = (
        header
        + ntuple_page_header
        + peak_table_header
        + "\n".join(point_lists)
        + "\n"
        + END_STRING
    )

    return jcamp_string
