import pytest

from refinitiv.dataplatform import ipa
from refinitiv.dataplatform.content.ipa.contracts.swaption import *

import refinitiv.dataplatform.content.ipa.contracts.swaption as swaption

import refinitiv.dataplatform as rdp


def test_rdp_level_scope_ok():
    assert rdp.get_swaption_analytics


def test_ipa_level_scope_fail():
    with pytest.raises(AttributeError):
        assert ipa.get_swaption_analytics


def test_module_level_scope():
    assert Definition
    assert CalculationParams


def test_module_level_scope_swaption():
    assert swaption.Definition
    assert swaption.CalculationParams

    with pytest.raises(AttributeError):
        _ = swaption._swaption_definition

    with pytest.raises(AttributeError):
        _ = swaption._swaption_pricing_parameters


def test_basic_level_scope_ipa():
    with pytest.raises(AttributeError):
        _ = ipa.get_swaption_analytics_async

    with pytest.raises(AttributeError):
        _ = ipa.Definition

    with pytest.raises(AttributeError):
        _ = ipa.CalculationParams

    with pytest.raises(AttributeError):
        _ = ipa._functions


def test_module_level_scope_ipa():
    assert ipa.swaption.Definition
    assert ipa.swaption.CalculationParams

    with pytest.raises(AttributeError):
        _ = ipa.contracts.swaption.Definition

    with pytest.raises(AttributeError):
        _ = ipa.contracts.swaption.CalculationParams

    with pytest.raises(AttributeError):
        _ = ipa.contracts.Definition

    with pytest.raises(AttributeError):
        _ = ipa.contracts.CalculationParams


def test_object_level_scope_ipa():
    assert ipa.FinancialContracts
    assert ipa.FinancialContracts.get_swaption_analytics
    assert ipa.FinancialContracts.get_swaption_analytics_async
