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

"""This module contains functions for converting between instances of the (Python) `Measurement` class and
instances of .NET classes like `UnitsNet.Quantity` and `DateTime`."""


import datetime
from numbers import Real
from functools import singledispatch

import dateutil.tz as duz
import toolz.curried as toolz

from orchid import (
    measurement as om,
    physical_quantity as opq,
    unit_system as units,
)

# noinspection PyUnresolvedReferences
from Orchid.FractureDiagnostics.RatioTypes import ProppantConcentration, SlurryRate
# noinspection PyUnresolvedReferences
from System import DateTime, DateTimeKind, Decimal
# noinspection PyUnresolvedReferences
import UnitsNet


class NetQuantityTimeZoneError(ValueError):
    """
    Raised when an error occurs accessing the `TimeZoneInfo` of a .NET `DateTime` instance.
    """
    pass


class NetQuantityLocalDateTimeKindError(NetQuantityTimeZoneError):
    """
    Raised when the `DateTime.Kind` property of a .NET `DateTime` instance is `DateTimeKind.Local`.
    """
    def __init__(self, net_time_point):
        """
        Construct an instance from a .NET DateTime point in time.

        Args:
            net_time_point: A .NET DateTime representing a specific point in time.
        """
        super().__init__(self, '.NET DateTime.Kind cannot be Local.', net_time_point.ToString("O"))


class NetQuantityUnspecifiedDateTimeKindError(NetQuantityTimeZoneError):
    """
    Raised when the `DateTime.Kind` property of a .NET `DateTime` instance is not recognized.
    """
    ERROR_PREFACE = '.NET DateTime.Kind is unexpectedly Unspecified.'

    ERROR_SUFFIX = """
    Although .NET DateTime.Kind should not be Unspecified, it may be
    safe to ignore this error by catching the exception.

    However, because it unexpected, **please** report the issue to
    Reveal Energy Services. 
    """

    def __init__(self, net_time_point):
        """
        Construct an instance from a .NET DateTime point in time.

        Args:
            net_time_point: A .NET DateTime representing a specific point in time.
        """
        super().__init__(self, NetQuantityUnspecifiedDateTimeKindError.ERROR_PREFACE,
                         net_time_point.ToString("O"), NetQuantityUnspecifiedDateTimeKindError.ERROR_SUFFIX)


class NetQuantityNoTzInfoError(NetQuantityTimeZoneError):
    """
    Raised when the `DateTime.Kind` property of a .NET `DateTime` instance is `DateTimeKind.Unspecified`.
    """
    def __init__(self, time_point):
        """
        Construct an instance from a Python point in time.

        Args:
            time_point: A Python `datetime.datetime` representing a specific point in time.
        """
        super().__init__(self, f'The Python time point must specify the time zone.', time_point.isoformat())


class EqualsComparisonDetails:
    def __init__(self, tolerance: Real = 1e-4,
                 net_comparison_type: UnitsNet.ComparisonType = UnitsNet.ComparisonType.Relative):
        """
        Construct an instance that uses `tolerance` and `comparison_type` to determine equality.

        This class exists because the `tolerance` and `comparison_type` are closely coupled; that is, one
        cannot correctly interpret the use of `tolerance` without a reference to the `comparison_type`.

        Args:
            tolerance: The maximum difference tolerated between two instances in determining equality.
            net_comparison_type: The type of comparison: `UnitsNet.ComparisonType.Relative` or
            `UnitsNet.ComparisonType.Absolute`.
        """
        self._tolerance = tolerance
        self._comparison_type = net_comparison_type

    @property
    def tolerance(self) -> Real:
        """
        Return the tolerance to be use in determining equality.

        Although this property is public, it is intended only to be read by the `equal_net_comparison`
        function.
        """
        return self._tolerance

    @property
    def comparison_type(self) -> UnitsNet.ComparisonType:
        """
        Return the comparison type to be use in determining equality.

        Although this property is public, it is intended only to be read by the `equal_net_comparison`
        function.
        """
        return self._comparison_type


