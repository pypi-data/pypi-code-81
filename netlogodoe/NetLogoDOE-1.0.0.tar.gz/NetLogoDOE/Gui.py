import PySimpleGUI as sg

from NetLogoDOE.src.gui.custom_windows import show_error_window
from NetLogoDOE.src.gui.navigation.ExperimentResultsScreen import ExperimentResultsScreen
from NetLogoDOE.src.gui.navigation.ExperimentScreen import ExperimentScreen
from NetLogoDOE.src.gui.navigation.ImportScreen import ImportScreen
from NetLogoDOE.src.gui.navigation.MainScreen import MainScreen
from NetLogoDOE.src.gui.navigation.RunScreen import RunScreen
from NetLogoDOE.src.gui.navigation.StandardResultsScreen import StandardResultsScreen
from NetLogoDOE.src.gui.navigation.StandardScreen import StandardScreen
from NetLogoDOE.src.gui.plots.experiment.ExperimentConfigTableScreen import ExperimentConfigTableScreen
from NetLogoDOE.src.gui.plots.experiment.HeatmapScreen import HeatmapScreen
from NetLogoDOE.src.gui.plots.experiment.ParallelCoordinatesScreen import ParallelCoordinatesScreen
from NetLogoDOE.src.gui.plots.experiment.ScatterplotScreen import ScatterplotScreen
from NetLogoDOE.src.gui.plots.standard.BoxplotScreen import BoxplotScreen
from NetLogoDOE.src.gui.plots.standard.DistributionplotScreen import DistributionplotScreen
from NetLogoDOE.src.gui.plots.standard.HistogramScreen import HistogramScreen
from NetLogoDOE.src.gui.plots.standard.StandardConfigTableScreen import StandardConfigTableScreen
from NetLogoDOE.src.gui.plots.standard.TimeSeriesplotScreen import TimeSeriesplotScreen
from NetLogoDOE.src.gui.plots.standard.ViolinplotScreen import ViolinplotScreen


class Gui:
    def __init__(self, netlogo_version=None, netlogo_home=None):
        sg.theme('DefaultNoMoreNagging')
        self.main_screen = MainScreen()
        self.experiment_screen = ExperimentScreen()
        self.standard_screen = StandardScreen()
        self.import_screen = ImportScreen()
        self.run_screen = RunScreen(netlogo_version, netlogo_home)
        self.experiment_result_screen = ExperimentResultsScreen()
        self.standard_result_screen = StandardResultsScreen()

        # Plot screens
        self.standard_configtable_screen = StandardConfigTableScreen()
        self.experiment_configtable_screen = ExperimentConfigTableScreen()
        self.parallel_coordinates_screen = ParallelCoordinatesScreen()
        self.scatterplot_screen = ScatterplotScreen()
        self.heatmap_screen = HeatmapScreen()
        self.timeseries_screen = TimeSeriesplotScreen()
        self.boxplot_screen = BoxplotScreen()
        self.violinplot_screen = ViolinplotScreen()
        self.histogram_screen = HistogramScreen()
        self.distplot_screen = DistributionplotScreen()

        window = self.create_gui()
        self.run(window)

    def create_gui(self):
        layout_main = self.main_screen.layout
        layout_experiment = self.experiment_screen.layout
        layout_standard = self.standard_screen.layout
        layout_import = self.import_screen.layout
        layout_run = self.run_screen.layout
        layout_experiment_result = self.experiment_result_screen.layout
        layout_standard_result = self.standard_result_screen.layout

        # Plot layouts
        layout_standard_configtable = self.standard_configtable_screen.layout
        layout_experiment_configtable = self.experiment_configtable_screen.layout
        layout_parallel_coordinates = self.parallel_coordinates_screen.layout
        layout_scatterplot = self.scatterplot_screen.layout
        layout_heatmap = self.heatmap_screen.layout
        layout_timeseries = self.timeseries_screen.layout
        layout_boxplot = self.boxplot_screen.layout
        layout_violinplot = self.violinplot_screen.layout
        layout_histogram = self.histogram_screen.layout
        layout_distplot = self.distplot_screen.layout

        layout_gui = [[sg.Column(layout_main, key='main_panel', element_justification='center'),
                       sg.Column(layout_experiment, key="experiment_panel", visible=False),
                       sg.Column(layout_standard, key="standard_panel", visible=False),
                       sg.Column(layout_import, key="import_panel", visible=False, element_justification='center'),
                       sg.Column(layout_run, key='run_panel', visible=False),
                       sg.Column(layout_experiment_result, key="experiment_result_panel", visible=False,
                                 element_justification='center'),
                       sg.Column(layout_standard_result, key="standard_result_panel", visible=False,
                                 element_justification='center'),
                       sg.Column(layout_standard_configtable, key="standard_configtable_panel", visible=False),
                       sg.Column(layout_experiment_configtable, key="experiment_configtable_panel", visible=False),
                       sg.Column(layout_parallel_coordinates, key="parcoords_panel", visible=False),
                       sg.Column(layout_scatterplot, key="scatterplot_panel", visible=False),
                       sg.Column(layout_heatmap, key="heatmap_panel", visible=False),
                       sg.Column(layout_timeseries, key="timeseries_panel", visible=False),
                       sg.Column(layout_boxplot, key="boxplot_panel", visible=False),
                       sg.Column(layout_violinplot, key="violinplot_panel", visible=False),
                       sg.Column(layout_histogram, key="histogram_panel", visible=False),
                       sg.Column(layout_distplot, key="distplot_panel", visible=False),
                       ]]

        # Create the window
        return sg.Window("NetLogoDOE", layout_gui, resizable=False, location=(600, 100))

    def run(self, window):
        while True:
            event, values = window.read()
            if event == 'main_close_button' or event == sg.WIN_CLOSED:
                break

            if event == 'show_error_window':
                window.read(timeout=0.01)
                show_error_window(values['show_error_window'],
                                  location=(window.CurrentLocation()[0] - ((434 - window.size[0]) / 2),
                                            window.CurrentLocation()[1] + 100))

            self.main_screen.check_events(event, values, window)
            self.experiment_screen.check_events(event, values, window)
            self.standard_screen.check_events(event, values, window)
            self.import_screen.check_events(event, values, window)
            self.run_screen.check_events(event, values, window)
            self.experiment_result_screen.check_events(event, values, window)
            self.standard_result_screen.check_events(event, values, window)

            self.standard_configtable_screen.check_events(event, values, window)
            self.experiment_configtable_screen.check_events(event, values, window)
            self.parallel_coordinates_screen.check_events(event, values, window)
            self.scatterplot_screen.check_events(event, values, window)
            self.heatmap_screen.check_events(event, values, window)
            self.timeseries_screen.check_events(event, values, window)
            self.boxplot_screen.check_events(event, values, window)
            self.violinplot_screen.check_events(event, values, window)
            self.histogram_screen.check_events(event, values, window)
            self.distplot_screen.check_events(event, values, window)

        window.close()
