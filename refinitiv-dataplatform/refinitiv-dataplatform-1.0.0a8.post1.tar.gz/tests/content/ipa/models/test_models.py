from inspect import signature

import pytest

from refinitiv.dataplatform.content.ipa.enum_types import *
from refinitiv.dataplatform.content.ipa.models import *
import conftest


@pytest.mark.parametrize(
    argnames="input_data",
    ids=[
        "AmericanMonteCarloParameters",
        "AmortizationItem",
        "BasketItem",
        "BidAskMid",
        "DayWeight",
        "FxDualCurrencyDefinition",
        "FxUnderlyingDefinition",
        "InterpolationWeight",
        "NumericalMethod",
        "PdeParameters",
    ],
    argvalues=[
        (AmericanMonteCarloParameters, {
            "american_monte_carlo_method": AmericanMonteCarloMethod.ANDERSEN,
            "additional_points": 2,
            "all_the_time_points_per_year": 3,
            "iteration_number": 4,
        }),
        (AmortizationItem, {
            "start_date": "start_date",
            "end_date": "end_date",
            "amortization_frequency": AmortizationFrequency.EVERY2ND_COUPON,
            "amortization_type": AmortizationType.LINEAR,
            "remaining_notional": 5.5,
            "amount": 7.7,
        }),
        (BasketItem, {
            "instrument_code": "instrument_code",
            "currency": "currency",
        }),
        (BidAskMid, {
            "bid": 1.1,
            "ask": 2.2,
            "mid": 3.3,
        }),
        (DayWeight, {
            "date": "date",
            "weight": 2.2,
        }),
        (FxDualCurrencyDefinition, {
            "deposit_start_date": "deposit_start_date",
            "margin_percent": 2.2,
        }),
        (FxUnderlyingDefinition, {
            "fx_cross_code": "fx_cross_code",
        }),
        (InterpolationWeight, {
            "days_list": [DayWeight()],
            "holidays": 2.2,
            "week_days": 3.3,
            "week_ends": 4.4,
        }),
        (NumericalMethod, {
            "american_monte_carlo_parameters": AmericanMonteCarloParameters(),
            "method": Method.ANALYTIC,
            "pde_parameters": PdeParameters(),
        }),
        (PdeParameters, {
            "pde_space_step_number": 1,
            "pde_standard_deviation": 2,
            "pde_time_step_number": 3,
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
