import pytest

from refinitiv.dataplatform.content import ipa
from refinitiv.dataplatform import ContentFactory


def test_fx_volatility_surface_class(open_session_for_ipa):
    """
    {
      "universe": [
        {
          "underlyingType": "Fx",
          "underlyingDefinition": {
            "fxCrossCode": "EURUSD"
          },
          "surfaceTag": "FxVol-EURUSD",
          "surfaceLayout": {
            "format": "Matrix"
          },
          "surfaceParameters": {
            "xAxis": "Date",
            "yAxis": "Strike",
            "calculationDate": "2018-08-20T00:00:00Z",
            "returnAtm": true
          }
        }
      ]
    }
    """
    response = ipa.surface.Surfaces(open_session_for_ipa).get_surface(
        universe=[
            ipa.surface.fx.Definition(
                fx_cross_code="EURUSD",
                tag="FxVol-EURUSD",
                layout=ipa.surface.SurfaceOutput(
                    format=ipa.enum_types.Format.MATRIX
                ),
                calculation_params=ipa.surface.fx.CalculationParams(
                    x_axis="Date",
                    y_axis="Strike",
                    calculation_date="2018-08-20T00:00:00Z"
                )
            )
        ]
    )

    data = response.data
    if data.df is None:
        pytest.fail(str(ContentFactory._last_error_status))
    assert not data.df.empty, ContentFactory._last_error_status
    assert data.surface


def test_fx_volatility_surface_function(open_session_for_ipa):
    """
    {
      "universe": [
        {
          "underlyingType": "Fx",
          "underlyingDefinition": {
            "fxCrossCode": "EURUSD"
          },
          "surfaceTag": "FxVol-EURUSD",
          "surfaceLayout": {
            "format": "Matrix"
          },
          "surfaceParameters": {
            "xAxis": "Date",
            "yAxis": "Strike",
            "calculationDate": "2018-08-20T00:00:00Z",
            "returnAtm": true
          }
        }
      ]
    }
    """
    df = ipa.get_surface(
        universe=[
            ipa.surface.fx.Definition(
                fx_cross_code="EURUSD",
                tag="FxVol-EURUSD",
                layout=ipa.surface.SurfaceOutput(
                    format=ipa.enum_types.Format.MATRIX
                ),
                calculation_params=ipa.surface.fx.CalculationParams(
                    x_axis="Date",
                    y_axis="Strike",
                    calculation_date="2018-08-20T00:00:00Z"
                )
            )
        ]
    )

    if df is None:
        pytest.fail(str(ContentFactory._last_error_status))
    assert not df.empty, ContentFactory._last_error_status


def test_eti_volatility_surface(open_session_for_ipa):
    """
    {
      "universe": [
        {
          "surfaceTag": "1",
          "underlyingType": "Eti",
          "underlyingDefinition": {
            "instrumentCode": "BNPP.PA@RIC"
          },
          "surfaceParameters": {
            "priceSide": "Mid",
            "volatilityModel": "SVI",
            "xAxis": "Date",
            "yAxis": "Strike"
          },
          "surfaceLayout": {
            "format": "Matrix",
            "yPointCount": 10
          }
        }
      ]
    }
    """
    df = ipa.get_surface(
        universe=[
            ipa.surface.eti.Definition(
                tag="1",
                instrument_code="BNPP.PA@RIC",
                calculation_params=ipa.surface.eti.CalculationParams(
                    price_side=ipa.enum_types.PriceSide.MID,
                    volatility_model=ipa.enum_types.VolatilityModel.SVI,
                    x_axis=ipa.enum_types.Axis.DATE,
                    y_axis=ipa.enum_types.Axis.STRIKE,
                ),
                layout=ipa.surface.SurfaceOutput(
                    format=ipa.enum_types.Format.MATRIX,
                    y_point_count=10
                ),
            ),
            ipa.surface.eti.Definition(
                tag="222",
                instrument_code="BNPP.PA@RIC",
                calculation_params=ipa.surface.eti.CalculationParams(
                    price_side=ipa.enum_types.PriceSide.MID,
                    volatility_model=ipa.enum_types.VolatilityModel.SVI,
                    x_axis=ipa.enum_types.Axis.DATE,
                    y_axis=ipa.enum_types.Axis.STRIKE,
                ),
                layout=ipa.surface.SurfaceOutput(
                    format=ipa.enum_types.Format.MATRIX,
                    y_point_count=10
                ),
            )
        ]
    )

    if df is None:
        pytest.fail(str(ContentFactory._last_error_status))
    assert not df.empty, ContentFactory._last_error_status


