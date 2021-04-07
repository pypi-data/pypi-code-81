from pathlib import Path

import pytest

from threedi_settings.threedimodel_config import ThreedimodelIni
from threedi_settings.threedimodel_config import AggregationIni

from threedi_settings.models import (
    GeneralSimulationConfig,
    TimeStepConfig,
    AggregationConfig,
    NumericalConfig,
    SimulationConfig
)

test_dir = Path(__file__).resolve()
INI = test_dir.parent / "model_config_fixture.ini"
AGGRE = test_dir.parent / "aggregate_fixture.ini"


@pytest.fixture(scope="session")
def model_ini():
    yield ThreedimodelIni(INI)


@pytest.fixture(scope="session")
def aggregation_ini():
    yield AggregationIni(AGGRE)


@pytest.fixture(scope="session")
def simulation_config():
    yield SimulationConfig(
        uid='1',
        sim_uid='1',
        general_config=GeneralSimulationConfig(uid='1', sim_uid='1',
                                               use_advection_1d=1,
                                               use_advection_2d=1),
        time_step_config=TimeStepConfig(
            uid='1',
            sim_uid='1',
            time_step=30.0,
            min_time_step=0.1,
            max_time_step=1.0,
            use_time_step_stretch=True,
            output_time_step=60.0
        ),
        numerical_config=NumericalConfig(
            uid='1',
            sim_uid='1',
            cfl_strictness_factor_1d=1.0,
            cfl_strictness_factor_2d=1.0,
            convergence_cg=1e-09,
            flow_direction_threshold=1e-05,
            friction_shallow_water_depth_correction=0,
            general_numerical_threshold=1e-08,
            time_integration_method=0,
            limiter_waterlevel_gradient_1d=1,
            limiter_waterlevel_gradient_2d=1,
            limiter_slope_crossectional_area_2d=0,
            limiter_slope_friction_2d=0,
            max_non_linear_newton_iterations=20,
            max_degree_gauss_seidel=20,
            min_friction_velocity=0.01,
            min_surface_area=1e-08,
            use_preconditioner_cg=1,
            preissmann_slot=0.0,
            pump_implicit_ratio=1.0,
            limiter_slope_thin_water_layer=0.01,
            use_of_cg=20,
            use_nested_newton=True,
            flooding_threshold=0.01
        ),
        aggregation_config=[
            AggregationConfig(uid='12', sim_uid='1',
                              flow_variable='interception', method='current',
                              interval=300.0, name=None),
            AggregationConfig(uid='11', sim_uid='1', flow_variable='volume',
                              method='current', interval=300.0, name=None),
            AggregationConfig(uid='10', sim_uid='1', flow_variable='leakage',
                              method='cum', interval=300.0, name=None),
            AggregationConfig(uid='9', sim_uid='1', flow_variable='discharge',
                              method='cum_positive', interval=300.0, name=None),
            AggregationConfig(uid='8', sim_uid='1', flow_variable='rain',
                              method='cum', interval=300.0, name=None),
            AggregationConfig(uid='7', sim_uid='1', flow_variable='discharge',
                              method='cum_negative', interval=300.0, name=None),
            AggregationConfig(uid='6', sim_uid='1',
                              flow_variable='simple_infiltration', method='cum',
                              interval=300.0, name=None),
            AggregationConfig(uid='5', sim_uid='1',
                              flow_variable='lateral_discharge', method='cum',
                              interval=300.0, name=None),
            AggregationConfig(uid='4', sim_uid='1',
                              flow_variable='pump_discharge', method='cum',
                              interval=300.0, name=None),
            AggregationConfig(uid='3', sim_uid='1', flow_variable='discharge',
                              method='cum', interval=300.0, name=None),
            AggregationConfig(uid='1', sim_uid='1', flow_variable='water_level',
                              method='min', interval=300.0, name='test')
        ]
    )


@pytest.fixture(scope="session")
def simulation_config_no_aggregation():
    yield SimulationConfig(
        uid='1',
        sim_uid='1',
        general_config=GeneralSimulationConfig(uid='1', sim_uid='1',
                                               use_advection_1d=1,
                                               use_advection_2d=1),
        time_step_config=TimeStepConfig(
            uid='1',
            sim_uid='1',
            time_step=30.0,
            min_time_step=0.1,
            max_time_step=1.0,
            use_time_step_stretch=True,
            output_time_step=60.0
        ),
        numerical_config=NumericalConfig(
            uid='1',
            sim_uid='1',
            cfl_strictness_factor_1d=1.0,
            cfl_strictness_factor_2d=1.0,
            convergence_cg=1e-09,
            flow_direction_threshold=1e-05,
            friction_shallow_water_depth_correction=0,
            general_numerical_threshold=1e-08,
            time_integration_method=0,
            limiter_waterlevel_gradient_1d=1,
            limiter_waterlevel_gradient_2d=1,
            limiter_slope_crossectional_area_2d=0,
            limiter_slope_friction_2d=0,
            max_non_linear_newton_iterations=20,
            max_degree_gauss_seidel=20,
            min_friction_velocity=0.01,
            min_surface_area=1e-08,
            use_preconditioner_cg=1,
            preissmann_slot=0.0,
            pump_implicit_ratio=1.0,
            limiter_slope_thin_water_layer=0.01,
            use_of_cg=20,
            use_nested_newton=True,
            flooding_threshold=0.01
        ),
        aggregation_config=[]
    )
