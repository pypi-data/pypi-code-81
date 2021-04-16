import pytest

from refinitiv.dataplatform import ipa
from refinitiv.dataplatform.content.ipa.contracts.bond import *

import refinitiv.dataplatform.content.ipa.contracts.bond as bond
import refinitiv.dataplatform as rdp


def test_rdp_level_scope_ok():
    assert rdp.get_bond_analytics


def test_ipa_level_scope_fail():
    with pytest.raises(AttributeError):
        assert ipa.get_bond_analytics


def test_module_level_scope():
    assert Definition
    assert CalculationParams


def test_module_level_scope_bond():
    assert bond.Definition
    assert bond.CalculationParams

    with pytest.raises(AttributeError):
        _ = bond._bond_definition

    with pytest.raises(AttributeError):
        _ = bond._bond_pricing_parameters


def test_basic_level_scope_ipa():
    with pytest.raises(AttributeError):
        _ = ipa.get_bond_analytics_async

    with pytest.raises(AttributeError):
        _ = ipa.Definition

    with pytest.raises(AttributeError):
        _ = ipa.CalculationParams

    with pytest.raises(AttributeError):
        _ = ipa._functions


def test_module_level_scope_ipa():
    assert ipa.bond.Definition
    assert ipa.bond.CalculationParams

    with pytest.raises(AttributeError):
        _ = ipa.contracts.bond.Definition

    with pytest.raises(AttributeError):
        _ = ipa.contracts.bond.CalculationParams

    with pytest.raises(AttributeError):
        _ = ipa.contracts.Definition

    with pytest.raises(AttributeError):
        _ = ipa.contracts.CalculationParams


def test_object_level_scope_ipa():
    assert ipa.FinancialContracts
    assert ipa.FinancialContracts.get_bond_analytics
    assert ipa.FinancialContracts.get_bond_analytics_async
