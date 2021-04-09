#  Copyright 2017-2021 Reveal Energy Services, Inc 
#
#  Licensed under the Apache License, Version 2.0 (the "License"); 
#  you may not use this file except in compliance with the License. 
#  You may obtain a copy of the License at 
#
#      http://www.apache.org/licenses/LICENSE-2.0 
#
#  Unless required by applicable law or agreed to in writing, software 
#  distributed under the License is distributed on an "AS IS" BASIS, 
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
#  See the License for the specific language governing permissions and 
#  limitations under the License. 
#
# This file is part of Orchid and related technologies.
#


from enum import IntEnum
from typing import Tuple, Union

import deal
import toolz.curried as toolz

from orchid import (
    dot_net_dom_access as dna,
    measurement as om,
    native_subsurface_point as nsp,
    native_treatment_curve_adapter as ntc,
    net_quantity as onq,
    reference_origins as origins,
    unit_system as units,
    validation
)

# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics import FormationConnectionType
# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics.Factories import Calculations

VALID_LENGTH_UNIT_MESSAGE = 'The parameter, `in_length_unit`, must be a unit system length.'


class ConnectionType(IntEnum):
    PLUG_AND_PERF = FormationConnectionType.PlugAndPerf,
    SLIDING_SLEEVE = FormationConnectionType.SlidingSleeve,
    SINGLE_POINT_ENTRY = FormationConnectionType.SinglePointEntry,
    OPEN_HOLE = FormationConnectionType.OpenHole


def as_connection_type(type_value):
    @toolz.curry
    def has_value(value, enum_type):
        return value == enum_type.value

    return toolz.pipe(iter(ConnectionType),
                      toolz.filter(has_value(type_value)),
                      toolz.nth(0))


# This pre-condition applies to the public methods:
# - bottom_location
# - center_location
# - cluster_location
# - top_location
# but is implemented here to ensure common behavior among all these public methods.
@deal.pre(lambda _depth_datum, _reference_frame, in_length_unit, _net_subsurface_point_func:
          validation.is_unit_system_length(in_length_unit),
          message=VALID_LENGTH_UNIT_MESSAGE)
def subsurface_point_in_length_unit(depth_datum: origins.DepthDatum,
                                    xy_reference_frame: origins.WellReferenceFrameXy,
                                    in_length_unit: Union[units.UsOilfield, units.Metric],
                                    net_subsurface_point_func) -> nsp.BaseSubsurfacePoint:
    """
    Calculate the subsurface point `in_length_unit` whose value is calculated by the
    callable, `net_subsurface_point_func`.

    Although this method is public, the author intends it to be "private." The author has made it public
    **only** to support unit testing. No other usage is supported.

    Args:
        depth_datum: The datum from which we measure depths.
        xy_reference_frame: The reference frame for easting-northing coordinates.
        in_length_unit: The unit of length available from the returned value.
        net_subsurface_point_func: The callable to calculate the subsurface point in .NET.

    Returns:
        The subsurface point in the requested unit of length.
    """
    net_subsurface_point = net_subsurface_point_func(xy_reference_frame.value, depth_datum.value)
    result = nsp.SubsurfacePoint(net_subsurface_point).as_length_unit(in_length_unit)
    return result


