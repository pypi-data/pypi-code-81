import pytest

import refinitiv.dataplatform as rdp
import response_tests


@pytest.mark.integrate
def test_basic_overview(open_session):
    response = rdp.ESG.get_basic_overview(
        universe='IBM111.N'
    )
    response_tests.not_success_response_tests(response, check_status=False)
    assert response.error_code
    assert response.error_message


@pytest.mark.integrate
def test_standard_scores(open_session):
    response = rdp.ESG.get_standard_scores(
        universe='5000002406',
        start=-3,
        end=-1
    )
    response_tests.not_success_response_tests(response, check_status=False)
    assert response.error_code
    assert response.error_message


@pytest.mark.integrate
def test_full_scores(open_session):
    response = rdp.ESG.get_full_scores(
        universe='5000002406',
        start=-21,
        end=0
    )
    response_tests.not_success_response_tests(response, check_status=False)
    assert response.error_code
    assert response.error_message
