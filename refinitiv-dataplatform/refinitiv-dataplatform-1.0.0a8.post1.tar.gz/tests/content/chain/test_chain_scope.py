import refinitiv.dataplatform as rdp


def test_scope():
    assert rdp.get_chain is not None
