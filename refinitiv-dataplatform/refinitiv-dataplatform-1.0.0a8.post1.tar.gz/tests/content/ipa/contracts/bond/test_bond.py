from inspect import signature

import pytest

from refinitiv.dataplatform import ContentFactory
from refinitiv.dataplatform.content import ipa
from refinitiv.dataplatform.content.ipa import BondRoundingParameters
from refinitiv.dataplatform.content.ipa.contracts.bond import Definition, CalculationParams
from refinitiv.dataplatform.content.ipa.enum_types import *
import conftest
import refinitiv.dataplatform as rdp


def test_single_bond(open_session_for_ipa, universe):
    df = rdp.get_bond_analytics(universe)
    assert df is not None, rdp.ContentFactory._last_error_status
    assert not df.empty, ContentFactory._last_error_status


def test_multiple_bonds(open_session_for_ipa, many_universes):
    df = rdp.get_bond_analytics(many_universes)
    assert df is not None, ContentFactory._last_error_status
    assert not df.empty


def test_multiple_bonds_(open_session_for_ipa):
    df = rdp.get_bond_analytics(["13063CUV0", Definition("13063CUV0")])
    assert df is not None, rdp.ContentFactory._last_error_status
    assert not df.empty, ContentFactory._last_error_status


def test_multiple_bonds__(open_session_for_ipa):
    df = rdp.get_bond_analytics(
        universe=[
            Definition("13063CUV0"),
            Definition("13063CUV0")],
        calculation_params=CalculationParams())
    if df is None:
        pytest.fail(str(ContentFactory._last_error_status))
    assert not df.empty, ContentFactory._last_error_status


def test_multiple_bonds_request_with_fields(open_session_for_ipa):
    df = rdp.get_bond_analytics(
        universe=[
            Definition("13063CUV0"),
            Definition("GBIL0F40="),
            Definition("US1YT=RR"),
            Definition("US5YT=RR"),
            Definition("US10YT=RR"),
            Definition("FR1YT=RR"),
            Definition("FR5YT=RR"),
            Definition("FR10YT=RR")
            ],
        fields=[
            "InstrumentCode",
            "MarketDataDate",
            "YieldPercent",
            "GovernmentSpreadBp",
            "GovCountrySpreadBp",
            "RatingSpreadBp",
            "SectorRatingSpreadBp",
            "EdsfSpreadBp",
            "IssuerSpreadBp"
            ]
        )
    assert df is not None, rdp.ContentFactory._last_error_status
    assert not df.empty


def test_multiple_bonds_request_with_global_parameters(open_session_for_ipa):
    df = rdp.get_bond_analytics(
        universe=[
            Definition("13063CUV0"),
            Definition("GBIL0F40="),
            Definition("US1YT=RR"),
            Definition("US5YT=RR"),
            Definition("US10YT=RR"),
            Definition("FR1YT=RR"),
            Definition("FR5YT=RR"),
            Definition("FR10YT=RR")
            ],
        calculation_params=CalculationParams(valuation_date="2019-07-05")
        )
    assert not df.empty, ContentFactory._last_error_status


def test_user_defined_bond(open_session_for_ipa):
    df = rdp.get_bond_analytics(
        Definition(
            issue_date="2002-02-28",
            end_date="2032-02-28",
            notional_ccy="USD",
            interest_payment_frequency="Annual",
            fixed_rate_percent=7,
            interest_calculation_method="Dcb_Actual_Actual"
            )
        )
    assert not df.empty


def test_multiple_bonds_request_with_global_parameters_and_specific_parameters(open_session_for_ipa, ):
    df = rdp.get_bond_analytics(
        universe=[
            # First Bond uses specific Pricing parameters
            (
                Definition("13063CUV0"),
                CalculationParams(
                    valuation_date="2019-07-05",
                    rounding_parameters={"yieldRounding": "Five"}
                    )
                ),
            # Other Bonds use global Pricing parameters
            Definition("GBIL0F40="),
            Definition("US1YT=RR"),
            Definition("US5YT=RR"),
            Definition("US10YT=RR"),
            Definition("FR1YT=RR"),
            Definition("FR5YT=RR"),
            Definition("FR10YT=RR")
            ],
        fields=[],
        calculation_params=CalculationParams(valuation_date="2019-07-05")
        )
    if df is None:
        pytest.fail(str(ContentFactory._last_error_status))
    assert not df.empty


def test_user_defined_bond_str(open_session_for_ipa, ):
    df = rdp.get_bond_analytics(
        Definition(
            issue_date="2002-02-28",
            end_date="2032-02-28",
            notional_ccy="USD",
            interest_payment_frequency="Annual",
            fixed_rate_percent=7,
            interest_calculation_method="Dcb_Actual_Actual"
            )
        )
    assert not df.empty


