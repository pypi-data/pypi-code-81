import asyncio
from inspect import signature

import pytest
import refinitiv.dataplatform as rdp

from refinitiv.dataplatform import RequiredError
from refinitiv.dataplatform.content import ipa
from refinitiv.dataplatform.content.ipa import AmortizationItem
from refinitiv.dataplatform.content.ipa.contracts.swap import LegDefinition, Definition, CalculationParams
from refinitiv.dataplatform.content.ipa.enum_types import *
import conftest
import response_tests


def test_get_swap_analytics(open_session_for_ipa):
    """
    {
      "fields": [
        "InstrumentTag",
        "InstrumentDescription",
        "FixedRate",
        "MarketValueInDealCcy",
        "MarketValueInReportCcy",
        "ErrorMessage"
      ],
      "outputs": [
        "Data",
        "Headers"
      ],
      "universe": [
        {
          "instrumentType": "Swap",
          "instrumentDefinition": {
            "instrumentTag": "EUR_AB6E 5Y swap",
            "template": "EUR_AB6E",
            "tenor": "5Y"
          },
          "pricingParameters": {
            "valuationDate": "2018-01-10T00:00:00Z",
            "reportCcy": "JPY"
          }
        }
      ]
    }

    """
    df = rdp.get_swap_analytics(
        universe=ipa.swap.Definition(
            instrument_tag="EUR_AB6E 5Y swap",
            template="EUR_AB6E",
            tenor="5Y",
        ),
        calculation_params=ipa.swap.CalculationParams(valuation_date="2018-01-10T00:00:00Z", report_ccy='JPY'),
        fields=[
            "InstrumentTag",
            "InstrumentDescription",
            "FixedRate",
            "MarketValueInDealCcy",
            "MarketValueInReportCcy",
            "ErrorMessage"
        ],
        outputs=[
            "Data",
            "Headers"
        ]
    )
    assert not df.empty


