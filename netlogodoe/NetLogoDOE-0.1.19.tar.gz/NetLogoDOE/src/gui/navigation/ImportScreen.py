import PySimpleGUI as sg
import ast
import pandas as pd
from NetLogoDOE.src.gui.custom_components import title, explanation, question_mark_button
from NetLogoDOE.src.gui.custom_windows import show_help_window
from NetLogoDOE.src.gui.help_dictionary import help_text


class ImportScreen:

    def __init__(self):
        button_size = (25, 1)
        button_pad = ((5, 0), (20, 0))
        self.layout = [[title('Import results')],
                       [sg.Input(key='import_dummy_experiment_results', enable_events=True, visible=False, size=(0, 0)),
                        sg.FileBrowse('Import experiment results', file_types=[("Text Files", "*.txt")],
                                      target='import_dummy_experiment_results',
                                      key='import_experiment_results_button', size=button_size, pad=button_pad),
                        question_mark_button('import_experiment_results_help_button', padding=button_pad)],
                       [explanation('whatever needs ot be said')],
                       [sg.Input(key='import_dummy_standard_results', enable_events=True, visible=False, size=(0, 0)),
                        sg.FileBrowse('Import standard results', file_types=[("Text Files", "*.txt")],
                                      target='import_dummy_standard_results',
                                      key='import_standard_results_button', size=button_size, pad=button_pad),
                        question_mark_button('import_standard_results_help_button', padding=button_pad)],
                       [explanation('whatever needs ot be said')],
                       [sg.Input(key='import_dummy_behaviorspace_results', enable_events=True, visible=False,
                                 size=(0, 0)),
                        sg.FileBrowse('Import BehaviorSpace results', file_types=[("Text Files", "*.txt")],
                                      target='import_dummy_behaviorspace_results',
                                      key='import_behaviorspace_results_button', size=button_size, pad=button_pad),
                        question_mark_button('import_behaviorspace_results_help_button', padding=button_pad)],
                       [explanation('whatever needs ot be said')],
                       [sg.Button('Back', key='import_back_button', pad=button_pad)]
                       ]

    def check_events(self, event, values, window):
        if event == 'import_dummy_experiment_results' and not (values['import_dummy_experiment_results'] == ''):
            self.import_experiment_results(values['import_dummy_experiment_results'], window)
        if event == 'import_dummy_standard_results' and not (values['import_dummy_standard_results'] == ''):
            self.import_standard_results(values['import_dummy_standard_results'], window)
        if event == 'import_dummy_behaviorspace_results' and not (values['import_dummy_behaviorspace_results'] == ''):
            self.import_behaviorspace_results(values['import_dummy_behaviorspace_results'], window)
        if event == 'import_back_button':
            window['main_panel'].update(visible=True)
            window['import_panel'].update(visible=False)

        # Help events
        if event == 'import_experiment_results_help_button':
            show_help_window(help_text['import_experiment'], location=window.CurrentLocation())
        if event == 'import_standard_results_help_button':
            show_help_window(help_text['import_standard'], location=window.CurrentLocation())
        if event == 'import_behaviorspace_results_help_button':
            show_help_window(help_text['import_behaviorspace'], location=window.CurrentLocation())


    def import_experiment_results(self, file_path, window):
        f = open(file_path, "r")
        experiment_string = f.read()
        f.close()

        try:
            experiment_dict = ast.literal_eval(experiment_string)
            config = experiment_dict['Configuration']
            exp = pd.DataFrame(experiment_dict['Parameter values'], columns=experiment_dict['Parameter names'])
            outcomes = experiment_dict['Reporter values']
        except (SyntaxError, KeyError):
            window.write_event_value('show_error_window', 'Invalid file syntax for experimental results')
            return

        window.write_event_value('experiment_write_results_event', (exp, outcomes, config))
        window['import_panel'].update(visible=False)
        window['experiment_result_panel'].update(visible=True)

    def import_standard_results(self, file_path, window):
        f = open(file_path, "r")
        standard_string = f.read()
        f.close()

        try:
            standard_dict = ast.literal_eval(standard_string)
            config = standard_dict['Configuration']
            results = (standard_dict['Parameter settings'], standard_dict['Reporter values'], config)
        except (SyntaxError, KeyError):
            window.write_event_value('show_error_window', 'Invalid file syntax for standard results')
            return

        window.write_event_value('standard_write_results_event', results)
        window['import_panel'].update(visible=False)
        window['standard_result_panel'].update(visible=True)

    def import_behaviorspace_results(self, file_path, window):
        print(file_path)
        print('Not implemented yet')