def test_cap_volatility_surface(open_session_for_ipa):
    """
    {
      "universe": [
        {
          "surfaceTag": "USD_Strike__Tenor_",
          "underlyingType": "Cap",
          "underlyingDefinition": {
            "instrumentCode": "USD",
            "referenceCapletTenor": "3M"
          },
          "surfaceLayout": {
            "Format": "Matrix"
          },
          "surfaceParameters": {
            "calculationDate": "2020-03-20",
            "xAxis": "Strike",
            "yAxis": "Tenor"
          }
        }
      ]
    }
    """
    df = ipa.get_surface(
        universe=[
            ipa.surface.cap.Definition(
                tag="1",
                instrument_code="USD",
                calculation_params=ipa.surface.cap.CalculationParams(
                    valuation_date="2020-03-20",
                    x_axis="Strike",
                    y_axis="Tenor"
                ),
                layout=ipa.surface.SurfaceOutput(
                    format=ipa.enum_types.Format.MATRIX,
                ),
            )
        ]
    )

    if df is None:
        pytest.fail(str(ContentFactory._last_error_status))
    assert not df.empty, ContentFactory._last_error_status


def test_swaption_volatility_surface(open_session_for_ipa):
    """
    {
      "universe": [
        {
          "surfaceTag": "My EUR VolCube",
          "underlyingType": "Swaption",
          "underlyingDefinition": {
            "instrumentCode": "EUR"
          },
          "surfaceParameters": {
            "calculationDate": "2020-04-20",
            "shiftPercent": 3,
            "includeCapletsVolatility": true,
            "xAxis": "Strike",
            "yAxis": "Tenor",
            "zAxis": "Expiry"
          },
          "surfaceLayout": {
            "format": "NDimensionalArray"
          }
        }
      ]
    }
    """
    df = ipa.get_surface(universe=ipa.surface.swaption.Definition(
        tag="My EUR VolCube",
        instrument_code="EUR",
        layout=ipa.surface.SurfaceOutput(format="NDimensionalArray"),
        calculation_params=ipa.surface.swaption.CalculationParams(
            valuation_date="2020-04-20",
            shift_percent=3,
            x_axis="Strike",
            y_axis="Tenor",
            z_axis="Expiry"
        ),
    ))
    if df is None:
        pytest.fail(str(ContentFactory._last_error_status))
    assert not df.empty, ContentFactory._last_error_status


def test_interest_rate_volatility_surface(open_session_for_ipa):
    """
    {
      "universe": [
        {
          "surfaceTag": "USD_Strike__Tenor_",
          "underlyingType": "Cap",
          "underlyingDefinition": {
            "instrumentCode": "USD",
            "referenceCapletTenor": "3M"
          },
          "surfaceLayout": {
            "Format": "Matrix"
          },
          "surfaceParameters": {
            "calculationDate": "2020-03-20",
            "xAxis": "Strike",
            "yAxis": "Tenor"
          }
        }
      ]
    }
    """
    df = ipa.get_surface(
        universe=[
            ipa.surface.ir.Definition(
                tag="1",
                instrument_code="USD",
                calculation_params=ipa.surface.ir.CalculationParams(
                    valuation_date="2020-03-20",
                    x_axis="Strike",
                    y_axis="Tenor"
                ),
                layout=ipa.surface.SurfaceOutput(
                    format=ipa.enum_types.Format.MATRIX,
                ),
            )
        ]
    )

    if df is None:
        pytest.fail(str(ContentFactory._last_error_status))
    assert not df.empty, ContentFactory._last_error_status
