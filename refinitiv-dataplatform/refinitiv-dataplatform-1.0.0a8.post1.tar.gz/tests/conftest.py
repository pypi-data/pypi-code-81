import asyncio
import json
import os
import sys
import time
import traceback
from importlib import reload
from threading import Thread
from unittest.mock import patch

import pytest

import mock_server
import refinitiv.dataplatform as rdp
from mocks import MockSession, MockAuthResponse
from refinitiv.dataplatform import configure
from refinitiv.dataplatform.content.ipa.enum_types import Frequency

EDP_USERNAME = ""
EDP_PASSWORD = ""
DESKTOP_APP_KEY = ""


def __parse():
    global EDP_USERNAME, EDP_PASSWORD, DESKTOP_APP_KEY

    DESKTOP_APP_KEY = os.environ.get('DESKTOP_APP_KEY')

    if DESKTOP_APP_KEY is None:
        raise Exception("DESKTOP_APP_KEY is not an env variable, 'DESKTOP_APP_KEY'.")

    EDP_PASSWORD = os.environ.get('EDP_PASSWORD')

    if EDP_PASSWORD is None:
        raise Exception("EDP_PASSWORD is not an env variable, 'EDP_PASSWORD'.")

    EDP_USERNAME = os.environ.get('EDP_USERNAME')

    if EDP_USERNAME is None:
        raise Exception("EDP_USERNAME is not an env variable, 'EDP_USERNAME'.")


__parse()


class SessionTest(rdp.Session):
    def get_omm_login_message_key_data(self):
        pass

    def _get_stream_status(self, stream_service):
        pass

    def _set_stream_status(self, stream_service, stream_status):
        pass

    def _get_stream_connection_configuration(self, stream_service):
        pass

    async def _create_and_start_stream_connection(self, stream_service):
        pass


def has_in_message(subs, message):
    return bool([s for s in subs if s in message])


phrases = [
    "is not entitled for headline search due to missing POs",
    "access denied. Scopes required to access the resource"
    ]


def check_for_access_and_skip_if_not(content="news"):
    # If we will raise pytest.fail here, fail will all process of collection tests
    open_platform_session(raise_fail=False)

    fail = None
    not_success = False
    try:
        if content == "news":
            response = rdp.news.get_headlines('R:AAPL.O')
            if not response.is_success and has_in_message(phrases, response.error_message):
                not_success = True
    except Exception as e:
        fail = str(e)

    if not_success:
        pytest.skip(f"{response.error_code}, {response.error_message}", allow_module_level=True)

    if fail:
        pytest.skip(f"Something went wrong: {fail}", allow_module_level=True)


def open_platform_session(
            key=DESKTOP_APP_KEY,
            login=EDP_USERNAME, password=EDP_PASSWORD,
            deployed_platform_host=None,
            raise_fail=True
            ):
    fail = None
    platform_session = None
    try:
        platform_session = rdp.open_platform_session(
            key,
            rdp.GrantPassword(
                login,
                password
                ),
            deployed_platform_host
            )
        status = platform_session._status
    except Exception as e:
        t, v, tb = sys.exc_info()
        tb = "\n".join([f"\t\t\t\tfile {o.filename}, line {o.lineno} in {o.name}" for o in traceback.extract_tb(tb)])
        fail = (f"Exception:\n"
                f"\t\t\ttype - {t},\n"
                f"\t\t\tvalue - {v},\n"
                f'\t\t\ttraceback: \n{tb}')
        status = "no status"

    fail = fail or not platform_session.is_open()

    if fail and raise_fail:
        pytest.fail(f"Session status: {status},\n"
                    f"\tlast_status: {rdp.get_last_status()},\n"
                    f"\tlast_error: {rdp.ContentFactory._get_last_error_status()},\n"
                    f"\terror: \n\t\t{fail}")

    return platform_session


success_request_desktop_api = None


def open_desktop_session():
    global success_request_desktop_api

    if success_request_desktop_api is None:
        success_request_desktop_api = request_desktop_api()

    not success_request_desktop_api and pytest.skip("Desktop API does not response.")

    desktop_session = rdp.open_desktop_session(DESKTOP_APP_KEY)
    if not desktop_session.is_open():
        pytest.fail(str(desktop_session._status))
    return desktop_session


def request_desktop_api():
    import requests
    import time

    url = "http://localhost:9000/api/status"

    num_tries = 12
    sleep_sec = 10
    success = False

    while num_tries:

        try:
            response = requests.get(url)
            success = response.status_code == requests.codes.ok
        except requests.exceptions.ConnectionError:
            success = False

        if success:
            break

        time.sleep(sleep_sec)
        num_tries -= 1

    return success


@pytest.fixture(scope="function")
def run_mock_server():
    config = {
        'data_filename': 'mock_server_data_set.json',
        'http_scenario': 'simple_lookup',
        'ready': False,
        'error': None
        }
    t = Thread(target=mock_server.run, args=("127.0.0.1", 9001, config))
    t.start()

    while not config['ready'] and not config['error']:
        time.sleep(0.001)

    if config['error']:
        pytest.fail(str(config['error']))

    yield mock_server
    mock_server.stop()


@pytest.fixture(scope="function")
def run_mock_server_and_open_session(run_mock_server):
    run_mock_server.set_scenario("streaming_chain")

    params = rdp.PlatformSession.Params().app_key("234").deployed_platform_host("127.0.0.1:9001")
    session = rdp.CoreFactory.create_session(params)
    session.open()
    yield session
    session.close()


