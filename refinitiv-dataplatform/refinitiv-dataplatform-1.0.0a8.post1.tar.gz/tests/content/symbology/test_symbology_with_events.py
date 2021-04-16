import asyncio
import datetime

import pytest

import refinitiv.dataplatform as rdp
import response_tests


def display_response(response):
    data_name = response.closure
    current_time = datetime.datetime.now().time()
    print('{} received at {}'.format(data_name, current_time))
    print(response.data.df)


def on_response(fut, closure):
    def wrapper(_, response):
        display_response(response)
        response_tests.success_response_tests(response=response, mock_closure=closure)
        fut.set_result(1)

    return wrapper


@pytest.mark.integrate
def test_convert_symbols(open_session):
    async def convert_symbols():
        fut = asyncio.Future()
        closure = "ConvertSymbols"
        await asyncio.get_event_loop().create_task(
            rdp.Symbology.convert_async(
                symbols=['MSFT.O', 'AAPL.O', 'GOOG.O', 'IBM.N', 'PEUP.PA'],
                from_symbol_type=rdp.SymbolTypes.RIC,  # rdp.SymbolTypes.RIC is the default.
                to_symbol_types=None,  # Default: None (means all symbol types are requested)
                on_response=on_response(fut, closure),
                closure=closure
            )
        )
        return await fut

    asyncio.get_event_loop().run_until_complete(convert_symbols())


@pytest.mark.integrate
def test_convert_isin_id_symbols(open_session):
    async def convert_isin_id_symbols():
        fut = asyncio.Future()
        closure = "ConvertSymbols"
        await asyncio.get_event_loop().create_task(
            rdp.Symbology.convert_async(
                symbols=['US5949181045', 'US02079K1079'],
                from_symbol_type=rdp.SymbolTypes.ISIN,
                to_symbol_types=[rdp.SymbolTypes.RIC, rdp.SymbolTypes.OAPermID],
                on_response=on_response(fut, closure),
                closure=closure
            )
        )
        return await fut

    asyncio.get_event_loop().run_until_complete(convert_isin_id_symbols())


@pytest.mark.integrate
def test_convert_lipper_id_symbols(open_session):
    async def convert_lipper_id_symbols():
        fut = asyncio.Future()
        closure = "ConvertSymbols"
        await asyncio.get_event_loop().create_task(
            rdp.Symbology.convert_async(
                symbols=['60000008', '60003513'],
                from_symbol_type=rdp.SymbolTypes.LipperID,
                on_response=on_response(fut, closure),
                closure=closure
            )
        )
        return await fut

    asyncio.get_event_loop().run_until_complete(convert_lipper_id_symbols())


@pytest.mark.integrate
def test_convert_lipper_id_symbols_without_closure(open_session):
    async def convert_lipper_id_symbols_without_closure():
        fut = asyncio.Future()
        await asyncio.get_event_loop().create_task(
            rdp.Symbology.convert_async(
                symbols=['60000008', '60003513'],
                from_symbol_type=rdp.SymbolTypes.LipperID,
                on_response=on_response(fut, None),
            )
        )
        return await fut

    asyncio.get_event_loop().run_until_complete(convert_lipper_id_symbols_without_closure())
