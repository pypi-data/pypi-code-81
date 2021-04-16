import pytest

from refinitiv.dataplatform import ipa
from refinitiv.dataplatform.content.ipa.contracts.capfloor import *

import refinitiv.dataplatform.content.ipa.contracts.capfloor as capfloor
import refinitiv.dataplatform as rdp


def test_rdp_level_scope_ok():
    assert rdp.get_capfloor_analytics


def test_ipa_level_scope_fail():
    with pytest.raises(AttributeError):
        assert ipa.get_capfloor_analytics


def test_module_level_scope():
    assert Definition
    assert CalculationParams


def test_module_level_scope_capfloor():
    assert capfloor.Definition
    assert capfloor.CalculationParams

    with pytest.raises(AttributeError):
        _ = capfloor._capfloor_definition

    with pytest.raises(AttributeError):
        _ = capfloor._capfloor_pricing_parameters


def test_basic_level_scope_ipa():
    with pytest.raises(AttributeError):
        _ = ipa.get_capfloor_analytics_async

    with pytest.raises(AttributeError):
        _ = ipa.Definition

    with pytest.raises(AttributeError):
        _ = ipa.CalculationParams

    with pytest.raises(AttributeError):
        _ = ipa._functions


def test_module_level_scope_ipa():
    assert ipa.capfloor.Definition
    assert ipa.capfloor.CalculationParams

    with pytest.raises(AttributeError):
        _ = ipa.contracts.capfloor.Definition

    with pytest.raises(AttributeError):
        _ = ipa.contracts.capfloor.CalculationParams

    with pytest.raises(AttributeError):
        _ = ipa.contracts.Definition

    with pytest.raises(AttributeError):
        _ = ipa.contracts.CalculationParams


def test_object_level_scope_ipa():
    assert ipa.FinancialContracts
    assert ipa.FinancialContracts.get_capfloor_analytics
    assert ipa.FinancialContracts.get_capfloor_analytics_async
