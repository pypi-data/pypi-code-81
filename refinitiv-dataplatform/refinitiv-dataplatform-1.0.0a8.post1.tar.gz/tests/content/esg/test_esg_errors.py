import pytest

import refinitiv.dataplatform as rdp


@pytest.mark.unit
def test_call_with_universe_none(open_session):
    with pytest.raises(rdp.RDPError):
        _ = rdp.ESG.get_basic_overview(universe=None)


@pytest.mark.unit
def test_call_with_data_type_none(open_session):
    with pytest.raises(rdp.RDPError):
        esg = rdp.ESG()
        _ = esg._get_data('5000002406', data_type=None)


@pytest.mark.unit
def test_call_without_universe(open_session):
    with pytest.raises(TypeError):
        _ = rdp.ESG.get_basic_overview()


@pytest.mark.unit
def test_call_without_data_type():
    with pytest.raises(TypeError):
        esg = rdp.ESG()
        _ = esg._get_data('5000002406')


@pytest.mark.unit
def test_call_without_start(open_session):
    with pytest.raises(rdp.RDPError):
        esg = rdp.ESG()
        _ = esg._get_data('5000002406', rdp.ESG.DataType.FullMeasures, end=-3)


@pytest.mark.unit
def test_call_without_end(open_session):
    with pytest.raises(rdp.RDPError):
        esg = rdp.ESG()
        _ = esg._get_data('5000002406', rdp.ESG.DataType.FullMeasures, start=0)
