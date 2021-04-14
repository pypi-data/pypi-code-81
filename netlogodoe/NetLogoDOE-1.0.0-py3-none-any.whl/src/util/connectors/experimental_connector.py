import math

import pyNetLogo as pnl
from pyNetLogo.core import NetLogoException


def run_experiments(child_conn, values, problem, param_samples, param_values, netlogo_version, netlogo_home):
    outcomes = {}
    repetitions = int(values['experiment_repetition_input'])
    ticks = int(values['experiment_tick_input'])
    steps = 100 / (len(param_samples) * repetitions)
    progress_bar = 1

    reporters = split_user_input(values['experiment_reporter_input'])
    for reporter in reporters:
        outcomes[reporter] = []

    try:
        netlogo = pnl.NetLogoLink(gui=False, netlogo_version=netlogo_version, netlogo_home=netlogo_home)
    except (TypeError, KeyError):
        child_conn.send(get_failure_message('Error in input: Invalid NetLogo version or path. Please make sure the '
                                            'values in gui_user.py are correct (this requires a restart of the GUI).'))
        return

    model = values['experiment_model_input']
    try:
        netlogo.load_model(model)
    except (FileNotFoundError, NetLogoException):
        child_conn.send(get_failure_message('Error in input: Invalid model file path. Please make sure the file path is'
                                            ' correct and points to a valid .nlogo file.'))
        return

    for scenario in range(len(param_samples)):
        for i, name in enumerate(problem['names']):
            if name == 'random-seed':
                netlogo.command(f'random-seed {param_samples[scenario, i]}')
            else:
                try:
                    netlogo.command(f'set {name} {param_samples[scenario, i]}')
                except NetLogoException:
                    child_conn.send(get_failure_message('Error in input: Invalid variable bounds input. Please '
                                                        'make sure all variable names and their bounds are correct.'))
                    netlogo.kill_workspace()
                    return

        for set_command in param_values:
            try:
                netlogo.command(f'set {set_command}')
            except NetLogoException:
                child_conn.send(get_failure_message('Error in input: Invalid variable value input. Please '
                                                    'make sure all variable names and their values are correct.'))
                netlogo.kill_workspace()
                return

        run_list = {}
        for reporter in reporters:
            run_list[reporter] = []

        for run in range(repetitions):
            setup_commands = split_user_input(values['experiment_setup_input'])
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
                run_list[reporter].append(list(results[reporter]))

            if (repetitions * scenario + run) * steps > progress_bar:
                progress_bar = math.ceil(progress_bar + steps)
                if steps < 1:
                    child_conn.send({'Progress': 1, 'Results': []})
                else:
                    child_conn.send({'Progress': steps, 'Results': []})
        for reporter in reporters:
            outcomes[reporter].append(run_list[reporter])

    netlogo.kill_workspace()

    results = (param_samples, outcomes)
    child_conn.send({'Progress': steps, 'Results': results})


def split_user_input(input):
    rows = input.split('\n')
    rows = list(filter(('').__ne__, rows))
    mapped_rows = list(map(lambda x: x.strip(), rows))
    return mapped_rows


def get_failure_message(msg):
    return {'Progress': 'Failure', 'Results': msg}
