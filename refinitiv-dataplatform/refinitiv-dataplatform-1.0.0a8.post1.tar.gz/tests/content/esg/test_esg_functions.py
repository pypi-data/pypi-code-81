import pytest

import refinitiv.dataplatform as rdp


@pytest.mark.integrate
def test_universe(open_session):
    df = rdp.get_esg_universe()
    assert df is not None, rdp.ContentFactory._last_error_status
    assert not df.empty


@pytest.mark.integrate
def test_basic_overview(open_session):
    df = rdp.get_esg_basic_overview(
        universe='IBM.N'
    )
    assert df is not None, rdp.ContentFactory._last_error_status
    assert not df.empty


@pytest.mark.integrate
def test_standard_scores(open_session):
    df = rdp.get_esg_standard_scores(
        universe='5000002406',
        start=0,
        end=-2)
    assert df is not None, rdp.ContentFactory._last_error_status
    assert not df.empty


@pytest.mark.integrate
def test_standard_scores_0_5(open_session):
    df = rdp.get_esg_standard_scores(
        universe='4295904307',
        start=0,
        end=-5
    )
    assert df is None


@pytest.mark.integrate
def test_full_scores(open_session):
    df = rdp.get_esg_full_scores(
        universe='4295904307',
        start=-5,
        end=0)
    assert df is not None, rdp.ContentFactory._last_error_status
    assert not df.empty


@pytest.mark.integrate
def test_standard_measures(open_session):
    df = rdp.get_esg_standard_measures(
        universe='BNPP.PA',
        start=0,
        end=-2)
    assert df is not None, rdp.ContentFactory._last_error_status
    assert not df.empty


@pytest.mark.integrate
def test_full_measures(open_session):
    df = rdp.get_esg_full_measures(
        universe='BNPP.PA',
        start=0,
        end=-3)
    assert df is not None, rdp.ContentFactory._last_error_status
    assert not df.empty
