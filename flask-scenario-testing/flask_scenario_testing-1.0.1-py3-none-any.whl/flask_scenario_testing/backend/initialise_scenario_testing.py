from collections import defaultdict
from datetime import datetime
from functools import wraps
import time

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
import flask_scenario_testing.backend.views as scenario_testing_views
import psutil

from flask_scenario_testing.analysis.support.Measurement import Measurement
from flask_scenario_testing.backend.Simulation import simulation
from flask_scenario_testing.backend.modifiers import Modifier

registered_modifier_types = {}
scheduler = BackgroundScheduler()
cpu_percents_measurements = []
latency_measurements = {}


def add_regression_wrapper(app, endpoint_name):
    f = app.view_functions[endpoint_name]

    @wraps(f)
    def wrapper(*args, **kwargs):
        relevant_regressions = [c for c in simulation.current_modifiers() if c['endpoint_name'] == endpoint_name]

        new_f = f
        for regression in relevant_regressions:
            regression_type = regression['type']

            apply = [c for c in registered_modifier_types if c.identifier() == regression_type]

            for a in apply:
                new_f = a.modify(f, endpoint_name, regression['args'])

        return new_f(*args, **kwargs)

    wrapper.original = f
    app.view_functions[endpoint_name] = wrapper


def add_latency_tracking_wrapper(app, endpoint_name):
    f = app.view_functions[endpoint_name]

    latency_measurements[endpoint_name] = []

    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = float(request.headers.get('sent-at', time.time()))

        results = f(*args, **kwargs)

        duration_in_ms = (time.time() - start_time) * 1000

        print('{}: {} ms'.format(endpoint_name, duration_in_ms))

        latency_measurements[endpoint_name].append(Measurement(
            time=datetime.utcnow(),
            value=duration_in_ms
        ))

        return results

    wrapper.original = f
    app.view_functions[endpoint_name] = wrapper


def get_cpu_percent():
    return max(psutil.cpu_percent(percpu=True))


def track_cpu_percent():
    cpu_percent = get_cpu_percent()

    cpu_percents_measurements.append(Measurement(time=datetime.utcnow(), value=cpu_percent))

    print('CPU: {}%'.format(cpu_percent))


def start_cpu_usage_tracker():
    scheduler.add_job(func=track_cpu_percent, trigger='interval', seconds=1)
    scheduler.start()


def initialise_scenario_testing(app: Flask, modifier_types: [Modifier]):
    app.register_blueprint(scenario_testing_views.blueprint)

    start_cpu_usage_tracker()

    global registered_modifier_types
    registered_modifier_types = modifier_types

    for rule in app.url_map.iter_rules():
        endpoint_name = rule.endpoint

        if endpoint_name.startswith('scenario-testing'):
            continue

        add_regression_wrapper(app, endpoint_name)
        add_latency_tracking_wrapper(app, endpoint_name)