def as_datetime(net_time_point: DateTime) -> datetime.datetime:
    """
    Convert a .NET `DateTime` instance to a `datetime.datetime` instance.

    Args:
        net_time_point: A point in time of type .NET `DateTime`.

    Returns:
        The `datetime.datetime` equivalent to the `net_time_point`.
    """
    if net_time_point.Kind == DateTimeKind.Utc:
        return datetime.datetime(net_time_point.Year, net_time_point.Month, net_time_point.Day,
                                 net_time_point.Hour, net_time_point.Minute, net_time_point.Second,
                                 net_time_point.Millisecond * 1000, duz.UTC)

    if net_time_point.Kind == DateTimeKind.Unspecified:
        raise NetQuantityUnspecifiedDateTimeKindError(net_time_point)

    if net_time_point.Kind == DateTimeKind.Local:
        raise NetQuantityLocalDateTimeKindError(net_time_point)

    raise ValueError(f'Unknown .NET DateTime.Kind, {net_time_point.Kind}.')


#
# Although Pint supports the unit `cu_ft`, we have chosen to use the synonym, `ft ** 3` (which is
# printed as 'ft\u00b3` (that is, 'ft' followed by a Unicode superscript 3)). According to a
# citation on [Wikipedia article](https://en.wikipedia.org/wiki/Cubic_foot), this "is the IEEE
# symbol for the cubic foot." Our general rule: we accept the Pint unit `cu_ft` as **input**,
# but, on various conversion, produce the Pint unit `ft**3`.
#
@singledispatch
@toolz.curry
def as_measurement(unknown, _net_quantity: UnitsNet.IQuantity) -> om.Quantity:
    """
    Convert a .NET UnitsNet.IQuantity to a `pint` `Quantity` instance.

    This function is registered as the type-handler for the `object` type. In our situation, arriving here
    indicates an error by an implementer and so raises an error.

    Args:
        unknown: A parameter whose type is not expected.
        _net_quantity: The .NET IQuantity instance to convert. (Unused in this base implementation.)
    """
    raise TypeError(f'First argument, {unknown}, has type {type(unknown)}, unexpected by `as_measurement`.')


@as_measurement.register(opq.PhysicalQuantity)
@toolz.curry
def as_measurement_using_physical_quantity(physical_quantity, net_quantity: UnitsNet.IQuantity) -> om.Quantity:
    """
    Convert a .NET UnitsNet.IQuantity to a `pint` `Quantity` instance in the same unit.

    Args:
        physical_quantity: The `PhysicalQuantity`. Although we try to determine a unique mapping between units
        in `pint` and .NET `UnitsNet` units, we cannot perform a unique mapping for density and proppant
        concentration measured in the metric system (the units of both these physical quantities are
        "kg/m**3").
        net_quantity: The .NET IQuantity instance to convert.

    Returns:
        The equivalent `pint` `Quantity` instance.
    """
    def is_proppant_concentration(physical_qty):
        return physical_qty == opq.PhysicalQuantity.PROPPANT_CONCENTRATION

    def is_slurry_rate(physical_qty):
        return physical_qty == opq.PhysicalQuantity.SLURRY_RATE

    def ratio_units(net_qty):
        return net_qty.NumeratorUnit, net_qty.DenominatorUnit

    def is_us_oilfield_proppant_concentration(numerator, denominator):
        return (numerator == UnitsNet.Units.MassUnit.Pound and
                denominator == UnitsNet.Units.VolumeUnit.UsGallon)

    def is_metric_proppant_concentration(numerator, denominator):
        return (numerator == UnitsNet.Units.MassUnit.Kilogram and
                denominator == UnitsNet.Units.VolumeUnit.CubicMeter)

    def is_us_oilfield_slurry_rate(numerator, denominator):
        return (numerator == UnitsNet.Units.VolumeUnit.OilBarrel and
                denominator == UnitsNet.Units.DurationUnit.Minute)

    def is_metric_slurry_rate(numerator, denominator):
        return (numerator == UnitsNet.Units.VolumeUnit.CubicMeter and
                denominator == UnitsNet.Units.DurationUnit.Minute)

    if is_proppant_concentration(physical_quantity):
        numerator_unit, denominator_unit = ratio_units(net_quantity)
        if is_us_oilfield_proppant_concentration(numerator_unit, denominator_unit):
            return net_quantity.Value * om.registry.lb / om.registry.gal
        elif is_metric_proppant_concentration(numerator_unit, denominator_unit):
            return net_quantity.Value * om.registry.kg / (om.registry.m ** 3)

    if is_slurry_rate(physical_quantity):
        numerator_unit, denominator_unit = ratio_units(net_quantity)
        if is_us_oilfield_slurry_rate(numerator_unit, denominator_unit):
            return net_quantity.Value * om.registry.oil_bbl / om.registry.min
        elif is_metric_slurry_rate(numerator_unit, denominator_unit):
            return net_quantity.Value * (om.registry.m ** 3) / om.registry.min

    pint_unit = _to_pint_unit(physical_quantity, net_quantity.Unit)

    # UnitsNet, for an unknown reason, handles the `Value` property of `Power` **differently** from almost all
    # other units (`Information` and `BitRate` appear to be handled in the same way). Specifically, the
    # `Value` property **does not** return a value of type `double` but of type `Decimal`. Python.NET
    # expectedly converts the value returned by `Value` to a Python `decimal.Decimal`. Then, additionally,
    # Pint has a problem handling a unit whose value is `decimal.Decimal`. I do not quite understand this
    # problem, but I have seen other issues on GitHub that seem to indicate similar problems.
    if physical_quantity == opq.PhysicalQuantity.POWER:
        return _net_decimal_to_float(net_quantity.Value) * pint_unit
    elif physical_quantity == opq.PhysicalQuantity.TEMPERATURE:
        return om.Quantity(net_quantity.Value, pint_unit)
    else:
        return net_quantity.Value * pint_unit


