import pytest

import refinitiv.dataplatform as rdp
import response_tests


@pytest.mark.integrate
def test_universe(open_session):
    response = rdp.ESG.get_universe()
    response_tests.success_response_tests(response)


@pytest.mark.integrate
def test_basic_overview(open_session):
    response = rdp.ESG.get_basic_overview(
        universe='IBM.N'
    )
    response_tests.success_response_tests(response)


@pytest.mark.integrate
def test_standard_scores(open_session):
    response = rdp.ESG.get_standard_scores(
        universe='5000002406',
        start=0,
        end=-2)
    response_tests.success_response_tests(response)


@pytest.mark.integrate
def test_full_scores(open_session):
    response = rdp.ESG.get_full_scores(
        universe='4295904307',
        start=0,
        end=-5)
    response_tests.success_response_tests(response)


@pytest.mark.integrate
def test_standard_measures(open_session):
    response = rdp.ESG.get_standard_measures(
        session=open_session,
        universe='BNPP.PA',
        start=0,
        end=-2)
    response_tests.success_response_tests(response)


@pytest.mark.integrate
def test_full_measures(open_session):
    response = rdp.ESG.get_full_measures(
        universe='BNPP.PA',
        start=0,
        end=-3)
    response_tests.success_response_tests(response)
