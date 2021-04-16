from inspect import signature

import pytest

from refinitiv.dataplatform.content.ipa.enum_types import *
from refinitiv.dataplatform.content.ipa.models import *
from refinitiv.dataplatform.content.ipa.contracts.option import *
import conftest
import refinitiv.dataplatform as rdp
from refinitiv.dataplatform import ContentFactory


def test_option(open_session_for_ipa):
    """
    {
      "fields": [
        "MarketValueInDealCcy",
        "DeltaPercent",
        "GammaPercent",
        "RhoPercent",
        "ThetaPercent",
        "VegaPercent"
      ],
      "outputs": [
        "Data",
        "Headers"
      ],
      "universe": [
        {
          "instrumentType": "Option",
          "instrumentDefinition": {
            "instrumentCode": "FCHI560000L1.p",
            "underlyingType": "Eti"
          }
        }
      ]
    }

    """
    df = rdp.get_option_analytics(
        universe=rdp.ipa.option.Definition(
            instrument_code="FCHI560000L1.p",
            underlying_type=rdp.ipa.option.UnderlyingType.ETI
        ),
        outputs=[
            "Data",
            "Headers"
        ],
        fields=[
            "MarketValueInDealCcy",
            "DeltaPercent",
            "GammaPercent",
            "RhoPercent",
            "ThetaPercent",
            "VegaPercent"
        ]
    )
    assert not df.empty, ContentFactory._last_error_status