# Define convenience functions when physical quantity is known.
as_angle_measurement = toolz.curry(as_measurement, opq.PhysicalQuantity.ANGLE)
as_density_measurement = toolz.curry(as_measurement, opq.PhysicalQuantity.DENSITY)
as_length_measurement = toolz.curry(as_measurement, opq.PhysicalQuantity.LENGTH)
as_pressure_measurement = toolz.curry(as_measurement, opq.PhysicalQuantity.PRESSURE)


@as_measurement.register(units.Common)
@toolz.curry
def as_measurement_in_common_unit(common_unit, net_quantity: UnitsNet.IQuantity) -> om.Quantity:
    """
    Convert a .NET UnitsNet.IQuantity to a `pint` `Quantity` instance in a common unit.

    Args:
        common_unit: The unit (from the units.Common) for the converted `Quantity` instance.
        net_quantity: The .NET IQuantity instance to convert.

    Returns:
        The equivalent `Quantity` instance.
    """
    # units.Common support no conversion so simply call another implementation.
    return as_measurement(common_unit.value.physical_quantity, net_quantity)


@as_measurement.register(units.Metric)
@as_measurement.register(units.UsOilfield)
@toolz.curry
def as_measurement_in_specified_unit(specified_unit, net_quantity: UnitsNet.IQuantity) -> om.Quantity:
    """
    Convert a .NET UnitsNet.IQuantity to a `pint` `Quantity` instance in a specified, but compatible unit.

    Args:
        specified_unit: The unit for the converted `Quantity` instance.
        net_quantity: The .NET IQuantity instance to convert.

    Returns:
        The equivalent `Quantity` instance in the specified unit.
    """
    result = toolz.pipe(net_quantity,
                        _convert_net_quantity_to_different_unit(specified_unit),
                        as_measurement(specified_unit.value.physical_quantity))
    return result


def as_net_date_time(time_point: datetime.datetime) -> DateTime:
    """
    Convert a `datetime.datetime` instance to a .NET `DateTime` instance.

    Args:
        time_point: The `datetime.datetime` instance to covert.

    Returns:
        The equivalent .NET `DateTime` instance.
    """
    if time_point.tzinfo != duz.UTC:
        raise NetQuantityNoTzInfoError(time_point)

    return DateTime(time_point.year, time_point.month, time_point.day, time_point.hour, time_point.minute,
                    time_point.second, microseconds_to_integral_milliseconds(time_point.microsecond),
                    DateTimeKind.Utc)


#
# Although Pint supports the unit `cu_ft`, we have chosen to use the synonym, `ft ** 3` (which is
# printed as 'ft\u00b3` (that is, 'ft' followed by a Unicode superscript 3)). According to a
# citation on [Wikipedia article](https://en.wikipedia.org/wiki/Cubic_foot), this "is the IEEE
# symbol for the cubic foot." Our general rule: we accept the Pint unit `cu_ft` as **input**,
# but, on various conversion, produce the Pint unit `ft**3`.
#
@singledispatch
@toolz.curry
def as_net_quantity(unknown, _measurement: om.Quantity) -> UnitsNet.IQuantity:
    """
    Convert a .NET UnitsNet.IQuantity to a `pint` `Quantity` instance.

    This function is registered as the type-handler for the `object` type. In our situation, arriving here
    indicates an error by an implementer and so raises an error.

    Args:
        unknown: A parameter whose type is not expected.
        _measurement: The `Quantity` instance to convert.

    Returns:
        The equivalent `UnitsNet.IQuantity` instance.
    """
    raise TypeError(f'First argument, {unknown}, has type {type(unknown)}, unexpected by `as_net_quantity`.')


