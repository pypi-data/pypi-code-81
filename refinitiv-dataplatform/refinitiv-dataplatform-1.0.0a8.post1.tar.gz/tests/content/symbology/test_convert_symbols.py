import pytest

import refinitiv.dataplatform as rdp


@pytest.mark.integrate
def test_convert_one_symbol(open_session):
    df = rdp.convert_symbols('MSFT.O')
    assert df is not None, rdp.ContentFactory._last_error_status
    columns = [
        not df.get(v).empty
        for v in rdp.SYMBOL_TYPE_VALUES
        if v in df.keys()
    ]
    assert columns and all(columns)
    assert not df.empty


@pytest.mark.integrate
def test_convert_list_of_symbols(open_session):
    df = rdp.convert_symbols(['MSFT.O', 'AAPL.O', 'GOOG.O', 'IBM.N', 'PEUP.PA'])
    assert df is not None, rdp.ContentFactory._last_error_status

    columns = [
        not df.get(v).empty
        for v in rdp.SYMBOL_TYPE_VALUES
        if v in df.keys()
    ]
    assert columns and all(columns)
    assert not df.empty


@pytest.mark.integrate
def test_twice_convert_list_of_symbols(open_session):
    rdp.convert_symbols(['MSFT.O', 'AAPL.O', 'GOOG.O', 'IBM.N', 'PEUP.PA'])
    df = rdp.convert_symbols(['MSFT.O', 'AAPL.O', 'GOOG.O', 'IBM.N', 'PEUP.PA'])
    assert df is not None, rdp.ContentFactory._last_error_status

    columns = [
        not df.get(v).empty
        for v in rdp.SYMBOL_TYPE_VALUES
        if v in df.keys()
    ]
    assert columns and all(columns)
    assert not df.empty


# noinspection PyPep8Naming
@pytest.mark.integrate
def test_convert_list_of_symbols_from_RIC_type_to_all_types(open_session):
    df = rdp.convert_symbols(
        symbols=['MSFT.O', 'AAPL.O', 'GOOG.O', 'IBM.N', 'PEUP.PA'],
        from_symbol_type=rdp.SymbolTypes.RIC,  # rdp.SymbolTypes.RIC is the default.
        to_symbol_types=None  # Default: None (means all symbol types are requested)
    )
    assert df is not None, rdp.ContentFactory._last_error_status

    assert not df.empty

    # SymbolTypes: RIC,ISIN,CUSIP,SEDOL,Ticker,OAPermID,LipperID
    #     - rdp.SymbolTypes.RIC => RIC
    #     - rdp.SymbolTypes.ISIN => IssueISIN
    #     - rdp.SymbolTypes.CUSIP => CUSIP
    #     - rdp.SymbolTypes.SEDOL => SEDOL
    #     - rdp.SymbolTypes.Ticker => TickerSymbol
    #     - rdp.SymbolTypes.OAPermID => IssuerOAPermID
    #     - rdp.SymbolTypes.LipperID => FundClassLipperID


# noinspection PyPep8Naming
@pytest.mark.integrate
def test_convert_list_of_symbols_from_ISIN_type_to_list_of_types(open_session):
    df = rdp.convert_symbols(
        symbols=['US5949181045', 'US02079K1079'],
        from_symbol_type=rdp.SymbolTypes.ISIN,
        to_symbol_types=[rdp.SymbolTypes.RIC, rdp.SymbolTypes.OAPermID]
    )
    assert df is not None, rdp.ContentFactory._last_error_status

    assert not df.empty


# noinspection PyPep8Naming
@pytest.mark.integrate
def test_convert_list_of_symbols_from_LipperID(open_session):
    df = rdp.convert_symbols(
        symbols=['60000008', '60003513'],
        from_symbol_type=rdp.SymbolTypes.LipperID
    )
    assert df is not None, rdp.ContentFactory._last_error_status

    assert not df.empty
