def get_experiment_config_dictionary(values):
    experiment_dict = {}
    experiment_dict['Experiment Name'] = values['experiment_name_input']
    experiment_dict['Model file'] = values['experiment_model_input']
    bounds = list(filter(''.__ne__, values['experiment_parameter_input'].split('\n')))
    experiment_dict['Parameter values'] = list(map(lambda x: x.strip(), bounds))
    experiment_dict['Number of scenarios'] = values['experiment_scenario_input']
    experiment_dict['Repetitions'] = values['experiment_repetition_input']
    experiment_dict['Ticks per run'] = values['experiment_tick_input']
    reporters = list(filter(''.__ne__, values['experiment_reporter_input'].split('\n')))
    experiment_dict['NetLogo reporters'] = list(map(lambda x: x.strip(), reporters))
    setup_commands = list(filter(''.__ne__, values['experiment_setup_input'].split('\n')))
    experiment_dict['Setup commands'] = list(map(lambda x: x.strip(), setup_commands))
    experiment_dict['Parallel executors'] = values['experiment_process_input']
    return experiment_dict