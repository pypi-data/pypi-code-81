import asyncio

import pytest

import refinitiv.dataplatform as rdp
import response_tests


@pytest.mark.integrate
@pytest.mark.asyncio
async def test_universe(open_session):
    response = await rdp.ESG.get_universe_async()
    response_tests.success_response_tests(response)


@pytest.mark.integrate
@pytest.mark.asyncio
async def test_basic_overview(open_session):
    response = await rdp.ESG.get_basic_overview_async(
        universe='IBM.N'
    )
    response_tests.success_response_tests(response)


@pytest.mark.integrate
@pytest.mark.asyncio
async def test_standard_scores(open_session):
    response = await rdp.ESG.get_standard_scores_async(
        universe='5000002406',
        start=0,
        end=-2
    )
    response_tests.success_response_tests(response)


@pytest.mark.integrate
@pytest.mark.asyncio
async def test_full_scores(open_session):
    response = await rdp.ESG.get_full_scores_async(
        universe='4295904307',
        start=0,
        end=-5
    )
    response_tests.success_response_tests(response)


@pytest.mark.integrate
@pytest.mark.asyncio
async def test_standard_measures(open_session):
    response = await rdp.ESG.get_standard_measures_async(
        session=open_session,
        universe='BNPP.PA',
        start=0,
        end=-2
    )
    response_tests.success_response_tests(response)


@pytest.mark.integrate
@pytest.mark.asyncio
async def test_full_measures(open_session):
    response = await rdp.ESG.get_full_measures_async(
        universe='BNPP.PA',
        start=0,
        end=-3
    )
    response_tests.success_response_tests(response)


@pytest.mark.integrate
@pytest.mark.asyncio
async def test_measures_and_scores(open_session):
    overview_res, std_scores_res, full_scores_res, std_measures_res, full_measures_res = await asyncio.gather(
        rdp.ESG.get_basic_overview_async(
            universe='IBM.N'
        ),
        rdp.ESG.get_standard_scores_async(
            universe='5000002406',
            start=0,
            end=-2
        ),
        rdp.ESG.get_full_scores_async(
            universe='4295904307',
            start=0,
            end=-5
        ),
        rdp.ESG.get_standard_measures_async(
            session=open_session,
            universe='BNPP.PA',
            start=0,
            end=-2
        ),
        rdp.ESG.get_full_measures_async(
            universe='BNPP.PA',
            start=0,
            end=-3
        )
    )
    response_tests.success_response_tests(overview_res)
    response_tests.success_response_tests(std_scores_res)
    response_tests.success_response_tests(full_scores_res)
    response_tests.success_response_tests(std_measures_res)
    response_tests.success_response_tests(full_measures_res)


@pytest.mark.integrate
@pytest.mark.asyncio
async def test_universe_one(open_session):
    response, *_ = await asyncio.gather(
        rdp.ESG.get_universe_async()
    )
    response_tests.success_response_tests(response)
