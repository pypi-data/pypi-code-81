import refinitiv.dataplatform as rdp


def test__doc__():
    assert rdp.get_bond_analytics.__doc__
    assert rdp.get_capfloor_analytics.__doc__
    assert rdp.get_cds_analytics.__doc__
    assert rdp.get_cross_analytics.__doc__
    assert rdp.get_option_analytics.__doc__
    assert rdp.get_repo_analytics.__doc__
    assert rdp.get_swap_analytics.__doc__
    assert rdp.get_swaption_analytics.__doc__
    assert rdp.get_term_deposit_analytics.__doc__
