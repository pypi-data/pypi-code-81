#
# This file is part of Orchid and related technologies.
#
# Copyright (c) 2017-2021 Reveal Energy Services.  All Rights Reserved.
#
# LEGAL NOTICE:
# Orchid contains trade secrets and otherwise confidential information
# owned by Reveal Energy Services. Access to and use of this information is 
# strictly limited and controlled by the Company. This file may not be copied,
# distributed, or otherwise disclosed outside of the Company's facilities 
# except under appropriate precautions to maintain the confidentiality hereof, 
# and may not be used in any way not expressly authorized by the Company.
#

import datetime as dt

import datetimerange as dtr

from orchid import (
    dot_net_dom_access as dna,
    net_quantity as onq,
)

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics import IMonitor


def make_time_range(start: dt.datetime, stop: dt.datetime) -> dtr.DateTimeRange:
    pass


class NativeMonitorAdapter(dna.DotNetAdapter):
    """Adapts a native IMonitor to python."""
    def __init__(self, net_monitor: IMonitor):
        """
        Constructs an instance adapting a .NET IMonitor.

        Args:
            net_monitor: The .NET monitor to be adapted.
        """
        super().__init__(net_monitor, dna.constantly(net_monitor.Project))

    display_name = dna.dom_property('display_name', 'The name used by engineers to identify this monitor.')
    name = dna.dom_property('name', 'The name of this monitor.')
    start_time = dna.transformed_dom_property('start_time', 'The start time of this monitor.', onq.as_datetime)
    stop_time = dna.transformed_dom_property('stop_time', 'The stop time of this monitor.', onq.as_datetime)

    @property
    def time_range(self):
        return dtr.DateTimeRange(self.start_time, self.stop_time)
