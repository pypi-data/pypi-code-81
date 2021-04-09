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

import enum

from orchid import (
    base_curve_adapter as bca,
    dot_net_dom_access as dna,
)

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.TimeSeries import IQuantityTimeSeries


class MonitorCurveTypes(enum.Enum):
    MONITOR_PRESSURE = 'Pressure'
    MONITOR_TEMPERATURE = 'Temperature'


class NativeMonitorCurveAdapter(bca.BaseCurveAdapter):
    def __init__(self, net_monitor_curve: IQuantityTimeSeries):
        super().__init__(net_monitor_curve, dna.constantly(net_monitor_curve.Well.Project))

    def quantity_name_unit_map(self, project_units):
        """
        Return a map (dictionary) between quantity names and units (from `unit_system`) of the samples.

        This method plays the role of "Primitive Operation" in the _Template Method_ design pattern. In this
        role, the "Template Method" defines an algorithm and delegates some steps of the algorithm to derived
        classes through invocation of "Primitive Operations".

        Args:
            project_units: The unit system of the project.
        """
        result = {
            MonitorCurveTypes.MONITOR_PRESSURE.value: project_units.PRESSURE,
            MonitorCurveTypes.MONITOR_TEMPERATURE.value: project_units.TEMPERATURE,
        }
        return result
