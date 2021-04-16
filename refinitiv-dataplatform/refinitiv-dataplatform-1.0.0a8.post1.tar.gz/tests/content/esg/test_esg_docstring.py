import refinitiv.dataplatform as rdp


def test__doc__():
    assert rdp.get_esg_basic_overview.__doc__
    assert rdp.get_esg_full_measures.__doc__
    assert rdp.get_esg_full_scores.__doc__
    assert rdp.get_esg_standard_measures.__doc__
    assert rdp.get_esg_standard_scores.__doc__
    assert rdp.get_esg_universe.__doc__
