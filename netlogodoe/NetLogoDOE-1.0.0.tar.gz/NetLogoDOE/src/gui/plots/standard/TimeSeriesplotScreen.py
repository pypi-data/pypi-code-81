import PySimpleGUI as sg
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import hex_to_rgb

from NetLogoDOE.src.gui.custom_components import title, question_mark_button, metric3_radio_buttons, explanation
from NetLogoDOE.src.gui.custom_windows import show_help_window
from NetLogoDOE.src.gui.help_dictionary import help_text
from NetLogoDOE.src.util.data_processing.merge_standard_data import merge_data


class TimeSeriesplotScreen:

    def __init__(self):
        self.layout = [[title('Timeseries plot')],
                       [sg.Text('Graph Title'), sg.Input(key='timeseries_title_input')],
                       [question_mark_button('timeseries_reporter_help_button'), sg.Text('Reporters to plot:')],
                       [sg.Multiline('', key='timeseries_reporter_input')],
                       [explanation('If this field is left empty, all reporters will be plotted.')],
                       [question_mark_button('timeseries_3metric_help_button'), sg.Text('Metric:')],
                       metric3_radio_buttons('timeseries'),
                       [self.collapse([
                           [sg.Text('Type of variance indication:')],
                           [sg.Radio('None', 'timeseries_variancegroup', key='timeseries_variance_1'),
                            sg.Radio('Error Bars', 'timeseries_variancegroup', key='timeseries_variance_2'),
                            sg.Radio('Shaded areas', 'timeseries_variancegroup', key='timeseries_variance_3')]],
                           'timeseries_variance_radiobuttons')],
                       [sg.Button('Generate', key='timeseries_generate_button')],
                       [sg.Button('Back', key='timeseries_back_button')]]
        self.results = None

    def check_events(self, event, values, window):
        if event == 'standard_write_results_event':
            self.results = values['standard_write_results_event']

        if event == 'timeseries_metric_1':
            window['timeseries_variance_radiobuttons'].update(visible=True)
        if event in ('timeseries_metric_2', 'timeseries_metric_3'):
            window['timeseries_variance_radiobuttons'].update(visible=False)

        if event == 'timeseries_generate_button':
            self.generate_timeseries(values, window)
        if event == 'timeseries_back_button':
            window['timeseries_panel'].update(visible=False)
            window['standard_result_panel'].update(visible=True)

        # Help events
        if event == 'timeseries_reporter_help_button':
            show_help_window(help_text['standard_plot_reporters'],
                             location=(window.CurrentLocation()[0] - ((434 - window.size[0]) / 2),
                                       window.CurrentLocation()[1] + 100))
        if event == 'timeseries_3metric_help_button':
            show_help_window(help_text['3_metric'],
                             location=(window.CurrentLocation()[0] - ((434 - window.size[0]) / 2),
                                       window.CurrentLocation()[1] + 100))

    def collapse(self, layout, key):
        return sg.pin(sg.Column(layout, key=key, visible=False))

    def generate_timeseries(self, values, window):
        reporters = self.format_reporters(values)
        metric = self.get_selected_radio_button(values, 'timeseries_metric', 3)
        variance = self.get_selected_radio_button(values, 'timeseries_variance', 3)
        merged_data = merge_data(self.results[1], metric)

        try:
            [merged_data[reporter] for reporter in reporters]
        except KeyError:
            window.write_event_value('show_error_window', 'Error in input: Invalid reporter name.\nPlease make '
                                                          'sure all reporters are valid with the current run '
                                                          'configuration.')
            return

        if variance > 1 and metric == 1:
            fig = self.generate_variance_figure(merged_data, variance, reporters)
        else:
            fig = go.Figure()
            for reporter in reporters:
                fig.add_trace(go.Scatter(y=merged_data[reporter], mode='lines', name=reporter))

        fig.update_layout(title=values['timeseries_title_input'])
        fig.update_xaxes(title_text='Ticks')
        fig.update_yaxes(title_text='Value')
        fig.show()

    def generate_variance_figure(self, merged_data, variance, reporters):
        fig = go.Figure()
        for i, reporter in enumerate(reporters):
            zipped = list(zip(*self.results[1][reporter]))
            zipped_std = list(map(lambda x: np.std(x), zipped))

            if variance == 2:
                fig.add_trace(go.Scatter(y=merged_data[reporter], mode='lines', name=reporter,
                                         error_y=dict(
                                             type='data',
                                             symmetric=False,
                                             array=zipped_std,
                                             arrayminus=zipped_std)
                                         ))
            if variance == 3:
                plus_std = [x + zipped_std[i] for i, x in enumerate(merged_data[reporter])]
                minus_std = [x - zipped_std[i] for i, x in enumerate(merged_data[reporter])]
                fig.add_trace(go.Scatter(y=merged_data[reporter], mode='lines', name=reporter))
                fig.add_trace(go.Scatter(y=plus_std, showlegend=False,
                                         line=dict(width=0), hoverinfo='skip'))
                fig.add_trace(go.Scatter(y=minus_std, showlegend=False,
                                         fill='tonexty',
                                         fillcolor=f"rgba{(*hex_to_rgb(px.colors.qualitative.Plotly[i]), 0.2)}",
                                         line=dict(width=0), hoverinfo='skip'))

        return fig

    def get_selected_radio_button(self, values, prefix, n):
        for i in range(n):
            if values[f'{prefix}_{i + 1}']:
                return i + 1
        return 1

    def format_reporters(self, values):
        if values['timeseries_reporter_input'] == '\n':
            return list(self.results[1].keys())
        reporters = list(filter(('').__ne__, values['timeseries_reporter_input'].split('\n')))
        reporters = list(map(lambda x: x.strip(), reporters))
        return reporters
