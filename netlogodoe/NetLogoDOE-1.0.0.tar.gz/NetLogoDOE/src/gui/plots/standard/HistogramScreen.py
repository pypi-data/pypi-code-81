import PySimpleGUI as sg
import plotly.graph_objects as go

from NetLogoDOE.src.gui.custom_components import title, metric3_radio_buttons, question_mark_button, explanation
from NetLogoDOE.src.gui.custom_windows import show_help_window
from NetLogoDOE.src.gui.help_dictionary import help_text
from NetLogoDOE.src.util.data_processing.merge_standard_data import merge_data


class HistogramScreen:

    def __init__(self):
        self.layout = [[title('Histogram')],
                       [sg.Text('Graph Title: '), sg.Input(key='histogram_title_input')],
                       [question_mark_button('histogram_reporter_help_button'), sg.Text('Reporters to plot:')],
                       [sg.Multiline('', key='histogram_reporter_input')],
                       [explanation('If this field is left empty, all reporters will be plotted.')],
                       [question_mark_button('histogram_3metric_help_button'), sg.Text('Metric:')],
                       metric3_radio_buttons('histogram'),
                       [sg.Button('Generate', key='histogram_generate_button')],
                       [sg.Button('Back', key='histogram_back_button')]]
        self.results = None

    def check_events(self, event, values, window):
        if event == 'standard_write_results_event':
            self.results = values['standard_write_results_event']
        if event == 'histogram_generate_button':
            self.generate_histogram(values, window)
        if event == 'histogram_back_button':
            window['histogram_panel'].update(visible=False)
            window['standard_result_panel'].update(visible=True)

        # Help events
        if event == 'histogram_reporter_help_button':
            show_help_window(help_text['standard_plot_reporters'],
                             location=(window.CurrentLocation()[0] - ((434 - window.size[0]) / 2),
                                       window.CurrentLocation()[1] + 100))
        if event == 'histogram_3metric_help_button':
            show_help_window(help_text['3_metric'],
                             location=(window.CurrentLocation()[0] - ((434 - window.size[0]) / 2),
                                       window.CurrentLocation()[1] + 100))

    def generate_histogram(self, values, window):
        reporters = self.format_reporters(values)
        metric = self.get_selected_radio_button(values)
        merged_data = merge_data(self.results[1], metric)
        try:
            [merged_data[reporter] for reporter in reporters]
        except KeyError:
            window.write_event_value('show_error_window', 'Error in input: Invalid reporter name.\nPlease make '
                                                          'sure all reporters are valid with the current run '
                                                          'configuration.')
            return
        fig = go.Figure()
        for reporter in reporters:
            fig.add_trace(go.Histogram(x=merged_data[reporter], name=reporter))

        fig.update_layout(title_text=values['histogram_title_input'],
                          xaxis_title_text='Value',
                          yaxis_title_text='Count'
                          )
        fig.show()

    def get_selected_radio_button(self, values):
        for i in range(3):
            if values[f'histogram_metric_{i + 1}']:
                return i + 1
        return 1

    def format_reporters(self, values):
        if values['histogram_reporter_input'] == '\n':
            return list(self.results[1].keys())
        reporters = list(filter(('').__ne__, values['histogram_reporter_input'].split('\n')))
        reporters = list(map(lambda x: x.strip(), reporters))
        return reporters
