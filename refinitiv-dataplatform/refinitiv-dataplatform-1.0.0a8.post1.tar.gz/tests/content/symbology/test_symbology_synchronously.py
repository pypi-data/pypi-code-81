import pytest

import refinitiv.dataplatform as rdp
import response_tests


@pytest.mark.integrate
def test_convert_from_ric_to_all(open_session):
    response = rdp.Symbology.convert(
        symbols=['MSFT.O', 'AAPL.O', 'GOOG.O', 'IBM.N', 'PEUP.PA'],
        from_symbol_type=rdp.SymbolTypes.RIC,  # rdp.SymbolTypes.RIC is the default.
        to_symbol_types=None  # Default: None (means all symbol types are requested)
    )
    response_tests.success_response_tests(response)

    assert not response.data.df.empty  # or response.data.raw for raw format
    assert response.data.raw
    assert response.status


@pytest.mark.integrate
def test_convert_from_isin_to_another_two(open_session):
    response = rdp.Symbology.convert(
        symbols=['US5949181045', 'US02079K1079'],
        from_symbol_type=rdp.SymbolTypes.ISIN,
        to_symbol_types=[rdp.SymbolTypes.RIC, rdp.SymbolTypes.OAPermID]
    )

    assert not response.data.df.empty


@pytest.mark.integrate
def test_convert_from_lipperid_to_all(open_session):
    response = rdp.Symbology.convert(
        symbols=['60000008', '60003513'],
        from_symbol_type=rdp.SymbolTypes.LipperID
    )

    assert not response.data.df.empty
