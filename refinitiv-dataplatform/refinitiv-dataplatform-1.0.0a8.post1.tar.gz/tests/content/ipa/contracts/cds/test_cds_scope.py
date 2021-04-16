import pytest

from refinitiv.dataplatform.content import ipa
import refinitiv.dataplatform as rdp


def test_rdp_level_scope_ok():
    assert rdp.get_cds_analytics


def test_ipa_level_scope_fail():
    with pytest.raises(AttributeError):
        assert ipa.get_cds_analytics


def test_module_level_scope_ok():
    assert ipa.cds.Definition


def test_object_level_scope_ok():
    assert ipa.FinancialContracts.get_cds_analytics
    assert ipa.FinancialContracts.get_cds_analytics_async


def test_basic_level_scope_fail():
    with pytest.raises(AttributeError):
        _ = ipa.Definition


def test_definition():
    with pytest.raises(AttributeError):
        ipa.cds._cds_definition


def test_leg_definition():
    with pytest.raises(AttributeError):
        ipa.cds._premium_leg_definition

    with pytest.raises(AttributeError):
        ipa.cds._protection_leg_definition


def test_pricing_parameters():
    with pytest.raises(AttributeError):
        ipa.cds._cds_pricing_parameters


def test_leg_level():
    assert ipa.cds.ProtectionLegDefinition
    assert ipa.cds.PremiumLegDefinition
