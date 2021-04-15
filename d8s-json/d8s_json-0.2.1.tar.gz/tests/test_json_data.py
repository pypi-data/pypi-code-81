import os

import pytest
from d8s_dates import date_now
from d8s_file_system import directory_create, directory_delete, file_delete, file_write

from d8s_json import (
    json_files,
    json_path_bracket_notation_to_dot_notation,
    json_path_dot_notation_to_bracket_notation,
    json_prettify,
    json_read,
    json_read_first_arg_string_decorator,
    json_search,
    json_structure,
    json_write,
)

NON_EXISTENT_FILE_PATH = './foo'
TEST_DIRECTORY_PATH = './test_files'
TEST_FILE_CONTENTS = '{"a": 1}'
TEST_FILE_NAME = 'a.json'
EXISTING_FILE_PATH = os.path.join(TEST_DIRECTORY_PATH, TEST_FILE_NAME)


@pytest.fixture(autouse=True)
def clear_testing_directory():
    """This function is run after every test."""
    directory_delete(TEST_DIRECTORY_PATH)
    directory_create(TEST_DIRECTORY_PATH)
    file_write(EXISTING_FILE_PATH, TEST_FILE_CONTENTS)


def setup_module():
    """This function is run before all of the tests in this file are run."""
    directory_create(TEST_DIRECTORY_PATH)


def teardown_module():
    """This function is run after all of the tests in this file are run."""
    directory_delete(TEST_DIRECTORY_PATH)


def test_json_files_docs_1():
    assert json_files(TEST_DIRECTORY_PATH) == ['a.json']


def test_json_write_docs_1():
    d = {'foo': 'bar'}
    json_write(EXISTING_FILE_PATH, d)
    assert json_read(EXISTING_FILE_PATH) == d


def test_json_write_docs_bad_json():
    # create a dict that has a datetime.datetime object in it
    d = {'a': 'foobar', 'b': date_now()}
    try:
        # this will raise an exception because the datetime.datetime object is not JSON serializable
        json_write(EXISTING_FILE_PATH, d)
    except Exception:
        # make sure the file at EXISTING_FILE_PATH has its original contents...
        # normally, if we were not using atomic writes, the file at EXISTING_FILE_PATH would have part of the data in d (the part before the datetime.datetime object which caused the failure)...
        # but, because we are using atomic file writes, the file at EXISTING_FILE_PATH keep its original contents
        assert json_read(EXISTING_FILE_PATH)['a'] == json_read(TEST_FILE_CONTENTS)['a']


def test_json_path_bracket_notation_to_dot_notation_1():
    dot_notation_path = ''
    result = json_path_bracket_notation_to_dot_notation(dot_notation_path)
    assert result == ''

    dot_notation_path = "['foo']"
    result = json_path_bracket_notation_to_dot_notation(dot_notation_path)
    assert result == 'foo'

    dot_notation_path = '["foo"]'
    result = json_path_bracket_notation_to_dot_notation(dot_notation_path)
    assert result == 'foo'

    dot_notation_path = "['foo']['bar']"
    result = json_path_bracket_notation_to_dot_notation(dot_notation_path)
    assert result == 'foo.bar'

    dot_notation_path = '["foo"]["bar"]'
    result = json_path_bracket_notation_to_dot_notation(dot_notation_path)
    assert result == 'foo.bar'

    dot_notation_path = "['foo']['bar']['buzz']"
    result = json_path_bracket_notation_to_dot_notation(dot_notation_path)
    assert result == 'foo.bar.buzz'

    dot_notation_path = '["foo"]["bar"]["buzz"]'
    result = json_path_bracket_notation_to_dot_notation(dot_notation_path)
    assert result == 'foo.bar.buzz'


def test_json_path_dot_notation_to_bracket_notation_1():
    dot_notation_path = ''
    result = json_path_dot_notation_to_bracket_notation(dot_notation_path)
    assert result == ''

    dot_notation_path = 'foo'
    result = json_path_dot_notation_to_bracket_notation(dot_notation_path)
    assert result == '["foo"]'

    dot_notation_path = 'foo.bar'
    result = json_path_dot_notation_to_bracket_notation(dot_notation_path)
    assert result == '["foo"]["bar"]'

    dot_notation_path = 'foo.bar.buzz'
    result = json_path_dot_notation_to_bracket_notation(dot_notation_path)
    assert result == '["foo"]["bar"]["buzz"]'


