import pytest

from refinitiv.dataplatform.content import ipa


def test_surface_output():
    with pytest.raises(AttributeError):
        _ = ipa.SurfaceOutput

    assert ipa.surface.SurfaceOutput


def test_fx_surface_scope():
    with pytest.raises(AttributeError):
        _ = ipa.Definition
    with pytest.raises(AttributeError):
        _ = ipa.CalculationParams

    with pytest.raises(AttributeError):
        _ = ipa.surface.Definition
    with pytest.raises(AttributeError):
        _ = ipa.surface.CalculationParams

    assert ipa.surface.fx.Definition
    assert ipa.surface.fx.CalculationParams


def test_eti_surface_scope():
    with pytest.raises(AttributeError):
        _ = ipa.Definition
    with pytest.raises(AttributeError):
        _ = ipa.CalculationParams

    with pytest.raises(AttributeError):
        _ = ipa.surface.Definition
    with pytest.raises(AttributeError):
        _ = ipa.surface.CalculationParams

    assert ipa.surface.eti.Definition
    assert ipa.surface.eti.CalculationParams


def test_ir_surface_scope():
    with pytest.raises(AttributeError):
        _ = ipa.Definition
    with pytest.raises(AttributeError):
        _ = ipa.CalculationParams

    with pytest.raises(AttributeError):
        _ = ipa.surface.Definition
    with pytest.raises(AttributeError):
        _ = ipa.surface.CalculationParams

    assert ipa.surface.ir.Definition
    assert ipa.surface.ir.CalculationParams
