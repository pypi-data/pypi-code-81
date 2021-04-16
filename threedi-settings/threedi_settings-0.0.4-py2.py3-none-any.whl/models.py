from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


@dataclass
class BaseConfig:
    """"""

    uid: str  # Unique id of setting
    sim_uid: str


@dataclass
class GeneralSimulationConfig(BaseConfig):
    use_advection_1d: int
    use_advection_2d: int


@dataclass
class TimeStepConfig(BaseConfig):
    time_step: float
    min_time_step: float
    max_time_step: float
    use_time_step_stretch: bool
    output_time_step: float


@dataclass
class NumericalConfig(BaseConfig):
    cfl_strictness_factor_1d: float
    cfl_strictness_factor_2d: float
    convergence_cg: float
    flow_direction_threshold: float
    friction_shallow_water_depth_correction: int
    general_numerical_threshold: float
    time_integration_method: int
    limiter_waterlevel_gradient_1d: int
    limiter_waterlevel_gradient_2d: int
    limiter_slope_crossectional_area_2d: int
    limiter_slope_friction_2d: int
    max_non_linear_newton_iterations: int
    max_degree_gauss_seidel: int
    min_friction_velocity: float
    min_surface_area: float
    use_preconditioner_cg: int
    preissmann_slot: float
    pump_implicit_ratio: float
    limiter_slope_thin_water_layer: float
    use_of_cg: int
    use_nested_newton: bool
    flooding_threshold: float


@dataclass
class AggregationConfig(BaseConfig):
    flow_variable: str
    method: str
    interval: float
    name: Optional[str] = ""


@dataclass
class SimulationConfig(BaseConfig):
    general_config: GeneralSimulationConfig
    time_step_config: TimeStepConfig
    numerical_config: NumericalConfig
    aggregation_config: Optional[List[AggregationConfig]] = field(
        default_factory=list
    )


class SourceTypes(int, Enum):
    ini_file = 1
    sqlite_file = 2
