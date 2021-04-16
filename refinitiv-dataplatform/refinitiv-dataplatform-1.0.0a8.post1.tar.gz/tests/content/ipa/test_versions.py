import refinitiv.dataplatform as rdp


def test_contracts_version():
    assert rdp.__version__ == '1.0.0a7'
    assert rdp.ipa.contracts.__version__ == '1.0.60'


def test_curves_surfaces_version():
    assert rdp.__version__ == '1.0.0a7'
    assert rdp.ipa.curve.__version__ == '1.0.41'
    assert rdp.ipa.surface.__version__ == '1.0.41'
