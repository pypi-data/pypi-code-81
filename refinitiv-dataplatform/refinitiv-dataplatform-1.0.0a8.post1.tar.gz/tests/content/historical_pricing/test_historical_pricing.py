def test_import_historical_pricing():
    try:
        from refinitiv.dataplatform import historical_pricing
    except ImportError:
        assert False


def test_not_exists_attributes():
    import refinitiv.dataplatform as rdp
    assert not hasattr(rdp, 'events')
    assert not hasattr(rdp, 'summaries')


def test_exists_events_and_summaries_attributes():
    from refinitiv.dataplatform import historical_pricing
    assert hasattr(historical_pricing, 'events')
    assert hasattr(historical_pricing, 'summaries')


def test_import_historical_pricing_events():
    try:
        from refinitiv.dataplatform.content.historical_pricing import events
    except ImportError:
        assert False


def test_import_historical_pricing_summaries():
    try:
        from refinitiv.dataplatform.content.historical_pricing import summaries
    except ImportError:
        assert False
