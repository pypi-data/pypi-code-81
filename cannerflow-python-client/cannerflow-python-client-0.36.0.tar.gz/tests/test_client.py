import csv
import os

import json_lines
import numpy as np
import pandas as pd
import pytest
from PIL.PngImagePlugin import PngImageFile

import cannerflow

ENDPOINT = os.getenv('ENDPOINT') or 'http://localhost:3000'

WORKSPACE_ID = os.getenv('WORKSPACE_ID')
if (WORKSPACE_ID is None):
    raise EnvironmentError('No workspace id')

JUPYTER_SECRET = os.getenv("CANNERFLOW_JUPYTER_SECRET") or 'jupyter-secret'
TOKEN = os.getenv('CANNERFLOW_PERSONAL_ACCESS_TOKEN')
if (WORKSPACE_ID is None):
    raise EnvironmentError('No personal access token')

CURRENT_PATH = os.path.dirname(__file__)
CSV_FILE = os.path.join(CURRENT_PATH, 'test.csv')
JSON_FILE = os.path.join(CURRENT_PATH, 'orders.json')
IMAGE_FILE = os.path.join(CURRENT_PATH, 'lena256.png')
NORMAL_CSV = os.path.join(CURRENT_PATH, 'normal.csv')

print({
    'endpoint': ENDPOINT,
    'workspaceId': WORKSPACE_ID,
    'csvFile': CSV_FILE,
    'secret': JUPYTER_SECRET,
    'token': TOKEN
})

# case one, secret-based client
secret_client = cannerflow.client.bootstrap(
    endpoint=ENDPOINT,
    workspace_id=WORKSPACE_ID,
    headers={
        'X-CANNERFLOW-SECRET': JUPYTER_SECRET,
        'X-CANNERFLOW-WORKSPACE-ID': WORKSPACE_ID
    }
)

# case two, token-based client
token_client = cannerflow.client.bootstrap(
    endpoint=ENDPOINT,
    workspace_id=WORKSPACE_ID,
    token=TOKEN,
)


@pytest.fixture(params=[secret_client, token_client])
def client(request):
    return request.param


def test_binary(client):
    with open(NORMAL_CSV, 'rb') as file:
        data = file.read()
        res = client.put_binary(absolute_path=CSV_FILE, data=data)
        assert res is True, "Should upload file"
        binary = client.get_binary(CSV_FILE)
        assert binary == data, "Uploaded file should be same as file"


def test_csv(client):
    with open(NORMAL_CSV) as file:
        spamreader = csv.reader(file)
        uploaded_csv = []
        for row in spamreader:
            uploaded_csv.append(row)
        res = client.put_csv(absolute_path=CSV_FILE, data=uploaded_csv)
        assert res is True, "Should upload csv"
        downloaded_csv = client.get_csv(absolute_path=CSV_FILE)
        assert type(downloaded_csv) is list, "csv should be a list"
        assert uploaded_csv == downloaded_csv, "Uploaded file should be same as file"


def test_pandas_csv(client):
    uploaded_csv = pd.read_csv(NORMAL_CSV)
    res = client.put_csv(absolute_path=CSV_FILE, data=uploaded_csv)
    assert res is True, "Should upload csv"
    downloaded_csv = client.get_pandas_csv(absolute_path=CSV_FILE)
    assert isinstance(downloaded_csv, pd.DataFrame), "should get data frame"
    assert uploaded_csv.equals(downloaded_csv), "Uploaded file should be same as file"


def test_json(client):
    with open(JSON_FILE) as file:
        spamreader = json_lines.reader(file)
        upload_json = []
        for row in spamreader:
            upload_json.append(row)
        res = client.put_json(absolute_path=JSON_FILE, data=upload_json)
        assert res is True, "Should upload json"
        downloaded_json = client.get_json(absolute_path=JSON_FILE)
        assert type(downloaded_json) is list, "json should be a list"
        assert upload_json == downloaded_json, "Uploaded file should be same as file"


def test_image(client):
    with open(IMAGE_FILE, 'rb') as file:
        data = file.read()
        res = client.put_binary(absolute_path=IMAGE_FILE, data=data)
        assert res is True, "Should upload file"

        pimage = client.get_pil_image(IMAGE_FILE)
        assert isinstance(pimage, PngImageFile), "Should be PngImageFile"
        assert pimage.height is 256, "height should be 256"
        assert pimage.width is 256, "width should be 256"

        nimage = client.get_np_image(IMAGE_FILE)
        assert isinstance(nimage, np.ndarray), "Should be ndarray"
        assert nimage.shape[0] is 256, "height should be 256"
        assert nimage.shape[1] is 256, "width should be 256"


def test_list_file(client):
    file = client.list_file()
    assert type(file) is list, "file list should be a list"


def test_list_saved_query(client):
    saved_query = client.list_saved_query()
    assert isinstance(saved_query, list), "should get a list"


def test_use_saved_query(client):
    saved_query = client.list_saved_query()
    if len(saved_query) is 0:
        return
    query = client.use_saved_query(saved_query[0])
    query.wait_for_finish()
    print(query)
    assert isinstance(query, cannerflow.query.Query), "should get a query instance"
    assert type(query.id) == str, "query id should be a string"
    assert type(query.status) == str, "query status should a string"
    assert type(query.row_count) == int, "query row_count should be a int"
    assert type(query.statement_id) == str, "query statement_id should a string"

    assert isinstance(query.columns, list), "columns should be list, but got" + query.columns

    first = query.get_first()
    assert len(first) == 2, "should only get 2 (includs one column row)"

    all_data = query.get_all()
    assert len(all_data) == query.row_count + 1, "should get row_count + 1 (includes the column)"

    any_data = query.get(10, 3)
    assert len(any_data) <= 11, "should get less than 11 rows (includes the column)"

    query.data_format = 'df'
    first = query.get_first()
    assert isinstance(first, pd.DataFrame), "should be a dataframe"

    query.data_format = 'np'
    first = query.get_first()
    assert isinstance(first, np.ndarray), "should be a np array"