@pytest.mark.parametrize(
    argnames="input_data",
    ids=[
        "EtiDoubleBarriersDefinition",
        "Definition",
        "EtiFixingInfo",
        "CalculationParams",
        "DoubleBinaryDefinition",
        "DoubleBarrierInfo",
        "DoubleBarrierDefinition",
        "FxBinaryDefinition",
        "FxBarrierDefinition",
        "AverageInfo",
        "EtiUnderlyingDefinition",
        "CBBCDefinition",
        "EtiBinaryDefinition",
        "EtiBarrierDefinition"
    ],
    argvalues=[
        (EtiDoubleBarriersDefinition, {
            "barriers_definition": [EtiBarrierDefinition()],
        }),
        (Definition, {
            "double_barrier_definition": DoubleBarrierDefinition(barrier_down=DoubleBarrierInfo(in_or_out="in_or_out")),
            "double_binary_definition": DoubleBinaryDefinition(),
            "dual_currency_definition": DualCurrencyDefinition(),
            "notional_amount": 1,
            "notional_ccy": 1,
            "tenor": 1,
            "instrument_tag": UnderlyingType.ETI,
            "instrument_code": "instrument_code",
            "end_date": "end_date",
            "asian_definition": EtiFixingInfo(),
            "barrier_definition": EtiBarrierDefinition(),
            "binary_definition": EtiBinaryDefinition(),
            "buy_sell": BuySell.SELL,
            "call_put": CallPut.CALL,
            "cbbc_definition": CBBCDefinition(),
            "double_barriers_definition": EtiDoubleBarriersDefinition(barriers_definition=[EtiBarrierDefinition()]),
            "exercise_style": ExerciseStyle.AMER,
            "underlying_definition": EtiUnderlyingDefinition(),
            "underlying_type": UnderlyingType.ETI,
            "deal_contract": 14,
            "lot_size": 15.15,
            "strike": 16.16
        }),
        (EtiFixingInfo, {
            "average_so_far": 123,
            "average_type": AverageType.GEOMETRIC_STRIKE,
            "fixing_frequency": FixingFrequency.WEEKLY,
            "fixing_calendar": "fixing_calendar",
            "fixing_end_date": "fixing_end_date",
            "fixing_start_date": "fixing_start_date",
            "include_holidays": True,
            "include_week_ends": True,
        }),
        (CalculationParams, {
            "atm_volatility_object": BidAskMid(),
            "butterfly_10d_object": BidAskMid(),
            "butterfly_25d_object": BidAskMid(),
            "domestic_deposit_rate_percent_object": BidAskMid(),
            "foreign_deposit_rate_percent_object": BidAskMid(),
            "forward_points_object": BidAskMid(),
            "fx_spot_object": BidAskMid(),
            "fx_swap_calculation_method": FxSwapCalculationMethod.DEPOSIT_CCY1_IMPLIED_FROM_FX_SWAP,
            "implied_volatility_object": BidAskMid(),
            "interpolation_weight": InterpolationWeight(),
            "option_price_side": PriceSide.BID,
            "option_time_stamp": TimeStamp.DEFAULT,
            "price_side": PriceSide.MID,
            "pricing_model_type": PricingModelType.BINOMIAL,
            "risk_reversal_10d_object": BidAskMid(),
            "risk_reversal_25d_object": BidAskMid(),
            "underlying_price_side": PriceSide.ASK,
            "underlying_time_stamp": TimeStamp.OPEN,
            "volatility_model": VolatilityModel.CUBIC_SPLINE,
            "volatility_type": VolatilityType.IMPLIED,
            "cutoff_time": "cutoff_time",
            "cutoff_time_zone": "cutoff_time_zone",
            "market_value_in_deal_ccy": 23.23,
            "risk_free_rate_percent": 24.24,
            "underlying_price": 25.25,
            "valuation_date": "valuation_date",
            "volatility_percent": 27.27,
            "market_data_date": "market_data_date"
        }),
        (DoubleBinaryDefinition, {
            "double_binary_type": DoubleBinaryType.DOUBLE_NO_TOUCH,
            "settlement_type": SettlementType.CASH,
            "payout_amount": 3.3,
            "payout_ccy": "payout_ccy",
            "trigger_down": 5.5,
            "trigger_up": 6.6,
        }),
        (DoubleBarrierInfo, {
            "in_or_out": InOrOut.IN,
            "level": 2.2,
            "rebate_amount": 3.3,
        }),
        (DoubleBarrierDefinition, {
            "barrier_down": DoubleBarrierInfo(),
            "barrier_mode": BarrierMode.EARLY_END_WINDOW,
            "barrier_up": DoubleBarrierInfo(),
        }),
        (FxBinaryDefinition, {
            "binary_type": FxBinaryType.ONE_TOUCH_DEFERRED,
            "settlement_type": SettlementType.UNDEFINED,
            "payout_amount": 3.3,
            "payout_ccy": "payout_ccy",
            "trigger": 5.5,
        }),
        (FxBarrierDefinition, {
            "barrier_mode": BarrierMode.EUROPEAN,
            "in_or_out": InOrOut.OUT,
            "up_or_down": UpOrDown.UP,
            "level": 4.4,
            "rebate_amount": 5.5,
            "window_end_date": "window_end_date",
            "window_start_date": "window_start_date",
        }),
        (AverageInfo, {
            "average_type": AverageType.GEOMETRIC_STRIKE,
            "fixing_frequency": FixingFrequency.ANNUAL,
            "average_so_far": 3.3,
            "fixing_ric_source": "str",
            "fixing_start_date": "str",
            "include_holidays": True,
            "include_week_ends": True,
        }),
        (EtiUnderlyingDefinition, {
            "instrument_code": "instrument_code",
        }),
        (CBBCDefinition, {
            "conversion_ratio": 1.1,
            "level": 2.2,
        }),
        (EtiBinaryDefinition, {
            "notional_amount": 1.1,
            "binary_type": EtiBinaryType.DIGITAL,
            "up_or_down": UpOrDown.DOWN,
            "level": 4.4,
        }),
        (EtiBarrierDefinition, {
            "barrier_style": BarrierStyle.AMERICAN,
            "in_or_out": InOrOut.IN,
            "up_or_down": UpOrDown.DOWN,
            "level": 3.3,
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
        if hasattr(v, "value") and attr == "Eti":
            assert attr == v.value, k
        else:
            assert attr == v, k
