import asyncio
from inspect import signature

import pytest
import refinitiv.dataplatform as rdp

from refinitiv.dataplatform.content.ipa import AmortizationItem
from refinitiv.dataplatform.content.ipa.contracts.capfloor import *
from refinitiv.dataplatform.content.ipa.enum_types import *
import conftest
import response_tests


def test_get_capfloor_analytics(open_session_for_ipa):
    """
    {
      "universe": [
        {
          "instrumentType": "CapFloor",
          "instrumentDefinition": {
            "notionalCcy": "EUR",
            "startDate": "2019-02-11",
            "amortizationSchedule": [
              {
                "startDate": "2021-02-11",
                "endDate": "2022-02-11",
                "amount": 100000,
                "amortizationType": "Schedule"
              },
              {
                "startDate": "2022-02-11",
                "endDate": "2023-02-11",
                "amount": -100000,
                "amortizationType": "Schedule"
              }
            ],
            "tenor": "5Y",
            "buySell": "Sell",
            "notionalAmount": 10000000,
            "interestPaymentFrequency": "Monthly",
            "capStrikePercent": 1
          },
          "pricingParameters": {
            "skipFirstCapFloorlet": true,
            "valuationDate": "2020-02-07"
          }
        }
      ]
    }
    """
    df = rdp.get_capfloor_analytics(
        universe=rdp.ipa.capfloor.Definition(
            notional_ccy="EUR",
            start_date="2019-02-11",
            amortization_schedule=[
                AmortizationItem(
                    start_date="2021-02-11",
                    end_date="2022-02-11",
                    amount=100000,
                    amortization_type="Schedule"
                ),
                AmortizationItem(
                    start_date="2022-02-11",
                    end_date="2023-02-11",
                    amount=-100000,
                    amortization_type="Schedule"
                ),
            ],
            tenor="5Y",
            buy_sell="Sell",
            notional_amount=10000000,
            interest_payment_frequency="Monthly",
            cap_strike_percent=1
        ),
        calculation_params=rdp.ipa.capfloor.CalculationParams(
            skip_first_cap_floorlet=True,
            valuation_date="2020-02-07"
        ),
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
    assert not bool(df.ErrorMessage[0]), df.ErrorMessage[0]
    assert not df.empty


def test_get_capfloor_analytics_async(open_session_for_ipa):
    """
    {
      "universe": [
        {
          "instrumentType": "CapFloor",
          "instrumentDefinition": {
            "notionalCcy": "EUR",
            "startDate": "2020-02-11",
            "tenor": "4Y",
            "buySell": "Buy",
            "notionalAmount": 10000000,
            "interestPaymentFrequency": "Quarterly",
            "capStrikePercent": 1,
            "floorStrikePercent": -1
          },
          "pricingParameters": {
            "skipFirstCapFloorlet": true,
            "valuationDate": "2020-02-07"
          }
        }
      ]
    }
    """
    tasks = asyncio.gather(rdp.ipa.FinancialContracts.get_capfloor_analytics_async(
        universe=rdp.ipa.capfloor.Definition(
            notional_ccy="EUR",
            start_date="2020-02-11",
            tenor="4Y",
            buy_sell="Buy",
            notional_amount=10000000,
            interest_payment_frequency="Quarterly",
            cap_strike_percent=1,
            floor_strike_percent=-1
        ),
        calculation_params=rdp.ipa.capfloor.CalculationParams(
            skip_first_cap_floorlet=True,
            valuation_date="2020-02-07"
        ),
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
        ]))
    asyncio.get_event_loop().run_until_complete(tasks)
    response, *_ = tasks.result()
    response_tests.success_response_tests(response)


@pytest.mark.parametrize(
    argnames="input_data",
    ids=[
        "Definition",
        "CalculationParams",
        "CapFloorMarketDataRule"
    ],
    argvalues=[
        (Definition, {
            "instrument_tag": "instrument_tag",
            "start_date": "start_date",
            "end_date": "end_date",
            "tenor": "tenor",
            "notional_ccy": "notional_ccy",
            "notional_amount": 6.6,
            "index_name": "index_name",
            "index_tenor": "index_tenor",
            "interest_payment_frequency": Frequency.ANNUAL,
            "interest_calculation_method": DayCountBasis.DCB_30_360,
            "payment_business_day_convention": BusinessDayConvention.BBSW_MODIFIED_FOLLOWING,
            "payment_roll_convention": DateRollingConvention.LAST,
            "index_reset_frequency": Frequency.ANNUAL,
            "index_reset_type": IndexResetType.IN_ADVANCE,
            "index_fixing_lag": 15,
            "amortization_schedule": [AmortizationItem()],
            "adjust_interest_to_payment_date": AdjustInterestToPaymentDate.ADJUSTED,
            "buy_sell": BuySell.BUY,
            "cap_strike_percent": 19.19,
            "floor_strike_percent": 20.20,
            "index_fixing_ric": "index_fixing_ric",
            "stub_rule": StubRule.MATURITY
        }),
        (CalculationParams, {
            "index_convexity_adjustment_integration_method": IndexConvexityAdjustmentIntegrationMethod.RIEMANN_SUM,
            "index_convexity_adjustment_method": IndexConvexityAdjustmentMethod.BLACK_SCHOLES,
            "market_value_in_deal_ccy": 2.2,
            "report_ccy": "str",
            "skip_first_cap_floorlet": True,
            "valuation_date": "valuation_date",
        }),
        (CapFloorMarketDataRule, {
            "counterparty_credit_curve_tag": "counterparty_credit_curve_tag",
            "discount": "discount",
            "discount_paid": "discount_paid",
            "forward": "forward",
            "self_credit_curve_tag": "self_credit_curve_tag",
        }),
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