def test_json_loads_single_quotes():
    string = "{'test': 'a'}"
    d = json_read(string)
    assert len(d) == 1
    assert d['test'] == 'a'


def test_json_loads_double_quotes():
    string = '{"test": "a"}'
    d = json_read(string)
    assert len(d) == 1
    assert d['test'] == 'a'


def test_json_load_file():
    file_path = './a.json'
    json_data = {'a': 'anthem', 'b': 'be'}

    file_write(file_path, json_data)
    assert json_read(file_path) == json_data
    file_delete(file_path)


# Jan 2021 - this test is intentionally disabled - see https://github.com/democritus-project/d8s-json/issues/2
# def test_json_load_url():
#     # TODO: this test is failing because, when using the request_or_read function, the content of the url below is json and is returned as a dict, which the json_read function tries to process and fails
#     url = 'https://jsonplaceholder.typicode.com/posts/1'
#     result = json_read(url)
#     assert result['userId'] == 1


def test_json_prettify_1():
    assert json_prettify({'test': 'a'}) == '{\n    "test": "a"\n}'


def test_json_structure_1():
    foo = [
        {
            '_attributes': {'style': 'text-align:center'},
            'a': [{'_attributes': {'href': '?id=1349421800'}, '_value': '1349421800'}],
        },
        {'_attributes': {'style': 'text-align:center'}, '_value': '2019-04-04'},
        {'_attributes': {'style': 'text-align:center'}, '_value': '2019-04-04'},
        {'_attributes': {'style': 'text-align:center'}, '_value': '2020-04-04'},
        {
            'a': [
                {
                    '_attributes': {'style': 'white-space:normal', 'href': '?caid=1191'},
                    '_value': 'C=US, O=DigiCert Inc, CN=DigiCert SHA2 Secure Server CA',
                }
            ]
        },
    ]
    structure = json_structure(foo)
    print('structure {}'.format(structure))
    assert structure.split('\n')[0] == "[0]['_attributes'] (list of 1 dict)"
    assert structure.split('\n')[16] == "[4]['a'][0]['_attributes'] (list of 2 dicts)"
    assert structure.split('\n')[-1] == "[4]['a'][0]['_value']: C=US, O=DigiCert Inc, CN=DigiCert SHA2 Secure Server CA"

    d = {'foo': '\n bar'}
    structure = json_structure(d)
    print('structure {}'.format(structure))
    assert structure == '''['foo']: \\n bar'''


def test_json_structure_2():
    foo = {'test': [1, '2', {'a': 'b'}]}
    assert (
        json_structure(foo)
        == "['test'] (list of 3 lists)\n['test'][0]: 1 (<class 'int'>)\n['test'][1]: 2 (<class 'str'>)\n['test'][2]['a']: b"
    )


def test_json_search_1():
    foo = [
        {
            '_attributes': {'style': 'text-align:center'},
            'a': [{'_attributes': {'href': '?id=1349421800'}, '_value': '1349421800'}],
        },
        {'_attributes': {'style': 'text-align:center'}, '_value': '2019-04-04'},
        {'_attributes': {'style': 'text-align:center'}, '_value': '2019-04-04'},
        {'_attributes': {'style': 'text-align:center'}, '_value': '2020-04-04'},
        {
            'a': [
                {
                    '_attributes': {'style': 'white-space:normal', 'href': '?caid=1191'},
                    '_value': 'C=US, O=DigiCert Inc, CN=DigiCert SHA2 Secure Server CA',
                }
            ]
        },
    ]
    paths = json_search(foo, 'text-align:center')
    assert paths == [
        "[0]['_attributes']['style']",
        "[1]['_attributes']['style']",
        "[2]['_attributes']['style']",
        "[3]['_attributes']['style']",
    ]
    paths = json_search(foo, 'C=US, O=DigiCert Inc, CN=DigiCert SHA2 Secure Server CA')
    assert paths == ["[4]['a'][0]['_value']"]


@json_read_first_arg_string_decorator
def json_read_first_arg_string_decorator_test_func_a(a):
    """."""
    return a


def test_json_read_first_arg_string_decorator_1():
    assert json_read_first_arg_string_decorator_test_func_a('{}') == {}
    assert json_read_first_arg_string_decorator_test_func_a({}) == {}
    assert json_read_first_arg_string_decorator_test_func_a('[{"name": "Bob", "daring": true}]') == [
        {'name': 'Bob', 'daring': True}
    ]
