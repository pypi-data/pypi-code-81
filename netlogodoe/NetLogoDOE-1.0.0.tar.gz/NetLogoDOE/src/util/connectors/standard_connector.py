import math

import pyNetLogo as pnl
from pyNetLogo.core import NetLogoException


def run_standard(child_conn, values, repetitions, netlogo_version, netlogo_home):
    outcomes = {}
    ticks = int(values['standard_tick_input'])
    steps = 100 / repetitions
    progress_bar = 1

    reporters = split_user_input(values['standard_reporter_input'])
    for reporter in reporters:
        outcomes[reporter] = []

    try:
        netlogo = pnl.NetLogoLink(gui=False, netlogo_version=netlogo_version, netlogo_home=netlogo_home)
    except (TypeError, KeyError):
        child_conn.send(get_failure_message('Error in input: Invalid NetLogo version or path. Please make sure the '
                                            'values in gui_user.py are correct (this requires a restart of the GUI).'))
        return

    model = values['standard_model_input']
    try:
        netlogo.load_model(model)
    except (FileNotFoundError, NetLogoException):
        child_conn.send(get_failure_message('Error in input: Invalid model file path. Please make sure the file path is'
                                            ' correct and points to a valid .nlogo file.'))
        return

    try:
        param_values = get_variable_dictionary(values['standard_value_input'])
    except (ValueError, IndexError):
        child_conn.send(get_failure_message('Error in input: Invalid parameter input. Please '
                                            'make sure the input uses the correct format.'))
        return

    for key in param_values.keys():
        try:
            netlogo.command(f'set {key} {param_values[key]}')
        except NetLogoException:
            child_conn.send(get_failure_message('Error in input: Invalid parameter input. Please '
                                                'make sure all variable names and their values are correct.'))
            netlogo.kill_workspace()
            return

    for run in range(repetitions):
        setup_commands = split_user_input(values['standard_setup_input'])
        for command in setup_commands:
            try:
                netlogo.command(command)
            except NetLogoException:
                child_conn.send(get_failure_message('Error in input: Invalid setup commands. Please '
                                                    'make sure they\'re all valid NetLogo commands'))
                netlogo.kill_workspace()
                return

        try:
            results = netlogo.repeat_report(reporters, ticks)
        except NetLogoException:
            child_conn.send(get_failure_message('Error in input: Invalid reporter commands. Please '
                                                'make sure all reporters are valid NetLogo commands'))
            netlogo.kill_workspace()
            return

        for reporter in outcomes.keys():
            outcomes[reporter].append(list(results[reporter]))

        if run * steps > progress_bar:
            progress_bar = math.ceil(progress_bar + steps)
            if steps < 1:
                child_conn.send({'Progress': 1, 'Results': []})
            else:
                child_conn.send({'Progress': steps, 'Results': []})

    netlogo.kill_workspace()

    results = param_values, outcomes
    child_conn.send({'Progress': steps, 'Results': results})


def split_user_input(input):
    rows = input.split('\n')
    rows = list(filter(('').__ne__, rows))
    mapped_rows = list(map(lambda x: x.strip(), rows))
    return mapped_rows


def get_variable_dictionary(var_values):
    rows = var_values.split('\n')
    rows = list(filter(('').__ne__, rows))
    stripped_rows = list(map(lambda x: x.strip().split(' '), rows))
    return {x[0]: x[1] for x in stripped_rows}


def get_failure_message(msg):
    return {'Progress': 'Failure', 'Results': msg}
