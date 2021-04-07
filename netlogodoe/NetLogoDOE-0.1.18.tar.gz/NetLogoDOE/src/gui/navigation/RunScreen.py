import PySimpleGUI as sg
from src.util.connectors.experimental_connector import run_experiments
from src.util.connectors.standard_connector import run_standard
from src.util.Runner import Runner
from src.util.config_dicts.get_experiment_dict import get_experiment_config_dictionary
from src.util.config_dicts.get_standard_dict import get_standard_config_dictionary
import pandas as pd


class RunScreen:

    def __init__(self, netlogo_version, netlogo_home):
        self.layout = [[sg.Text("Running experiments...")],
                       [sg.ProgressBar(100, size=(20, 20), orientation='h', key='run_progressbar')]]
        self.netlogo_version = netlogo_version
        self.netlogo_home = netlogo_home

    def check_events(self, event, values, window):
        if event == 'experiment_run_signal':
            runner_list = []
            process_amount = int(values['experiment_process_input'])

            problem = values['experiment_run_signal'][0]
            experiments = values['experiment_run_signal'][1]
            exp_per_process = [len(experiments) // process_amount + (1 if x < len(experiments) % process_amount else 0)
                                for x in range(process_amount)]
            frames = [experiments[i:i + exp_per_process[i]] for i in range(0, len(exp_per_process))]

            for i in range(process_amount):
                runner = Runner(run_experiments, (values, problem, frames[i], self.netlogo_version, self.netlogo_home))
                runner_list.append(runner)
                runner.run()

            results = []
            progress = 0
            while runner_list:
                for i, runner in enumerate(runner_list):
                    res = runner.get_result()
                    if res is None:
                        window.read(timeout=0.01)
                        continue
                    elif res['Progress'] == 'Failure':
                        window['experiment_panel'].update(visible=True)
                        window['run_panel'].update(visible=False)
                        window.write_event_value('show_error_window', res['Results'])
                        return
                    elif res['Results']:
                        results.append(res)
                        runner_list.remove(runner)
                    progress += (res["Progress"] / process_amount)
                    window['run_progressbar'].update_bar(progress)

            data = self.merge_experiment_data(results, problem['names'])
            config = self.get_experiment_config(values)
            window.write_event_value('experiment_write_results_event', data + (config,))
            window['experiment_result_panel'].update(visible=True)
            window['run_panel'].update(visible=False)
            window['run_progressbar'].update_bar(0)

        if event == 'standard_run_signal':
            runner_list = []
            process_amount = int(values['standard_process_input'])
            repetitions = int(values['standard_repetition_input'])
            reps_per_process = [repetitions // process_amount + (1 if x < repetitions % process_amount else 0)
                                for x in range(process_amount)]

            for i in range(process_amount):
                runner = Runner(run_standard, (values, reps_per_process[i], self.netlogo_version, self.netlogo_home))
                runner_list.append(runner)
                runner.run()

            results = []
            progress = 0
            while runner_list:
                for i, runner in enumerate(runner_list):
                    res = runner.get_result()
                    if res is None:
                        window.read(timeout=0.01)
                        continue
                    elif res['Progress'] == 'Failure':
                        window['standard_panel'].update(visible=True)
                        window['run_panel'].update(visible=False)
                        window.write_event_value('show_error_window', res['Results'])
                        return
                    elif res['Results']:
                        results.append(res)
                        runner_list.remove(runner)
                    progress += (res["Progress"] / process_amount)
                    window['run_progressbar'].update_bar(progress)

            data = self.merge_standard_data(results)
            config = self.get_standard_config(values)
            window.write_event_value('standard_write_results_event', data + (config,))
            window['standard_result_panel'].update(visible=True)
            window['run_panel'].update(visible=False)
            window['run_progressbar'].update_bar(0)

    def merge_experiment_data(self, results, names):
        results = list(map(lambda x: {'Results': x['Results']}, results))
        experiments = []
        outcomes = {}

        for key in results[0]['Results'][1].keys():
            outcomes[key] = []

        for process in results:
            for exp in process['Results'][0]:
                experiments.append(exp)
            for key in process['Results'][1].keys():
                for scenario in process['Results'][1][key]:
                    outcomes[key].append(scenario)

        experiments_df = pd.DataFrame(experiments, columns=names)
        return experiments_df, outcomes

    def merge_standard_data(self, results):
        results = list(map(lambda x: {'Results': x['Results']}, results))
        var_values = results[0]['Results'][0]
        outcomes = {}

        for key in results[0]['Results'][1].keys():
            outcomes[key] = []

        for process in results:
            for key in outcomes.keys():
                for repetition in process['Results'][1][key]:
                    outcomes[key].append(repetition)

        return var_values, outcomes

    def get_experiment_config(self, values):
        experiment_dict = get_experiment_config_dictionary(values)

        table_list = []
        for key in experiment_dict.keys():
            table_list.append([key, experiment_dict[key]])
        return table_list

    def get_standard_config(self, values):
        standard_dict = get_standard_config_dictionary(values)

        table_list = []
        for key in standard_dict.keys():
            table_list.append([key, standard_dict[key]])
        return table_list

    def handle_error(self, window, msg):
        window['experiment_panel'].update(visible=True)
        window['run_panel'].update(visible=False)
        window.write_event_value('show_error_window', msg)
