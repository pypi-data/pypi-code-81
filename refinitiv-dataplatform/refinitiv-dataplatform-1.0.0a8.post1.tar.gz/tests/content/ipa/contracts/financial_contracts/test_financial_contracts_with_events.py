import asyncio

import response_tests

from refinitiv.dataplatform import ipa


def on_response(fut):
    def inner(params, response):
        fut.set_result(response)

    return inner


def test_synchronized_parallel_calls(open_session_for_ipa):
    fut1 = asyncio.Future()
    task1 = asyncio.get_event_loop().create_task(
        ipa.FinancialContracts.get_bond_analytics_async(
            universe=["US1YT=RR", "US5YT=RR", "US10YT=RR"],
            on_response=on_response(fut1)
        ))

    fut2 = asyncio.Future()
    task2 = asyncio.get_event_loop().create_task(
        ipa.FinancialContracts.get_option_analytics_async(
            universe=["FCHI560000L0.p", "FCHI560000L1.p"],
            on_response=on_response(fut2)
        ))

    fut3 = asyncio.Future()
    task3 = asyncio.get_event_loop().create_task(
        ipa.FinancialContracts.get_instrument_analytics_async(
            universe=[
                ipa.bond.Definition("US1YT=RR"),
                ipa.bond.Definition("US5YT=RR"),
                ipa.bond.Definition("US10YT=RR"),
                (
                    ipa.option.Definition("FCHI560000L0.p"),
                    ipa.option.CalculationParams(
                        market_data_date="2019-07-05",
                        pricing_model_type=ipa.enum_types.PricingModelType.BLACK_SCHOLES
                    )
                ),
                ipa.option.Definition(
                    instrument_code="FCHI560000L1.p",
                    underlying_type=ipa.option.UnderlyingType.ETI
                )
            ],
            calculation_params=ipa.bond.CalculationParams(
                market_data_date="2019-07-05",
                price_side=ipa.enum_types.PriceSide.BID
            ),
            on_response=on_response(fut3)
        ))

    resp1, resp2, resp3, *_ = asyncio.get_event_loop().run_until_complete(
        asyncio.gather(task1, task2, task3, fut1, fut2, fut3)
    )
    response_tests.success_response_tests(resp1)
    response_tests.success_response_tests(resp2)
    response_tests.success_response_tests(resp3)