_PINT_UNIT_CREATE_NET_UNITS = {
    om.registry.deg: lambda qv: UnitsNet.Angle.FromDegrees(qv),
    om.registry.min: lambda qv: UnitsNet.Duration.FromMinutes(qv),
    om.registry.ft_lb: lambda qv: UnitsNet.Energy.FromFootPounds(qv),
    om.registry.J: lambda qv: UnitsNet.Energy.FromJoules(qv),
    om.registry.lbf: lambda qv: UnitsNet.Force.FromPoundsForce(qv),
    om.registry.N: lambda qv: UnitsNet.Force.FromNewtons(qv),
    om.registry.ft: lambda qv: UnitsNet.Length.FromFeet(qv),
    om.registry.m: lambda qv: UnitsNet.Length.FromMeters(qv),
    om.registry.lb: lambda qv: UnitsNet.Mass.FromPounds(qv),
    om.registry.kg: lambda qv: UnitsNet.Mass.FromKilograms(qv),
    om.registry.hp: lambda qv: UnitsNet.Power.FromMechanicalHorsepower(qv),
    om.registry.W: lambda qv: UnitsNet.Power.FromWatts(qv),
    om.registry.psi: lambda qv: UnitsNet.Pressure.FromPoundsForcePerSquareInch(qv),
    om.registry.kPa: lambda qv: UnitsNet.Pressure.FromKilopascals(qv),
    om.registry.oil_bbl / om.registry.min:
        lambda qv: SlurryRate(qv, UnitsNet.Units.VolumeUnit.OilBarrel, UnitsNet.Units.DurationUnit.Minute),
    ((om.registry.m ** 3) / om.registry.min):
        lambda qv: SlurryRate(qv, UnitsNet.Units.VolumeUnit.CubicMeter, UnitsNet.Units.DurationUnit.Minute),
    om.registry.degF: lambda qv: UnitsNet.Temperature.FromDegreesFahrenheit(qv),
    om.registry.degC: lambda qv: UnitsNet.Temperature.FromDegreesCelsius(qv),
    om.registry.oil_bbl: lambda qv: UnitsNet.Volume.FromOilBarrels(qv),
    (om.registry.m ** 3): lambda qv: UnitsNet.Volume.FromCubicMeters(qv),
}


def _us_oilfield_slurry_rate(qv):
    return UnitsNet.Density.FromPoundsPerCubicFoot(qv)


_PHYSICAL_QUANTITY_PINT_UNIT_NET_UNITS = {
    opq.PhysicalQuantity.DENSITY: {
        om.registry.lb / om.registry.cu_ft: _us_oilfield_slurry_rate,
        om.registry.lb / om.registry.ft ** 3: _us_oilfield_slurry_rate,
        om.registry.kg / (om.registry.m ** 3):
            lambda qv: UnitsNet.Density.FromKilogramsPerCubicMeter(qv),
    },
    opq.PhysicalQuantity.PROPPANT_CONCENTRATION: {
        om.registry.lb / om.registry.gal:
            lambda qv: ProppantConcentration(float(qv), UnitsNet.Units.MassUnit.Pound,
                                             UnitsNet.Units.VolumeUnit.UsGallon),
        om.registry.kg / (om.registry.m ** 3):
            lambda qv: ProppantConcentration(float(qv), UnitsNet.Units.MassUnit.Kilogram,
                                             UnitsNet.Units.VolumeUnit.CubicMeter),
    },
}


