import asyncio
import datetime

import pytest

import refinitiv.dataplatform as rdp
import response_tests


def display_response(response):
    data_name = response.closure
    current_time = datetime.datetime.now().time()
    print('{} received at {}'.format(data_name, current_time))
    print(response.data.df)


def on_response(fut, closure):
    def wrapper(_, response):
        display_response(response)
        response_tests.success_response_tests(response, closure)
        fut.set_result(1)

    return wrapper


@pytest.mark.integrate
def test_universe(open_session):
    async def get_universe():
        fut = asyncio.Future()
        closure = "Universe"
        await asyncio.get_event_loop().create_task(
            rdp.ESG.get_universe_async(
                closure=closure,
                on_response=on_response(fut, closure)
            )
        )
        return await fut

    asyncio.get_event_loop().run_until_complete(get_universe())


@pytest.mark.integrate
def test_basic_overview(open_session):
    async def get_basic_overview():
        fut = asyncio.Future()
        closure = "BasicOverview"
        await asyncio.get_event_loop().create_task(
            rdp.ESG.get_basic_overview_async(
                universe='IBM.N',
                closure=closure,
                on_response=on_response(fut, closure)
            )
        )
        return await fut

    asyncio.get_event_loop().run_until_complete(get_basic_overview())


@pytest.mark.integrate
def test_standard_scores(open_session):
    async def get_standard_scores():
        fut = asyncio.Future()
        closure = "StandardScores"
        await asyncio.get_event_loop().create_task(
            rdp.ESG.get_standard_scores_async(
                universe='5000002406',
                start=0,
                end=-2,
                closure=closure,
                on_response=on_response(fut, closure)
            )
        )
        return await fut

    asyncio.get_event_loop().run_until_complete(get_standard_scores())


@pytest.mark.integrate
def test_full_scores(open_session):
    async def get_full_scores():
        fut = asyncio.Future()
        closure = "FullScores"
        await asyncio.get_event_loop().create_task(
            rdp.ESG.get_full_scores_async(
                universe='4295904307',
                start=0,
                end=-5,
                closure=closure,
                on_response=on_response(fut, closure)
            )
        )
        return await fut

    asyncio.get_event_loop().run_until_complete(get_full_scores())


@pytest.mark.integrate
def test_standard_measures(open_session):
    async def get_standard_measures():
        fut = asyncio.Future()
        closure = "StandardMeasures"
        await asyncio.get_event_loop().create_task(
            rdp.ESG.get_standard_measures_async(
                session=open_session,
                universe='BNPP.PA',
                start=0,
                end=-2,
                closure=closure,
                on_response=on_response(fut, closure)
            )
        )
        return await fut

    asyncio.get_event_loop().run_until_complete(get_standard_measures())


@pytest.mark.integrate
def test_full_measures(open_session):
    async def get_full_measures():
        fut = asyncio.Future()
        closure = "FullMeasures"
        await asyncio.get_event_loop().create_task(
            rdp.ESG.get_full_measures_async(
                universe='BNPP.PA',
                start=0,
                end=-3,
                closure=closure,
                on_response=on_response(fut, closure)
            )
        )
        return await fut

    asyncio.get_event_loop().run_until_complete(get_full_measures())
