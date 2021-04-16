import pytest

from refinitiv.dataplatform.content import ipa
import refinitiv.dataplatform as rdp


def test_rdp_level_scope_ok():
    assert rdp.get_option_analytics


def test_ipa_level_scope_fail():
    with pytest.raises(AttributeError):
        assert ipa.get_option_analytics


def test_module_level_scope_ok():
    assert ipa.option.Definition


def test_object_level_scope_ok():
    assert ipa.FinancialContracts.get_option_analytics
    assert ipa.FinancialContracts.get_option_analytics_async


def test_basic_level_scope_fail():
    with pytest.raises(AttributeError):
        _ = ipa.Definition


def test_definition():
    with pytest.raises(AttributeError):
        ipa.option._option_definition


def test_leg_definition():
    with pytest.raises(AttributeError):
        ipa.option._option_leg_definition


def test_pricing_parameters():
    with pytest.raises(AttributeError):
        ipa.option._option_pricing_parameters
