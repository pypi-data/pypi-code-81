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


from collections import namedtuple
from typing import Callable

from orchid import (
    project_loader as loader,
    net_quantity as onq,
    physical_quantity as opq,
)

#
# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics import IStage
# noinspection PyUnresolvedReferences,PyPackageRequirements
from Orchid.FractureDiagnostics.Calculations import (ICalculationResult,
                                                     ITreatmentCalculations)
# noinspection PyUnresolvedReferences,PyPackageRequirements
from System import DateTime


CalculationResult = namedtuple('CalculationResult', ['measurement', 'warnings'])


def perform_calculation(native_calculation_func: Callable[[ITreatmentCalculations, IStage, DateTime, DateTime],
                                                          ICalculationResult],
                        stage: IStage, start: DateTime, stop: DateTime, physical_quantity: opq.PhysicalQuantity):
    """
    Perform the specific native calculation function for stage from start through (and including) stop.

    Args:
        native_calculation_func: The specific native treatment calculation function.
        stage: The stage on which the calculation is being made.
        start: The (inclusive) start time of the calculation.
        stop: The (inclusive) stop time of the calculation.
        physical_quantity: The physical quantity of the measurement to be returned as the result.

    Returns:
        The calculation result (measurement and warnings) for the calculation.
    """
    native_treatment_calculations = loader.native_treatment_calculations()
    native_calculation_result = native_calculation_func(native_treatment_calculations, stage, start, stop)
    calculation_measurement = onq.as_measurement(physical_quantity, native_calculation_result.Result)
    warnings = native_calculation_result.Warnings
    return CalculationResult(calculation_measurement, warnings)


def median_treating_pressure(stage: IStage, start: DateTime, stop: DateTime):
    """
    Return the median treating pressure for stage from start to (and including) stop.

    Args:
        stage: The stage on which the calculation is being made.
        start: The (inclusive) start time of the calculation.
        stop: The (inclusive) stop time of the calculation.

    Returns:
        The median treating pressure result (measurement and warnings).
    """
    def median_treatment_pressure_calculation(calculations, for_stage, start_time, stop_time):
        calculation_result = calculations.GetMedianTreatmentPressure(for_stage.dom_object,
                                                                     onq.as_net_date_time(start_time),
                                                                     onq.as_net_date_time(stop_time))
        return calculation_result

    result = perform_calculation(median_treatment_pressure_calculation,
                                 stage, start, stop, opq.PhysicalQuantity.PRESSURE)
    return result


def pumped_fluid_volume(stage: IStage, start: DateTime, stop: DateTime):
    """
    Return the pumped (fluid) volume for stage from start to (and including) stop.

    Args:
        stage: The stage on which the calculation is being made.
        start: The (inclusive) start time of the calculation.
        stop: The (inclusive) stop time of the calculation.

    Returns:
        The pumped (fluid) volume result (measurement and warnings).
    """

    def pumped_fluid_volume_calculation(calculations, for_stage, start_time, stop_time):
        calculation_result = calculations.GetPumpedVolume(for_stage.dom_object, onq.as_net_date_time(start_time),
                                                          onq.as_net_date_time(stop_time))
        return calculation_result

    result = perform_calculation(pumped_fluid_volume_calculation, stage, start, stop, opq.PhysicalQuantity.VOLUME)
    return result


def total_proppant_mass(stage: IStage, start: DateTime, stop: DateTime):
    """
    Return the pumped (fluid) volume for stage from start to (and including) stop.

    Args:
        stage: The stage on which the calculation is being made.
        start: The (inclusive) start time of the calculation.
        stop: The (inclusive) stop time of the calculation.

    Returns:
        The pumped (fluid) volume result (measurement and warnings).
    """
    def total_proppant_mass_calculation(calculations, for_stage, start_time, stop_time):
        calculation_result = calculations.GetTotalProppantMass(for_stage.dom_object,
                                                               onq.as_net_date_time(start_time),
                                                               onq.as_net_date_time(stop_time))
        return calculation_result

    result = perform_calculation(total_proppant_mass_calculation, stage, start, stop, opq.PhysicalQuantity.MASS)
    return result
