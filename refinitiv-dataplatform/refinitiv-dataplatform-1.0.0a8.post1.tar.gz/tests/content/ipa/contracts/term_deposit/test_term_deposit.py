import asyncio
from inspect import signature

import pytest
from refinitiv.dataplatform import ContentFactory

from refinitiv.dataplatform.content import ipa
from refinitiv.dataplatform.content.ipa.enum_types import *
from refinitiv.dataplatform.content.ipa.contracts.term_deposit import *
import conftest
import response_tests
import refinitiv.dataplatform as rdp


def test_get_term_deposit_analytics(open_session_for_ipa):
    df = rdp.get_term_deposit_analytics(
        universe=ipa.term_deposit.Definition(
            instrument_tag="AED_AM1A",
            tenor="5Y",
            notional_ccy="GBP",
            fixed_rate_percent=1
            ),
        calculation_params=ipa.term_deposit.CalculationParams(valuation_date="2018-01-10T00:00:00Z"),
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
    assert df is not None, ContentFactory._last_error_status
    assert not bool(df.ErrorMessage[0]), df.ErrorMessage[0]
    assert not df.empty


def test_get_term_deposit_analytics_async(open_session_for_ipa):
    tasks = asyncio.gather(ipa.FinancialContracts.get_term_deposit_analytics_async(
        universe=ipa.term_deposit.Definition(
            instrument_tag="AED_AM1A",
            tenor="5Y",
            notional_ccy="euro",
            ),
        calculation_params=ipa.capfloor.CalculationParams(valuation_date="2018-01-10T00:00:00Z"),
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
        "CalculationParams"
        ],
    argvalues=[
        (Definition, {
            "instrument_tag": "instrument_tag",
            "instrument_code": "instrument_code",
            "start_date": "start_date",
            "end_date": "end_date",
            "tenor": "tenor",
            "notional_ccy": "notional_ccy",
            "notional_amount": 7.7,
            "fixed_rate_percent": 8.8,
            "payment_business_day_convention": BusinessDayConvention.NO_MOVING,
            "payment_roll_convention": DateRollingConvention.LAST28,
            "year_basis": DayCountBasis.DCB_30_360_ISDA,
            "calendar": "calendar",
            }),
        (CalculationParams, {
            "price_side": PriceSide.LAST,
            "income_tax_percent": 2.2,
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
