import asyncio
from inspect import signature

import pytest

from refinitiv.dataplatform import RequiredError
import refinitiv.dataplatform as rdp

from refinitiv.dataplatform.content.ipa.contracts.cds import Definition, CalculationParams, ProtectionLegDefinition, PremiumLegDefinition
from refinitiv.dataplatform.content.ipa.enum_types import *
import conftest
import response_tests


def test_cds(open_session_for_ipa):
    """
    {
      "fields": [
        "InstrumentTag",
        "ValuationDate",
        "InstrumentDescription",
        "StartDate",
        "EndDate",
        "SettlementDate",
        "UpfrontAmountInDealCcy",
        "CashAmountInDealCcy",
        "AccruedAmountInDealCcy",
        "AccruedBeginDate",
        "NextCouponDate",
        "UpfrontPercent",
        "ConventionalSpreadBp",
        "ParSpreadBp",
        "AccruedDays",
        "ErrorCode",
        "ErrorMessage"
      ],
      "outputs": [
        "Data",
        "Headers"
      ],
      "universe": [
        {
          "instrumentType": "Cds",
          "instrumentDefinition": {
            "instrumentTag": "Cds1_InstrumentCode",
            "instrumentCode": "BNPP5YEUAM=R"
          },
          "pricingParameters": {
            "marketDataDate": "2020-01-01"
          }
        }
      ]
    }
    """

    df = rdp.get_cds_analytics(
        universe=rdp.ipa.cds.Definition(
            instrument_tag="Cds1_InstrumentCode",
            instrument_code="BNPP5YEUAM=R",
            cds_convention=rdp.ipa.enum_types.CdsConvention.ISDA,
            trade_date="2019-05-21T00:00:00Z",
            step_in_date="2019-05-22T00:00:00Z",
            start_date="2019-05-20T00:00:00Z",
            end_date_moving_convention=rdp.ipa.enum_types.BusinessDayConvention.NO_MOVING,
            adjust_to_isda_end_date=True,
        ),
        calculation_params=rdp.ipa.cds.CalculationParams(
            market_data_date="2020-01-01"
        ),
        outputs=[
            "Data",
            "Headers"
        ],
        fields=[
            "InstrumentTag",
            "ValuationDate",
            "InstrumentDescription",
            "StartDate",
            "EndDate",
            "SettlementDate",
            "UpfrontAmountInDealCcy",
            "CashAmountInDealCcy",
            "AccruedAmountInDealCcy",
            "AccruedBeginDate",
            "NextCouponDate",
            "UpfrontPercent",
            "ConventionalSpreadBp",
            "ParSpreadBp",
            "AccruedDays",
            "ErrorCode",
            "ErrorMessage"
        ]
    )

    assert not df.empty


def test_get_cds_analytics(open_session_for_ipa):
    df = rdp.get_cds_analytics(
        universe=rdp.ipa.cds.Definition(
            instrument_tag="Cds1_InstrumentCode",
            instrument_code="BNPP5YEUAM=R",
            cds_convention=CdsConvention.ISDA,
            trade_date="2019-05-21T00:00:00Z",
            step_in_date="2019-05-22T00:00:00Z",
            start_date="2019-05-20T00:00:00Z",
            end_date_moving_convention=BusinessDayConvention.NO_MOVING,
            adjust_to_isda_end_date=True,
        ),
        fields=[
            "InstrumentTag",
            "ValuationDate",
            "InstrumentDescription",
            "StartDate",
            "EndDate",
            "SettlementDate",
            "UpfrontAmountInDealCcy",
            "CashAmountInDealCcy",
            "AccruedAmountInDealCcy",
            "AccruedBeginDate",
            "NextCouponDate",
            "UpfrontPercent",
            "ConventionalSpreadBp",
            "ParSpreadBp",
            "AccruedDays",
            "ErrorCode",
            "ErrorMessage"
        ],
        outputs=[
            "Data",
            "Headers"
        ],
    )

    assert not df.empty


def test_get_cds_analytics_async(open_session_for_ipa):
    tasks = asyncio.gather(rdp.ipa.FinancialContracts.get_cds_analytics_async(
        universe=rdp.ipa.cds.Definition(
            instrument_tag="Cds1_InstrumentCode",
            instrument_code="BNPP5YEUAM=R",
            cds_convention=CdsConvention.ISDA,
            trade_date="2019-05-21T00:00:00Z",
            step_in_date="2019-05-22T00:00:00Z",
            start_date="2019-05-20T00:00:00Z",
            end_date_moving_convention=BusinessDayConvention.NO_MOVING,
            adjust_to_isda_end_date=True,
        )))
    asyncio.get_event_loop().run_until_complete(tasks)
    response, *_ = tasks.result()
    response_tests.success_response_tests(response)


def test_get_cds_analytics_with_legs(open_session_for_ipa):
    tasks = asyncio.gather(rdp.ipa.FinancialContracts.get_cds_analytics_async(
        universe=rdp.ipa.cds.Definition(
            instrument_tag="Cds1_InstrumentCode",
            instrument_code="BNPP5YEUAM=R",
            cds_convention=CdsConvention.ISDA,
            trade_date="2019-05-21T00:00:00Z",
            step_in_date="2019-05-22T00:00:00Z",
            start_date="2019-05-20T00:00:00Z",
            end_date_moving_convention=BusinessDayConvention.NO_MOVING,
            adjust_to_isda_end_date=True,
        )))
    asyncio.get_event_loop().run_until_complete(tasks)
    response, *_ = tasks.result()
    response_tests.success_response_tests(response)


