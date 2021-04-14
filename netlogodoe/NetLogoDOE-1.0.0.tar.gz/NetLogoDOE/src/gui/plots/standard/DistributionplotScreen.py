import PySimpleGUI as sg
import plotly.figure_factory as ff

from NetLogoDOE.src.gui.custom_components import title, metric3_radio_buttons, question_mark_button, explanation
from NetLogoDOE.src.gui.custom_windows import show_help_window
from NetLogoDOE.src.gui.help_dictionary import help_text
from NetLogoDOE.src.util.data_processing.merge_standard_data import merge_data


class DistributionplotScreen:

    def __init__(self):
        self.layout = [[title('Distribution plot')],
                       [sg.Text('Graph Title:'), sg.Input(key='distplot_title_input')],
                       [question_mark_button('distplot_reporter_help_button'), sg.Text('Reporters to plot:')],
                       [sg.Multiline('', key='distplot_reporter_input')],
                       [explanation('If this field is left empty, all reporters will be plotted.')],
                       [question_mark_button('distplot_3metric_help_button'), sg.Text('Metric:')],
                       metric3_radio_buttons('distplot'),
                       [question_mark_button('distplot_indicators_help_button'), sg.Text('Distribution indicators:')],
                       [sg.Checkbox('Show curve', key='distplot_curve_checkbox', default=True),
                       sg.Checkbox('Show histogram', key='distplot_histogram_checkbox', default=True),
                       sg.Checkbox('Show rug', key='distplot_rug_checkbox', default=True)],
                       [sg.Button('Generate', key='distplot_generate_button')],
                       [sg.Button('Back', key='distplot_back_button')]]
        self.results = None

    def check_events(self, event, values, window):
        if event == 'standard_write_results_event':
            self.results = values['standard_write_results_event']

        if event == 'distplot_generate_button':
            self.generate_distributionplot(values, window)
        if event == 'distplot_back_button':
            window['distplot_panel'].update(visible=False)
            window['standard_result_panel'].update(visible=True)

        # Help events
        if event == 'distplot_reporter_help_button':
            show_help_window(help_text['standard_plot_reporters'],
                             location=(window.CurrentLocation()[0] - ((434 - window.size[0]) / 2),
                                       window.CurrentLocation()[1] + 100))
        if event == 'distplot_3metric_help_button':
            show_help_window(help_text['3_metric'],
                             location=(window.CurrentLocation()[0] - ((434 - window.size[0]) / 2),
                                       window.CurrentLocation()[1] + 100))
        if event == 'distplot_indicators_help_button':
            show_help_window(help_text['distributionplot_indicators'],
                             location=(window.CurrentLocation()[0] - ((434 - window.size[0]) / 2),
                                       window.CurrentLocation()[1] + 100))

    def generate_distributionplot(self, values, window):
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

        hist_data = []
        for reporter in reporters:
            hist_data.append(merged_data[reporter])

        bin_size = [(max(data)-min(data))/30 for data in hist_data]
        fig = ff.create_distplot(hist_data, reporters, bin_size,
                                 show_curve=values['distplot_curve_checkbox'],
                                 show_hist=values['distplot_histogram_checkbox'],
                                 show_rug=values['distplot_rug_checkbox'],
                                 )
        fig.update_layout(title_text=values['distplot_title_input'],
                          xaxis_title_text='Value',
                          )
        fig.show()

    def get_selected_radio_button(self, values):
        for i in range(3):
            if values[f'distplot_metric_{i + 1}']:
                return i + 1
        return 1

    def format_reporters(self, values):
        if values['distplot_reporter_input'] == '\n':
            return list(self.results[1].keys())
        reporters = list(filter(('').__ne__, values['distplot_reporter_input'].split('\n')))
        reporters = list(map(lambda x: x.strip(), reporters))
        return reporters
