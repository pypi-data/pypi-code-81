# coding: utf-8
from collections import namedtuple
from datetime import datetime
from time import sleep

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_optional
from flask_scenario_testing.backend.Simulation import Simulation, simulation

blueprint = Blueprint('scenario-testing', __name__)

Measurement = namedtuple('Measurement', ['time', 'measurement'])


def success():
    return jsonify({'status': 'success'})


def get_cpu_usage_measurements(start: datetime, end: datetime):
    from flask_scenario_testing.backend.initialise_scenario_testing import cpu_percents_measurements

    return [
        {'time': measurement.time.isoformat(), 'measurement': measurement.value}
        for measurement in cpu_percents_measurements
        if start <= measurement.time <= end
    ]


@blueprint.route('/api/simulation/start', methods=('POST',))
@jwt_optional
def start_simulation():
    print('Starting simulation')

    simulation.start()

    return success()


@blueprint.route('/api/simulation/start-scenario', methods=('POST',))
@jwt_optional
def start_new_scenario():
    data = request.json

    print('Starting new scenario')

    simulation.start_scenario(data['name'], data['modifiers'])

    return success()


@blueprint.route('/api/simulation/stop-running-scenario', methods=('POST',))
@jwt_optional
def stop_running_scenario():
    print('Stopping running scenario')

    simulation.stop_running_scenario()

    return success()


@blueprint.route('/api/simulation/stop', methods=('POST',))
@jwt_optional
def stop_simulation():
    adjusted_ms = request.json['adjust_ms']
    print('Adjusted ms: {}'.format(adjusted_ms))

    from flask_scenario_testing.backend.initialise_scenario_testing import latency_measurements

    simulation.stop()

    endpoints = []
    for (endpoint_name, measurements) in latency_measurements.items():
        endpoints.append(dict(
            active=len(measurements) > 0,
            latency_measurements=[dict(
                measurement=m.value - float(adjusted_ms),
                time=m.time.isoformat()
            ) for m in measurements],
            name=endpoint_name,
            request_count=len(measurements)
        ))

    cpu_usage_measurements = get_cpu_usage_measurements(simulation.started_at(), simulation.stopped_at())

    scenario_data = []

    for scenario in simulation.scenarios():
        scenario_data.append(dict(
            start=scenario.started_at().isoformat(),
            end=scenario.ended_at().isoformat(),
            modifiers=scenario.modifiers(),
            name=scenario.name()
        ))

    return jsonify(dict(
        started_at=simulation.started_at().isoformat(),
        stopped_at=simulation.stopped_at().isoformat(),
        scenarios=scenario_data,
        endpoints=endpoints,
        cpu_usage_measurements=cpu_usage_measurements
    ))


@blueprint.route('/api/measure-travel-time', methods=('POST',))
@jwt_optional
def measure_travel_time():
    return jsonify(dict(
        current_time=datetime.utcnow().isoformat()
    ))
