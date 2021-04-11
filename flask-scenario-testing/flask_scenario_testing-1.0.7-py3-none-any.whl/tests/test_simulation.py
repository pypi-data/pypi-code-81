import pytest

from flask_scenario_testing.backend.Simulation import Simulation


def test_can_start_simulation():
    simulation = Simulation()

    simulation.start()

    assert simulation.is_running()


def test_cant_stop_simulation_thats_not_running():
    simulation = Simulation()

    with pytest.raises(Exception):
        simulation.stop()


def test_can_not_start_simulation_thats_already_running():
    simulation = Simulation()
    simulation.start()

    with pytest.raises(Exception):
        simulation.start()


def test_can_start_scenario():
    simulation = Simulation()
    simulation.start()

    simulation.start_scenario('5 users')

    assert simulation.scenario_is_running()

    running_scenario = simulation.running_scenario()
    assert running_scenario.name() == '5 users'
    assert running_scenario.started_at()
    assert not running_scenario.has_modifiers()


def test_starting_a_second_scenario_will_stop_previous_scenario():
    simulation = Simulation()
    simulation.start()

    simulation.start_scenario('5 users')
    assert simulation.scenarios()[0].is_running()

    simulation.start_scenario('10 users')
    assert not simulation.scenarios()[0].is_running()
    assert simulation.scenarios()[1].is_running()

    simulation.start_scenario('15 users')
    assert not simulation.scenarios()[0].is_running()
    assert not simulation.scenarios()[1].is_running()
    assert simulation.scenarios()[2].is_running()


def test_can_stop_running_scenario():
    simulation = Simulation()

    simulation.start()
    simulation.start_scenario('5 users')
    simulation.stop_running_scenario()

    assert not simulation.scenario_is_running()
    assert simulation.scenarios()[0].started_at() is not None
    assert not simulation.scenarios()[0].is_running()


def test_can_convert_to_dict():
    simulation = Simulation()

    simulation.start()
    simulation.start_scenario('5 users')