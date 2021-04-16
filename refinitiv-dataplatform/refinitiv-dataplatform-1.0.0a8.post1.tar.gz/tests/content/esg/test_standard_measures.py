from unittest import mock
import pytest
import conftest
from refinitiv.dataplatform.content.esg.data_type import DataType
import response_tests
import refinitiv.dataplatform as rdp
import asyncio


@pytest.fixture
def open_session():
    session = conftest.open_platform_session()
    yield
    session.close()


def test_import_standard_measures():
    try:
        from refinitiv.dataplatform.content.esg import standard_measures
    except ImportError:
        assert False


def test_has_attributes(open_session):
    definition = rdp.esg.standard_measures.Definition('', session=open_session)
    assert hasattr(definition, 'universe')
    assert hasattr(definition, 'start')
    assert hasattr(definition, 'end')
    assert hasattr(definition, 'closure')
    assert hasattr(definition, 'get_data')
    # assert definition._Definition__data_type == DataType.StandardMeasures


def test_get_data_with_session_argument(open_session):
    definition = rdp.esg.standard_measures.Definition('', session=open_session)

    with mock.patch('refinitiv.dataplatform.content.ESG._get_data') as universe_mock:
        response = definition.get_data()
        assert universe_mock.call_count == 1


def test_get_data_without_session_argument(open_session):
    definition = rdp.esg.standard_measures.Definition('')

    with mock.patch('refinitiv.dataplatform.content.ESG._get_data') as universe_mock:
        response = definition.get_data()
        assert universe_mock.call_count == 1


def test_get_data_async(open_session):
    async def get_data():
        definition = rdp.esg.standard_measures.Definition(
            universe='BNPP.PA',
            start=0,
            end=-2
        )
        response = await definition.get_data_async()
        response_tests.success_response_tests(response)
    asyncio.get_event_loop().run_until_complete(get_data())