def test_gen_query_with_row_data(client):
    query = client.gen_query('SELECT CAST(ROW(ARRAY[1], 2.0) AS ROW(x ARRAY(BIGINT), y DOUBLE))', cache_refresh=True)
    query.wait_for_finish()
    assert query.status == 'FINISHED', "status must be finished"
    assert query.row_count == 1, "should have row_count"
    assert len(query.get_first(1)) == 2, "should get two columns"


def test_gen_query_with_empty_data(client):
    query = client.gen_query('select * from tpch.tiny.lineitem limit 0', cache_refresh=True)
    query.wait_for_finish()
    assert query.status == 'FINISHED', "status must be finished"
    assert query.row_count == 0, "should have row_count"
    assert len(query.get_first(1)) == 1, "should only get column"


def test_gen_query_with_empty_data_in_df(client):
    query = client.gen_query('select * from tpch.tiny.lineitem limit 0', cache_refresh=True, data_format='df')
    query.wait_for_finish()
    assert query.status == 'FINISHED', "status must be finished"
    assert query.row_count == 0, "should have row_count"
    df = query.get_all()

    assert len(df.columns.tolist()) != 0, "should get columns in data frame"


def test_gen_query(client):
    query = client.gen_query('select * from tpch.tiny.lineitem limit 1000', cache_refresh=True)
    query.wait_for_finish()
    assert query.status == 'FINISHED', "status must be finished"
    assert query.row_count > 0, "should have row_count"
    assert len(query.get_first(1)) == 2, "should get 2 rows include column"


def test_query_iterator(client):
    query = client.gen_query('select * from tpch.tiny.lineitem limit 37435', cache_refresh=True)
    query.wait_for_finish()
    assert query.status == 'FINISHED', "status must be finished"
    assert query.row_count > 0, "should have row_count"
    count = 0
    for row in query.get_iterrows():
        assert len(row) == 2, "should format as [columns, data]"
        count += 1
    assert count == 37435, "should get 37435 lines"


def test_query_iterator_small_data(client):
    query = client.gen_query('select * from tpch.tiny.lineitem limit 100', cache_refresh=True)
    query.wait_for_finish()
    assert query.status == 'FINISHED', "status must be finished"
    assert query.row_count > 0, "should have row_count"
    count = 0
    for row in query.get_iterrows():
        assert len(row) == 2, "should format as [columns, data]"
        count += 1
    assert count == 100, "should get 100 lines"


def test_query_iterator_df(client):
    query = client.gen_query('select * from tpch.tiny.lineitem limit 100', cache_refresh=True, data_format="df")
    query.wait_for_finish()
    assert query.status == 'FINISHED', "status must be finished"
    assert query.row_count > 0, "should have row_count"
    count = 0
    for row in query.get_iterrows():
        assert isinstance(row, pd.DataFrame), "should be format as data frame"
        count += 1
    assert count == 100, "should get 100 lines"


def test_get_data_flow(client):
    query = client.gen_query(""" SELECT * FROM (
        VALUES (1, 10), (2, 20), (3, 30), (4, 40), (5, 50), (6, 60), (7, 70), (8, 80), (9, 90), (10, 100)
    ) AS testtable(col, col10)
    """)
    query.wait_for_finish(timeout=5, period=3)
    data: list = query.get_all()
    assert data[0] == ['col', 'col10']
    data = data[1:11]  # remove header
    assert len(data) is 10

    first3 = query.get_first(limit=3)
    first3 = first3[1:4]  # remove header
    assert len(first3) is 3
    assert first3 == data[0:3]

    last3 = query.get_last(limit=3)
    last3 = last3[1:4]  # remove header
    assert len(last3) is 3
    assert last3 == data[7:10]

    middle = query.get(limit=3, offset=3)
    middle = middle[1:4]  # remove header
    assert len(middle) is 3
    assert middle == data[3:6]


def test_show_nested_warning(client, caplog):
    nestedsql = """SELECT * FROM (
        VALUES (
            ARRAY[CAST(ROW(1, 2.0) AS ROW(x BIGINT, y DOUBLE)), CAST(ROW(2, 4.0) AS ROW(x BIGINT, y DOUBLE))],
            MAP(ARRAY['1', '2'], ARRAY[CAST(ROW(1, 2.0) AS ROW(x BIGINT, y DOUBLE)), CAST(ROW(2, 4.0) AS ROW(x BIGINT, y DOUBLE))]),
            CAST(ROW(1, CAST(ROW(1, 2.0) AS ROW(x BIGINT, y DOUBLE))) AS ROW(x BIGINT, y ROW(x BIGINT, y DOUBLE)))
        )
    ) AS nestedtable (arrayofrow, mapofrow, rowofrow)"""

    query = client.gen_query(nestedsql, data_format='df', fetch_by='storage')
    query.wait_for_finish()
    df = query.get_all()
    assert len(caplog.messages) is 3, f"Expect that got 3 warnings but {len(caplog.messages)}."
    assert caplog.messages[0].find('arrayofrow'), "Didn't get the warning for arrayofrow column."
    assert caplog.messages[1].find('mapofrow'), "Didn't get the warning for mapofrow column."
    assert caplog.messages[2].find('rowofrow'), "Didn't get the warning for rowofrow column."

