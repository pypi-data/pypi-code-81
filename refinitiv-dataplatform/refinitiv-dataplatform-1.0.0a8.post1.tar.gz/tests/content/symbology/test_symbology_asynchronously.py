import asyncio

import pytest

import refinitiv.dataplatform as rdp


@pytest.mark.integrate
@pytest.mark.asyncio
async def test_measures_and_scores(open_session):
    rics_response, isins_response, lipperids_response = await asyncio.gather(
        rdp.Symbology.convert_async(
            symbols=['MSFT.O', 'AAPL.O', 'GOOG.O', 'IBM.N', 'PEUP.PA'],
            from_symbol_type=rdp.SymbolTypes.RIC,  # rdp.SymbolTypes.RIC is the default.
            to_symbol_types=None  # Default: None (means all symbol types are requested)
            ),
        rdp.Symbology.convert_async(
            symbols=['US5949181045', 'US02079K1079'],
            from_symbol_type=rdp.SymbolTypes.ISIN,
            to_symbol_types=[rdp.SymbolTypes.RIC, rdp.SymbolTypes.OAPermID]
            ),
        rdp.Symbology.convert_async(
            symbols=['60000008', '60003513'],
            from_symbol_type=rdp.SymbolTypes.LipperID
            ),
        )

    assert rics_response.data.df is not None and not rics_response.data.df.empty, (
        f"Error {rics_response.error_code} - {rics_response.error_message}")
    assert isins_response.data.df is not None and not isins_response.data.df.empty, (
        f"Error {isins_response.error_code} - {isins_response.error_message}")
    assert lipperids_response.data.df is not None and not lipperids_response.data.df.empty, (
        f"Error {lipperids_response.error_code} - {lipperids_response.error_message}")
