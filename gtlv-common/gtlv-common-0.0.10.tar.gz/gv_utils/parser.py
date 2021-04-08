#!/usr/bin/env python3

import asyncio
import io
import json
import os
from typing import Any, Callable, Generator

import numpy as np
import pandas as pd
from pandas.api import types as pdtypes
from shapely.geometry.base import BaseGeometry

from gv_utils.datetime import datetime, from_timestamp, to_timestamp
from gv_utils.enums import AttId, Message, MessageData, MessageKind
from gv_utils.geometry import decode_geometry, encode_geometry


class MessageEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, datetime):
            return to_timestamp(o)
        elif isinstance(o, BaseGeometry):
            return encode_geometry(o)
        elif isinstance(o, pd.DataFrame):
            return encode_pandas(o)
        else:
            return super().default(o)


def encode_pandas(dataframe: pd.DataFrame) -> str:
    dataframe.fillna(MessageData.nan, inplace=True)
    for col in dataframe.columns:
        try:
            if pdtypes.is_numeric_dtype(dataframe[col]):
                dataframe[col] = dataframe[col].round().astype('int')
            else:
                dataframe[col] = dataframe[col].map(json.dumps)
        except:
            pass
    dataframe.replace(MessageData.nan, '', inplace=True)
    return dataframe.to_csv(sep=MessageData.csvseparator)


async def encode_message(message: Any) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, sync_encode_message, message)


def sync_encode_message(message: Any) -> str:
    return json.dumps(message, cls=MessageEncoder)


def add_main_prefix(messagekind: str) -> str:
    return '{prefix}{sep}{kind}'.format(prefix=MessageKind.mainprefix, sep=MessageKind.separator, kind=messagekind)


def object_hook(obj: dict, custom_data_decoder: Callable = None) -> dict:
    for key in obj:
        val = None
        if key == Message.kind:
            val = __remove_past_prefix(obj[key])
        elif key == Message.timestamp:
            val = from_timestamp(obj[key])
        elif key == Message.data:
            if isinstance(obj[key], str):
                if custom_data_decoder is None:
                    custom_data_decoder = decode_pandas
            if custom_data_decoder is not None:
                val = custom_data_decoder(obj[key])
        elif key == AttId.geom:
            val = decode_geometry(obj[key])
        if val is not None:
            obj[key] = val
    return obj


async def decode_message(message: str, custom_data_decoder: Callable = None) -> dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, sync_decode_message, message, custom_data_decoder)


def sync_decode_message(message: str, custom_data_decoder: Callable = None) -> dict:
    return json.loads(message, object_hook=lambda o: object_hook(o, custom_data_decoder))


def decode_pandas(data: str) -> pd.DataFrame:
    dataframe = pd.read_csv(io.StringIO(data), sep=MessageData.csvseparator, index_col=0)
    for col in dataframe.columns:
        try:
            if not pdtypes.is_numeric_dtype(dataframe[col]):
                dataframe[col] = dataframe[col].map(json.loads)
        except:
            pass
    dataframe.replace(MessageData.nan, np.NaN, inplace=True)
    dataframe.replace(str(MessageData.nan), np.NaN, inplace=True)
    try:
        dataframe.index = dataframe.index.astype('str')
    except:
        pass
    return dataframe


def merge_types(types: list) -> str:
    return MessageKind.separator.join(types)


def __remove_past_prefix(messagekind: str) -> str:
    sep = MessageKind.separator
    splited = messagekind.split(sep)
    return messagekind if splited[0] != MessageKind.past else sep.join(splited[1:])


def remove_data_type_suffix_from_message_kind(messagekind: str) -> str:
    sep = MessageKind.separator
    splited = messagekind.split(sep)
    return messagekind if splited[0] != MessageKind.datapoint else sep.join(splited[:-1])


def remove_data_point_from_message_kind(messagekind: str) -> str:
    sep = MessageKind.separator
    splited = messagekind.split(sep)
    if len(splited) >= 3:
        try:
            splited.remove(MessageKind.datapoint)
        except ValueError:
            pass
    return sep.join(splited)


def data_to_gen(data: Any, datadate: datetime = None, sampletimefield: str = None) -> Generator[dict, None, None]:
    gen = None
    if isinstance(data, dict):
        gen = data_dict_to_gen
    elif isinstance(data, str):
        gen = data_csv_to_gen
    elif isinstance(data, pd.DataFrame):
        gen = data_pandas_to_gen
    if gen is not None:
        data = gen(data, datadate, sampletimefield)
    return data


def data_dict_to_gen(datadict: dict, datadate: datetime = None,
                     sampletimefield: str = None) -> Generator[Any, None, None]:
    for eid, values in datadict.items():
        yield expand_dict(values, eid, datadate, sampletimefield)


def data_csv_to_gen(datacsv: str, datadate: datetime = None,
                    sampletimefield: str = None) -> Generator[Any, None, None]:
    def _get_line(rawline):
        return rawline.strip(os.linesep).split(MessageData.csvseparator)

    csvbuffer = io.StringIO(datacsv)
    header = _get_line(csvbuffer.readline())
    if datadate is None:
        datadate = from_timestamp(int(header.pop(0)))
    if sampletimefield is None:
        sampletimefield = AttId.sampletime
    for line in csvbuffer.readlines():
        line = _get_line(line)
        eid = line.pop(0)
        values = {}
        for i in range(len(header)):
            value = line[i]
            try:
                value = int(value)
            except ValueError:
                try:
                    value = json.loads(value)  # if error add: .replace('\'', '"')
                except (AttributeError, json.decoder.JSONDecodeError):
                    pass
            values[header[i]] = value
        yield expand_dict(values, eid, datadate, sampletimefield)
    csvbuffer.close()


def data_pandas_to_gen(dataframe: pd.DataFrame, sampletimefield: str = None) -> Generator[Any, None, None]:
    yield from data_dict_to_gen(data_pandas_to_dict(dataframe), from_timestamp(int(dataframe.index.name)),
                                sampletimefield)


def data_pandas_to_dict(dataframe: pd.DataFrame) -> dict:
    return dataframe.to_dict(orient='index')


def expand_dict(values: dict, eid: str, datadate: datetime, sampletimefield: str) -> dict:
    extradict = {AttId.eid: eid}
    if sampletimefield is not None and datadate is not None:
        extradict[sampletimefield] = datadate
    return dict(**values, **extradict)