def test_get_swap_analytics_with_legs(open_session_for_ipa):
    """
    {
      "fields": [
        "InstrumentTag",
        "InstrumentDescription",
        "FixedRate",
        "MarketValueInDealCcy",
        "PV01Bp",
        "DiscountCurveName",
        "ForwardCurveName",
        "CashFlowDatesArray",
        "CashFlowTotalAmountsInDealCcyArray",
        "CashFlowDiscountFactorsArray",
        "CashFlowResidualAmountsInDealCcyArray",
        "ErrorMessage"
      ],
      "outputs": [
        "Data",
        "Headers"
      ],
      "universe": [
        {
          "instrumentType": "Swap",
          "instrumentDefinition": {
            "instrumentTag": "user-defined GBP IRS",
            "startDate": "2019-05-21T00:00:00Z",
            "tenor": "10Y",
            "legs": [
              {
                "direction": "Paid",
                "notionalAmount": "10000000",
                "notionalCcy": "GBP",
                "interestType": "Fixed",
                "interestPaymentFrequency": "Annual",
                "interestCalculationMethod": "Dcb_30_360",
                "paymentBusinessDayConvention": "ModifiedFollowing",
                "paymentRollConvention": "Same",
                "paymentBusinessDays": "UKG",
                "amortizationSchedule": [
                  {
                    "remainingNotional": 200000,
                    "amortizationFrequency": "EveryCoupon",
                    "amortizationType": "Linear"
                  }
                ]
              },
              {
                "direction": "Received",
                "notionalAmount": "10000000",
                "notionalCcy": "GBP",
                "interestType": "Float",
                "interestPaymentFrequency": "SemiAnnual",
                "indexResetFrequency": "SemiAnnual",
                "interestCalculationMethod": "Dcb_Actual_360",
                "paymentBusinessDayConvention": "ModifiedFollowing",
                "paymentRollConvention": "Same",
                "paymentBusinessDays": "UKG",
                "SpreadBp": 20,
                "indexName": "LIBOR",
                "indexTenor": "6M",
                "indexResetType": "InAdvance",
                "amortizationSchedule": [
                  {
                    "remainingNotional": 200000,
                    "amortizationFrequency": "Every2ndCoupon",
                    "amortizationType": "Linear"
                  }
                ]
              }
            ]
          },
          "pricingParameters": {
            "discountingTenor": "ON"
          }
        }
      ]
    }
    """
    df = rdp.get_swap_analytics(
        universe=ipa.swap.Definition(
            instrument_tag="user-defined GBP IRS",
            start_date="2019-05-21T00:00:00Z",
            tenor="10Y",
            legs=[
                ipa.swap.LegDefinition(
                    direction=Direction.PAID,
                    notional_amount="10000000",
                    notional_ccy="GBP",
                    interest_type=InterestType.FIXED,
                    interest_payment_frequency=Frequency.ANNUAL,
                    interest_calculation_method=DayCountBasis.DCB_30_360,
                    payment_business_day_convention=BusinessDayConvention.MODIFIED_FOLLOWING,
                    payment_roll_convention=DateRollingConvention.SAME,
                    payment_business_days="UKG",
                    amortization_schedule=[
                        AmortizationItem(
                            remaining_notional=200000,
                            amortization_frequency=AmortizationFrequency.EVERY_COUPON,
                            amortization_type=AmortizationType.LINEAR
                        )
                    ]
                ),
                ipa.swap.LegDefinition(
                    direction=Direction.RECEIVED,
                    notional_amount="10000000",
                    notional_ccy="GBP",
                    interest_type=InterestType.FLOAT,
                    interest_payment_frequency=Frequency.SEMI_ANNUAL,
                    index_reset_frequency=Frequency.SEMI_ANNUAL,
                    interest_calculation_method=DayCountBasis.DCB_ACTUAL_360,
                    payment_business_day_convention=BusinessDayConvention.MODIFIED_FOLLOWING,
                    payment_roll_convention=DateRollingConvention.SAME,
                    payment_business_days="UKG",
                    spread_bp=20,
                    index_name="LIBOR",
                    index_tenor="6M",
                    index_reset_type=IndexResetType.IN_ADVANCE,
                    amortization_schedule=[
                        AmortizationItem(
                            remaining_notional=200000,
                            amortization_frequency=AmortizationFrequency.EVERY2ND_COUPON,
                            amortization_type=AmortizationType.LINEAR
                        )
                    ]

                )
            ]
        ),
        calculation_params=ipa.swap.CalculationParams(discounting_tenor="ON"),
        fields=[
            "InstrumentTag",
            "InstrumentDescription",
            "FixedRate",
            "MarketValueInDealCcy",
            "PV01Bp",
            "DiscountCurveName",
            "ForwardCurveName",
            "CashFlowDatesArray",
            "CashFlowTotalAmountsInDealCcyArray",
            "CashFlowDiscountFactorsArray",
            "CashFlowResidualAmountsInDealCcyArray",
            "ErrorMessage"
        ],
        outputs=[
            "Data",
            "Headers"
        ]
    )
    assert not df.empty


def test_empty_definition():
    with pytest.raises(RequiredError):
        ipa.swap.Definition()


def test_minimum_definition():
    ipa.swap.Definition(
        end_date="date",
        legs=[ipa.swap.LegDefinition(
            direction="Paid",
            interest_type="Fixed",
            notional_ccy="",
            interest_payment_frequency="Everyday",
            interest_calculation_method="Dcb_30E_360_ISMA",
        )]
    )


def test_definition_end_date_empty():
    with pytest.raises(RequiredError):
        ipa.swap.Definition(
            legs=[ipa.swap.LegDefinition(
                direction="Paid",
                interest_type="Fixed",
                notional_ccy="",
                interest_payment_frequency="Everyday",
                interest_calculation_method="Dcb_30E_360_ISMA",
            )]
        )


def test_definition_instrument_code_empty():
    with pytest.raises(RequiredError):
        ipa.swap.Definition(
            end_date="date",
        )


def test_empty_leg_definition():
    with pytest.raises(TypeError):
        ipa.swap.LegDefinition()


def test_minimum_leg_definition():
    ipa.swap.LegDefinition(
        direction="Paid",
        interest_type="Fixed",
        notional_ccy="",
        interest_payment_frequency="Everyday",
        interest_calculation_method="Dcb_30E_360_ISMA",
    )


