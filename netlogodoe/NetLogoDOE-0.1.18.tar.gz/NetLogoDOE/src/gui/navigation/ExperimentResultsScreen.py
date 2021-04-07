import PySimpleGUI as sg
from src.gui.custom_components import title, question_mark_button
from src.gui.help_dictionary import help_text
from src.gui.custom_windows import show_help_window


class ExperimentResultsScreen:

    def __init__(self):
        button_size = (30, 1)
        button_pad = ((5, 0), (20, 0))
        self.layout = [[title("Experiment results")],
                       [sg.Button('Experiment Configuration Information', key='experiment_results_configtable_button',
                                  size=button_size, pad=button_pad),
                        question_mark_button('experiment_results_configtable_help_button', padding=button_pad)],
                       [sg.Button('Parallel Coordinates', key='experiment_results_parcoords_button',
                                  size=button_size, pad=button_pad),
                        question_mark_button('experiment_results_parcoords_help_button', padding=button_pad)],
                       [sg.Button('Scatterplot', key='experiment_results_scatterplot_button',
                                  size=button_size, pad=button_pad),
                        question_mark_button('experiment_results_scatterplot_help_button', padding=button_pad)],
                       [sg.Button('Heatmap', key='experiment_results_heatmap_button',
                                  size=button_size, pad=button_pad),
                        question_mark_button('experiment_results_heatmap_help_button', padding=button_pad)],
                       [sg.Input(key='experiment_results_dummy_export', enable_events=True, visible=False, size=(0, 0)),
                        sg.SaveAs('Save Results', file_types=[("Text Files", "*.txt")],
                                  target='experiment_results_dummy_export', key="experiment_results_save_button",
                                  size=button_size, pad=button_pad),
                        question_mark_button('experiment_results_save_help_button', padding=button_pad)],
                       [sg.Button('Back to main menu', key='experiment_results_back_button',
                                  size=button_size, pad=button_pad)]
                       ]
        self.results = None

    def check_events(self, event, values, window):
        if event == 'experiment_write_results_event':
            self.results = values['experiment_write_results_event']

        if event == 'experiment_results_configtable_button':
            window['experiment_result_panel'].update(visible=False)
            window['experiment_configtable_panel'].update(visible=True)
        if event == 'experiment_results_parcoords_button':
            window['experiment_result_panel'].update(visible=False)
            window['parcoords_panel'].update(visible=True)
        if event == 'experiment_results_scatterplot_button':
            window['experiment_result_panel'].update(visible=False)
            window['scatterplot_panel'].update(visible=True)
        if event == 'experiment_results_heatmap_button':
            window['experiment_result_panel'].update(visible=False)
            window['heatmap_panel'].update(visible=True)

        if event == 'experiment_results_dummy_export' and not (values['experiment_results_dummy_export'] == ''):
            self.export_experiment_results(values, values['experiment_results_dummy_export'])
        if event == 'experiment_results_back_button':
            window['experiment_result_panel'].update(visible=False)
            window['main_panel'].update(visible=True)

        # Help events
        if event == 'experiment_results_configtable_help_button':
            show_help_window(help_text['config_information'], location=window.CurrentLocation())
        if event == 'experiment_results_parcoords_help_button':
            show_help_window(help_text['parallel_coordinates'], location=window.CurrentLocation())
        if event == 'experiment_results_scatterplot_help_button':
            show_help_window(help_text['scatterplot'], location=window.CurrentLocation())
        if event == 'experiment_results_heatmap_help_button':
            show_help_window(help_text['heatmap'], location=window.CurrentLocation())
        if event == 'experiment_results_save_help_button':
            show_help_window(help_text['save_results'], location=window.CurrentLocation())

    def export_experiment_results(self, values, file_path):
        results_dict = {}
        results_dict['Configuration'] = self.results[2]
        results_dict['Parameter names'] = list(self.results[0].columns)
        results_dict['Parameter values'] = self.results[0].values.tolist()
        results_dict['Reporter names'] = list(self.results[1].keys())
        results_dict['Reporter values'] = self.results[1]

        f = open(file_path, "w")
        f.write(str(results_dict))
        f.close()
