import PySimpleGUI as sg
import ast
from src.util.config_dicts.get_standard_dict import get_standard_config_dictionary
from src.gui.custom_components import title, question_mark_button
from src.gui.help_dictionary import help_text
from src.gui.custom_windows import show_help_window

class StandardScreen:

    def __init__(self):
        question_mark_padding = ((0, 0), (0, 0))
        self.layout = [[title('Standard runs')],
                       [sg.Text('Configuration name'), sg.Input(key='standard_name_input'),
                        sg.Input(key='standard_dummy_import', enable_events=True, visible=False, size=(0, 0)),
                        sg.FileBrowse('Import Run Configuration', file_types=[("Text Files", "*.txt")],
                                      target='standard_dummy_import', key='standard_import_button')],
                       [sg.Text('Model file name'), sg.Input(key='standard_model_input'),
                        sg.Input(key='standard_model_dummy_import', enable_events=True, visible=False, size=(0, 0)),
                        sg.FileBrowse('Import model', file_types=[("NetLogo Files", "*.nlogo")],
                                      target='standard_model_dummy_import', key='standard_model_import_button')],
                       [question_mark_button('standard_value_help_button'),
                        sg.Text('Set variables as follows:')],
                       [sg.Multiline(key='standard_value_input')],
                       [sg.Text('Explain the format: variable-name variable-value')],
                       [question_mark_button('standard_repetition_help_button'),
                        sg.Text('Number of repetitions:'),
                        sg.Input('10', key='standard_repetition_input')],
                       [question_mark_button('standard_tick_help_button'),
                        sg.Text('Maximum number of ticks per run:'),
                        sg.Input('100', key='standard_tick_input')],
                       [question_mark_button('standard_reporter_help_button'),
                        sg.Text('Measure runs using these reporters:')],
                       [sg.Multiline(key='standard_reporter_input')],
                       [sg.Text('Only input a single reporter on each line')],
                       [question_mark_button('standard_setup_help_button'),
                        sg.Text('Setup commands:')],
                       [sg.Multiline('setup', key='standard_setup_input')],
                       [question_mark_button('standard_process_help_button'),
                        sg.Text('Number of parallel executors:'),
                        sg.Input('2', key='standard_process_input')],
                       [sg.Button('Run', key="standard_run_button")],
                       [sg.Button('Back', key="standard_back_button"),
                        sg.Input(key='standard_dummy_export', enable_events=True, visible=False, size=(0, 0)),
                        sg.SaveAs('Save Run Configuration', file_types=[("Text Files", "*.txt")],
                                  target='standard_dummy_export', key="standard_save_button")]]

    def check_events(self, event, values, window):
        if event == 'standard_run_button':
            valid, error_message = self.validate_user_input(values)
            if not valid:
                window.write_event_value('show_error_window', error_message)
                return

            window['standard_panel'].update(visible=False)
            window['run_panel'].update(visible=True)
            window.read(timeout=0.01)

            window.write_event_value('standard_run_signal', '')
        if event == 'standard_dummy_import' and not (values['standard_dummy_import'] == ''):
            self.import_run(window, values['standard_dummy_import'])
        if event == 'standard_model_dummy_import' and not (values['standard_model_dummy_import'] == ''):
            window['standard_model_input'].update(values['standard_model_dummy_import'])
        if event == 'standard_dummy_export' and not (values['standard_dummy_export'] == ''):
            self.export_run(values, values['standard_dummy_export'])
        if event == 'standard_back_button':
            window['main_panel'].update(visible=True)
            window['standard_panel'].update(visible=False)

        # Help events
        if event == 'standard_value_help_button':
            show_help_window(help_text['standard_variables'], location=window.CurrentLocation())
        if event == 'standard_repetition_help_button':
            show_help_window(help_text['run_repetitions'], location=window.CurrentLocation())
        if event == 'standard_tick_help_button':
            show_help_window(help_text['run_ticks'], location=window.CurrentLocation())
        if event == 'standard_reporter_help_button':
            show_help_window(help_text['run_reporters'], location=window.CurrentLocation())
        if event == 'standard_setup_help_button':
            show_help_window(help_text['run_setup'], location=window.CurrentLocation())
        if event == 'standard_process_help_button':
            show_help_window(help_text['run_processes'], location=window.CurrentLocation())

    def import_run(self, window, file_path):
        f = open(file_path, "r")
        run_string = f.read()
        f.close()

        try:
            run_dict = ast.literal_eval(run_string)
            window['standard_name_input'].update(run_dict['Configuration Name'])
            window['standard_model_input'].update(run_dict['Model file'])
            window['standard_value_input'].update('\n'.join(run_dict['Variable values']))
            window['standard_repetition_input'].update(run_dict['Repetitions'])
            window['standard_tick_input'].update(run_dict['Ticks per run'])
            window['standard_reporter_input'].update('\n'.join(run_dict['NetLogo reporters']))
            window['standard_setup_input'].update('\n'.join(run_dict['Setup commands']))
            window['standard_process_input'].update(run_dict['Parallel executors'])
        except (SyntaxError, KeyError, TypeError, IndexError):
            window.write_event_value('show_error_window', 'Invalid file syntax for standard configuration')
            return

    def export_run(self, values, file_path):
        run_dict = get_standard_config_dictionary(values)

        f = open(file_path, "w")
        f.write(str(run_dict))
        f.close()

    def validate_user_input(self, values):
        if values['standard_model_input'] == '' or \
                values['standard_value_input'] == '\n' or \
                values['standard_repetition_input'] == '' or \
                values['standard_tick_input'] == '' or \
                values['standard_reporter_input'] == '\n' or \
                values['standard_setup_input'] == '\n' or \
                values['standard_process_input'] == '':
            return False, 'Error in input: One or more field are empty. ' \
                          'Please make sure all options are filled out.'

        try:
            repetitions = int(values['standard_repetition_input'])
        except ValueError:
            return False, 'Error in input: Invalid value for the number of repetitions. ' \
                          'Please make sure it\'s an integer'
        try:
            repetitions = int(values['standard_tick_input'])
        except ValueError:
            return False, 'Error in input: Invalid value for the maximum number of ticks. ' \
                          'Please make sure it\'s an integer'
        try:
            process_amount = int(values['standard_process_input'])
        except ValueError:
            return False, 'Error in input: Invalid value for the number of executors. Please make sure it\'s an integer'

        return True, ''
