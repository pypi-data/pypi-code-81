from unittest import mock
import response_tests
import asyncio
import refinitiv.dataplatform as rdp
import conftest
import pytest


@pytest.fixture
def open_session():
    session = conftest.open_platform_session()
    yield
    session.close()


def test_get_data(open_session):
    with mock.patch('refinitiv.dataplatform.content.HistoricalPricing._get_events') as hp_mock:
        with mock.patch('refinitiv.dataplatform.legacy.tools.get_default_session') as m:
            rdp.historical_pricing.events.Definition('').get_data()
            assert hp_mock.call_count == 1

    with mock.patch('refinitiv.dataplatform.content.HistoricalPricing._get_events') as hp_mock:
        rdp.historical_pricing.events.Definition('').get_data(session=open_session)
        assert hp_mock.call_count == 1


def test_get_data_async(open_session):
    async def get_async():
        definition = rdp.historical_pricing.events.Definition('VOD.L')
        response = await definition.get_data_async()
        response_tests.success_response_tests(response)
    asyncio.get_event_loop().run_until_complete(get_async())
