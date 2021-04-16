import pytest

from refinitiv.dataplatform import ipa
from refinitiv.dataplatform.content.ipa.contracts.term_deposit import *

import refinitiv.dataplatform.content.ipa.contracts.term_deposit as term_deposit

import refinitiv.dataplatform as rdp


def test_rdp_level_scope_ok():
    assert rdp.get_term_deposit_analytics


def test_ipa_level_scope_fail():
    with pytest.raises(AttributeError):
        assert ipa.get_term_deposit_analytics


def test_module_level_scope():
    assert Definition
    assert CalculationParams


def test_module_level_scope_term_deposit():
    assert term_deposit.Definition
    assert term_deposit.CalculationParams

    with pytest.raises(AttributeError):
        _ = term_deposit._term_deposit_definition

    with pytest.raises(AttributeError):
        _ = term_deposit._term_deposit_pricing_parameters


def test_basic_level_scope_ipa():
    with pytest.raises(AttributeError):
        _ = ipa.get_term_deposit_analytics_async

    with pytest.raises(AttributeError):
        _ = ipa.Definition

    with pytest.raises(AttributeError):
        _ = ipa.CalculationParams

    with pytest.raises(AttributeError):
        _ = ipa._functions


def test_module_level_scope_ipa():
    assert ipa.term_deposit.Definition
    assert ipa.term_deposit.CalculationParams

    with pytest.raises(AttributeError):
        _ = ipa.contracts.term_deposit.Definition

    with pytest.raises(AttributeError):
        _ = ipa.contracts.term_deposit.CalculationParams

    with pytest.raises(AttributeError):
        _ = ipa.contracts.Definition

    with pytest.raises(AttributeError):
        _ = ipa.contracts.CalculationParams


def test_object_level_scope_ipa():
    assert ipa.FinancialContracts
    assert ipa.FinancialContracts.get_term_deposit_analytics
    assert ipa.FinancialContracts.get_term_deposit_analytics_async
