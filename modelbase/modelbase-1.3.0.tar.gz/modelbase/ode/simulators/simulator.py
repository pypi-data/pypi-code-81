"""Write me."""

# Standard Library
import concurrent.futures as futures
import copy
import itertools as it
import sys as sys
import warnings
from functools import partial

# Third party
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Local code
from ...core.utils import warning_on_one_line
from ...utils.plotting import _get_plot_kwargs, _style_subplot, plot, plot_grid
from .basesimulator import _BaseSimulator

from mpl_toolkits.mplot3d import Axes3D as _Axes3D  # flake8: NOQA


warnings.formatwarning = warning_on_one_line


class _Simulate(_BaseSimulator):
    """Simulator for ODE models."""

    def __init__(self, model, integrator_name, **kwargs):
        super().__init__(model=model, integrator_name=integrator_name, **kwargs)
        self.full_results = None
        self.simulation_parameters = kwargs.get("parameters", [])

    def __reduce__(self):
        """Pickle this class."""
        return (
            self.__class__,
            (
                self.model,
                self.integrator_name,
            ),
            (
                ("y0", self.y0),
                ("time", self.time),
                ("results", self.results),
                ("parameters", self.simulation_parameters),
            ),
        )

    def copy(self):
        """Return a deepcopy of this class."""
        new = copy.deepcopy(self)
        new.simulation_parameters = self.simulation_parameters.copy()
        if new.results is not None:
            new._initialise_integrator(y0=new.results[-1])
        elif new.y0 is not None:
            new.initialise(y0=new.y0, test_run=False)
        return new

    def clear_results(self):
        """Clear simulation results."""
        super().clear_results()
        self.full_results = None
        self.simulation_parameters = []

    def _test_run(self):
        """Test run of a single integration step to get proper error handling."""
        y = self.model.get_full_concentration_dict(y=self.y0, t=0)
        self.model.get_fluxes_dict(y=y, t=0)
        self.model.get_right_hand_side(y=y, t=0)

    def update_parameter(self, parameter_name, parameter_value):
        """Update a model parameter.

        Parameters
        ----------
        parameter_name : str
            Name of the parameter
        parameter_value : num
            Numeric value of the parameter
        meta_info : dict, optional
            Meta info of the parameter. Allowed keys are
            {unit, database_links, notes}

        Warns
        -----
        UserWarning
            If parameter is not in the model

        See Also
        --------
        update_parameters
        """
        self.model.update_parameter(parameter_name=parameter_name, parameter_value=parameter_value)

    def update_parameters(self, parameters):
        """Update existing model parameters.

        Parameters
        ----------
        parameters : dict(str: num)
            Dictionary containing the parameter and value pairs

        See Also
        --------
        update_parameter
        """
        self.model.update_parameters(parameters=parameters)

    def _save_simulation_results(self, *, time, results, skipfirst):
        super()._save_simulation_results(time=time, results=results, skipfirst=skipfirst)
        self.simulation_parameters.append(self.model.parameters.copy())

    def simulate(self, t_end=None, steps=None, time_points=None, **integrator_kwargs):
        """Simulate the model.

        You can either supply only a terminal time point, or additionally also the
        number of steps or exact time points for which values should be returned.

        Parameters
        ----------
        t_end : num, optional
        steps : int, optional
            Number of integration time steps to be returned
        time_points : iterable(num), optional
            Explicit time points which shall be returned
        integrator_kwargs : dict
            Integrator options

        Returns
        -------
        t : numpy.array
        y : numpy.array
        """
        self.model._update_derived_parameters()
        time, results = super().simulate(
            t_end=t_end,
            steps=steps,
            time_points=time_points,
            **integrator_kwargs,
        )
        self.full_results = None
        return time, results

    def simulate_to_steady_state(self, tolerance=1e-8, simulation_kwargs=None, **integrator_kwargs):
        """Simulate the model to steady state.

        Parameters
        ----------
        tolerance : float
        simulation_kwargs : dict
        integrator_kwargs : dict

        Returns
        -------
        t : numpy.array
        y : numpy.array
        """
        self.model._update_derived_parameters()
        time, results = super().simulate_to_steady_state(
            tolerance=tolerance,
            simulation_kwargs=simulation_kwargs,
            **integrator_kwargs,
        )
        self.full_results = None
        return time, results

    @staticmethod
    def _parameter_scan_worker(
        parameter_value,
        *,
        parameter_name,
        model,
        Sim,
        integ_name,
        tolerance,
        y0,
        integrator_kwargs,
    ):
        m = model.copy()
        s = Sim(model=m, integrator_name=integ_name)
        s.initialise(y0=y0, test_run=False)
        s.update_parameter(parameter_name=parameter_name, parameter_value=parameter_value)
        try:
            t, y = s.simulate_to_steady_state(tolerance=tolerance, **integrator_kwargs)
            return s.get_full_results_array()[-1]
        except ValueError:
            return np.full(len(m.get_all_compounds()), np.NaN)

    def parameter_scan(
        self,
        parameter_name,
        parameter_values,
        tolerance=1e-8,
        multiprocessing=True,
        **integrator_kwargs,
    ):
        """Scan the model steady state changes caused by a change to a parameter.

        Parameters
        ----------
        parameter_name : str
        parameter_values : iterable(num)
        multiprocessing : bool

        Returns
        -------
        steady_state_concentrations : pandas.DataFrame
        """
        is_windows_os = sys.platform in ["win32", "cygwin"]
        if is_windows_os:  # pragma: no cover
            warnings.warn(
                """
                Windows does not behave well with multiple processes.
                Falling back to threading routine."""
            )
        if is_windows_os or not multiprocessing:
            results = map(
                partial(
                    self._parameter_scan_worker,
                    **{
                        "parameter_name": parameter_name,
                        "model": self.model,
                        "Sim": self.__class__,
                        "integ_name": self.integrator_name,
                        "tolerance": tolerance,
                        "y0": self.y0,
                        "integrator_kwargs": integrator_kwargs,
                    },
                ),
                parameter_values,
            )
        else:
            with futures.ProcessPoolExecutor() as executor:
                results = executor.map(
                    partial(
                        self._parameter_scan_worker,
                        **{
                            "parameter_name": parameter_name,
                            "model": self.model,
                            "Sim": self.__class__,
                            "integ_name": self.integrator_name,
                            "tolerance": tolerance,
                            "y0": self.y0,
                            "integrator_kwargs": integrator_kwargs,
                        },
                    ),
                    parameter_values,
                )
        return pd.DataFrame(data=results, index=parameter_values, columns=self.model.get_all_compounds())

    def get_fluxes_array(self, normalise=None, concatenated=True):
        """Get the model fluxes for the simulation.

        Returns
        -------
        results : numpy.array
        """
        fluxes = []
        for t, y, pars in zip(self.time, self.results, self.simulation_parameters):
            self.update_parameters(parameters=pars)
            fluxes_array = self.model.get_fluxes_array(y=y, t=t)
            fluxes.append(fluxes_array)

        if normalise is not None:
            fluxes = self._normalise_split_array(split_array=fluxes, normalise=normalise)
        if concatenated:
            return np.concatenate(fluxes, axis=0)
        else:
            return fluxes

    def get_fluxes_dict(self, normalise=None, concatenated=True):
        """Get the model fluxes for the simulation.

        Returns
        -------
        results : dict
        """
        fluxes = self.get_fluxes_array(normalise=normalise, concatenated=concatenated)
        if concatenated:
            return dict(zip(self.model.rates, fluxes.T))
        else:
            return [dict(zip(self.model.rates, i.T)) for i in fluxes]

    def get_fluxes_df(self, normalise=None, concatenated=True):
        """Get the model fluxes for the simulation.

        Returns
        -------
        results : pandas.DataFrame
        """
        fluxes = self.get_fluxes_array(normalise=normalise, concatenated=concatenated)
        time = self.get_time(concatenated=concatenated)
        if concatenated:
            return pd.DataFrame(
                data=fluxes,
                index=self.get_time(),
                columns=self.model.get_rate_names(),
            )
        else:
            return [
                pd.DataFrame(
                    data=flux,
                    index=t,
                    columns=self.model.get_rate_names(),
                )
                for t, flux in zip(time, fluxes)
            ]

    def _calculate_full_results(self):
        full_results = []
        for t, y, p in zip(self.time, self.results, self.simulation_parameters):
            self.update_parameters(parameters=p)
            results = self.model.get_full_concentration_dict(y=y, t=t)
            del results["time"]
            full_results.append(np.reshape(list(results.values()), (len(results), len(t))).T)
        self.full_results = full_results

    def get_full_results_array(self, normalise=None, concatenated=True):
        """Get simulation results and derived compounds.

        Returns
        -------
        results : numpy.array
        """
        if self.full_results is None:
            self._calculate_full_results()
        full_results = self.full_results.copy()
        if normalise is not None:
            full_results = self._normalise_split_array(split_array=full_results, normalise=normalise)
        if concatenated:
            return np.concatenate(full_results, axis=0)
        else:
            return full_results

    def get_full_results_dict(self, normalise=None, concatenated=True):
        """Get simulation results and derived compounds.

        Returns
        -------
        results : dict
        """
        full_results = self.get_full_results_array(normalise=normalise, concatenated=concatenated)
        if concatenated:
            return dict(zip(self.model.get_all_compounds(), full_results.T))
        else:
            return [dict(zip(self.model.get_all_compounds(), i.T)) for i in full_results]

    def get_full_results_df(self, normalise=None, concatenated=True):
        """Get simulation results and derived compounds.

        Returns
        -------
        results : pandas.DataFrame
        """
        full_results = self.get_full_results_array(normalise=normalise, concatenated=concatenated)
        time = self.get_time(concatenated=concatenated)

        if concatenated:
            return pd.DataFrame(data=full_results, index=time, columns=self.model.get_all_compounds())
        else:
            return [
                pd.DataFrame(data=res, index=t, columns=self.model.get_all_compounds())
                for t, res in zip(time, full_results)
            ]

    def get_variable(self, variable, normalise=None, concatenated=True):
        """Get simulation results for a specific variable.

        Returns
        -------
        results : numpy.array
        """
        full_results_dict = self.get_full_results_dict(normalise=normalise, concatenated=concatenated)
        if concatenated:
            return full_results_dict[variable]
        else:
            return [i[variable] for i in full_results_dict]

    def get_variables(self, variables, normalise=None, concatenated=True):
        """Get simulation results for a specific variable.

        Returns
        -------
        results : tuple(numpy.array)
        """
        full_results_df = self.get_full_results_df(normalise=normalise, concatenated=concatenated)
        if concatenated:
            return full_results_df.loc[:, variables].values
        else:
            return [i.loc[:, variables].values for i in full_results_df]

    def plot(
        self,
        xlabel=None,
        ylabel=None,
        title=None,
        normalise=None,
        grid=True,
        tight_layout=True,
        ax=None,
        figure_kwargs=None,
        subplot_kwargs=None,
        plot_kwargs=None,
        grid_kwargs=None,
        legend_kwargs=None,
        tick_kwargs=None,
        label_kwargs=None,
        title_kwargs=None,
    ):
        """Plot simulation results for a selection of compounds.

        Parameters
        ----------
        compounds : iterable(str)
        xlabel : str
        ylabel : str
        title : str
        grid : bool
        tight_layout : bool
        ax : matplotlib axes
        figure_kwargs : dict
        subplot_kwargs : dict
        plot_kwargs : dict
        grid_kwargs : dict
        legend_kwargs : dict
        tick_kwargs : dict
        label_kwargs : dict
        title_kwargs : dict

        Returns
        -------
        fig : matplotlib Figure
        ax : matplotlib axes
        """
        compounds = self.model.get_compounds()
        x = self.get_time()
        y = self.get_full_results_df(normalise=normalise, concatenated=True).loc[:, compounds]
        return plot(
            plot_args=(x, y),
            legend=compounds,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_log(
        self,
        xlabel=None,
        ylabel=None,
        title=None,
        normalise=None,
        grid=True,
        tight_layout=True,
        ax=None,
        figure_kwargs=None,
        subplot_kwargs=None,
        plot_kwargs=None,
        grid_kwargs=None,
        legend_kwargs=None,
        tick_kwargs=None,
        label_kwargs=None,
        title_kwargs=None,
    ):
        """Plot simulation results for a selection of compounds.

        Parameters
        ----------
        compounds : iterable(str)
        xlabel : str
        ylabel : str
        title : str
        grid : bool
        tight_layout : bool
        ax : matplotlib axes
        figure_kwargs : dict
        subplot_kwargs : dict
        plot_kwargs : dict
        grid_kwargs : dict
        legend_kwargs : dict
        tick_kwargs : dict
        label_kwargs : dict
        title_kwargs : dict

        Returns
        -------
        fig : matplotlib Figure
        ax : matplotlib axes
        """
        compounds = self.model.get_compounds()
        x = self.get_time()
        y = self.get_full_results_df(normalise=normalise, concatenated=True).loc[:, compounds]
        fig, ax = plot(
            plot_args=(x, y),
            legend=compounds,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )
        ax.set_xscale("log")
        ax.set_yscale("log")
        return fig, ax

    def plot_semilog(
        self,
        log_axis="y",
        xlabel=None,
        ylabel=None,
        title=None,
        normalise=None,
        grid=True,
        tight_layout=True,
        ax=None,
        figure_kwargs=None,
        subplot_kwargs=None,
        plot_kwargs=None,
        grid_kwargs=None,
        legend_kwargs=None,
        tick_kwargs=None,
        label_kwargs=None,
        title_kwargs=None,
    ):
        """Plot simulation results for a selection of compounds.

        Parameters
        ----------
        compounds : iterable(str)
        xlabel : str
        ylabel : str
        title : str
        grid : bool
        tight_layout : bool
        ax : matplotlib axes
        figure_kwargs : dict
        subplot_kwargs : dict
        plot_kwargs : dict
        grid_kwargs : dict
        legend_kwargs : dict
        tick_kwargs : dict
        label_kwargs : dict
        title_kwargs : dict

        Returns
        -------
        fig : matplotlib Figure
        ax : matplotlib axes
        """
        compounds = self.model.get_compounds()
        x = self.get_time()
        y = self.get_full_results_df(normalise=normalise, concatenated=True).loc[:, compounds]
        fig, ax = plot(
            plot_args=(x, y),
            legend=compounds,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )
        if log_axis == "y":
            ax.set_yscale("log")
        elif log_axis == "x":
            ax.set_xscale("log")
        else:
            raise ValueError("log_axis must be either x or y")
        return fig, ax

    def plot_derived(
        self,
        xlabel=None,
        ylabel=None,
        title=None,
        normalise=None,
        grid=True,
        tight_layout=True,
        ax=None,
        figure_kwargs=None,
        subplot_kwargs=None,
        plot_kwargs=None,
        grid_kwargs=None,
        legend_kwargs=None,
        tick_kwargs=None,
        label_kwargs=None,
        title_kwargs=None,
    ):
        """Plot simulation results for the derived compounds.

        Parameters
        ----------
        xlabel : str
        ylabel : str
        title : str
        grid : bool
        tight_layout : bool
        ax : matplotlib axes
        figure_kwargs : dict
        subplot_kwargs : dict
        plot_kwargs : dict
        grid_kwargs : dict
        legend_kwargs : dict
        tick_kwargs : dict
        label_kwargs : dict
        title_kwargs : dict

        Returns
        -------
        fig : matplotlib Figure
        ax : matplotlib axes
        """
        compounds = self.model.get_derived_compounds()
        x = self.get_time()
        y = self.get_full_results_df(normalise=normalise, concatenated=True).loc[:, compounds]
        return plot(
            plot_args=(x, y),
            legend=compounds,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_all(
        self,
        xlabel=None,
        ylabel=None,
        title=None,
        normalise=None,
        grid=True,
        tight_layout=True,
        ax=None,
        figure_kwargs=None,
        subplot_kwargs=None,
        plot_kwargs=None,
        grid_kwargs=None,
        legend_kwargs=None,
        tick_kwargs=None,
        label_kwargs=None,
        title_kwargs=None,
    ):
        """Plot simulation results for the derived compounds.

        Parameters
        ----------
        xlabel : str
        ylabel : str
        title : str
        grid : bool
        tight_layout : bool
        ax : matplotlib axes
        figure_kwargs : dict
        subplot_kwargs : dict
        plot_kwargs : dict
        grid_kwargs : dict
        legend_kwargs : dict
        tick_kwargs : dict
        label_kwargs : dict
        title_kwargs : dict

        Returns
        -------
        fig : matplotlib Figure
        ax : matplotlib axes
        """
        compounds = self.model.get_all_compounds()
        x = self.get_time()
        y = self.get_full_results_df(normalise=normalise, concatenated=True).loc[:, compounds]
        return plot(
            plot_args=(x, y),
            legend=compounds,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_selection(
        self,
        compounds,
        xlabel=None,
        ylabel=None,
        title=None,
        normalise=None,
        grid=True,
        tight_layout=True,
        ax=None,
        figure_kwargs=None,
        subplot_kwargs=None,
        plot_kwargs=None,
        grid_kwargs=None,
        legend_kwargs=None,
        tick_kwargs=None,
        label_kwargs=None,
        title_kwargs=None,
    ):
        """Plot simulation results for the derived compounds.

        Parameters
        ----------
        xlabel : str
        ylabel : str
        title : str
        grid : bool
        tight_layout : bool
        ax : matplotlib axes
        figure_kwargs : dict
        subplot_kwargs : dict
        plot_kwargs : dict
        grid_kwargs : dict
        legend_kwargs : dict
        tick_kwargs : dict
        label_kwargs : dict
        title_kwargs : dict

        Returns
        -------
        fig : matplotlib Figure
        ax : matplotlib axes
        """
        x = self.get_time()
        y = self.get_full_results_df(normalise=normalise, concatenated=True).loc[:, compounds]
        return plot(
            plot_args=(x, y),
            legend=compounds,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_grid(
        self,
        compound_groups,
        ncols=None,
        sharex=True,
        sharey=True,
        xlabels=None,
        ylabels=None,
        normalise=None,
        plot_titles=None,
        figure_title=None,
        grid=True,
        tight_layout=True,
        ax=None,
        figure_kwargs=None,
        subplot_kwargs=None,
        plot_kwargs=None,
        grid_kwargs=None,
        legend_kwargs=None,
        tick_kwargs=None,
        label_kwargs=None,
        title_kwargs=None,
    ):
        """Plot simulation results of the compound groups as a grid.

        Parameters
        ----------
        compound_groups : iterable(iterable(str))
        ncols : int
        sharex : bool
        sharey : bool
        xlabel : str
        ylabel : str
        plot_titles : iterable(str)
        figure_title : str
        grid : bool
        tight_layout : bool
        ax : matplotlib axes
        figure_kwargs : dict
        subplot_kwargs : dict
        plot_kwargs : dict
        grid_kwargs : dict
        legend_kwargs : dict
        tick_kwargs : dict
        label_kwargs : dict
        title_kwargs : dict

        Returns
        -------
        fig : matplotlib Figure
        ax : matplotlib axes
        """
        time = self.get_time()
        plot_groups = [
            (
                time,
                self.get_full_results_df(normalise=normalise, concatenated=True).loc[:, compounds].values,
            )
            for compounds in compound_groups
        ]

        return plot_grid(
            plot_groups=plot_groups,
            legend_groups=compound_groups,
            ncols=ncols,
            sharex=sharex,
            sharey=sharey,
            xlabels=xlabels,
            ylabels=ylabels,
            figure_title=figure_title,
            plot_titles=plot_titles,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_against_variable(
        self,
        variable,
        xlabel=None,
        ylabel=None,
        title=None,
        grid=True,
        tight_layout=True,
        ax=None,
        figure_kwargs=None,
        subplot_kwargs=None,
        plot_kwargs=None,
        grid_kwargs=None,
        legend_kwargs=None,
        tick_kwargs=None,
        label_kwargs=None,
        title_kwargs=None,
    ):
        """Plot all simulation results against another result.

        Parameters
        ----------
        variable : str
        xlabel : str
        ylabel : str
        title : str
        grid : bool
        tight_layout : bool
        ax : matplotlib axes
        figure_kwargs : dict
        subplot_kwargs : dict
        plot_kwargs : dict
        grid_kwargs : dict
        legend_kwargs : dict
        tick_kwargs : dict
        label_kwargs : dict
        title_kwargs : dict

        Returns
        -------
        fig : matplotlib Figure
        ax : matplotlib axes
        """
        if xlabel is None:
            xlabel = variable
        compounds = self.model.get_compounds()
        x = self.get_variable(variable=variable)
        y = self.get_full_results_df(concatenated=True).loc[:, compounds]
        return plot(
            plot_args=(x, y),
            legend=compounds,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_derived_against_variable(
        self,
        variable,
        xlabel=None,
        ylabel=None,
        title=None,
        grid=True,
        tight_layout=True,
        ax=None,
        figure_kwargs=None,
        subplot_kwargs=None,
        plot_kwargs=None,
        grid_kwargs=None,
        legend_kwargs=None,
        tick_kwargs=None,
        label_kwargs=None,
        title_kwargs=None,
    ):
        """Plot all simulation results against another result.

        Parameters
        ----------
        variable : str
        xlabel : str
        ylabel : str
        title : str
        grid : bool
        tight_layout : bool
        ax : matplotlib axes
        figure_kwargs : dict
        subplot_kwargs : dict
        plot_kwargs : dict
        grid_kwargs : dict
        legend_kwargs : dict
        tick_kwargs : dict
        label_kwargs : dict
        title_kwargs : dict

        Returns
        -------
        fig : matplotlib Figure
        ax : matplotlib axes
        """
        if xlabel is None:
            xlabel = variable
        compounds = self.model.get_derived_compounds()
        x = self.get_variable(variable=variable)
        y = self.get_full_results_df(concatenated=True).loc[:, compounds]
        return plot(
            plot_args=(x, y),
            legend=compounds,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_all_against_variable(
        self,
        variable,
        xlabel=None,
        ylabel=None,
        title=None,
        grid=True,
        tight_layout=True,
        ax=None,
        figure_kwargs=None,
        subplot_kwargs=None,
        plot_kwargs=None,
        grid_kwargs=None,
        legend_kwargs=None,
        tick_kwargs=None,
        label_kwargs=None,
        title_kwargs=None,
    ):
        """Plot simulation results and derived compounds against another result.

        Parameters
        ----------
        variable : str
        xlabel : str
        ylabel : str
        title : str
        grid : bool
        tight_layout : bool
        ax : matplotlib axes
        figure_kwargs : dict
        subplot_kwargs : dict
        plot_kwargs : dict
        grid_kwargs : dict
        legend_kwargs : dict
        tick_kwargs : dict
        label_kwargs : dict
        title_kwargs : dict

        Returns
        -------
        fig : matplotlib Figure
        ax : matplotlib axes
        """
        if xlabel is None:
            xlabel = variable
        compounds = self.model.get_all_compounds()
        x = self.get_variable(variable=variable)
        y = self.get_full_results_df(concatenated=True).loc[:, compounds]
        return plot(
            plot_args=(x, y),
            legend=compounds,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_selection_against_variable(
        self,
        compounds,
        variable,
        xlabel=None,
        ylabel=None,
        title=None,
        grid=True,
        tight_layout=True,
        ax=None,
        figure_kwargs=None,
        subplot_kwargs=None,
        plot_kwargs=None,
        grid_kwargs=None,
        legend_kwargs=None,
        tick_kwargs=None,
        label_kwargs=None,
        title_kwargs=None,
    ):
        """Plot select simulation results against another result.

        Parameters
        ----------
        compounds : iterable(str)
        variable : str
        xlabel : str
        ylabel : str
        title : str
        grid : bool
        tight_layout : bool
        ax : matplotlib axes
        figure_kwargs : dict
        subplot_kwargs : dict
        plot_kwargs : dict
        grid_kwargs : dict
        legend_kwargs : dict
        tick_kwargs : dict
        label_kwargs : dict
        title_kwargs : dict

        Returns
        -------
        fig : matplotlib Figure
        ax : matplotlib axes
        """
        if xlabel is None:
            xlabel = variable
        x = self.get_variable(variable=variable)
        y = self.get_full_results_df(concatenated=True).loc[:, compounds]
        return plot(
            plot_args=(x, y),
            legend=compounds,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_fluxes(
        self,
        xlabel=None,
        ylabel=None,
        title=None,
        normalise=None,
        grid=True,
        tight_layout=True,
        ax=None,
        figure_kwargs=None,
        subplot_kwargs=None,
        plot_kwargs=None,
        grid_kwargs=None,
        legend_kwargs=None,
        tick_kwargs=None,
        label_kwargs=None,
        title_kwargs=None,
    ):
        """Plot fluxes of all results.

        Parameters
        ----------
        variable : str
        xlabel : str
        ylabel : str
        title : str
        grid : bool
        tight_layout : bool
        ax : matplotlib axes
        figure_kwargs : dict
        subplot_kwargs : dict
        plot_kwargs : dict
        grid_kwargs : dict
        legend_kwargs : dict
        tick_kwargs : dict
        label_kwargs : dict
        title_kwargs : dict

        Returns
        -------
        fig : matplotlib Figure
        ax : matplotlib axes
        """
        rate_names = self.model.get_rate_names()
        x = self.get_time()
        y = self.get_fluxes_df(normalise=normalise, concatenated=True).loc[:, rate_names]
        return plot(
            plot_args=(x, y),
            legend=rate_names,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_flux_selection(
        self,
        rate_names,
        xlabel=None,
        ylabel=None,
        title=None,
        normalise=None,
        grid=True,
        tight_layout=True,
        ax=None,
        figure_kwargs=None,
        subplot_kwargs=None,
        plot_kwargs=None,
        grid_kwargs=None,
        legend_kwargs=None,
        tick_kwargs=None,
        label_kwargs=None,
        title_kwargs=None,
    ):
        """Plot fluxes of a selection of results.

        Parameters
        ----------
        rate_names : iterable(str)
        variable : str
        xlabel : str
        ylabel : str
        title : str
        grid : bool
        tight_layout : bool
        ax : matplotlib axes
        figure_kwargs : dict
        subplot_kwargs : dict
        plot_kwargs : dict
        grid_kwargs : dict
        legend_kwargs : dict
        tick_kwargs : dict
        label_kwargs : dict
        title_kwargs : dict

        Returns
        -------
        fig : matplotlib Figure
        ax : matplotlib axes
        """
        x = self.get_time()
        y = self.get_fluxes_df(normalise=normalise, concatenated=True).loc[:, rate_names]
        return plot(
            plot_args=(x, y),
            legend=rate_names,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_fluxes_against_variable(
        self,
        variable,
        xlabel=None,
        ylabel=None,
        title=None,
        grid=True,
        tight_layout=True,
        ax=None,
        figure_kwargs=None,
        subplot_kwargs=None,
        plot_kwargs=None,
        grid_kwargs=None,
        legend_kwargs=None,
        tick_kwargs=None,
        label_kwargs=None,
        title_kwargs=None,
    ):
        """Plot all fluxes against another result.

        Parameters
        ----------
        variable : str
        xlabel : str
        ylabel : str
        title : str
        grid : bool
        tight_layout : bool
        ax : matplotlib axes
        figure_kwargs : dict
        subplot_kwargs : dict
        plot_kwargs : dict
        grid_kwargs : dict
        legend_kwargs : dict
        tick_kwargs : dict
        label_kwargs : dict
        title_kwargs : dict

        Returns
        -------
        fig : matplotlib Figure
        ax : matplotlib axes
        """
        if xlabel is None:
            xlabel = variable
        rate_names = self.model.get_rate_names()
        x = self.get_variable(variable=variable)
        y = self.get_fluxes_df(concatenated=True).loc[:, rate_names]
        return plot(
            plot_args=(x, y),
            legend=rate_names,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_flux_selection_against_variable(
        self,
        rate_names,
        variable,
        xlabel=None,
        ylabel=None,
        title=None,
        grid=True,
        tight_layout=True,
        ax=None,
        figure_kwargs=None,
        subplot_kwargs=None,
        plot_kwargs=None,
        grid_kwargs=None,
        legend_kwargs=None,
        tick_kwargs=None,
        label_kwargs=None,
        title_kwargs=None,
    ):
        """Plot fluxes of a selection of results against another result.

        Parameters
        ----------
        rate_names : iterable(str)
        variable : str
        xlabel : str
        ylabel : str
        title : str
        grid : bool
        tight_layout : bool
        ax : matplotlib axes
        figure_kwargs : dict
        subplot_kwargs : dict
        plot_kwargs : dict
        grid_kwargs : dict
        legend_kwargs : dict
        tick_kwargs : dict
        label_kwargs : dict
        title_kwargs : dict

        Returns
        -------
        fig : matplotlib Figure
        ax : matplotlib axes
        """
        if xlabel is None:
            xlabel = variable
        x = self.get_variable(variable=variable)
        y = self.get_fluxes_df(concatenated=True).loc[:, rate_names]
        return plot(
            plot_args=(x, y),
            legend=rate_names,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_phase_plane(
        self,
        cpd1,
        cpd2,
        xlabel=None,
        ylabel=None,
        title=None,
        grid=True,
        tight_layout=True,
        ax=None,
        figure_kwargs=None,
        subplot_kwargs=None,
        plot_kwargs=None,
        grid_kwargs=None,
        legend_kwargs=None,
        tick_kwargs=None,
        label_kwargs=None,
        title_kwargs=None,
    ):
        """Plot two variables against each other.

        Parameters
        ----------
        cpd1 : str
        cpd2 : str
        xlabel : str
        ylabel : str
        title : str
        grid : bool
        tight_layout : bool
        ax : matplotlib axes
        figure_kwargs : dict
        subplot_kwargs : dict
        plot_kwargs : dict
        grid_kwargs : dict
        legend_kwargs : dict
        tick_kwargs : dict
        label_kwargs : dict
        title_kwargs : dict

        Returns
        -------
        fig : matplotlib Figure
        ax : matplotlib axes
        """
        if xlabel is None:
            xlabel = cpd1
        if ylabel is None:
            ylabel = cpd2
        x = self.get_variable(variable=cpd1)
        y = self.get_variable(variable=cpd2)
        return plot(
            plot_args=(x, y),
            legend=None,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            tight_layout=tight_layout,
            ax=ax,
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            legend_kwargs=legend_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
        )

    def plot_phase_space(
        self,
        cpd1,
        cpd2,
        cpd3,
        xlabel=None,
        ylabel=None,
        zlabel=None,
        title=None,
        grid=True,
        tight_layout=True,
        ax=None,
        figure_kwargs=None,
        subplot_kwargs=None,
        plot_kwargs=None,
        grid_kwargs=None,
        legend_kwargs=None,
        tick_kwargs=None,
        label_kwargs=None,
        title_kwargs=None,
    ):
        """Plot three variables against each other.

        Parameters
        ----------
        cpd1 : str
        cpd2 : str
        cpd3 : str
        xlabel : str
        ylabel : str
        zlabel : str
        title : str
        grid : bool
        tight_layout : bool
        ax : matplotlib axes
        figure_kwargs : dict
        subplot_kwargs : dict
        plot_kwargs : dict
        grid_kwargs : dict
        legend_kwargs : dict
        tick_kwargs : dict
        label_kwargs : dict
        title_kwargs : dict

        Returns
        -------
        fig : matplotlib Figure
        ax : matplotlib axes
        """
        kwargs = _get_plot_kwargs(
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
            legend_kwargs=legend_kwargs,
        )
        kwargs["subplot"].update({"projection": "3d"})

        if ax is None:
            fig, ax = plt.subplots(1, 1, subplot_kw=kwargs["subplot"], **kwargs["figure"])
        else:
            fig = ax.get_figure()

        ax.plot(
            self.get_variable(variable=cpd1),
            self.get_variable(variable=cpd2),
            self.get_variable(variable=cpd3),
            **kwargs["plot"],
        )

        xlabel = cpd1 if xlabel is None else xlabel
        ylabel = cpd2 if ylabel is None else ylabel
        zlabel = cpd3 if zlabel is None else zlabel

        _style_subplot(
            ax=ax,
            xlabel=xlabel,
            ylabel=ylabel,
            zlabel=zlabel,
            title=title,
            grid=grid,
            kwargs=kwargs,
        )
        if tight_layout:
            fig.tight_layout()
        return fig, ax

    def plot_trajectories(
        self,
        cpd1,
        cpd2,
        cpd1_bounds,
        cpd2_bounds,
        n,
        y0,
        t0=0,
        xlabel=None,
        ylabel=None,
        title=None,
        grid=True,
        tight_layout=True,
        ax=None,
        figure_kwargs=None,
        subplot_kwargs=None,
        plot_kwargs=None,
        grid_kwargs=None,
        legend_kwargs=None,
        tick_kwargs=None,
        label_kwargs=None,
        title_kwargs=None,
    ):
        """Plot trajectories of two variables against each other.

        Parameters
        ----------
        cpd1 : str
        cpd2 : str
        cpd1_bounds : iterable(num)
        cpd2_bounds : iterable(num)
        xlabel : str
        ylabel : str
        title : str
        grid : bool
        tight_layout : bool
        ax : matplotlib axes
        figure_kwargs : dict
        subplot_kwargs : dict
        plot_kwargs : dict
        grid_kwargs : dict
        legend_kwargs : dict
        tick_kwargs : dict
        label_kwargs : dict
        title_kwargs : dict

        Returns
        -------
        fig : matplotlib Figure
        ax : matplotlib axes
        """
        kwargs = _get_plot_kwargs(
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
            legend_kwargs=legend_kwargs,
        )

        x = np.linspace(*cpd1_bounds, n)
        y = np.linspace(*cpd2_bounds, n)
        u = np.zeros((n, n))
        v = np.zeros((n, n))

        fcd = self.model.get_full_concentration_dict(y=y0, t=t0)
        for i, s1 in enumerate(x):
            for j, s2 in enumerate(y):
                # Update y0 to new values
                fcd.update({cpd1: s1, cpd2: s2})
                rhs = self.model.get_right_hand_side(y=fcd, t=t0)
                u[i, j] = rhs[f"d{cpd1}dt"]
                v[i, j] = rhs[f"d{cpd2}dt"]

        if ax is None:
            fig, ax = plt.subplots(1, 1, subplot_kw=kwargs["subplot"], **kwargs["figure"])
        else:
            fig = ax.get_figure()
        ax.quiver(x, y, u.T, v.T)
        xlabel = cpd1 if xlabel is None else xlabel
        ylabel = cpd2 if ylabel is None else ylabel
        _style_subplot(
            ax=ax,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=grid,
            kwargs=kwargs,
        )
        if tight_layout:
            fig.tight_layout()
        return fig, ax

    def plot_3d_trajectories(
        self,
        cpd1,
        cpd2,
        cpd3,
        cpd1_bounds,
        cpd2_bounds,
        cpd3_bounds,
        n,
        y0,
        t0=0,
        xlabel=None,
        ylabel=None,
        zlabel=None,
        title=None,
        grid=True,
        tight_layout=True,
        ax=None,
        figure_kwargs=None,
        subplot_kwargs=None,
        plot_kwargs=None,
        grid_kwargs=None,
        legend_kwargs=None,
        tick_kwargs=None,
        label_kwargs=None,
        title_kwargs=None,
    ):
        """Plot trajectories of three variables against each other.

        Parameters
        ----------
        cpd1 : str
        cpd2 : str
        cpd3 : str
        cpd1_bounds : iterable(num)
        cpd2_bounds : iterable(num)
        cpd3_bounds : iterable(num)
        xlabel : str
        ylabel : str
        title : str
        grid : bool
        tight_layout : bool
        ax : matplotlib axes
        figure_kwargs : dict
        subplot_kwargs : dict
        plot_kwargs : dict
        grid_kwargs : dict
        legend_kwargs : dict
        tick_kwargs : dict
        label_kwargs : dict
        title_kwargs : dict

        Returns
        -------
        fig : matplotlib Figure
        ax : matplotlib axes
        """
        kwargs = _get_plot_kwargs(
            figure_kwargs=figure_kwargs,
            subplot_kwargs=subplot_kwargs,
            plot_kwargs=plot_kwargs,
            grid_kwargs=grid_kwargs,
            tick_kwargs=tick_kwargs,
            label_kwargs=label_kwargs,
            title_kwargs=title_kwargs,
            legend_kwargs=legend_kwargs,
        )
        kwargs["subplot"].update({"projection": "3d"})

        x = np.linspace(*cpd1_bounds, n)
        y = np.linspace(*cpd2_bounds, n)
        z = np.linspace(*cpd3_bounds, n)
        u = np.zeros((n, n, n))
        v = np.zeros((n, n, n))
        w = np.zeros((n, n, n))

        fcd = self.model.get_full_concentration_dict(y=y0, t=t0)
        for i, s1 in enumerate(x):
            for j, s2 in enumerate(y):
                for k, s3 in enumerate(y):
                    fcd.update({cpd1: s1, cpd2: s2, cpd3: s3})
                    rhs = self.model.get_right_hand_side(y=fcd, t=t0)
                    u[i, j, k] = rhs[f"d{cpd1}dt"]
                    v[i, j, k] = rhs[f"d{cpd2}dt"]
                    w[i, j, k] = rhs[f"d{cpd3}dt"]

        if ax is None:
            fig, ax = plt.subplots(1, 1, subplot_kw=kwargs["subplot"], **kwargs["figure"])
        else:
            fig = ax.get_figure()
        X, Y, Z = np.meshgrid(x, y, z)
        ax.quiver(
            X,
            Y,
            Z,
            np.transpose(u, [1, 0, 2]),
            np.transpose(v, [1, 0, 2]),
            np.transpose(w, [1, 0, 2]),
            length=0.05,
            normalize=True,
            alpha=0.5,
        )
        xlabel = cpd1 if xlabel is None else xlabel
        ylabel = cpd2 if ylabel is None else ylabel
        zlabel = cpd3 if zlabel is None else zlabel
        _style_subplot(
            ax=ax,
            xlabel=xlabel,
            ylabel=ylabel,
            zlabel=zlabel,
            title=title,
            grid=grid,
            kwargs=kwargs,
        )
        if tight_layout:
            fig.tight_layout()
        return fig, ax
