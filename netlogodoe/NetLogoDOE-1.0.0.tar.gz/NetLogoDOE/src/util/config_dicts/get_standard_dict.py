def get_standard_config_dictionary(values):
    run_dict = {}
    run_dict['Configuration Name'] = values['standard_name_input']
    run_dict['Model file'] = values['standard_model_input']
    var_values = list(filter(''.__ne__, values['standard_value_input'].split('\n')))
    run_dict['Parameter values'] = list(map(lambda x: x.strip(), var_values))
    run_dict['Repetitions'] = values['standard_repetition_input']
    run_dict['Ticks per run'] = values['standard_tick_input']
    reporters = list(filter(''.__ne__, values['standard_reporter_input'].split('\n')))
    run_dict['NetLogo reporters'] = list(map(lambda x: x.strip(), reporters))
    setup_commands = list(filter(''.__ne__, values['standard_setup_input'].split('\n')))
    run_dict['Setup commands'] = list(map(lambda x: x.strip(), setup_commands))
    run_dict['Parallel executors'] = values['standard_process_input']
    return run_dict