@as_net_quantity.register(opq.PhysicalQuantity)
@toolz.curry
def as_net_quantity_using_physical_quantity(physical_quantity, measurement: om.Quantity) -> UnitsNet.IQuantity:
    """
    Convert a `Quantity` instance to a .NET `UnitsNet.IQuantity` instance.

    Args:
        physical_quantity: The `PhysicalQuantity`. Although we try to determine a unique mapping between units
        in `pint` and .NET `UnitsNet` units, we cannot perform a unique mapping for density and proppant
        concentration measured in the metric system (the units of both these physical quantities are
        "kg/m**3").
        measurement: The `Quantity` instance to convert.

    Returns:
        The equivalent `UnitsNet.IQuantity` instance.
    """
    quantity = UnitsNet.QuantityValue.op_Implicit(measurement.magnitude)
    if physical_quantity == opq.PhysicalQuantity.DENSITY:
        return toolz.get_in([physical_quantity, measurement.units], _PHYSICAL_QUANTITY_PINT_UNIT_NET_UNITS)(quantity)

    if physical_quantity == opq.PhysicalQuantity.PROPPANT_CONCENTRATION:
        return toolz.get_in([physical_quantity, measurement.units],
                            _PHYSICAL_QUANTITY_PINT_UNIT_NET_UNITS)(measurement.magnitude)

    if physical_quantity == opq.PhysicalQuantity.SLURRY_RATE:
        return toolz.get(measurement.units, _PINT_UNIT_CREATE_NET_UNITS)(measurement.magnitude)

    return toolz.get(measurement.units, _PINT_UNIT_CREATE_NET_UNITS)(quantity)


@as_net_quantity.register(units.Common)
@toolz.curry
def as_net_quantity_using_common_units(to_common_unit, measurement: om.Quantity) -> UnitsNet.IQuantity:
    """
    Convert a `Quantity` instance to a .NET `UnitsNet.IQuantity` instance corresponding `to_unit`.

    Args:
        to_common_unit: The target unit of measurement.
        measurement: The `Quantity` instance to convert.

    Returns:
        The equivalent `UnitsNet.IQuantity` instance.
    """
    # units.Common support no conversion so simply call another implementation.
    return as_net_quantity(to_common_unit.value.physical_quantity, measurement)


@as_net_quantity.register(units.Metric)
@as_net_quantity.register(units.UsOilfield)
@toolz.curry
def as_net_quantity_in_specified_unit(specified_unit, measurement: om.Quantity) -> UnitsNet.IQuantity:
    """
    Convert a .NET UnitsNet.IQuantity to a `pint` `Quantity` instance in a specified, but compatible unit.

    Args:
        specified_unit: The unit for the converted `Quantity` instance.
        measurement: The `Quantity` instance to convert.

    Returns:
        The equivalent `Quantity` instance in the specified unit.
    """
    target_measurement = measurement.to(specified_unit.value.unit)
    return as_net_quantity(specified_unit.value.physical_quantity, target_measurement)


def equal_net_quantities(left_quantity: UnitsNet.IQuantity, right_quantity: UnitsNet.IQuantity,
                         comparison_details: EqualsComparisonDetails = EqualsComparisonDetails()):
    """
    Compares two UnitsNet.IQuantity instances for equality

    Python.NET transforms == (perhaps indirectly) into a call to Equals. Unfortunately, comparing
    two measurements that have been transformed may have floating point differences. Specifically,
    UnitsNet marks the `Equals` method as `Obsolete` with the following message:
    > "It is not safe to compare equality due to using System.Double as the internal representation.
    > It is very easy to get slightly different values due to floating point operations. Instead use
    > Equals(Length, double, ComparisonType) to provide the max allowed absolute or relative error."

    Consequently, to determine if two `UnitsNet.IQuantity` instances are equal, I use the
    `Equals(Length, double, ComparisonType)` method applied to each instance.

    Args:
        left_quantity: The `IQuantity` instance on the "left-hand-side" of the (implicit) == operator.
        right_quantity: The `IQuantity` instance on the "right-hand-side" of the (implicit) == operator.
        comparison_details: The details of how to compare the two `UnitsNet.IQuantity` instances.

    Returns:

    """
    return left_quantity.Equals(right_quantity, comparison_details.tolerance, comparison_details.comparison_type)


def microseconds_to_integral_milliseconds(to_convert: int) -> int:
    """
    Convert microseconds to an integral number of milliseconds.

    Args:
        to_convert: The milliseconds to convert.

    Returns:
        An integral number of milliseconds equivalent to `to_convert` microseconds.

    """
    return int(round(to_convert / 1000))


def net_decimal_to_float(net_decimal: Decimal) -> float:
    """
    Convert a .NET Decimal value to a Python float.

    Python.NET currently leaves .NET values of type `Decimal` unconverted. For example, UnitsNet models units
    of the physical quantity, power, as values of type .NET 'QuantityValue` whose `Value` property returns a
    value of .NET `Decimal` type. This function assists in converting those values to Python values of type
    `float`.

    Args:
        net_decimal: The .NET `Decimal` value to convert.

    Returns:
        A value of type `float` that is "equivalent" to the .NET `Decimal` value. Note that this conversion is
        "lossy" because .NET `Decimal` values are exact, but `float` values are not.
    """
    return Decimal.ToDouble(net_decimal)


