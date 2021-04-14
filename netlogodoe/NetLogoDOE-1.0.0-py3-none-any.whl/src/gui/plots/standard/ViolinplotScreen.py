import PySimpleGUI as sg
import plotly.graph_objects as go

from NetLogoDOE.src.gui.custom_components import title, question_mark_button, explanation
from NetLogoDOE.src.gui.custom_windows import show_help_window
from NetLogoDOE.src.gui.help_dictionary import help_text
from NetLogoDOE.src.util.data_processing.merge_standard_data import merge_data


class ViolinplotScreen:

    def __init__(self):
        self.layout = [[title('Violin plot')],
                       [sg.Text('Graph Title: '), sg.Input(key='violinplot_title_input')],
                       [question_mark_button('violinplot_reporter_help_button'), sg.Text('Reporters to plot:')],
                       [sg.Multiline('', key='violinplot_reporter_input')],
                       [explanation('If this field is left empty, all reporters will be plotted.')],
                       [sg.Button('Generate', key='violinplot_generate_button')],
                       [sg.Button('Back', key='violinplot_back_button')]]
        self.results = None

    def check_events(self, event, values, window):
        if event == 'standard_write_results_event':
            self.results = values['standard_write_results_event']
        if event == 'violinplot_generate_button':
            self.generate_violinplot(values, window)
        if event == 'violinplot_back_button':
            window['violinplot_panel'].update(visible=False)
            window['standard_result_panel'].update(visible=True)

        # Help events
        if event == 'violinplot_reporter_help_button':
            show_help_window(help_text['standard_plot_reporters'],
                             location=(window.CurrentLocation()[0] - ((434 - window.size[0]) / 2),
                                       window.CurrentLocation()[1] + 100))

    def generate_violinplot(self, values, window):
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
            fig.add_trace(go.Violin(y=merged_data[key], name=key))

        fig.update_layout(title_text=values['violinplot_title_input'],
                          yaxis_title_text='Value')
        fig.show()

    def format_reporters(self, values):
        if values['violinplot_reporter_input'] == '\n':
            return list(self.results[1].keys())
        reporters = list(filter(('').__ne__, values['violinplot_reporter_input'].split('\n')))
        reporters = list(map(lambda x: x.strip(), reporters))
        return reporters