def test_user_defined_bond_enum(open_session_for_ipa, ):
    df = rdp.get_bond_analytics(
        Definition(
            issue_date="2002-02-28",
            end_date="2032-02-28",
            notional_ccy="USD",
            interest_payment_frequency=Frequency.ANNUAL,
            fixed_rate_percent=7,
            interest_calculation_method=DayCountBasis.DCB_ACTUAL_ACTUAL
            )
        )
    assert not df.empty


def test_raise_error_definition():
    with pytest.raises(ValueError):
        rdp.get_bond_analytics((1, CalculationParams()))


def test_raise_error_pricing_parameters():
    with pytest.raises(ValueError):
        rdp.get_bond_analytics((Definition(), 2))


def test_raise_error_tuple_three():
    with pytest.raises(ValueError):
        rdp.get_bond_analytics((1, 2, 3))


def test_raise_error_tuple_one():
    with pytest.raises(ValueError):
        rdp.get_bond_analytics((1,))


def test_fields_selection(open_session_for_ipa, ):
    df = rdp.get_bond_analytics(
        universe=[
            "US1YT=RR",
            "US5YT=RR",
            "US10YT=RR"
            ],
        fields=[
            "InstrumentCode",
            "MarketDataDate",
            "YieldPercent",
            "GovernmentSpreadBp",
            "GovCountrySpreadBp",
            "RatingSpreadBp",
            "SectorRatingSpreadBp",
            "EdsfSpreadBp",
            "IssuerSpreadBp"
            ]
        )
    assert not df.empty


def test_global_pricing_parameters(open_session_for_ipa, ):
    df = rdp.get_bond_analytics(
        universe=[
            "US1YT=RR",
            "US5YT=RR",
            "US10YT=RR"
            ],
        calculation_params=CalculationParams(
            valuation_date="2019-07-05",
            price_side=PriceSide.BID
            )
        )
    assert not df.empty


def test_global_and_individual_pricing_parameters(open_session_for_ipa, ):
    df = rdp.get_bond_analytics(
        universe=[
            "US1YT=RR",
            (
                Definition("US5YT=RR"),
                CalculationParams(price_side=PriceSide.ASK)
                ),
            "US10YT=RR"
            ],
        calculation_params=CalculationParams(
            valuation_date="2019-07-05",
            price_side=PriceSide.BID
            )
        )
    assert not df.empty