_UNIT_NET_UNITS = {
    units.Common.ANGLE: UnitsNet.Units.AngleUnit.Degree,
    units.Common.DURATION: UnitsNet.Units.DurationUnit.Minute,
    units.UsOilfield.DENSITY: UnitsNet.Units.DensityUnit.PoundPerCubicFoot,
    units.Metric.DENSITY: UnitsNet.Units.DensityUnit.KilogramPerCubicMeter,
    units.UsOilfield.ENERGY: UnitsNet.Units.EnergyUnit.FootPound,
    units.Metric.ENERGY: UnitsNet.Units.EnergyUnit.Joule,
    units.UsOilfield.FORCE: UnitsNet.Units.ForceUnit.PoundForce,
    units.Metric.FORCE: UnitsNet.Units.ForceUnit.Newton,
    units.UsOilfield.LENGTH: UnitsNet.Units.LengthUnit.Foot,
    units.Metric.LENGTH: UnitsNet.Units.LengthUnit.Meter,
    units.UsOilfield.MASS: UnitsNet.Units.MassUnit.Pound,
    units.Metric.MASS: UnitsNet.Units.MassUnit.Kilogram,
    units.UsOilfield.POWER: UnitsNet.Units.PowerUnit.MechanicalHorsepower,
    units.Metric.POWER: UnitsNet.Units.PowerUnit.Watt,
    units.UsOilfield.PRESSURE: UnitsNet.Units.PressureUnit.PoundForcePerSquareInch,
    units.Metric.PRESSURE: UnitsNet.Units.PressureUnit.Kilopascal,
    units.UsOilfield.TEMPERATURE: UnitsNet.Units.TemperatureUnit.DegreeFahrenheit,
    units.Metric.TEMPERATURE: UnitsNet.Units.TemperatureUnit.DegreeCelsius,
    units.UsOilfield.VOLUME: UnitsNet.Units.VolumeUnit.OilBarrel,
    units.Metric.VOLUME: UnitsNet.Units.VolumeUnit.CubicMeter,
}


@toolz.curry
def _convert_net_quantity_to_different_unit(target_unit: units.UnitSystem,
                                            net_quantity: UnitsNet.IQuantity) -> UnitsNet.IQuantity:
    """
    Convert one .NET `UnitsNet.IQuantity` to another .NET `UnitsNet.IQuantity` in a different unit `target_unit`
    Args:
        net_quantity: The `UnitsNet.IQuantity` instance to convert.
        target_unit: The unit to which to convert `net_quantity`.

    Returns:
        The .NET `UnitsNet.IQuantity` converted to `target_unit`.
    """

    if _is_proppant_concentration(target_unit):
        return _create_proppant_concentration(net_quantity, target_unit)

    if _is_slurry_rate(target_unit):
        return _create_slurry_rate(net_quantity, target_unit)

    result = net_quantity.ToUnit(_UNIT_NET_UNITS[target_unit])
    return result


def _create_proppant_concentration(net_to_convert, target_unit):
    if target_unit == units.UsOilfield.PROPPANT_CONCENTRATION:
        mass_unit = UnitsNet.Units.MassUnit.Pound
        volume_unit = UnitsNet.Units.VolumeUnit.UsGallon
    elif target_unit == units.Metric.PROPPANT_CONCENTRATION:
        mass_unit = UnitsNet.Units.MassUnit.Kilogram
        volume_unit = UnitsNet.Units.VolumeUnit.CubicMeter
    # noinspection PyUnboundLocalVariable
    converted_magnitude = net_to_convert.As(mass_unit, volume_unit)
    return ProppantConcentration(converted_magnitude, mass_unit, volume_unit)


def _create_slurry_rate(net_to_convert, target_unit):
    if target_unit == units.UsOilfield.SLURRY_RATE:
        volume_unit = UnitsNet.Units.VolumeUnit.OilBarrel
    elif target_unit == units.Metric.SLURRY_RATE:
        volume_unit = UnitsNet.Units.VolumeUnit.CubicMeter
    duration_unit = UnitsNet.Units.DurationUnit.Minute
    # noinspection PyUnboundLocalVariable
    converted_magnitude = net_to_convert.As(volume_unit, duration_unit)
    return SlurryRate(converted_magnitude, volume_unit, duration_unit)


