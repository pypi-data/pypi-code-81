import PySimpleGUI as sg
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import statsmodels.api as sm
import re
import math
from NetLogoDOE.src.util.data_processing.merge_experiment_data import merge_data
from NetLogoDOE.src.gui.custom_components import title, metric4_radio_buttons, question_mark_button
from NetLogoDOE.src.gui.custom_windows import show_help_window
from NetLogoDOE.src.gui.help_dictionary import help_text


class ScatterplotScreen:

    def __init__(self):
        self.layout = [[title('Scatterplot')],
                       [question_mark_button('scatterplot_variable_help_button'), sg.Text('Variable combinations to plot:')],
                       [sg.Multiline('"sheep-reproduce" "count sheep"', key='scatterplot_variable_input')],
                       [sg.Text('Explain the format: "x-variable" "y-variable"')],
                       [question_mark_button('scatterplot_4metric_help_button'), sg.Text('Metric:')],
                       metric4_radio_buttons('scatter'),
                       [sg.Button('Generate', key='scatterplot_generate_button')],
                       [sg.Button('Back', key='scatterplot_back_button')]]
        self.results = None

    def check_events(self, event, values, window):
        if event == 'experiment_write_results_event':
            self.results = values['experiment_write_results_event']
        if event == 'scatterplot_generate_button':
            valid, error_message = self.validate_user_input(values)
            if not valid:
                window.write_event_value('show_error_window', error_message)
                return
            self.generate_scatter_plot(values, window)
        if event == 'scatterplot_back_button':
            window['scatterplot_panel'].update(visible=False)
            window['experiment_result_panel'].update(visible=True)

        # Help events
        if event == 'scatterplot_4metric_help_button':
            show_help_window(help_text['4_metric'], location=window.CurrentLocation())
        if event == 'scatterplot_variable_help_button':
            show_help_window(help_text['scatterplot_variables'], location=window.CurrentLocation())

    def generate_scatter_plot(self, values, window):
        exp = self.results[0]
        outcomes = self.results[1]

        repetitions = len(self.results[1][list(self.results[1].keys())[0]][0])
        metric = self.get_selected_radio_button(values)
        merged_data = merge_data(exp, outcomes, repetitions, metric)
        axis_variables = self.format_scatter_axis(values['scatterplot_variable_input'])
        try:
            [merged_data[var] for variables in axis_variables for var in variables]
        except KeyError:
            window.write_event_value('show_error_window', 'Error in input: Invalid variable name.\nPlease make '
                                                          'sure all x and y variables are either a model parameter or '
                                                          'NetLogo reporter used in the experiment configuration.')
            return

        rows, cols = self.get_subplots_format(len(axis_variables))
        titles = [f'Effect of "{variables[0]}" on "{variables[1]}"'
                  for variables in axis_variables]

        fig = make_subplots(rows=rows, cols=cols, subplot_titles=titles)
        colors = px.colors.qualitative.Plotly
        for i, variables in enumerate(axis_variables):
            x = merged_data[variables[0]]
            y = merged_data[variables[1]]
            row = math.floor(i / cols) + 1
            col = (i % cols) + 1

            fig.append_trace(go.Scatter(x=x, y=y, mode='markers', showlegend=False,
                                        line=dict(color=colors[i % 9])), row=row, col=col)

            fit_results = sm.OLS(y, sm.add_constant(x), missing="drop").fit()
            res = fit_results.predict()
            fig.append_trace(go.Scatter(x=x, y=res, mode='lines', showlegend=False,
                                        line=dict(color=colors[i % 9])), row=row, col=col)
            fig.update_xaxes(title_text=variables[0], row=row, col=col)
            fig.update_yaxes(title_text=variables[1], row=row, col=col)

        fig.show()

    def get_selected_radio_button(self, values):
        for i in range(4):
            if values[f'scatter_metric_{i + 1}']:
                return i + 1
        return 1

    def format_scatter_axis(self, variables):
        rows = list(filter(('').__ne__, variables.split('\n')))
        mapped_rows = list(map(lambda x: re.findall('"([^"]*)"', x), rows))
        mapped_rows = list(map(lambda x: (x[0], x[1]), mapped_rows))
        return mapped_rows

    def get_subplots_format(self, subplots):
        if subplots == 1:
            return 1, 1
        elif subplots == 2:
            return 1, 2
        elif subplots == 3:
            return 1, 3
        elif subplots == 4:
            return 2, 2
        else:
            rows = math.floor(subplots / 3)
            if subplots % 3 == 0:
                return rows, 3
            else:
                return rows + 1, 3

    def validate_user_input(self, values):
        if values['scatterplot_variable_input'] == '\n':
            return False, 'Error in input: One or more fields are empty. ' \
                          'Please make sure all options are filled out.'

        try:
            self.format_scatter_axis(values['scatterplot_variable_input'])
        except IndexError:
            return False, 'Error in input: Incorrect format for the variables to plot.\n' \
                          'Please make sure the format is correct, specifically the double quotes.'

        return True, ''