class NativeStageAdapter(dna.DotNetAdapter):
    """Adapts a .NET IStage to be more Pythonic."""

    def __init__(self, adaptee, calculations_factory=None):
        super().__init__(adaptee, dna.constantly(adaptee.Well.Project))
        self.calculations_factory = Calculations.FractureDiagnosticsCalculationsFactory() \
            if not calculations_factory else calculations_factory

    cluster_count = dna.dom_property('number_of_clusters', 'The number of clusters for this stage')
    display_name_with_well = dna.dom_property('display_name_with_well',
                                              'The display stage number including the well name')
    display_name_without_well = dna.dom_property('display_name_without_well',
                                                 'The display stage number excluding the well name')
    display_stage_number = dna.dom_property('display_stage_number', 'The display stage number for the stage')
    global_stage_sequence_number = dna.dom_property('global_stage_sequence_number',
                                                    'The global sequence number of this stage')
    order_of_completion_on_well = dna.dom_property('order_of_completion_on_well',
                                                   'The order in which this stage was completed on its well')
    stage_type = dna.transformed_dom_property('stage_type', 'The formation connection type of this stage',
                                              as_connection_type)
    start_time = dna.transformed_dom_property('start_time', 'The start time of the stage treatment', onq.as_datetime)
    stop_time = dna.transformed_dom_property('stop_time', 'The stop time of the stage treatment', onq.as_datetime)

    @property
    def isip(self) -> om.Quantity:
        """
        Return the instantaneous shut in pressure of this stage in project units.
        """
        return onq.as_measurement(self.maybe_project_units.PRESSURE, self.dom_object.Isip)

    @property
    def pnet(self) -> om.Quantity:
        """
        Return the net pressure of this stage in project units.

        The net pressure of a stage is calculated by the formula:
            pnet = isip + fluid-density * tvd - shmin (where tvd is the true vertical depth)
        """
        return onq.as_measurement(self.maybe_project_units.PRESSURE, self.dom_object.Pnet)

    @property
    def shmin(self) -> om.Quantity:
        """
        Return the minimum horizontal stress of this stage in project units.
        """
        return onq.as_measurement(self.maybe_project_units.PRESSURE, self.dom_object.Shmin)

    @staticmethod
    def _sampled_quantity_name_curve_map(sampled_quantity_name):
        candidates = toolz.pipe(ntc.TreatmentCurveTypes,
                                toolz.filter(lambda e: e.value == sampled_quantity_name),
                                list)
        if len(candidates) == 0:
            raise KeyError(f'Unknown sampled quantity name: "{sampled_quantity_name}"')

        assert len(candidates) == 1, f'Sampled quantity name "{sampled_quantity_name}"' \
                                     f' selects many curve types: {candidates}'

        return candidates[0]

    def _center_location_depth(self, in_length_unit: Union[units.UsOilfield, units.Metric],
                               depth_datum: origins.DepthDatum) -> om.Quantity:
        """
        Return the depth of the stage center relative to the specified `depth_datum.`

        Args:
            in_length_unit: The unit of length for the returned Measurement.
            depth_datum: The reference datum for the depth.
        """
        subsurface_point = self.center_location(in_length_unit, origins.WellReferenceFrameXy.ABSOLUTE_STATE_PLANE,
                                                depth_datum)
        return subsurface_point.depth

    def bottom_location(self, in_length_unit: Union[units.UsOilfield, units.Metric],
                        xy_reference_frame: origins.WellReferenceFrameXy,
                        depth_datum: origins.DepthDatum) -> nsp.BaseSubsurfacePoint:
        """
        Return the location of the bottom of this stage in the `xy_well_reference_frame` using the
        `depth_datum` in the specified unit.

        Args:
            in_length_unit: The unit of length available from the returned value.
            xy_reference_frame: The reference frame for easting-northing coordinates.
            depth_datum: The datum from which we measure depths.

        Returns:
            The `BaseSubsurfacePoint` of the stage bottom.
        """

        return subsurface_point_in_length_unit(depth_datum, xy_reference_frame, in_length_unit,
                                               self.dom_object.GetStageLocationBottom)

    def center_location(self, in_length_unit: Union[units.UsOilfield, units.Metric],
                        xy_reference_frame: origins.WellReferenceFrameXy,
                        depth_datum: origins.DepthDatum) -> nsp.BaseSubsurfacePoint:
        """
        Return the location of the center of this stage in the `xy_well_reference_frame` using the `depth_datum`
        in the specified unit.

        Args:
            in_length_unit: The unit of length available from the returned value.
            xy_reference_frame: The reference frame for easting-northing coordinates.
            depth_datum: The datum from which we measure depths.

        Returns:
            The `BaseSubsurfacePoint` of the stage center.
        """
        return subsurface_point_in_length_unit(depth_datum, xy_reference_frame, in_length_unit,
                                               self.dom_object.GetStageLocationCenter)

    def center_location_easting(self, in_length_unit: Union[units.UsOilfield, units.Metric],
                                xy_well_reference_frame: origins.WellReferenceFrameXy) -> om.Quantity:
        """
        Return the easting location of the stage center relative to the specified reference frame in the
        specified unit.

        Args:
            in_length_unit: An unit of the unit of length for the returned Measurement.
            xy_well_reference_frame: The reference frame defining the origin.

        Returns:
            A measurement.
        """
        result = self.center_location(in_length_unit, xy_well_reference_frame, origins.DepthDatum.KELLY_BUSHING).x
        return result

    def center_location_northing(self, in_length_unit: Union[units.UsOilfield, units.Metric],
                                 xy_well_reference_frame: origins.WellReferenceFrameXy) -> om.Quantity:
        """
        Return the northing location of the stage center in the `xy_well_reference_frame` in the specified unit.

        Args:
            in_length_unit: The requested resultant length unit.
            xy_well_reference_frame: The reference frame defining the origin.

        Returns:
            A measurement.
        """
        subsurface_point = self.center_location(in_length_unit, xy_well_reference_frame,
                                                origins.DepthDatum.KELLY_BUSHING)
        return subsurface_point.y

    def center_location_md(self, in_length_unit: Union[units.UsOilfield, units.Metric]) -> om.Quantity:
        """
        Return the measured depth of the stage center in project units.

        Args:
            in_length_unit: The unit of length for the returned Measurement.
        """
        return self._center_location_depth(in_length_unit, origins.DepthDatum.KELLY_BUSHING)

    def center_location_tvdgl(self, in_length_unit: Union[units.UsOilfield, units.Metric]) -> om.Quantity:
        """
        Returns the total vertical depth from ground level of the stage center in project units.

        Args:
            in_length_unit: The unit of length for the returned Measurement.
        """
        return self._center_location_depth(in_length_unit, origins.DepthDatum.GROUND_LEVEL)

    def center_location_tvdss(self, in_length_unit: Union[units.UsOilfield, units.Metric]) -> om.Quantity:
        """
        Returns the total vertical depth from sea level of the stage center in project units.

        Args:
            in_length_unit: The unit of length for the returned Measurement.
        """
        return self._center_location_depth(in_length_unit, origins.DepthDatum.SEA_LEVEL)

    def center_location_xy(self, in_length_unit: Union[units.UsOilfield, units.Metric],
                           xy_well_reference_frame: origins.WellReferenceFrameXy) -> Tuple[om.Quantity,
                                                                                           om.Quantity]:
        """
        Return the easting-northing location of the stage center in the `xy_well_reference_frame` in project units.

        Args:
            in_length_unit: The unit of length for the returned Measurement.
            xy_well_reference_frame: The reference frame defining the origin.

        Returns:
            A tuple
        """
        subsurface_point = self.center_location(in_length_unit, xy_well_reference_frame,
                                                origins.DepthDatum.KELLY_BUSHING)
        return subsurface_point.x, subsurface_point.y

    @deal.pre(lambda _self, _in_length_unit, cluster_no, _xy_reference_frame, _depth_datum: cluster_no >= 0)
    def cluster_location(self, in_length_unit: Union[units.UsOilfield, units.Metric], cluster_no: int,
                         xy_reference_frame: origins.WellReferenceFrameXy,
                         depth_datum: origins.DepthDatum) -> nsp.BaseSubsurfacePoint:
        """
        Return the location of the bottom of this stage in the `xy_well_reference_frame` using the
        `depth_datum` in the specified unit.

        Args:
            in_length_unit: The unit of length available from the returned value.
            cluster_no: The number identifying the cluster whose location is sought.
            xy_reference_frame: The reference frame for easting-northing coordinates.
            depth_datum: The datum from which we measure depths.

        Returns:
            The `BaseSubsurfacePoint` of the stage cluster identified by `cluster_no`.
        """
        stage_location_cluster_func = toolz.curry(self.dom_object.GetStageLocationCluster, cluster_no)
        return subsurface_point_in_length_unit(depth_datum, xy_reference_frame, in_length_unit,
                                               stage_location_cluster_func)

    @deal.pre(validation.arg_is_acceptable_pressure_unit)
    def isip_in_pressure_unit(self, target_unit: Union[units.UsOilfield, units.Metric]) -> om.Quantity:
        return onq.as_measurement(target_unit, self.dom_object.Isip)

    def md_bottom(self, in_length_unit: Union[units.UsOilfield, units.Metric]):
        """
        Return the measured depth of the bottom of this stage (farthest from the well head / closest to the toe)
        in the specified unit.

        Args:
            in_length_unit: An unit of the unit of length for the returned Measurement.

        Returns:
             The measured depth of the stage bottom in the specified unit.
        """
        return onq.as_measurement(in_length_unit, self.dom_object.MdBottom)

    def md_top(self, in_length_unit: Union[units.UsOilfield, units.Metric]) -> om.Quantity:
        """
        Return the measured depth of the top of this stage (closest to the well head / farthest from the toe)
        in the specified unit.

        Args:
            in_length_unit: An unit of the requested resultant length unit.

        Returns;
         The measured depth of the stage top in the specified unit.
        """
        return onq.as_measurement(in_length_unit, self.dom_object.MdTop)

    @deal.pre(validation.arg_is_acceptable_pressure_unit)
    def pnet_in_pressure_unit(self, target_unit: Union[units.UsOilfield, units.Metric]) -> om.Quantity:
        return onq.as_measurement(target_unit, self.dom_object.Pnet)

    @deal.pre(validation.arg_is_acceptable_pressure_unit)
    def shmin_in_pressure_unit(self, target_unit: Union[units.UsOilfield, units.Metric]) -> om.Quantity:
        return onq.as_measurement(target_unit, self.dom_object.Shmin)

    def stage_length(self, in_length_unit: Union[units.UsOilfield, units.Metric]) -> om.Quantity:
        """
        Return the stage length in the specified unit.

        Args:
            in_length_unit: An unit of the unit of length for the returned Measurement.

        Returns:
            The Measurement of the length of this stage.
        """
        return self.md_bottom(in_length_unit) - self.md_top(in_length_unit)

    def top_location(self, in_length_unit: Union[units.UsOilfield, units.Metric],
                     xy_reference_frame: origins.WellReferenceFrameXy,
                     depth_datum: origins.DepthDatum) -> nsp.BaseSubsurfacePoint:
        """
        Return the location of the top of this stage in the `xy_well_reference_frame` using the `depth_datum`
        in the specified unit.

        Args:
            in_length_unit: The unit of length available from the returned value.
            xy_reference_frame: The reference frame for easting-northing coordinates.
            depth_datum: The datum from which we measure depths.

        Returns:
            The `BaseSubsurfacePoint` of the stage top.
        """
        return subsurface_point_in_length_unit(depth_datum, xy_reference_frame, in_length_unit,
                                               self.dom_object.GetStageLocationTop)

    def treatment_curves(self):
        """
        Returns the dictionary of treatment curves for this treatment_stage.

        Request a specific curve from the dictionary using the constants defined in `orchid`:

        - `PROPPANT_CONCENTRATION`
        - `SLURRY_RATE`
        - `TREATING_PRESSURE`

        Returns:
            The dictionary containing the available treatment curves.
        """
        if not self.dom_object.TreatmentCurves.Items:
            return {}

        def add_curve(so_far, treatment_curve):
            curve_name = self._sampled_quantity_name_curve_map(treatment_curve.sampled_quantity_name)
            treatment_curve_map = {curve_name: treatment_curve}
            return toolz.merge(treatment_curve_map, so_far)

        result = toolz.pipe(self.dom_object.TreatmentCurves.Items,  # start with .NET treatment curves
                            toolz.map(ntc.NativeTreatmentCurveAdapter),  # wrap them in a facade
                            # Transform the map to a dictionary keyed by the sampled quantity name
                            lambda cs: toolz.reduce(add_curve, cs, {}))
        return result
