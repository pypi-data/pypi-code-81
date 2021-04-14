#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.
import pandas as pd
import pytest
import json

from mitosheet.tests.test_utils import create_mito_wrapper_dfs


def test_sheet_json_holds_dates_correctly():
    df = pd.DataFrame({
        'name': ['alice','bob','charlie'],
        'date_of_birth': ['2005-10-25','2002-10-2','2001-11-14']
    })

    df['date_of_birth'] = pd.to_datetime(df['date_of_birth'])

    mito = create_mito_wrapper_dfs(df)
    
    sheet_json = json.loads(mito.mito_widget.sheet_json)
    assert sheet_json[0]['data'][0][1] == '2005-10-25 00:00:00'
    assert sheet_json[0]['data'][1][1] == '2002-10-02 00:00:00'
    assert sheet_json[0]['data'][2][1] == '2001-11-14 00:00:00'


# Tests that formatting time_deltas correctly handles positive and negative deltas, and NaN's
def test_sheet_json_holds_timed_deltas_correctly():
    df = pd.DataFrame({
        'dob': ['2005-10-23','2002-8-2 05:12:00','2001-11-14', None],
        'dob2': ['2004-10-23 10:15:15','2002-10-2','2001-07-14 14:15:00', '2005-07-14 14:15:00']
    })

    df['dob'] = pd.to_datetime(df['dob'])
    df['dob2'] = pd.to_datetime(df['dob2'])

    mito = create_mito_wrapper_dfs(df)

    mito.set_formula('=dob - dob2', 0, 'time_deltas', True)
    
    sheet_json = json.loads(mito.mito_widget.sheet_json)
    assert sheet_json[0]['data'][0][2] == '364 days 13:44:45'
    assert sheet_json[0]['data'][1][2] == '-61 days +05:12:00'
    assert sheet_json[0]['data'][2][2] == '122 days 09:45:00'
    assert sheet_json[0]['data'][3][2] == 'NaT'

