from unittest import mock
import pytest
import refinitiv.dataplatform as rdp
import conftest
import response_tests
import asyncio


@pytest.fixture
def open_session():
    session = conftest.open_platform_session()
    yield
    session.close()


def test_import_basic_overview():
    try:
        from refinitiv.dataplatform.content.esg import basic_overview
    except ImportError:
        assert False


def test_has_attributes(open_session):
    definition = rdp.esg.basic_overview.Definition('')
    assert hasattr(definition, 'closure')
    assert hasattr(definition, 'get_data')


def test_get_data_with_session_argument(open_session):
    definition = rdp.esg.basic_overview.Definition('')

    with mock.patch('refinitiv.dataplatform.content.ESG._get_data') as universe_mock:
        response = definition.get_data(session=open_session)
        assert universe_mock.call_count == 1


def test_get_data_without_session_argument(open_session):
    definition = rdp.esg.basic_overview.Definition('')

    with mock.patch('refinitiv.dataplatform.content.ESG._get_data') as universe_mock:
        response = definition.get_data()
        assert universe_mock.call_count == 1


def test_get_data_async(open_session):
    async def get_data():
        definition = rdp.esg.basic_overview.Definition('IBM.N')
        response = await definition.get_data_async()
        response_tests.success_response_tests(response)

    asyncio.get_event_loop().run_until_complete(get_data())
