import PySimpleGUI as sg
from NetLogoDOE.src.gui.custom_components import title, configuration_parameter_text, configuration_value_text, configuration_horizontal_line


class StandardConfigTableScreen:

    def __init__(self):
        self.layout = [[title('Standard Configuration')],
                       [configuration_parameter_text('Configuration Name:'),
                        configuration_value_text('', 'standard_configtable_configuration_text')],
                       [configuration_horizontal_line()],
                       [configuration_parameter_text('Model file:'),
                        configuration_value_text('', 'standard_configtable_model_text')],
                       [configuration_horizontal_line()],
                       [configuration_parameter_text('Parameter bounds:'),
                        configuration_value_text('', 'standard_configtable_variable_text')],
                       [configuration_horizontal_line()],
                       [configuration_parameter_text('Repetitions:'),
                        configuration_value_text('', 'standard_configtable_repetition_text')],
                       [configuration_horizontal_line()],
                       [configuration_parameter_text('Ticks per run:'),
                        configuration_value_text('', 'standard_configtable_tick_text')],
                       [configuration_horizontal_line()],
                       [configuration_parameter_text('NetLogo reporters:'),
                        configuration_value_text('', 'standard_configtable_reporter_text')],
                       [configuration_horizontal_line()],
                       [configuration_parameter_text('Setup commands:'),
                        configuration_value_text('', 'standard_configtable_setup_text')],
                       [configuration_horizontal_line()],
                       [configuration_parameter_text('Parallel executors:'),
                        configuration_value_text('', 'standard_configtable_process_text')],
                       [configuration_horizontal_line()],
                       [sg.Button('Back', key='standard_configtable_back_button')]]
        self.results = None

    def check_events(self, event, values, window):
        if event == 'standard_write_results_event':
            self.results = values['standard_write_results_event']
            self.fill_table_values(self.results[2], window)

        if event == 'standard_configtable_back_button':
            window['standard_configtable_panel'].update(visible=False)
            window['standard_result_panel'].update(visible=True)

    def fill_table_values(self, values, window):
        window['standard_configtable_configuration_text'].update(values[0][1])
        window['standard_configtable_configuration_text'].set_size((len(values[0][1]), 1))

        window['standard_configtable_model_text'].update(values[1][1])
        window['standard_configtable_model_text'].set_size((len(values[1][1]), 1))

        window['standard_configtable_variable_text'].update('\n'.join(values[2][1]))
        window['standard_configtable_variable_text'].set_size(
            (len(max(values[2][1], key=len)) + 2, len(values[2][1])))

        window['standard_configtable_repetition_text'].update(values[3][1])
        window['standard_configtable_repetition_text'].set_size((10, 1))

        window['standard_configtable_tick_text'].update(values[4][1])
        window['standard_configtable_tick_text'].set_size((10, 1))

        window['standard_configtable_reporter_text'].update('\n'.join(values[5][1]))
        window['standard_configtable_reporter_text'].set_size(
            (len(max(values[5][1], key=len)) + 2, len(values[5][1])))

        window['standard_configtable_setup_text'].update('\n'.join(values[6][1]))
        window['standard_configtable_setup_text'].set_size(
            (len(max(values[6][1], key=len)) + 2, len(values[6][1])))

        window['standard_configtable_process_text'].update(values[7][1])
        window['standard_configtable_process_text'].set_size((10, 1))
