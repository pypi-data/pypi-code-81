import pytest

import refinitiv.dataplatform as rdp


@pytest.mark.asyncio
@pytest.mark.integrate
async def test_all_params_async(open_session):
    streaming_prices = rdp.pricing.StreamingPrices(
        universe=["EUR="],
        fields=['BID', 'ASK', 'VOLUME', 'OPEN_PRC'],
        service="IDN_RDF",
        on_complete=lambda st: print(f"Complete: {st}"),
        on_refresh=lambda st, data: print(f"Refresh: {data}"),
        on_status=lambda st, ric, status: print(f"Status[{ric}] : {status}"),
        on_update=lambda st, ric, update: print(f"Update[{ric}] : {update}")
        )
    state = await streaming_prices.open_async()
    assert state is rdp.StreamState.Open
    streaming_prices.close()


@pytest.mark.integrate
def test_all_params_sync(open_session):
    streaming_prices = rdp.pricing.StreamingPrices(
        universe=["EUR="],
        session=open_session,
        fields=['BID', 'ASK', 'VOLUME', 'OPEN_PRC'],
        service="IDN_RDF",
        on_complete=lambda st: print(f"Complete: {st}"),
        on_refresh=lambda st, data: print(f"Refresh: {data}"),
        on_status=lambda st, ric, status: print(f"Status[{ric}] : {status}"),
        on_update=lambda st, ric, update: print(f"Update[{ric}] : {update}")
        )
    state = streaming_prices.open()
    assert state is rdp.StreamState.Open
    streaming_prices.close()


@pytest.mark.integrate
def test_required_param(open_session):
    streaming_prices = rdp.StreamingPrices(universe=["EUR="])
    state = streaming_prices.open()
    assert state is rdp.StreamState.Open
    streaming_prices.close()


@pytest.mark.integrate
def test_universe_error(open_session):
    with pytest.raises(rdp.RDPError):
        rdp.StreamingPrices(universe=[None])

    with pytest.raises(rdp.RDPError):
        rdp.StreamingPrices(universe=None)


@pytest.mark.unit
def test_universe_str(open_session):
    prices = rdp.StreamingPrices(universe="RIC")
    assert prices is not None


@pytest.mark.unit
def test_len(open_session):
    universe = ["RIC"]
    stp = rdp.StreamingPrices(universe=universe)
    assert len(stp) == len(universe)


@pytest.mark.unit
def test_get_item(open_session):
    universe = ["RIC"]
    stp = rdp.StreamingPrices(universe=universe)
    item = stp[universe[0]]
    assert item.name == universe[0]


@pytest.mark.unit
def test_get_item_error(open_session):
    universe = ["RIC"]
    stp = rdp.StreamingPrices(universe=universe)
    with pytest.raises(KeyError):
        stp["__mock__"]


@pytest.mark.integrate
def test_get_snapshot_fields_error(open_session):
    universe = ["EUR="]
    streaming_prices = rdp.StreamingPrices(universe=universe)
    with pytest.raises(rdp.RDPError):
        streaming_prices.get_snapshot(universe, ["__mock__"])
    streaming_prices.open()
    streaming_prices.close()


@pytest.mark.integrate
def test_get_snapshot_universe_error(open_session):
    universe = ["EUR="]
    streaming_prices = rdp.StreamingPrices(universe=universe)
    with pytest.raises(rdp.RDPError):
        streaming_prices.get_snapshot(["__mock__"])
    streaming_prices.open()
    streaming_prices.close()
