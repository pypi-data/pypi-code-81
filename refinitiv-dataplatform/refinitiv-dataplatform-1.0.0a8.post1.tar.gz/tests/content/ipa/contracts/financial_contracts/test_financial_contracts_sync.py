from refinitiv.dataplatform.content import ipa
import response_tests


def test_bond_pricing_one(open_session_for_ipa):
    response = ipa.FinancialContracts.get_bond_analytics("13063CUV0")
    response_tests.success_response_tests(response)


def test_bond_pricing_many(open_session_for_ipa):
    response = ipa.FinancialContracts.get_bond_analytics(["US1YT=RR", "US5YT=RR", "US10YT=RR"])
    response_tests.success_response_tests(response)


def test_bond_pricing_many_with_calculation_params(open_session_for_ipa):
    response = ipa.FinancialContracts.get_bond_analytics(
        universe=[
            "US1YT=RR",
            (
                ipa.bond.Definition("US5YT=RR"),
                ipa.bond.CalculationParams(price_side=ipa.enum_types.PriceSide.ASK)
            ),
            "US10YT=RR"
        ],
        calculation_params=ipa.bond.CalculationParams(
            market_data_date="2019-07-05",
            price_side=ipa.enum_types.PriceSide.BID
        )
    )
    response_tests.success_response_tests(response)


def test_option_pricing_one(open_session_for_ipa):
    response = ipa.FinancialContracts.get_instrument_analytics(
        ipa.option.Definition(
            instrument_code="FCHI560000L0.p",
            underlying_type=ipa.option.UnderlyingType.ETI
        )
    )
    response_tests.success_response_tests(response)


def test_option_pricing_many(open_session_for_ipa):
    response = ipa.FinancialContracts.get_instrument_analytics(
        [
            ipa.option.Definition(
                instrument_code="FCHI560000L0.p",
                underlying_type=ipa.option.UnderlyingType.ETI
            ),
            ipa.option.Definition(
                instrument_code="FCHI560000L1.p",
                underlying_type=ipa.option.UnderlyingType.ETI
            )
        ]
    )
    response_tests.success_response_tests(response)


def test_option_pricing_not_success(open_session_for_ipa):
    response = ipa.FinancialContracts.get_instrument_analytics(
        ipa.option.Definition(
            instrument_code="FCHI560000L1.p",
            underlying_type=ipa.option.UnderlyingType.FX
        )
    )
    response_tests.not_success_response_tests(response)


def test_option_pricing_many_with_fields_and_calculation_params(open_session_for_ipa):
    response = ipa.FinancialContracts.get_instrument_analytics(
        universe=[
            ipa.option.Definition("FCHI560000L0.p", ipa.option.UnderlyingType.ETI),
            (
                ipa.option.Definition("FCHI560000L1.p", ipa.option.UnderlyingType.FX),
                ipa.option.CalculationParams(pricing_model_type=ipa.enum_types.PricingModelType.WHALEY)
            )
        ],
        calculation_params=ipa.option.CalculationParams(
            market_data_date="2019-07-05",
            pricing_model_type=ipa.enum_types.PricingModelType.BLACK_SCHOLES
        ),
        fields=[
            "ValuationDate",
            "InstrumentDescription",
            "InstrumentCode",
            "EndDate",
            "StrikePrice",
            "OptionType",
            "DeltaPercent",
            "GammaPercent",
            "RhoPercent",
            "ThetaPercent_BidMidAsk",
            "VegaPosition_BidMidAsk",
            "Gearing_BidMidAsk",
            "BreakEvenTime_BidMidAsk"
        ]
    )
    response_tests.success_response_tests(response)


def test_instrument_pricing(open_session_for_ipa):
    response = ipa.FinancialContracts.get_instrument_analytics(
        universe=[
            ipa.bond.Definition("US1YT=RR"),
            ipa.bond.Definition("US5YT=RR"),
            ipa.bond.Definition("US10YT=RR"),
            (
                ipa.option.Definition("FCHI560000L0.p", ipa.option.UnderlyingType.ETI),
                ipa.option.CalculationParams(
                    market_data_date="2019-07-05",
                    pricing_model_type=ipa.enum_types.PricingModelType.BLACK_SCHOLES
                )
            )
        ],
        calculation_params=ipa.bond.CalculationParams(
            market_data_date="2019-07-05",
            price_side=ipa.enum_types.PriceSide.BID
        )
    )
    response_tests.success_response_tests(response)
