import asyncio
from inspect import signature

import pytest

from refinitiv.dataplatform.content import ipa
from refinitiv.dataplatform.content.ipa.contracts.swap import Definition as SwapDefinition
from refinitiv.dataplatform.content.ipa.contracts.swaption import *
from refinitiv.dataplatform.content.ipa.enum_types import *
import conftest
import response_tests
import refinitiv.dataplatform as rdp


def test_get_swaption_analytics_1(open_session_for_ipa):
    """
    {
      "outputs": [
        "Data",
        "Headers",
        "MarketData"
      ],
      "universe": [
        {
          "instrumentType": "Swaption",
          "instrumentDefinition": {
            "instrumentTag": "BermudanEURswaption",
            "settlementType": "Cash",
            "tenor": "7Y",
            "strikePercent": 2.75,
            "buySell": "Buy",
            "callPut": "Call",
            "exerciseStyle": "BERM",
            "bermudanSwaptionDefinition": {
              "ExerciseScheduleType": "FloatLeg",
              "NotificationPeriod": 0
            },
            "underlyingDefinition": {
              "tenor": "3Y",
              "template": "EUR_AB6E"
            }
          },
          "pricingParameters": {
            "valuationDate": "2020-04-24",
            "nbIterations": 80
          },
          "marketData": {
            "interestRateVolatilitySurfaces": [
              {
                "surfaceParameters": {
                  "inputVolatilityType": "NormalizedVolatility"
                }
              }
            ]
          }
        }
      ]
    }
    """
    df = rdp.get_swaption_analytics(
        universe=ipa.swaption.Definition(
            instrument_tag="BermudanEURswaption",
            settlement_type=SwaptionSettlementType.CASH,
            tenor="7Y",
            strike_percent=2.75,
            buy_sell=BuySell.BUY,
            call_put=CallPut.CALL,
            exercise_style=ExerciseStyle.BERM,
            bermudan_swaption_definition=BermudanSwaptionDefinition(
                exercise_schedule_type=ExerciseScheduleType.FLOAT_LEG,
                notification_days=0
            ),
            underlying_definition=SwapDefinition(
                tenor="3Y",
                template="EUR_AB6E"
            )
        ),
        calculation_params=ipa.swaption.CalculationParams(valuation_date="2020-04-24", nb_iterations=80),
        outputs=[
            "Data",
            "Headers",
            "MarketData"
        ]
    )
    assert not bool(df.ErrorMessage[0]), df.ErrorMessage[0]
    assert not df.empty


def test_get_swaption_analytics_2(open_session_for_ipa):
    """
    {
      "fields": [
        "MarketValueInDealCcy",
        "DeltaPercent",
        "GammaPercent",
        "ThetaPercent",
        "ErrorCode",
        "ErrorMessage"
      ],
      "outputs": [
        "Data",
        "Headers",
        "MarketData"
      ],
      "universe": [
        {
          "instrumentType": "Swaption",
          "instrumentDefinition": {
            "instrumentTag": "myEURswaption",
            "instrumentCode": "",
            "settlementType": "Cash",
            "tenor": "5Y",
            "strikePercent": 2,
            "buySell": "Buy",
            "callPut": "Call",
            "exerciseStyle": "EURO",
            "underlyingDefinition": {
              "tenor": "5Y",
              "template": "EUR_AB6E"
            }
          },
          "pricingParameters": {
            "valuationDate": "2020-04-24"
          }
        }
      ],
      "marketData": {}
    }
    """
    df = rdp.get_swaption_analytics(
        fields=[
            "MarketValueInDealCcy",
            "DeltaPercent",
            "GammaPercent",
            "ThetaPercent",
            "ErrorCode",
            "ErrorMessage"
        ],
        outputs=[
            "Data",
            "Headers",
            "MarketData"
        ],
        universe=ipa.swaption.Definition(
            instrument_tag="myEURswaption",
            settlement_type=SwaptionSettlementType.CASH,
            tenor="5Y",
            strike_percent=2,
            buy_sell=BuySell.BUY,
            call_put=CallPut.CALL,
            exercise_style=ExerciseStyle.EURO,
            underlying_definition=SwapDefinition(
                tenor="5Y",
                template="EUR_AB6E"
            )
        ),
        calculation_params=ipa.swaption.CalculationParams(valuation_date="2020-04-24"),
    )
    assert not bool(df.ErrorMessage[0]), df.ErrorMessage[0]
    assert not df.empty


def test_get_swaption_analytics_async(open_session_for_ipa):
    tasks = asyncio.gather(ipa.FinancialContracts.get_swaption_analytics_async(
        universe=ipa.swaption.Definition(
            instrument_tag="BermudanEURswaption",
            settlement_type=SwaptionSettlementType.CASH,
            tenor="7Y",
            strike_percent=2.75,
            buy_sell=BuySell.BUY,
            call_put=CallPut.CALL,
            exercise_style=ExerciseStyle.BERM,
            bermudan_swaption_definition=BermudanSwaptionDefinition(
                exercise_schedule_type=ExerciseScheduleType.FLOAT_LEG,
                notification_days=0
            ),
            underlying_definition=SwapDefinition(
                tenor="3Y",
                template="EUR_AB6E"
            )
        ),
        calculation_params=ipa.swaption.CalculationParams(valuation_date="2020-04-24", nb_iterations=80),
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
            "Headers",
            "MarketData"
        ]))
    asyncio.get_event_loop().run_until_complete(tasks)
    response, *_ = tasks.result()
    response_tests.success_response_tests(response)


@pytest.mark.parametrize(
    argnames="input_data",
    ids=[
        "Definition",
        "CalculationParams",
        "SwaptionMarketDataRule",
        "BermudanSwaptionDefinition"
    ],
    argvalues=[
        (Definition, {
            "instrument_tag": "instrument_tag",
            "end_date": "end_date",
            "tenor": "tenor",
            "bermudan_swaption_definition": BermudanSwaptionDefinition(),
            "buy_sell": BuySell.BUY,
            "call_put": CallPut.PUT,
            "exercise_style": ExerciseStyle.EURO,
            "settlement_type": SwaptionSettlementType.CASH,
            "underlying_definition": SwapDefinition(tenor="5Y", template="template"),
            "strike_percent": 10.10,
        }),
        (CalculationParams, {
            "market_data_rule": SwaptionMarketDataRule(),
            "market_value_in_deal_ccy": 3.3,
            "nb_iterations": 4,
            "valuation_date": "valuation_date",
        }),
        (SwaptionMarketDataRule, {
            "discount": "discount",
            "forward": "forward",
        }),
        (BermudanSwaptionDefinition, {
            "exercise_schedule": ["exercise_schedule"],
            "exercise_schedule_type": ExerciseScheduleType.FIXED_LEG,
            "notification_days": 3,
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
