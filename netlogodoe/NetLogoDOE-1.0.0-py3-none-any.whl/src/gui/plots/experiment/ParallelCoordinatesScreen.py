import PySimpleGUI as sg
import plotly.express as px

from NetLogoDOE.src.gui.custom_components import title, metric4_radio_buttons, question_mark_button
from NetLogoDOE.src.gui.custom_windows import show_help_window
from NetLogoDOE.src.gui.help_dictionary import help_text
from NetLogoDOE.src.util.data_processing.merge_experiment_data import merge_data


class ParallelCoordinatesScreen:

    def __init__(self):
        self.layout = [[title('Parallel Coordinates')],
                       [sg.Text('Graph Title:'), sg.Input(key='parcoords_title_input')],
                       [sg.Text('Line Color:'), sg.Input('Blue', key='parcoords_line_color_input')],
                       [sg.Text('Background Color:'), sg.Input('White', key='parcoords_background_color_input')],
                       [question_mark_button('parcoords_4metric_help_button'), sg.Text('Metric:')],
                       metric4_radio_buttons('parcoords'),
                       [sg.Button('Generate', key='parcoords_generate_button')],
                       [sg.Button('Back', key='parcoords_back_button')]]
        self.results = None

    def check_events(self, event, values, window):
        if event == 'experiment_write_results_event':
            self.results = values['experiment_write_results_event']
        if event == 'parcoords_generate_button':
            self.generate_parallel_coordinates(values, window)
        if event == 'parcoords_back_button':
            window['parcoords_panel'].update(visible=False)
            window['experiment_result_panel'].update(visible=True)

        # Help events
        if event == 'parcoords_4metric_help_button':
            show_help_window(help_text['4_metric'],
                             location=(window.CurrentLocation()[0] - ((434 - window.size[0]) / 2),
                                       window.CurrentLocation()[1] + 100))

    def generate_parallel_coordinates(self, values, window):
        exp = self.results[0]
        outcomes = self.results[1]

        repetitions = len(self.results[1][list(self.results[1].keys())[0]][0])
        metric = self.get_selected_radio_button(values)
        merged_data = merge_data(exp, outcomes, repetitions, metric)

        fig = px.parallel_coordinates(merged_data, title=values['parcoords_title_input'])
        try:
            fig = fig.update_layout(
                colorway=[values['parcoords_line_color_input'].lower()],
                plot_bgcolor=values['parcoords_background_color_input'],
                paper_bgcolor=values['parcoords_background_color_input'],
                title_x=0.5,
            )
            fig.show()
        except ValueError:
            window.write_event_value('show_error_window', 'Error in input: Invalid color value for the line or '
                                                          'background.\nPlease make sure the input is a valid CSS '
                                                          'color string (black), hexidecimal (#FFFFFF) or rgb value '
                                                          '(rbg(255, 255, 255))')

    def get_selected_radio_button(self, values):
        for i in range(4):
            if values[f'parcoords_metric_{i + 1}']:
                return i + 1
        return 1
