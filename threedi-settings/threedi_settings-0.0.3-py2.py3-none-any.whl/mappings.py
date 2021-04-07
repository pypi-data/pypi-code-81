from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class FieldInfo:
    name: str
    type: Any


@dataclass(frozen=True)
class FieldInfoIni(FieldInfo):
    ini_section: str


@dataclass(frozen=True)
class AggregationFieldInfoOld(FieldInfo):
    pass


@dataclass(frozen=True)
class FieldInfoAPI(FieldInfo):
    default: Optional[Any]


general_settings_map = {
    "use_advection_1d": [
        FieldInfoIni("advection_1d", int, "physics"),
        FieldInfoAPI("use_advection_1d", int, 1),
    ],
    "use_advection_2d": [
        FieldInfoIni("advection_2d", int, "physics"),
        FieldInfoAPI("use_advection_2d", int, 1),
    ],
}

time_step_settings_map = {
    "time_step": [
        FieldInfoIni("timestep", float, "simulation"),
        FieldInfoAPI("time_step", float, 1.0),
    ],
    "min_time_step": [
        FieldInfoIni("minimum_timestep", float, "simulation"),
        FieldInfoAPI("min_time_step", float, 0.1),
    ],
    "max_time_step": [
        FieldInfoIni("maximum_timestep", float, "simulation"),
        FieldInfoAPI("max_time_step", float, 1.0),
    ],
    "use_time_step_stretch": [
        FieldInfoIni("timestep_plus", bool, "numerics"),
        FieldInfoAPI("use_time_step_stretch", bool, False),
    ],
    "output_time_step": [
        FieldInfoIni("output_timestep", float, "output"),
        FieldInfoAPI("output_time_step", float, 1.0),
    ],
}

# old -> new
numerical_settings_map = {
    "cfl_strictness_factor_1d": [
        FieldInfoIni("cfl_strictness_factor_1d", float, "numerics"),
        FieldInfoAPI("cfl_strictness_factor_1d", float, 1.0),
    ],
    "cfl_strictness_factor_2d": [
        FieldInfoIni("cfl_strictness_factor_2d", float, "numerics"),
        FieldInfoAPI("cfl_strictness_factor_2d", float, 1.0),
    ],
    "flow_direction_threshold": [
        FieldInfoIni("flow_direction_threshold", float, "numerics"),
        FieldInfoAPI("flow_direction_threshold", float, 1e-05),
    ],
    "convergence_cg": [
        FieldInfoIni("convergence_cg", float, "numerics"),
        FieldInfoAPI("convergence_cg", float, 1.0e-9),
    ],
    "friction_shallow_water_depth_correction": [
        FieldInfoIni(
            "friction_shallow_water_correction", int, "physical_attributes"
        ),
        FieldInfoAPI(
            "friction_shallow_water_depth_correction",
            int,
            0,
        ),
    ],
    "general_numerical_threshold": [
        FieldInfoIni("general_numerical_threshold", float, "numerics"),
        FieldInfoAPI("general_numerical_threshold", float, 1.0e-8),
    ],
    "time_integration_method": [
        FieldInfoIni("integration_method", int, "numerics"),
        FieldInfoAPI("time_integration_method", int, 0),
    ],
    "limiter_waterlevel_gradient_1d": [
        FieldInfoIni("limiter_grad_1d", int, "numerics"),
        FieldInfoAPI("limiter_waterlevel_gradient_1d", int, 1),
    ],
    "limiter_waterlevel_gradient_2d": [
        FieldInfoIni("limiter_grad_2d", int, "numerics"),
        FieldInfoAPI("limiter_waterlevel_gradient_2d", int, 1),
    ],
    "limiter_slope_crossectional_area_2d": [
        FieldInfoIni("limiter_slope_crossectional_area_2d", int, "numerics"),
        FieldInfoAPI("limiter_slope_crossectional_area_2d", int, 0),
    ],
    "limiter_slope_friction_2d": [
        FieldInfoIni("limiter_slope_friction_2d", int, "numerics"),
        FieldInfoAPI("limiter_slope_friction_2d", int, 0),
    ],
    "max_non_linear_newton_iterations": [
        FieldInfoIni("max_nonlinear_iteration", int, "numerics"),
        FieldInfoAPI("max_non_linear_newton_iterations", int, 20),
    ],
    "max_degree_gauss_seidel": [
        FieldInfoIni("maximum_degree", int, "numerics"),
        FieldInfoAPI("max_degree_gauss_seidel", int, 20),
    ],
    "min_friction_velocity": [
        FieldInfoIni("minimum_friction_velocity", float, "numerics"),
        FieldInfoAPI("min_friction_velocity", float, 0.01),
    ],
    "min_surface_area": [
        FieldInfoIni("minimum_surface_area", float, "numerics"),
        FieldInfoAPI("min_surface_area", float, 1.0e-8),
    ],
    "use_preconditioner_cg": [
        FieldInfoIni("precon_cg", int, "numerics"),
        FieldInfoAPI("use_preconditioner_cg", int, 1),
    ],
    "preissmann_slot": [
        FieldInfoIni("preissmann_slot", float, "numerics"),
        FieldInfoAPI("preissmann_slot", float, 0.0),
    ],
    "pump_implicit_ratio": [
        FieldInfoIni("pump_implicit_ratio", float, "numerics"),
        FieldInfoAPI("pump_implicit_ratio", float, 1.0),
    ],
    "limiter_slope_thin_water_layer": [
        FieldInfoIni("thin_water_layer_definition", float, "numerics"),
        FieldInfoAPI("limiter_slope_thin_water_layer", float, 0.01),
    ],
    "use_of_cg": [
        FieldInfoIni("use_of_cg", int, "numerics"),
        FieldInfoAPI("use_of_cg", int, 20),
    ],
    "use_nested_newton": [
        FieldInfoIni("nested_newton", int, "numerics"),
        FieldInfoAPI("use_nested_newton", bool, True),
    ],
    "flooding_threshold": [
        FieldInfoIni("flooding_threshold", float, "numerics"),
        FieldInfoAPI("flooding_threshold", float, 0.000001),
    ],
}

aggregation_settings_map = {
    "flow_variable": [
        AggregationFieldInfoOld("flow_variable", str),
        FieldInfoAPI("flow_variable", str, None),
    ],
    "method": [
        AggregationFieldInfoOld("aggregation_method", str),
        FieldInfoAPI("method", str, None),
    ],
    "interval": [
        AggregationFieldInfoOld("timestep", float),
        FieldInfoAPI("interval", float, None),
    ],
}


settings_map = {
    **general_settings_map,
    **time_step_settings_map,
    **numerical_settings_map,
}
