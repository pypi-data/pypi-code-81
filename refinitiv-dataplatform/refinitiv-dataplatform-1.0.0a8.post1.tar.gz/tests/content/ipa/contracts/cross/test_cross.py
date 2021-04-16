from inspect import signature

import pytest
import refinitiv.dataplatform as rdp

from refinitiv.dataplatform.content import ipa
from refinitiv.dataplatform.content.ipa.contracts.cross import Definition, LegDefinition, CalculationParams
from refinitiv.dataplatform.content.ipa.enum_types import *
from refinitiv.dataplatform.content.ipa.enum_types import FxCrossType, PriceSide, BuySell, FxLegType
import conftest


def test_fx_cross_1(open_session_for_ipa):
    """
    {
      "fields": [
        "ValuationDate",
        "InstrumentDescription",
        "EndDate",
        "FxSwapsCcy1Ccy2",
        "MarketValueInReportCcy",
        "DeltaAmountInReportCcy",
        "RhoContraCcyAmountInReportCcy",
        "RhoDealCcyAmountInReportCcy"
      ],
      "outputs": [
        "Data",
        "Headers"
      ],
      "universe": [
        {
          "instrumentType": "FxCross",
          "instrumentDefinition": {
            "fxCrossType": "FxNonDeliverableForward",
            "fxCrossCode": "USDINR",
            "legs": [
              {
                "dealAmount": 1000000,
                "contraAmount": 65762500,
                "dealCcyBuySell": "Buy",
                "tenor": "4Y"
              }
            ]
          },
          "pricingParameters": {
            "valuationDate": "2017-11-15T00:00:00Z"
          }
        }
      ]
    }
    """
    df = rdp.get_cross_analytics(
        universe=[
            ipa.cross.Definition(
                fx_cross_type=ipa.enum_types.FxCrossType.FX_NON_DELIVERABLE_FORWARD,
                fx_cross_code="USDINR",
                legs=[
                    ipa.cross.LegDefinition(
                        deal_amount=1000000,
                        contra_amount=65762500,
                        deal_ccy_buy_sell=ipa.enum_types.BuySell.BUY,
                        tenor="4Y"
                    )
                ],
            ),
        ],
        calculation_params=ipa.cross.CalculationParams(
            valuation_date="2017-11-15T00:00:00Z"
        ),
        fields=[
            "ValuationDate",
            "InstrumentDescription",
            "EndDate",
            "FxSwapsCcy1Ccy2",
            "MarketValueInReportCcy",
            "DeltaAmountInReportCcy",
            "RhoContraCcyAmountInReportCcy",
            "RhoDealCcyAmountInReportCcy"
        ],
        outputs=[
            "Data",
            "Headers"
        ]
    )

    assert not df.empty


def test_fx_cross_2(open_session_for_ipa):
    """
    {
      "fields": [
        "InstrumentTag",
        "ValuationDate",
        "InstrumentDescription",
        "FxOutrightCcy1Ccy2",
        "ErrorCode",
        "ErrorMessage"
      ],
      "universe": [
        {
          "instrumentDefinition": {
            "instrumentTag": "00102700008910C",
            "fxCrossType": "FxForward",
            "fxCrossCode": "USDEUR",
            "legs": [
              {
                "endDate": "2015-04-09T00:00:00Z"
              }
            ]
          },
          "pricingParameters": {
            "valuationDate": "2015-02-02T00:00:00Z",
            "priceSide": "Mid"
          },
          "instrumentType": "FxCross"
        }
      ],
      "outputs": [
        "Data",
        "Headers"
      ]
    }
    """
    df = rdp.get_cross_analytics(
        universe=[
            ipa.cross.Definition(
                instrument_tag="00102700008910C",
                fx_cross_type=ipa.enum_types.FxCrossType.FX_FORWARD,
                fx_cross_code="USDEUR",
                legs=[
                    ipa.cross.LegDefinition(
                        end_date="2015-04-09T00:00:00Z"
                    )
                ],
            ),
        ],
        calculation_params=ipa.cross.CalculationParams(
            valuation_date="2015-02-02T00:00:00Z",
            price_side=PriceSide.MID
        ),
        fields=[
            "InstrumentTag",
            "ValuationDate",
            "InstrumentDescription",
            "FxOutrightCcy1Ccy2",
            "ErrorCode",
            "ErrorMessage"
        ],
        outputs=[
            "Data",
            "Headers"
        ]
    )
    assert not df.empty


