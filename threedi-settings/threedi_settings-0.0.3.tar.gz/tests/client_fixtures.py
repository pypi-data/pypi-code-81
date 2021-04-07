from openapi_client.models import SimulationSettingsOverview
from openapi_client.models import AggregationSettings
from openapi_client.models import GeneralSettings
from openapi_client.models import TimeStepSettings
from openapi_client.models import NumericalSettings

import pytest


@pytest.fixture(scope="session")
def simulation_overview():
    data = {'aggregation_settings': [{'flow_variable': 'interception',
                               'interval': 300.0,
                               'method': 'current',
                               'name': None,
                               'url': 'http://localhost:8000/v3.0/simulations/3/settings/aggregation/32/'},
                              {'flow_variable': 'volume',
                               'interval': 300.0,
                               'method': 'current',
                               'name': None,
                               'url': 'http://localhost:8000/v3.0/simulations/3/settings/aggregation/31/'},
                              {'flow_variable': 'leakage',
                               'interval': 300.0,
                               'method': 'cum',
                               'name': None,
                               'url': 'http://localhost:8000/v3.0/simulations/3/settings/aggregation/30/'},
                              {'flow_variable': 'discharge',
                               'interval': 300.0,
                               'method': 'cum_positive',
                               'name': None,
                               'url': 'http://localhost:8000/v3.0/simulations/3/settings/aggregation/29/'},
                              {'flow_variable': 'rain',
                               'interval': 300.0,
                               'method': 'cum',
                               'name': None,
                               'url': 'http://localhost:8000/v3.0/simulations/3/settings/aggregation/28/'},
                              {'flow_variable': 'discharge',
                               'interval': 300.0,
                               'method': 'cum_negative',
                               'name': None,
                               'url': 'http://localhost:8000/v3.0/simulations/3/settings/aggregation/27/'},
                              {'flow_variable': 'simple_infiltration',
                               'interval': 300.0,
                               'method': 'cum',
                               'name': None,
                               'url': 'http://localhost:8000/v3.0/simulations/3/settings/aggregation/26/'},
                              {'flow_variable': 'lateral_discharge',
                               'interval': 300.0,
                               'method': 'cum',
                               'name': None,
                               'url': 'http://localhost:8000/v3.0/simulations/3/settings/aggregation/25/'},
                              {'flow_variable': 'pump_discharge',
                               'interval': 300.0,
                               'method': 'cum',
                               'name': None,
                               'url': 'http://localhost:8000/v3.0/simulations/3/settings/aggregation/24/'},
                              {'flow_variable': 'discharge',
                               'interval': 300.0,
                               'method': 'cum',
                               'name': None,
                               'url': 'http://localhost:8000/v3.0/simulations/3/settings/aggregation/23/'}],
     'general_settings': {'id': 7,
                          'simulation_id': 3,
                          'use_advection_1d': 1,
                          'use_advection_2d': 1},
     'numerical_settings': {'cfl_strictness_factor_1d': 1.0,
                            'cfl_strictness_factor_2d': 1.0,
                            'convergence_cg': 1e-09,
                            'flooding_threshold': 0.01,
                            'flow_direction_threshold': 1e-05,
                            'friction_shallow_water_depth_correction': 0,
                            'general_numerical_threshold': 1e-08,
                            'id': 3,
                            'limiter_slope_crossectional_area_2d': 0,
                            'limiter_slope_friction_2d': 0,
                            'limiter_slope_thin_water_layer': 0.01,
                            'limiter_waterlevel_gradient_1d': 1,
                            'limiter_waterlevel_gradient_2d': 1,
                            'max_degree_gauss_seidel': 20,
                            'max_non_linear_newton_iterations': 20,
                            'min_friction_velocity': 0.01,
                            'min_surface_area': 1e-08,
                            'preissmann_slot': 0.0,
                            'pump_implicit_ratio': 1.0,
                            'simulation_id': 3,
                            'time_integration_method': 0,
                            'use_nested_newton': True,
                            'use_of_cg': 20,
                            'use_preconditioner_cg': 1},
     'time_step_settings': {'id': 3,
                            'max_time_step': 1.0,
                            'min_time_step': 0.1,
                            'output_time_step': 60.0,
                            'simulation_id': 3,
                            'time_step': 30.0,
                            'use_time_step_stretch': True}}
    aggr_data = data.pop("aggregation_settings")
    agg_list = [AggregationSettings(**entry) for entry in aggr_data]
    data["aggregation_settings"] = agg_list
    gen_data = data.pop("general_settings")
    gen_sett = GeneralSettings(**gen_data)
    data["general_settings"] = gen_sett
    ts_data = data.pop("time_step_settings")
    ts_sett = TimeStepSettings(**ts_data)
    data["time_step_settings"] = ts_sett
    n_data = data.pop("numerical_settings")
    n_sett = NumericalSettings(**n_data)
    data["numerical_settings"] = n_sett
    yield SimulationSettingsOverview(**data)
