import asyncio

from refinitiv.dataplatform.content import ipa
import response_tests


def test_synchronized_parallel_calls(open_session_for_ipa):
    tasks = asyncio.gather(
        ipa.FinancialContracts.get_bond_analytics_async(
            universe=["US1YT=RR", "US5YT=RR", "US10YT=RR"]
        ),
        ipa.FinancialContracts.get_option_analytics_async(
            universe=["FCHI560000L0.p", "FCHI560000L1.p"],
            calculation_params=ipa.option.CalculationParams(
                market_data_date="2019-07-05",
                pricing_model_type=ipa.enum_types.PricingModelType.BLACK_SCHOLES
            )
        ),
        ipa.FinancialContracts.get_instrument_analytics_async(
            universe=[
                ipa.bond.Definition("US1YT=RR"),
                ipa.bond.Definition("US5YT=RR"),
                ipa.bond.Definition("US10YT=RR"),
                ipa.option.Definition("FCHI560000L0.p"),
                (
                    ipa.option.Definition(
                        instrument_code="FCHI560000L1.p",
                        underlying_type=ipa.option.UnderlyingType.ETI
                    ),
                    ipa.option.CalculationParams(
                        market_data_date="2019-07-05",
                        pricing_model_type=ipa.enum_types.PricingModelType.BLACK_SCHOLES
                    )
                )
            ],
            calculation_params=ipa.bond.CalculationParams(
                market_data_date="2019-07-05",
                price_side=ipa.enum_types.PriceSide.BID
            ),
        )
    )

    asyncio.get_event_loop().run_until_complete(tasks)
    bonds, options, bonds_and_options = tasks.result()
    response_tests.success_response_tests(bonds)
    response_tests.success_response_tests(options)
    response_tests.success_response_tests(bonds_and_options)