def test_fx_cross_3(open_session_for_ipa):
    """
    {
      "fields": [
        "InstrumentTag",
        "ValuationDate",
        "InstrumentDescription",
        "EndDate",
        "FxSwapsCcy1",
        "FxSwapsCcy2",
        "FxSwapsCcy1Ccy2",
        "FxOutrightCcy1Ccy2",
        "ErrorCode",
        "ErrorMessage"
      ],
      "outputs": [
        "Data",
        "Headers"
      ],
      "universe": [
        {
          "instrumentType": "FxCross",
          "instrumentDefinition": {
            "instrumentTag": "1Y-CHFJPY",
            "fxCrossType": "FxSwap",
            "fxCrossCode": "CHFJPY",
            "legs": [
              {
                "dealCcyBuySell": "Buy",
                "fxLegType": "SwapNear",
                "dealAmount": 1000000,
                "contraAmount": 897008.3,
                "tenor": "1M"
              },
              {
                "dealCcyBuySell": "Sell",
                "fxLegType": "SwapFar",
                "dealAmount": 1000000,
                "contraAmount": 900000,
                "tenor": "1Y"
              }
            ]
          },
          "pricingParameters": {
            "valuationDate": "2018-02-17T00:00:00Z",
            "priceSide": "Ask"
          }
        }
      ]
    }
    """
    df = rdp.get_cross_analytics(
        universe=ipa.cross.Definition(
            instrument_tag="1Y-CHFJPY",
            fx_cross_type=ipa.enum_types.FxCrossType.FX_SWAP,
            fx_cross_code="CHFJPY",
            legs=[
                ipa.cross.LegDefinition(
                    deal_ccy_buy_sell=ipa.enum_types.BuySell.BUY,
                    fx_leg_type=ipa.enum_types.FxLegType.SWAP_NEAR,
                    deal_amount=1000000,
                    contra_amount=897008.3,
                    tenor="1M"
                ),
                ipa.cross.LegDefinition(
                    deal_ccy_buy_sell=ipa.enum_types.BuySell.SELL,
                    fx_leg_type=ipa.enum_types.FxLegType.SWAP_FAR,
                    deal_amount=1000000,
                    contra_amount=900000,
                    tenor="1Y"
                ),
            ],
        ),
        calculation_params=ipa.cross.CalculationParams(
            valuation_date="2018-02-17T00:00:00Z",
            price_side=ipa.enum_types.PriceSide.ASK
        ),
        fields=[
            "InstrumentTag",
            "ValuationDate",
            "InstrumentDescription",
            "EndDate",
            "FxSwapsCcy1",
            "FxSwapsCcy2",
            "FxSwapsCcy1Ccy2",
            "FxOutrightCcy1Ccy2",
            "ErrorCode",
            "ErrorMessage"
        ],
        outputs=[
            "Data",
            "Headers"
        ]
    )
    assert not df.empty


def test_get_cross_analytics_fx_forward(open_session_for_ipa):
    df = rdp.get_cross_analytics(
        universe=ipa.cross.Definition(
            instrument_tag="00102700008910C",
            fx_cross_type=FxCrossType.FX_FORWARD,
            fx_cross_code="USDEUR",
            traded_cross_rate="",
            traded_swap_points="",
            reference_spot_rate="",
            reference_swap_points="",
            ndf_fixing_settlement_ccy="",
            legs=[ipa.cross.LegDefinition(end_date="2015-04-09T00:00:00Z")],
        ),
        calculation_params=ipa.cross.CalculationParams(
            valuation_date="2015-02-02T00:00:00Z",
            price_side=PriceSide.MID
        ),
        fields=[
            "InstrumentTag",
            "ValuationDate",
            "InstrumentDescription",
            "FxOutrightCcy1Ccy2",
            "ErrorCode",
            "ErrorMessage"
        ],
        outputs=[
            "Data",
            "Headers"
        ]
    )

    assert not df.empty


