"""Simulator for LinearLabelModels."""

# Standard Library
import copy

# Local code
from ...utils.plotting import plot, plot_grid
from .basesimulator import _BaseSimulator


class _LinearLabelSimulate(_BaseSimulator):
    """Simulator for LinearLabelModels."""

    def __init__(self, model, integrator_name, **kwargs):
        super().__init__(model=model, integrator_name=integrator_name, **kwargs)

    def _test_run(self):
        self.model.get_fluxes_dict(
            y=self.y0,
            v_ss=self.model._v_ss,
            external_label=self.model._external_label,
            t=0,
        )
        self.model.get_right_hand_side(
            y_labels=self.y0,
            y_ss=self.model._y_ss,
            v_ss=self.model._v_ss,
            external_label=self.model._external_label,
            t=0,
        )

    def copy(self):
        """Return a deepcopy of this class."""
        new = copy.deepcopy(self)
        if new.results is not None:
            new._initialise_integrator(y0=new.results[-1])
        elif new.y0 is not None:
            new.initialise(
                label_y0=new.y0,
                y_ss=new.model._y_ss,
                v_ss=new.model._v_ss,
                external_label=new.model._external_label,
                test_run=False,
            )
        return new

    def initialise(self, label_y0, y_ss, v_ss, external_label=1, test_run=True):
        """Initialise the integrator.

        Parameters
        ----------
        y0 : Union(dict(str: num), iterable(num))
        test_run : bool
            Whether to perform a test_run to get proper error handling.
        """
        self.model._y_ss = y_ss
        self.model._v_ss = v_ss
        self.model._external_label = external_label
        super().initialise(y0=label_y0, test_run=test_run)

    def get_label_position(self, compound, position):
        """Get relative concentration of a single isotopomer.

        Parameters
        ----------
        compound : str
            name of the base compound
        position : int
            position

        Returns
        -------
        isotopomer_concentration : numpy.ndarray

        Examples
        --------
        get_label_position(compound="GAP", position=2)
        """
        return self.get_results_dict()[self.model.isotopomers[compound][position]]

    def get_label_distribution(self, compound):
        """Get relative concentrations of all compound isotopomers.

        Parameters
        ----------
        compound : str
            name of the base compound

        Returns
        -------
        isotopomer_concentrations : numpy.ndarray

        Examples
        --------
        get_label_position(compound="GAP")
        """
        compounds = self.model.isotopomers[compound]
        return self.get_results_df().loc[:, compounds].values

    def plot_label_distribution(
        self,
        compound,
        relative=True,
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
        """Plot label distribution of a compound.

        Parameters
        ----------
        compound : str
        relative : bool
        xlabel : str
        ylabel : str
        title : str
        grid : bool
        ax : matplotlib.axes
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
        concentrations : numpy.array
        """
        if ylabel is None and relative:
            ylabel = "Relative concentration"

        x = self.get_time()
        y = self.get_label_distribution(compound=compound)
        legend = [f"Pos {i}" for i in range(len(self.model.isotopomers[compound]))]
        if title is None:
            title = compound
        return plot(
            plot_args=(x, y),
            legend=legend,
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

    def plot_label_distribution_grid(
        self,
        compounds,
        relative=True,
        ncols=None,
        sharex=True,
        sharey=True,
        xlabels=None,
        ylabels=None,
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
        """Plot label distributions of multiple compounds on a grid.

        Parameters
        ----------
        compounds : iterable(str)
        relative : bool
        ncols : int
        xlabel : str
        ylabel : str
        title : str
        grid : bool
        ax : matplotlib.axes
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
        concentrations : numpy.array
        """
        time = self.get_time()
        plot_groups = [(time, self.get_label_distribution(compound=compound)) for compound in compounds]
        legend_groups = [[f"Pos {i}" for i in range(len(self.model.isotopomers[compound]))] for compound in compounds]
        if ylabels is None and relative:
            ylabels = "Relative concentration"
        if plot_titles is None:
            plot_titles = compounds
        return plot_grid(
            plot_groups=plot_groups,
            legend_groups=legend_groups,
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

    def plot_all_label_distributions(
        self,
        relative=True,
        ncols=None,
        sharex=True,
        sharey=True,
        xlabels=None,
        ylabels=None,
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
        """Plot label distributions of all compounds on a grid.

        Parameters
        ----------
        relative : bool
        ncols : int
        xlabel : str
        ylabel : str
        title : str
        grid : bool
        ax : matplotlib.axes
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
        concentrations : numpy.array
        """
        time = self.get_time()
        compounds = self.model.isotopomers
        plot_groups = [(time, self.get_label_distribution(compound=compound)) for compound in compounds]
        legend_groups = [[f"Pos {i}" for i in range(len(self.model.isotopomers[compound]))] for compound in compounds]
        if ylabels is None and relative:
            ylabels = "Relative concentration"
        if plot_titles is None:
            plot_titles = compounds

        return plot_grid(
            plot_groups=plot_groups,
            legend_groups=legend_groups,
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
