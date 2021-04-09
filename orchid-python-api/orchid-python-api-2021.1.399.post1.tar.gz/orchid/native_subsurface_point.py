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


import abc
from typing import Union


from orchid import (
    dot_net_dom_access as dna,
    net_quantity as onq,
    unit_system as units,
)

import toolz.curried as toolz

# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics import ISubsurfacePoint


class BaseSubsurfacePoint(dna.DotNetAdapter):
    """An abstract base class for subsurface points."""

    depth_origin = dna.dom_property('depth_datum',
                                    'The datum or origin for the z-coordinate of this point.')
    xy_origin = dna.dom_property('well_reference_frame_xy',
                                 'The reference frame or origin for the x-y coordinates of this point.')

    @property
    @abc.abstractmethod
    def x(self):
        """The x-coordinate of this point."""
        pass

    @property
    @abc.abstractmethod
    def y(self):
        """The y-coordinate of this point."""
        pass

    @property
    @abc.abstractmethod
    def depth(self):
        """The depth of this point."""
        pass


class SubsurfacePointUsingLengthUnit(BaseSubsurfacePoint):
    """Adapts a .NET ISubsurfacePoint to be more Pythonic. Always returns lengths in the specified units."""

    def __init__(self, adaptee: ISubsurfacePoint, target_length_unit: Union[units.UsOilfield, units.Metric]):
        """
        Construct an instance adapting `adaptee` so that all lengths are expressed in `target_length_unit`.

        Args:
            adaptee: The .NET `ISubsurfacePoint` being adapted.
            target_length_unit: The target unit for all lengths.
        """
        super().__init__(adaptee)
        self._as_length_measurement_func = onq.as_measurement(target_length_unit)

    @property
    def x(self):
        """The x-coordinate of this point."""
        return self._as_length_measurement_func(self.dom_object.X)

    @property
    def y(self):
        """The y-coordinate of this point."""
        return self._as_length_measurement_func(self.dom_object.Y)

    @property
    def depth(self):
        """The depth of this point."""
        return self._as_length_measurement_func(self.dom_object.Depth)


@toolz.curry
def make_subsurface_point_using_length_unit(target_unit: Union[units.UsOilfield, units.Metric],
                                            net_subsurface_point: ISubsurfacePoint) -> SubsurfacePointUsingLengthUnit:
    return SubsurfacePointUsingLengthUnit(net_subsurface_point, target_unit)


class SubsurfacePoint(BaseSubsurfacePoint):
    """Adapts a .NET ISubsurfacePoint to be more Pythonic."""

    x = dna.transformed_dom_property('x', 'The x-coordinate of this point.', onq.as_length_measurement)
    y = dna.transformed_dom_property('y', 'The y-coordinate of this point.', onq.as_length_measurement)
    depth = dna.transformed_dom_property('depth', 'The z-coordinate (depth) of this point.', onq.as_length_measurement)

    def as_length_unit(self, as_length_unit: Union[units.UsOilfield, units.Metric]) -> SubsurfacePointUsingLengthUnit:
        """
        Convert all lengths returned to callers to `as_length_unit`.

        Args:
            as_length_unit: The unit to which all returned lengths are converted.

        Returns:
            A `SubsurfacePoint` that returns all lengths `as_length_unit`.

        """
        return SubsurfacePointUsingLengthUnit(self.dom_object, as_length_unit)
