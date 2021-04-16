import pytest

from refinitiv.dataplatform.content import ipa


def test_basic_level_scope_fail():
    with pytest.raises(AttributeError):
        _ = ipa.get_instrument_analytics
    with pytest.raises(AttributeError):
        _ = ipa.get_instrument_analytics_async


def test_module_level_scope_fail():
    with pytest.raises(AttributeError):
        _ = ipa.financial_contracts
    with pytest.raises(AttributeError):
        _ = ipa.financial_contracts.FinancialContracts.get_instrument_analytics
    with pytest.raises(AttributeError):
        _ = ipa.financial_contracts.FinancialContracts.get_instrument_analytics_async
    with pytest.raises(AttributeError):
        _ = ipa.financial_contracts.get_instrument_analytics
    with pytest.raises(AttributeError):
        _ = ipa.financial_contracts.get_instrument_analytics_async


def test_object_level_scope_ok():
    assert ipa.FinancialContracts.get_instrument_analytics
    assert ipa.FinancialContracts.get_instrument_analytics_async