def patch_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.get_event_loop()
    asyncio.set_event_loop(loop)
    loop._close = loop.close
    loop.close = lambda: None


@pytest.fixture(scope="function", params=[open_platform_session, open_desktop_session])
# @pytest.fixture(scope="function", params=[open_platform_session])
def open_session(request):
    patch_loop()
    open_session = request.param
    session = open_session()
    yield session
    session.close()


@pytest.fixture(scope="function")
def open_session_for_ipa():
    session = open_platform_session(
        login="Artem.Kharchyshyn@refinitiv.com",
        password="w1nS9pnCKSFS",
        )
    yield session
    session.close()


@pytest.fixture(scope="function")
def open_deployed_session():
    session = open_platform_session(
        "256",
        deployed_platform_host="10.3.177.158:15000"  # "10.67.4.28:15000"
        )
    yield session
    session.close()


@pytest.fixture(scope="function")
def open_prod_session(monkeypatch):
    monkeypatch.setenv(configure._RDPLIB_ENV, 'prod')
    reload(configure)
    session = open_platform_session()
    yield session
    session.close()


@pytest.fixture(scope="function")
def open_beta_session(monkeypatch):
    monkeypatch.setenv(configure._RDPLIB_ENV, 'beta')
    reload(configure)
    session = open_platform_session()
    yield session
    session.close()


@pytest.fixture(scope="function")
def open_mock_session():
    with patch('requests_async.sessions.Session') as mock_session:
        MockSession.response = MockAuthResponse()
        mock_session.return_value = MockSession()
        session = open_platform_session()
    yield session
    session.close()


def pytest_addoption(parser):
    parser.addoption("--unit", action="store_true", default=False, help="run unit tests")
    parser.addoption("--integrate", action="store_true", default=False, help="run integration tests")


def pytest_configure(config):
    config.addinivalue_line("markers", "unit: mark test as unit test")
    config.addinivalue_line("markers", "integrate: mark test as integration test")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--unit"):
        skip = pytest.mark.skip(reason="run only unit tests")
        for item in items:
            if "unit" not in item.keywords:
                item.add_marker(skip)

    if config.getoption("--integrate"):
        skip = pytest.mark.skip(reason="run only integration tests")
        for item in items:
            if "integrate" not in item.keywords:
                item.add_marker(skip)


USER_CONFIG_PATH = os.path.join(os.path.expanduser('~'), configure._config_filename)
PROJECT_CONFIG_PATH = os.path.join(os.getcwd(), configure._config_filename)


def remove_user_config():
    remove_config(USER_CONFIG_PATH)


def remove_project_config():
    remove_config(PROJECT_CONFIG_PATH)


def remove_config(path):
    while os.path.exists(path):
        try:
            os.remove(path)
            import time
            time.sleep(1)
        except (PermissionError, FileNotFoundError):
            pass


def pytest_runtest_teardown(item, nextitem):
    configure.unload()


@pytest.fixture()
def user_config_path():
    return USER_CONFIG_PATH


@pytest.fixture()
def project_config_path():
    return PROJECT_CONFIG_PATH


@pytest.fixture(scope="function")
def write_user_config(user_config_path):
    def inner(s):
        if isinstance(s, dict):
            s = json.dumps(s)
        f = open(user_config_path, 'w')
        f.write(s)
        f.close()
        return user_config_path

    yield inner

    configure.unload()

    remove_user_config()


@pytest.fixture(scope="function")
def write_project_config(project_config_path):
    def inner(arg):
        if isinstance(arg, dict):
            arg = json.dumps(arg)
        f = open(project_config_path, 'w')
        f.write(arg)
        f.close()
        return project_config_path

    yield inner

    configure.unload()

    remove_project_config()


@pytest.fixture(scope="module", params=["13063CUV0", "US10YT=RR"])
def universe(request):
    return request.param


@pytest.fixture(scope="module", params=[
    pytest.param(["US1YT=RR", "US5YT=RR", "US10YT=RR"]),
    pytest.param(["13063CUV0", "US10YT=RR"]),
    pytest.param(["13063CUV0"])
    ])
def many_universes(request):
    return request.param


@pytest.fixture(scope="module", params=[t.value for t in Frequency])
def frequency(request):
    return request.param


def get_property_names(cls):
    return [p for p in dir(cls) if isinstance(getattr(cls, p), property)]


def has_property_names_in_class(cls, expected_property_names):
    if isinstance(expected_property_names, dict):
        expected_property_names = list(expected_property_names.keys())
    return set(get_property_names(cls)) == set(expected_property_names)


@pytest.fixture(scope="module", params=[15, 350])
def count(request):
    return request.param


@pytest.fixture(scope="module", params=[rdp.SortOrder.old_to_new, rdp.SortOrder.new_to_old])
def sort_order(request):
    return request.param


@pytest.fixture(scope="module", params=['USA daterange:"2019-06-01,2019-06-07"'])
def query_with_daterange(request):
    return request.param


@pytest.fixture(scope="module",
                params=['R:USA.O', 'R:USA.L', 'USA daterange:"2019-06-01,2019-06-07"', 'USA last 5 days'])
def query(request):
    return request.param


@pytest.fixture(scope="module", params=['urn:newsml:reuters.com:20190531:nL2N237053:2'])
def story_id(request):
    return request.param
