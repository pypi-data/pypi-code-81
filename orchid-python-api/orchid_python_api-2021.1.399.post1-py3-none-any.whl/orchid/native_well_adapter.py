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

from typing import Iterable

import toolz.curried as toolz

from orchid import (
    dot_net_dom_access as dna,
    measurement as om,
    native_stage_adapter as nsa,
    native_subsurface_point as nsp,
    native_trajectory_adapter as nta,
    net_quantity as onq,
    reference_origins as origins,
)

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IWell
# noinspection PyUnresolvedReferences
import UnitsNet
# noinspection PyUnresolvedReferences
from System import Array

from collections import namedtuple

WellHeadLocation = namedtuple('WellHeadLocation',
                              ['easting', 'northing', 'depth'])


def replace_no_uwi_with_text(uwi):
    return uwi if uwi else 'No UWI'


class NativeWellAdapter(dna.DotNetAdapter):
    """Adapts a native IWell to python."""

    def __init__(self, net_well: IWell):
        """
        Constructs an instance adapting a .NET IWell.

        Args:
            net_well: The .NET well to be adapted.
        """
        super().__init__(net_well, dna.constantly(net_well.Project))

    name = dna.dom_property('name', 'The name of the adapted .NET well.')
    display_name = dna.dom_property('display_name', 'The display name of the adapted .NET well.')
    stages = dna.transformed_dom_property_iterator('stages', 'An iterator over the NativeStageAdapters.',
                                                   nsa.NativeStageAdapter)
    trajectory = dna.transformed_dom_property('trajectory', 'The trajectory of the adapted .NET well.',
                                              nta.NativeTrajectoryAdapter)
    uwi = dna.transformed_dom_property('uwi', 'The UWI of the adapted .', replace_no_uwi_with_text)

    # The formation property **does not** check when a `None` value is passed from Orchid.
    # Although it is possible, it is very unlikely to occur from IWell.Formation.
    formation = dna.dom_property('formation', 'The production formation the well is landed')

    @property
    def ground_level_elevation_above_sea_level(self) -> om.Quantity:
        return onq.as_measurement(self.maybe_project_units.LENGTH, self.dom_object.GroundLevelElevationAboveSeaLevel)

    @property
    def kelly_bushing_height_above_ground_level(self) -> om.Quantity:
        return onq.as_measurement(self.maybe_project_units.LENGTH, self.dom_object.KellyBushingHeightAboveGroundLevel)

    @property
    def wellhead_location(self):
        dom_whl = self.dom_object.WellHeadLocation
        result = toolz.pipe(dom_whl,
                            toolz.map(onq.as_measurement(self.maybe_project_units.LENGTH)),
                            list, )
        return WellHeadLocation(*result)

    def locations_for_md_kb_values(self,
                                   md_kb_values: Iterable[om.Quantity],
                                   well_reference_frame_xy: origins.WellReferenceFrameXy,
                                   depth_origin: origins.DepthDatum) -> Iterable[nsp.BaseSubsurfacePoint]:
        sample_at = Array[UnitsNet.Length](toolz.map(onq.as_net_quantity(self.maybe_project_units.LENGTH),
                                                     md_kb_values))
        result = toolz.pipe(
            self.dom_object.GetLocationsForMdKbValues(sample_at, well_reference_frame_xy, depth_origin),
            toolz.map(nsp.make_subsurface_point_using_length_unit(self.maybe_project_units.LENGTH)),
            list,
        )
        return result