def _is_proppant_concentration(to_test):
    return (to_test == units.UsOilfield.PROPPANT_CONCENTRATION
            or to_test == units.Metric.PROPPANT_CONCENTRATION)


def _is_slurry_rate(to_test):
    return (to_test == units.UsOilfield.SLURRY_RATE
            or to_test == units.Metric.SLURRY_RATE)


def _net_decimal_to_float(net_decimal: Decimal) -> float:
    """
    Convert a .NET Decimal value to a Python float.

    Python.NET currently leaves .NET values of type `Decimal` unconverted. For example, UnitsNet models units
    of the physical quantity, power, as values of type .NET 'QuantityValue` whose `Value` property returns a
    value of .NET `Decimal` type. This function assists in converting those values to Python values of type
    `float`.

    Args:
        net_decimal: The .NET `Decimal` value to convert.

    Returns:
        A value of type `float` that is "equivalent" to the .NET `Decimal` value. Note that this conversion is
        "lossy" because .NET `Decimal` values are exact, but `float` values are not.
    """
    return Decimal.ToDouble(net_decimal)


_PHYSICAL_QUANTITY_NET_UNIT_PINT_UNITS = {
    opq.PhysicalQuantity.DENSITY: {
        UnitsNet.Units.DensityUnit.PoundPerCubicFoot: om.registry.lb / om.registry.ft ** 3,
        UnitsNet.Units.DensityUnit.KilogramPerCubicMeter: om.registry.kg / (om.registry.m ** 3),
    },
    opq.PhysicalQuantity.ENERGY: {
        UnitsNet.Units.EnergyUnit.FootPound: om.registry.ft_lb,
        UnitsNet.Units.EnergyUnit.Joule: om.registry.J,
    },
    opq.PhysicalQuantity.FORCE: {
        UnitsNet.Units.ForceUnit.PoundForce: om.registry.lbf,
        UnitsNet.Units.ForceUnit.Newton: om.registry.N,
    },
    opq.PhysicalQuantity.LENGTH: {
        UnitsNet.Units.LengthUnit.Foot: om.registry.ft,
        UnitsNet.Units.LengthUnit.Meter: om.registry.m,
    },
    opq.PhysicalQuantity.MASS: {
        UnitsNet.Units.MassUnit.Pound: om.registry.lb,
        UnitsNet.Units.MassUnit.Kilogram: om.registry.kg,
    },
    opq.PhysicalQuantity.POWER: {
        UnitsNet.Units.PowerUnit.MechanicalHorsepower: om.registry.hp,
        UnitsNet.Units.PowerUnit.Watt: om.registry.W,
    },
    opq.PhysicalQuantity.PRESSURE: {
        UnitsNet.Units.PressureUnit.PoundForcePerSquareInch: om.registry.psi,
        UnitsNet.Units.PressureUnit.Kilopascal: om.registry.kPa,
    },
    opq.PhysicalQuantity.TEMPERATURE: {
        UnitsNet.Units.TemperatureUnit.DegreeFahrenheit: om.registry.degF,
        UnitsNet.Units.TemperatureUnit.DegreeCelsius: om.registry.degC,
    },
    opq.PhysicalQuantity.VOLUME: {
        UnitsNet.Units.VolumeUnit.OilBarrel: om.registry.oil_bbl,
        UnitsNet.Units.VolumeUnit.CubicMeter: om.registry.m ** 3,
    },
}


def _to_pint_unit(physical_quantity: opq.PhysicalQuantity, net_unit: UnitsNet.Units) -> om.Unit:
    """
    Convert `net_unit`, a unit of measure for `physical_quantity`, to a `pint` unit.

    Args:
        physical_quantity: The physical quantity measured by `net_unit`.
        net_unit: The .NET UnitsNet.Unit to be converted.

    Returns:
        The `pint` Unit corresponding to `net_unit`.
    """
    result = toolz.get_in([physical_quantity, net_unit], _PHYSICAL_QUANTITY_NET_UNIT_PINT_UNITS)
    if result is not None:
        return result
    elif physical_quantity == opq.PhysicalQuantity.ANGLE:
        return om.registry.deg
    elif physical_quantity == opq.PhysicalQuantity.DURATION:
        return om.registry.min
