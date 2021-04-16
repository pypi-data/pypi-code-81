import pytest
from unittest.mock import patch, PropertyMock

from threedi_settings.threedimodel_config import ThreedimodelIni
from threedi_settings.threedimodel_config import AggregationIni
from threedi_settings.models import SimulationConfig
from threedi_settings.http.api_clients import OpenAPINumericalSettings
from threedi_settings.http.api_clients import OpenAPITimeStepSettings
from threedi_settings.http.api_clients import OpenAPIGeneralSettings
from threedi_settings.http.api_clients import OpenApiSettingsModel
from threedi_settings.http.api_clients import OpenAPIAggregationSettings
from threedi_settings.http.api_clients import OpenAPISimulationSettings
from openapi_client.models import GeneralSettings
from openapi_client.models import TimeStepSettings
from openapi_client.models import NumericalSettings
from openapi_client.models import AggregationSettings
from openapi_client.models import SimulationSettingsOverview
from openapi_client import ApiException
from threedi_settings.models import SourceTypes

from tests.fixtures import model_ini
from tests.fixtures import aggregation_ini
from tests.client_fixtures import simulation_overview


def test_openapi_settings_clients(model_ini):
    # smoke tests
    config = model_ini.as_dict()
    clients = [
        OpenAPIGeneralSettings(1, config, SourceTypes.ini_file),
        OpenAPINumericalSettings(1, config, SourceTypes.ini_file),
        OpenAPITimeStepSettings(1, config, SourceTypes.ini_file),
    ]
    for client in clients:
        assert isinstance(
            client.instance, (
                GeneralSettings,
                TimeStepSettings,
                NumericalSettings)
        )


def test_openapi_name_conversions(model_ini):
    config = model_ini.as_dict()
    client = OpenAPIGeneralSettings(1, config, SourceTypes.ini_file)
    # should have attributes use_advection_2d/1d now
    assert client.instance.use_advection_2d == 0  # from ini
    assert client.instance.use_advection_1d == 0  # from ini


def test_openapi_defaults_from_mapping(model_ini):
    config = model_ini.as_dict()
    client = OpenAPINumericalSettings(1, config, SourceTypes.ini_file)
    # should have a default from mapping
    assert client.instance.friction_shallow_water_depth_correction == 0


def test_openapi_type_conversions(model_ini):
    config = model_ini.as_dict()
    client = OpenAPINumericalSettings(1, config, SourceTypes.ini_file)
    # should have a default from mapping
    assert client.instance.use_nested_newton is False


def test_openapi__create_method_property(model_ini):
    config = model_ini.as_dict()
    client = OpenAPITimeStepSettings(1, config, SourceTypes.ini_file)
    assert callable(client._create_method)


@patch.object(
    OpenAPITimeStepSettings, "create_method_name", new_callable=PropertyMock)
def test_openapi__create_method_error(mock_create_method, model_ini):
    config = model_ini.as_dict()
    mock_create_method.return_value = "invalid"
    client = OpenAPITimeStepSettings(1, config, SourceTypes.ini_file)
    with pytest.raises(AttributeError):
        client._create_method()


@patch.object(OpenAPIGeneralSettings, 'create')
def test_create_general_settings_resource(mock_create, model_ini):
    config = model_ini.as_dict()
    client = OpenAPIGeneralSettings(1, config, SourceTypes.ini_file)

    mock_create.return_value = client.instance
    resp = client.create()
    assert resp == client.instance


@patch.object(OpenAPIGeneralSettings, 'create')
def test_create_general_settings_resource_error(mock_create, model_ini):
    config = model_ini.as_dict()
    client = OpenAPIGeneralSettings(1, config, SourceTypes.ini_file)

    mock_create.side_effect = ApiException
    # create, side effect ApiExc, AttrErr
    with pytest.raises(ApiException):
        client.create()


def test_aggregation_settings_client(aggregation_ini):
    client = OpenAPIAggregationSettings(1, aggregation_ini.as_dict())
    for i in client.instances:
        assert isinstance(i, AggregationSettings)


@patch.object(OpenAPIAggregationSettings, 'create')
def test_create_aggregation_settings_resource_error(mock_create, aggregation_ini):
    config = aggregation_ini.as_dict()
    client = OpenAPIAggregationSettings(1, config)

    mock_create.return_value = client.instances
    resp = client.create()
    assert resp == client.instances

    @patch.object(OpenAPIAggregationSettings, 'create')
    def test_create_aggregation_settings_resource(mock_create, aggregation_ini):
        config = aggregation_ini.as_dict()
        client = OpenAPIAggregationSettings(1, config)

        mock_create.side_effect = ApiException
        # create, side effect ApiExc, AttrErr
        with pytest.raises(ApiException):
            client.create()


@patch.object(OpenAPISimulationSettings, "retrieve")
def test_simulation_settings_client(mock, simulation_overview):
    client = OpenAPISimulationSettings(1)
    mock.return_value = simulation_overview
    assert isinstance(client.simulation_config, SimulationConfig)


@patch.object(OpenAPISimulationSettings, "retrieve")
def test_simulation_settings_client_error(mock, simulation_overview):
    client = OpenAPISimulationSettings(1)
    mock.side_effect = ApiException
    with pytest.raises(ApiException):
        client.retrieve()


def test_get_aggregations(simulation_overview):
    client = OpenAPISimulationSettings(1)
    aggr = client._get_aggregations(simulation_overview, "1")
    assert len(aggr) == 10