def test_get_cross_analytics_fx_swap(open_session_for_ipa):
    df = rdp.get_cross_analytics(
        universe=ipa.cross.Definition(
            instrument_tag="1Y-CHFJPY",
            fx_cross_type=FxCrossType.FX_SWAP,
            traded_cross_rate="",
            traded_swap_points="",
            reference_spot_rate="",
            reference_swap_points="",
            ndf_fixing_settlement_ccy="",
            legs=[
                ipa.cross.LegDefinition(
                    deal_ccy_buy_sell=BuySell.BUY,
                    fx_leg_type=FxLegType.SWAP_NEAR,
                    deal_amount=1000000,
                    contra_amount=897008.3,
                    tenor="1M"
                ),
                ipa.cross.LegDefinition(
                    deal_ccy_buy_sell=BuySell.SELL,
                    fx_leg_type=FxLegType.SWAP_FAR,
                    deal_amount=1000000,
                    contra_amount=900000,
                    tenor="1Y"
                )
            ],
        ),
        calculation_params=ipa.cross.CalculationParams(
            valuation_date="2018-02-17T00:00:00Z",
            price_side=PriceSide.ASK
        ),
        fields=[
            "InstrumentTag",
            "ValuationDate",
            "InstrumentDescription",
            "EndDate",
            "FxSwapsCcy1",
            "FxSwapsCcy2",
            "FxSwapsCcy1Ccy2",
            "FxOutrightCcy1Ccy2",
            "ErrorCode",
            "ErrorMessage"
        ],
        outputs=[
            "Data",
            "Headers"
        ]
    )

    assert not df.empty


def test_get_cross_analytics_fx_non_deliverable_forward(open_session_for_ipa):
    df = rdp.get_cross_analytics(
        universe=ipa.cross.Definition(
            instrument_tag="1Y-CHFJPY",
            fx_cross_type=FxCrossType.FX_NON_DELIVERABLE_FORWARD,
            fx_cross_code="USDINR",
            traded_cross_rate="",
            traded_swap_points="",
            reference_spot_rate="",
            reference_swap_points="",
            ndf_fixing_settlement_ccy="",
            legs=[
                ipa.cross.LegDefinition(
                    deal_amount=1000000,
                    contra_amount=65762500,
                    deal_ccy_buy_sell=BuySell.BUY,
                    tenor="4Y"
                )
            ],
        ),
        calculation_params=ipa.cross.CalculationParams(
            valuation_date="2017-11-15T00:00:00Z",
        ),
        fields=[
            "ValuationDate",
            "InstrumentDescription",
            "EndDate",
            "FxSwapsCcy1Ccy2",
            "MarketValueInReportCcy",
            "DeltaAmountInReportCcy",
            "RhoContraCcyAmountInReportCcy",
            "RhoDealCcyAmountInReportCcy"
        ],
        outputs=[
            "Data",
            "Headers"
        ]
    )

    assert not df.empty


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
            "legs": [LegDefinition()],
            "fx_cross_type": FxCrossType.FX_FORWARD,
            "fx_cross_code": "fx_cross_code",
            "ndf_fixing_settlement_ccy": "ndf_fixing_settlement_ccy",
            "reference_spot_rate": 6.6,
            "traded_cross_rate": 7.7,
            "traded_swap_points": 8.8,
            "reference_swap_points": 9.9
        }),
        (LegDefinition, {
            # "start_date": "start_date",
            "end_date": "end_date",
            "tenor": "tenor",
            "leg_tag": "leg_tag",
            "deal_ccy_buy_sell": BuySell.BUY,
            "fx_leg_type": FxLegType.FX_SPOT,
            "contra_amount": 7.7,
            "deal_countra_amount": 8.8,
            # "contra_ccy": "contra_ccy",
            "deal_amount": 9.9,
            "deal_ccy": "deal_ccy",
            # "start_tenor": "start_tenor",
        }),
        (CalculationParams, {
            "market_data_date": "market_data_date",
            "fx_swap_calculation_method": FxSwapCalculationMethod.DEPOSIT_CCY2_IMPLIED_FROM_FX_SWAP,
            "price_side": PriceSide.ASK,
            # "user_turn_dates": ["user_turn_dates"],
            "ignore_ref_ccy_holidays": True,
            # "ignore_usd_holidays": False,
            # "one_day_values": "one_day_values",
            # "roll_over_time_policy": "roll_over_time_policy",
            # "spread_margin_in_bp": 8.8,
            # "turns_calibration": "turns_calibration",
            "valuation_date": "valuation_date",
            "report_ccy": "report_ccy",
            "calc_end_from_fwd_start": True,
            "calc_end_from_pre_spot_start": True
        })
    ])
def test_parameter(input_data):
    cls, kwargs = input_data
    args_names = list(kwargs.keys())
    inst = cls(**kwargs)

    s = signature(cls.__init__)
    assert len(s.parameters) == (len(args_names) + 1), cls  # +1 for (self)

    assert conftest.has_property_names_in_class(cls, args_names), set(args_names) ^ set(
        conftest.get_property_names(cls))

    for k, v in kwargs.items():
        attr = getattr(inst, k)
        assert attr == v, k