def test_get_cds_analytics_instrument_code_empty_legs_empty_error():
    with pytest.raises(RequiredError):
        rdp.get_cds_analytics(
            universe=rdp.ipa.cds.Definition(
                instrument_tag="Cds1_InstrumentCode",
                cds_convention=CdsConvention.ISDA,
                trade_date="2019-05-21T00:00:00Z",
                step_in_date="2019-05-22T00:00:00Z",
                start_date="2019-05-20T00:00:00Z",
                end_date_moving_convention=BusinessDayConvention.NO_MOVING,
                adjust_to_isda_end_date=True,
            ))


def test_get_cds_analytics_instrument_code_error():
    with pytest.raises(RequiredError):
        rdp.get_cds_analytics(
            universe=rdp.ipa.cds.Definition(
                instrument_tag="Cds1_InstrumentCode",
                cds_convention=CdsConvention.ISDA,
                trade_date="2019-05-21T00:00:00Z",
                step_in_date="2019-05-22T00:00:00Z",
                start_date="2019-05-20T00:00:00Z",
                end_date_moving_convention=BusinessDayConvention.NO_MOVING,
                adjust_to_isda_end_date=True,
                premium_leg=rdp.ipa.cds.PremiumLegDefinition(
                    direction=Direction.PAID,
                    interest_payment_ccy="ISO code here",
                    interest_payment_frequency=Frequency.ANNUAL,
                    interest_calculation_method=DayCountBasis.DCB_ACTUAL_360
                ),
                protection_leg=rdp.ipa.cds.ProtectionLegDefinition(
                    index_factor=1.01,
                    index_series=1,
                    notional_amount=1.001,
                    recovery_rate=1.001,
                    seniority=Seniority.PREFERENCE,
                    settlement_convention="3WD"
                )
            ))


@pytest.mark.parametrize(
    argnames="input_data",
    ids=[
        "Definition",
        "PremiumLegDefinition",
        "ProtectionLegDefinition",
        "CalculationParams",
    ],
    argvalues=[
        (Definition, {
            "instrument_tag": "instrument_tag",
            "instrument_code": "instrument_code",
            "cds_convention": CdsConvention.ISDA,
            "trade_date": "trade_date",
            "step_in_date": "step_in_date",
            "start_date": "start_date",
            "end_date": "end_date",
            "tenor": "tenor",
            "start_date_moving_convention": BusinessDayConvention.MODIFIED_FOLLOWING,
            "end_date_moving_convention": BusinessDayConvention.NO_MOVING,
            "adjust_to_isda_end_date": True,
            "protection_leg": ProtectionLegDefinition(
                index_factor="index_factor",
                index_series="index_series",
                notional_amount="notional_amount",
                recovery_rate="recovery_rate",
                seniority=Seniority.PREFERENCE,
                settlement_convention="settlement_convention",
            ),
            "premium_leg": PremiumLegDefinition(
                direction=Direction.PAID,
                interest_payment_ccy="interest_payment_ccy",
                interest_payment_frequency=Frequency.SEMI_ANNUAL,
                interest_calculation_method=DayCountBasis.DCB_ACTUAL_360,
            ),
            "accrued_begin_date": "accrued_begin_date",
        }),
        (PremiumLegDefinition, {
            "direction": Direction.PAID,
            "notional_ccy": "notional_ccy",
            "notional_amount": 3.3,
            "fixed_rate_percent": 4.4,
            "interest_payment_frequency": Frequency.ANNUAL,
            "interest_calculation_method": DayCountBasis.DCB_30_360,
            "accrued_calculation_method": DayCountBasis.DCB_30_ACTUAL,
            "payment_business_day_convention": BusinessDayConvention.NO_MOVING,
            "first_regular_payment_date": "first_regular_payment_date",
            "last_regular_payment_date": "last_regular_payment_date",
            "payment_business_days": "payment_business_days",
            "stub_rule": StubRule.MATURITY,
            "accrued_paid_on_default": True,
            "interest_payment_ccy": "interest_payment_ccy",
        }),
        (ProtectionLegDefinition, {
            "direction": Direction.RECEIVED,
            "notional_ccy": "notional_ccy",
            "notional_amount": 3.3,
            "doc_clause": DocClause.EX_RESTRUCT14,
            "seniority": Seniority.SENIOR_UNSECURED,
            "index_factor": 6.6,
            "index_series": 7,
            "recovery_rate": 8.8,
            "recovery_rate_percent": 9.9,
            "reference_entity": "reference_entity",
            "settlement_convention": "settlement_convention",
        }),
        (CalculationParams, {
            "market_data_date": "market_data_date",
            "report_ccy": "report_ccy",
            "cash_amount_in_deal_ccy": 1.1,
            "clean_price_percent": 2.2,
            "conventional_spread_bp": 3.3,
            "upfront_amount_in_deal_ccy": 4.4,
            "upfront_percent": 5.5,
            "valuation_date": "valuation_date",
        })
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
