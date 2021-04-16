import asyncio

import pytest

import refinitiv.dataplatform as rdp
import response_tests


@pytest.mark.integrate
def test_get_universe(open_session):
    try:
        rdp.ESG.get_universe(session=open_session)
    except Exception as exc:
        print(exc)
        assert False

    assert True


@pytest.mark.integrate
def test_on_response_callback(open_session):
    async def on_response_callback():
        fut = asyncio.Future()

        def on_response(_, response):
            response_tests.success_response_tests(response=response)
            fut.set_result(1)

        rdp.ESG.get_universe(session=open_session,
                             on_response=on_response)
        return await fut

    asyncio.get_event_loop().run_until_complete(on_response_callback())
