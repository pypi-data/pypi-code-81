# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from vrt_lss_fieldservice.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from vrt_lss_fieldservice.model.analytics_task import AnalyticsTask
from vrt_lss_fieldservice.model.calculation_detail import CalculationDetail
from vrt_lss_fieldservice.model.capacity import Capacity
from vrt_lss_fieldservice.model.capacity_factor import CapacityFactor
from vrt_lss_fieldservice.model.check_result import CheckResult
from vrt_lss_fieldservice.model.convert_settings import ConvertSettings
from vrt_lss_fieldservice.model.convert_task import ConvertTask
from vrt_lss_fieldservice.model.cost_penalty import CostPenalty
from vrt_lss_fieldservice.model.cost_reward import CostReward
from vrt_lss_fieldservice.model.inline_response400 import InlineResponse400
from vrt_lss_fieldservice.model.inline_response401 import InlineResponse401
from vrt_lss_fieldservice.model.inline_response404 import InlineResponse404
from vrt_lss_fieldservice.model.inline_response406 import InlineResponse406
from vrt_lss_fieldservice.model.inline_response415 import InlineResponse415
from vrt_lss_fieldservice.model.inline_response429 import InlineResponse429
from vrt_lss_fieldservice.model.inline_response500 import InlineResponse500
from vrt_lss_fieldservice.model.inline_response501 import InlineResponse501
from vrt_lss_fieldservice.model.inline_response502 import InlineResponse502
from vrt_lss_fieldservice.model.inline_response503 import InlineResponse503
from vrt_lss_fieldservice.model.inline_response504 import InlineResponse504
from vrt_lss_fieldservice.model.inline_response_default import InlineResponseDefault
from vrt_lss_fieldservice.model.location import Location
from vrt_lss_fieldservice.model.matrix_line import MatrixLine
from vrt_lss_fieldservice.model.measurements import Measurements
from vrt_lss_fieldservice.model.objects_metrics import ObjectsMetrics
from vrt_lss_fieldservice.model.order import Order
from vrt_lss_fieldservice.model.order_cost import OrderCost
from vrt_lss_fieldservice.model.performer import Performer
from vrt_lss_fieldservice.model.performer_blacklist import PerformerBlacklist
from vrt_lss_fieldservice.model.performer_features import PerformerFeatures
from vrt_lss_fieldservice.model.performer_restrictions import PerformerRestrictions
from vrt_lss_fieldservice.model.plan_assumptions import PlanAssumptions
from vrt_lss_fieldservice.model.plan_id import PlanId
from vrt_lss_fieldservice.model.plan_info import PlanInfo
from vrt_lss_fieldservice.model.plan_result import PlanResult
from vrt_lss_fieldservice.model.plan_settings import PlanSettings
from vrt_lss_fieldservice.model.plan_statistics import PlanStatistics
from vrt_lss_fieldservice.model.plan_status import PlanStatus
from vrt_lss_fieldservice.model.plan_task import PlanTask
from vrt_lss_fieldservice.model.predict_result import PredictResult
from vrt_lss_fieldservice.model.predict_result_window import PredictResultWindow
from vrt_lss_fieldservice.model.predict_task import PredictTask
from vrt_lss_fieldservice.model.quality_statistics import QualityStatistics
from vrt_lss_fieldservice.model.routing import Routing
from vrt_lss_fieldservice.model.routing_matrix import RoutingMatrix
from vrt_lss_fieldservice.model.shift import Shift
from vrt_lss_fieldservice.model.statistics import Statistics
from vrt_lss_fieldservice.model.stop_statistics import StopStatistics
from vrt_lss_fieldservice.model.tariff import Tariff
from vrt_lss_fieldservice.model.tariff_primary import TariffPrimary
from vrt_lss_fieldservice.model.time_window import TimeWindow
from vrt_lss_fieldservice.model.time_window_violation import TimeWindowViolation
from vrt_lss_fieldservice.model.trace_data import TraceData
from vrt_lss_fieldservice.model.traffic_factor import TrafficFactor
from vrt_lss_fieldservice.model.transport_factor import TransportFactor
from vrt_lss_fieldservice.model.transport_load import TransportLoad
from vrt_lss_fieldservice.model.transport_type import TransportType
from vrt_lss_fieldservice.model.trip import Trip
from vrt_lss_fieldservice.model.trip_action import TripAction
from vrt_lss_fieldservice.model.trip_statistics import TripStatistics
from vrt_lss_fieldservice.model.unplanned_order import UnplannedOrder
from vrt_lss_fieldservice.model.validate_result import ValidateResult
from vrt_lss_fieldservice.model.validation import Validation
from vrt_lss_fieldservice.model.version_result import VersionResult
from vrt_lss_fieldservice.model.waypoint import Waypoint
