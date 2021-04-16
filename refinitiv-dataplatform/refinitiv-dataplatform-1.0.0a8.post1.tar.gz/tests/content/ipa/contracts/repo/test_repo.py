from inspect import signature

import pytest
from refinitiv.dataplatform.content import ipa
import refinitiv.dataplatform as rdp

from refinitiv.dataplatform.content.ipa.enum_types import *
from refinitiv.dataplatform.content.ipa.contracts.repo import Definition, UnderlyingContract, RepoParameters, CalculationParams, \
    UnderlyingCalculationParams
import conftest


@pytest.mark.parametrize(
    argnames="input_data",
    ids=[
        "Definition",
        "RepoParameters",
        "CalculationParams",
        "UnderlyingContract",
        "UnderlyingCalculationParams",
    ],
    argvalues=[
        (Definition, {
            "instrument_tag": "instrument_tag",
            "start_date": "start_date",
            "end_date": "end_date",
            "tenor": "tenor",
            "day_count_basis": DayCountBasis.DCB_30_365_BRAZIL,
            "underlying_instruments": [UnderlyingContract()],
            "is_coupon_exchanged": True,
            "repo_rate_percent": 8.8,
        }),
        (RepoParameters, {
            "coupon_paid_at_horizon": True,
            "haircut_rate_percent": 2.2,
            "initial_margin_percent": 3.3,
        }),
        (CalculationParams, {
            "market_data_date": "market_data_date",
            "settlement_convention": "settlement_convention",
            "report_ccy": "report_ccy",
            "coupon_reinvestment_rate_percent": 1.1,
            "repo_curve_type": RepoCurveType.LIBOR_FIXING,
            "valuation_date": "valuation_date",
        }),
        (UnderlyingContract, {
            "instrument_type": "instrument_type",
            "instrument_definition": ipa.bond.Definition(),
            "pricing_parameters": UnderlyingCalculationParams(),
        }),
        (UnderlyingCalculationParams, {
            "pricing_parameters_at_end": ipa.bond.CalculationParams(),
            "pricing_parameters_at_start": ipa.bond.CalculationParams(),
            "repo_parameters": RepoParameters(),
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


def test_repo(open_session_for_ipa):
    """
    {
      "universe": [
        {
          "instrumentType": "Repo",
          "instrumentDefinition": {
            "startDate": "2019-11-27",
            "tenor": "1M",
            "underlyingInstruments": [
              {
                "instrumentType": "Bond",
                "instrumentDefinition": {
                  "instrumentCode": "US191450264="
                }
              }
            ]
          },
          "pricingParameters": {
            "marketdataDate": "2019-11-25"
          }
        }
      ]
    }
    """
    df = rdp.get_repo_analytics(
        universe=Definition(
            start_date="2019-11-27",
            tenor="1M",
            underlying_instruments=[
                UnderlyingContract(
                    instrument_type="Bond",
                    instrument_definition=ipa.bond.Definition(
                        instrument_code="US191450264="
                    )
                )
            ]
        ),
        calculation_params=CalculationParams(
            market_data_date="2019-11-25"
        )
    )

    assert not df.empty