@pytest.mark.parametrize(
    argnames="input_data",
    ids=[
        "Definition",
        "CalculationParams",
        "BondRoundingParameters"
        ],
    argvalues=[
        (Definition, {
            "instrument_code": "instrument_code",
            "instrument_tag": "instrument_tag",
            "end_date": "end_date",
            # "direction": Direction,
            # "interest_type": InterestType,
            "notional_ccy": "notional_ccy",
            "notional_amount": 7.7,
            "fixed_rate_percent": 8.8,
            # "spread_bp": 9.9,
            "interest_payment_frequency": Frequency.EVERY14_DAYS,
            "interest_calculation_method": DayCountBasis.DCB_30_360_ISDA,
            "accrued_calculation_method": DayCountBasis.DCB_30_360,
            "payment_business_day_convention": BusinessDayConvention.MODIFIED_FOLLOWING,
            "payment_roll_convention": DateRollingConvention.LAST28,
            # "index_reset_frequency": Frequency,
            # "index_fixing_lag": 16,
            # "first_regular_payment_date": "first_regular_payment_date",
            # "last_regular_payment_date": "last_regular_payment_date",
            # "amortization_schedule": AmortizationItem,
            # "payment_business_days": "payment_business_days",
            # "adjust_interest_to_payment_date": AdjustInterestToPaymentDate,
            # "index_compounding_method": IndexCompoundingMethod,
            # "interest_payment_delay": 23,
            # "stub_rule": StubRule,
            "issue_date": "issue_date",
            # "index_fixing_ric": "index_fixing_ric",
            # "is_perpetual": True,
            "first_accrual_date": "str",
            "template": "str"
            }),
        (CalculationParams, {
            "initial_margin_percent": "initial_margin_percent",
            "haircut_rate_percent": "haircut_rate_percent",
            "clean_future_price": "clean_future_price",
            "dirty_future_price": "dirty_future_price",
            "interpolate_missing_points": "interpolate_missing_points",
            "report_ccy": "report_ccy",
            "market_data_date": "market_data_date",
            # "trade_date": "trade_date",
            "benchmark_yield_selection_mode": BenchmarkYieldSelectionMode.INTERPOLATE,
            # "fx_price_side": PriceSide.ASK,
            "price_side": PriceSide.MID,
            "projected_index_calculation_method": ProjectedIndexCalculationMethod.CONSTANT_INDEX,
            "redemption_date_type": RedemptionDateType.REDEMPTION_AT_BEST_DATE,
            "rounding_parameters": BondRoundingParameters(),
            "yield_type": YieldType.DISCOUNT_ACTUAL_360,
            "adjusted_clean_price": 9.9,
            "adjusted_dirty_price": 10.10,
            "adjusted_yield_percent": 11.11,
            "apply_tax_to_full_pricing": True,
            "asset_swap_spread_bp": 13.13,
            "benchmark_at_issue_price": 14.14,
            "benchmark_at_issue_ric": "benchmark_at_issue_ric",
            "benchmark_at_issue_spread_bp": 16.16,
            "benchmark_at_issue_yield_percent": 17.17,
            "benchmark_at_redemption_price": 18.18,
            "benchmark_at_redemption_spread_bp": 19.19,
            "benchmark_at_redemption_yield_percent": 20.20,
            "cash_amount": 21.21,
            "clean_price": 22.22,
            "concession_fee": 23.23,
            "current_yield_percent": 24.24,
            "dirty_price": 25.25,
            "discount_margin_bp": 26.26,
            "discount_percent": 27.27,
            "edsf_benchmark_curve_yield_percent": 28.28,
            "edsf_spread_bp": 29.29,
            "efp_benchmark_price": 30.30,
            "efp_benchmark_ric": "efp_benchmark_ric",
            "efp_benchmark_yield_percent": 32.32,
            "efp_spread_bp": 33.33,
            "gov_country_benchmark_curve_price": 34.34,
            "gov_country_benchmark_curve_yield_percent": 35.35,
            "gov_country_spread_bp": 36.36,
            "government_benchmark_curve_price": 37.37,
            "government_benchmark_curve_yield_percent": 38.38,
            "government_spread_bp": 39.39,
            "issuer_benchmark_curve_yield_percent": 40.40,
            "issuer_spread_bp": 41.41,
            "market_value_in_deal_ccy": 42.42,
            "market_value_in_report_ccy": 43.43,
            "net_price": 44.44,
            "neutral_yield_percent": 45.45,
            # "ois_zc_benchmark_curve_yield_percent": 46.46,
            # "ois_zc_spread_bp": 47.47,
            "option_adjusted_spread_bp": 48.48,
            "price": 49.49,
            "quoted_price": 50.50,
            "rating_benchmark_curve_yield_percent": 51.51,
            "rating_spread_bp": 52.52,
            "redemption_date": "redemption_date",
            "sector_rating_benchmark_curve_yield_percent": 54.54,
            "sector_rating_spread_bp": 55.55,
            "settlement_convention": "settlement_convention",
            "simple_margin_bp": 57.57,
            "strip_yield_percent": 58.58,
            "swap_benchmark_curve_yield_percent": 59.59,
            "swap_spread_bp": 60.60,
            "tax_on_capital_gain_percent": 61.61,
            "tax_on_coupon_percent": 62.62,
            "tax_on_price_percent": 63.63,
            "tax_on_yield_percent": 64.64,
            # "use_settlement_date_from_quote": bool,
            "user_defined_benchmark_price": 66.66,
            "user_defined_benchmark_yield_percent": 67.67,
            "user_defined_spread_bp": 68.68,
            "valuation_date": "valuation_date",
            "yield_percent": 70.70,
            "z_spread_bp": 71.71,
            "quote_fallback_logic": QuoteFallbackLogic.BEST_FIELD
            }),
        (BondRoundingParameters, {
            "accrued_rounding": Rounding.FOUR,
            "accrued_rounding_type": RoundingType.FACE_NEAR,
            "price_rounding": Rounding.FIVE,
            "price_rounding_type": RoundingType.FACE_DOWN,
            "spread_rounding": Rounding.EIGHT,
            "spread_rounding_type": RoundingType.CEIL,
            "yield_rounding": Rounding.DEFAULT,
            "yield_rounding_type": RoundingType.FACE_UP,
            })
        ])
def test_parameter(input_data):
    cls, kwargs = input_data
    args_names = list(kwargs.keys())
    inst = cls(**kwargs)

    s = signature(cls.__init__)
    assert len(s.parameters) == (len(args_names) + 1), cls  # +1 for (self)

    assert conftest.has_property_names_in_class(cls, args_names), set(args_names) - set(
        conftest.get_property_names(cls))

    for k, v in kwargs.items():
        attr = getattr(inst, k)
        assert attr == v, k
