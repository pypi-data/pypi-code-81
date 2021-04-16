import pytest

import refinitiv.dataplatform as rdp
import conftest
import response_tests


@pytest.mark.unit
def test_create_obj_with_invalid_session():
    with pytest.raises(AttributeError):
        inst = rdp.ESG({})
        inst._get_universe()


@pytest.mark.integrate
def test_create_obj_with_correct_session():
    platform_session = conftest.open_platform_session()
    inst = rdp.ESG(platform_session)

    assert inst

    platform_session.close()


@pytest.mark.integrate
def test_pass_session():
    params = {
        "app_key": conftest.DESKTOP_APP_KEY,
        "oauth_grant_type": rdp.GrantPassword(
            username=conftest.EDP_USERNAME,
            password=conftest.EDP_PASSWORD
        ),
        "take_signon_control": True
    }
    platform_session = rdp.CoreFactory.create_platform_session(**params)
    platform_session = platform_session
    platform_session.open()

    response = rdp.ESG.get_basic_overview(
        universe="AAPL.O",
        session=platform_session
    )

    response_tests.success_response_tests(response)
