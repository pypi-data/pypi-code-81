import pytest

from refinitiv.dataplatform.content import ipa
import refinitiv.dataplatform as rdp


def test_rdp_level_scope_ok():
    assert rdp.get_swap_analytics


def test_ipa_level_scope_fail():
    with pytest.raises(AttributeError):
        assert ipa.get_swap_analytics


def test_module_level_scope_ok():
    assert ipa.swap.Definition


def test_object_level_scope_ok():
    assert ipa.FinancialContracts.get_swap_analytics
    assert ipa.FinancialContracts.get_swap_analytics_async


def test_basic_level_scope_fail():
    with pytest.raises(AttributeError):
        _ = ipa.Definition


def test_definition():
    with pytest.raises(AttributeError):
        ipa.swap._swap_definition


def test_leg_definition():
    with pytest.raises(AttributeError):
        ipa.swap._swap_leg_definition


def test_pricing_parameters():
    with pytest.raises(AttributeError):
        ipa.swap._swap_pricing_parameters


def test_leg_level():
    assert ipa.swap.LegDefinition
