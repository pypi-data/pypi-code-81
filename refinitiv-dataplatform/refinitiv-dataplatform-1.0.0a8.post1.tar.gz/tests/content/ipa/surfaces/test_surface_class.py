from refinitiv.dataplatform.content.ipa.surface._surfaces_class import Surfaces
from unittest import mock
import conftest
from refinitiv.dataplatform.content import ipa
import refinitiv.dataplatform as rdp
import pickle
import os

error_raw = {'data': [{'surfaceTag': '1',
                       'error': {
                           'id': '7465d882-2c6c-48a4-b37f-d10d0fc21353/3a644903-5641-4574-948e-6a4c8ced70c4',
                           'status': 'Error',
                           'message': 'No underlying price available.',
                           'code': 'QPS-DPS.8019'}
                       }]}


cur_dir = os.path.dirname(__file__)
correct_raw_filepath = os.path.join(cur_dir, "correct_raw.pkl")
with open(correct_raw_filepath, "rb") as f:
    correct_raw = pickle.load(f)


def test_error():
    class Data(object):
        raw = error_raw

    session = conftest.open_platform_session()
    with mock.patch.object(rdp.ipa.surface.BaseDefinition, 'Data', return_value=Data) as df:
        response = ipa.surface.Surfaces().get_surface(
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
                )
            ],
            outputs=[ipa.surface.Surfaces.Outputs.DATA]
        )

        assert response.status == 'Error'
        assert response.error_message == 'No underlying price available.'
        session.close()


def test_correct():
    class Data(object):
        raw = correct_raw

    session = conftest.open_platform_session()
    with mock.patch.object(rdp.ipa.surface.BaseDefinition, 'Data', return_value=Data) as df:
        response = ipa.surface.Surfaces().get_surface(
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
                )
            ],
            outputs=[ipa.surface.Surfaces.Outputs.DATA]
        )

        assert response.status == {'http_reason': 'OK', 'http_status_code': 200}
        assert response.error_message is None
        session.close()
