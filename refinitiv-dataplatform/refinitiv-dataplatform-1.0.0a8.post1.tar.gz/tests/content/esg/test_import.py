def test_import_esg():
    try:
        from refinitiv.dataplatform import esg
    except ImportError:
        assert False


def test_not_exists_attributes():
    import refinitiv.dataplatform as rdp
    assert not hasattr(rdp, 'basic_overview')
    assert not hasattr(rdp, 'standard_measures')
    assert not hasattr(rdp, 'full_measures')
    assert not hasattr(rdp, 'standard_scores')
    assert not hasattr(rdp, 'full_scores')
    assert not hasattr(rdp, 'universe')


def test_exists_events_and_summaries_attributes():
    from refinitiv.dataplatform import esg
    assert hasattr(esg, 'basic_overview')
    assert hasattr(esg, 'standard_measures')
    assert hasattr(esg, 'full_measures')
    assert hasattr(esg, 'standard_scores')
    assert hasattr(esg, 'full_scores')
    assert hasattr(esg, 'universe')
