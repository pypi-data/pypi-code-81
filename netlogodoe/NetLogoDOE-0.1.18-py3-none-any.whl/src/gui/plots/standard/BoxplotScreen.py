import PySimpleGUI as sg
from src.util.data_processing.merge_standard_data import merge_data
import plotly.graph_objects as go
from src.gui.custom_components import title, question_mark_button
from src.gui.custom_windows import show_help_window
from src.gui.help_dictionary import help_text

class BoxplotScreen:

    def __init__(self):
        self.layout = [[title('Boxplot')],
                       [sg.Text('Graph Title: '), sg.Input('', key='boxplot_title_input')],
                       [question_mark_button('boxplot_reporter_help_button'), sg.Text('Reporters to plot:')],
                       [sg.Multiline('count sheep', key='boxplot_reporter_input')],
                       [sg.Text('Only input a single reporter on each line')],
                       [sg.Button('Generate', key='boxplot_generate_button')],
                       [sg.Button('Back', key='boxplot_back_button')]]
        self.results = None

    def check_events(self, event, values, window):
        if event == 'standard_write_results_event':
            self.results = values['standard_write_results_event']
        if event == 'boxplot_generate_button':
            valid, error_message = self.validate_user_input(values)
            if not valid:
                window.write_event_value('show_error_window', error_message)
                return
            self.generate_boxplot(values, window)
        if event == 'boxplot_back_button':
            window['boxplot_panel'].update(visible=False)
            window['standard_result_panel'].update(visible=True)

        # Help events
        if event == 'boxplot_reporter_help_button':
            show_help_window(help_text['standard_plot_reporters'], location=window.CurrentLocation())

    def generate_boxplot(self, values, window):
        reporters = self.format_reporters(values)
        merged_data = merge_data(self.results[1], 1)

        try:
            [merged_data[reporter] for reporter in reporters]
        except KeyError:
            window.write_event_value('show_error_window', 'Error in input: Invalid reporter name.\nPlease make '
                                                          'sure all reporters are valid with the current run '
                                                          'configuration.')
            return

        fig = go.Figure()
        for key in reporters:
            fig.add_trace(go.Box(y=merged_data[key], name=key))

        fig.update_layout(title_text=values['boxplot_title_input'],
                          yaxis_title_text='Value')
        fig.show()

    def format_reporters(self, values):
        reporters = list(filter(('').__ne__, values['boxplot_reporter_input'].split('\n')))
        reporters = list(map(lambda x: x.strip(), reporters))
        return reporters

    def validate_user_input(self, values):
        if values['boxplot_reporter_input'] == '\n':
            return False, 'Error in input: One or more fields are empty. ' \
                          'Please make sure all options are filled out.'

        return True, ''