def test_get_swap_analytics_async(open_session_for_ipa):
    tasks = asyncio.gather(ipa.FinancialContracts.get_swap_analytics_async(
        universe=ipa.swap.Definition(
            instrument_tag="AED_AM1A",
            template="EUR_AB6E",
            tenor="5Y",
        )))
    asyncio.get_event_loop().run_until_complete(tasks)
    response, *_ = tasks.result()
    response_tests.success_response_tests(response)


@pytest.mark.parametrize(
    argnames="input_data",
    ids=[
        "Definition",
        "LegDefinition",
        "CalculationParams"
    ],
    argvalues=[
        (Definition, {
            "instrument_tag": "instrument_tag",
            "instrument_code": "instrument_code",
            "trade_date": "trade_date",
            "start_date": "start_date",
            "end_date": "end_date",
            "tenor": "tenor",
            "legs": [LegDefinition(
                direction=Direction.RECEIVED,
                interest_type=InterestType.STEPPED,
                notional_ccy="notional_ccy",
                interest_payment_frequency=Frequency.BI_MONTHLY,
                interest_calculation_method=DayCountBasis.DCB_30_360_US,
            )],
            "is_non_deliverable": True,
            "settlement_ccy": "settlement_ccy",
            "template": "template",
        }),
        (LegDefinition, {
            # "instrument_tag": "instrument_tag",
            "leg_tag": "leg_tag",
            "direction": Direction.RECEIVED,
            "interest_type": InterestType.FIXED,
            "notional_ccy": "notional_ccy",
            "notional_amount": 6.6,
            "fixed_rate_percent": 7.7,
            "index_name": "index_name",
            "index_tenor": "index_tenor",
            "spread_bp": 10.10,
            "interest_payment_frequency": Frequency.EVERY14_DAYS,
            "interest_calculation_method": DayCountBasis.DCB_30_360_ISDA,
            "accrued_calculation_method": DayCountBasis.DCB_30_365_BRAZIL,
            "payment_business_day_convention": BusinessDayConvention.NEXT_BUSINESS_DAY,
            "payment_roll_convention": DateRollingConvention.LAST28,
            "index_reset_frequency": Frequency.BI_MONTHLY,
            "index_reset_type": IndexResetType.IN_ARREARS,
            "index_fixing_lag": 18,
            "first_regular_payment_date": "first_regular_payment_date",
            "last_regular_payment_date": "last_regular_payment_date",
            "amortization_schedule": [AmortizationItem()],
            "payment_business_days"

            : "payment_business_days",
            "notional_exchange": NotionalExchange.BOTH,
            "adjust_interest_to_payment_date": AdjustInterestToPaymentDate.ADJUSTED,
            "index_compounding_method": IndexCompoundingMethod.COMPOUNDED,
            "interest_payment_delay": 26,
            "stub_rule": StubRule.SHORT_FIRST_PRO_RATA,
            "index_fixing_ric": "index_fixing_ric",
            # "upfront_amount": 29.29,
        }),
        (CalculationParams, {
            "report_ccy": "report_ccy",
            "market_data_date": "market_data_date",
            "index_convexity_adjustment_integration_method": IndexConvexityAdjustmentIntegrationMethod.RIEMANN_SUM,
            "index_convexity_adjustment_method": IndexConvexityAdjustmentMethod.BLACK_SCHOLES,
            "discounting_ccy": "discounting_ccy",
            "discounting_tenor": "discounting_tenor",
            "market_value_in_deal_ccy": 4.4,
            "valuation_date": "valuation_date",
        }),
    ])
def test_parameter(input_data):
    cls, kwargs = input_data
    args_names = list(kwargs.keys())
    inst = cls(**kwargs)

    s = signature(cls.__init__)
    assert len(s.parameters) == (len(args_names) + 1)  # +1 for (self)

    assert conftest.has_property_names_in_class(cls, args_names), set(args_names) - set(conftest.get_property_names(cls))

    for k, v in kwargs.items():
        attr = getattr(inst, k)
        assert attr == v, k
