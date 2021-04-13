"""Simulator for LabelModels."""

# Standard Library
import re as re

# Third party
import numpy as np

# Local code
from ...utils.plotting import plot, plot_grid
from .simulator import _Simulate


class _LabelSimulate(_Simulate):
    """Simulator for LabelModels."""

    def __init__(self, model, integrator_name, **kwargs):
        super().__init__(model=model, integrator_name=integrator_name, **kwargs)

    def generate_y0(self, base_y0, label_positions):
        """Generate y0 for all isotopomers given a base y0.

        Parameters
        ----------
        base_y0 : dict(str : num)
        label_positions : dict(str : num)

        Returns
        -------
        y0 : dict(str : num)

        Examples
        --------
        >>> base_y0 = {"GAP": 1, "DHAP": 0, "FBP": 0}
        >>> generate_y0(base_y0=base_y0, label_positions={"GAP": 0})
        {"GAP__100": 1, "DHAP__000": 1, "FBP__000000": 1}  # excluding the zeros
        """
        return self.model.generate_y0(base_y0=base_y0, label_positions=label_positions)

    def get_total_concentration(self, compound):
        """Get the total concentration of all isotopomers of a compound.

        Parameters
        ----------
        compound : str

        Returns
        -------
        concentrations : numpy.array
        """
        return self.get_full_results_dict()[compound + "__total"]

    def get_unlabeled_concentration(self, compound):
        """Get the concentration of an isotopomer that is unlabeled.

        Parameters
        ----------
        compound : str

        Returns
        -------
        concentrations : numpy.array
        """
        carbons = "0" * self.model.label_compounds[compound]["num_labels"]
        return self.get_full_results_dict()[compound + f"__{carbons}"]

    def get_total_label_concentration(self, compound):
        """Get the total concentration of all labeled isotopomers of a compound.

        Parameters
        ----------
        compound : str

        Returns
        -------
        concentrations : numpy.array
        """
        return self.get_total_concentration(compound=compound) - self.get_unlabeled_concentration(compound=compound)

    def get_all_isotopomer_concentrations_array(self, compound):
        """Get concentrations of all isotopomers of a compound.

        Parameters
        ----------
        compound : str

        Returns
        -------
        concentrations : numpy.array
        """
        return self.get_all_isotopomer_concentrations_df(compound=compound).values

    def get_all_isotopomer_concentrations_dict(self, compound):
        """Get concentrations of all isotopomers of a compound.

        Parameters
        ----------
        compound : str

        Returns
        -------
        concentrations : dict
        """
        df = self.get_all_isotopomer_concentrations_df(compound=compound)
        return dict(zip(df.columns, df.values.T))

    def get_all_isotopomer_concentrations_df(self, compound):
        """Get concentrations of all isotopomers of a compound.

        Parameters
        ----------
        compound : str

        Returns
        -------
        concentrations : pandas.DataFrame
        """
        isotopomers = self.model.get_compound_isotopomers(compound=compound)
        return self.get_results_df()[isotopomers]

    def get_concentrations_by_reg_exp_array(self, reg_exp):
        """Get concentrations of all isotopomers matching the regular expression.

        Parameters
        ----------
        reg_exp : str

        Returns
        -------
        concentrations : numpy.array
        """
        isotopomers = [i for i in self.model.get_compounds() if re.match(reg_exp, i)]
        return self.get_results_df()[isotopomers].values

    def get_concentrations_by_reg_exp_dict(self, reg_exp):
        """Get concentrations of all isotopomers of a compound.

        Parameters
        ----------
        compound : str

        Returns
        -------
        concentrations : dict
        """
        isotopomers = [i for i in self.model.get_compounds() if re.match(reg_exp, i)]
        df = self.get_results_df()[isotopomers]
        return dict(zip(df.columns, df.values.T))

    def get_concentrations_by_reg_exp_df(self, reg_exp):
        """Get concentrations of all isotopomers of a compound.

        Parameters
        ----------
        compound : str

        Returns
        -------
        concentrations : pandas.DataFrame
        """
        isotopomers = [i for i in self.model.get_compounds() if re.match(reg_exp, i)]
        return self.get_results_df()[isotopomers]

    def get_concentration_at_positions(self, compound, positions):
        """Get concentration of an isotopomer labelled at certain position(s).

        Parameters
        ----------
        compound : str
        positions : Union(int, iterable(int))

        Returns
        -------
        concentrations : numpy.array
        """
        if isinstance(positions, int):
            positions = [positions]
        num_labels = self.model.label_compounds[compound]["num_labels"]
        label_positions = ["[01]"] * num_labels
        for position in positions:
            label_positions[position] = "1"
        reg_exp = f"{compound}__{''.join(label_positions)}"
        return np.sum(self.get_concentrations_by_reg_exp_array(reg_exp=reg_exp), axis=1)

    def get_concentrations_of_n_labeled_array(self, compound, n_labels):
        """Get concentrations of all isotopomers that carry n labels.

        Parameters
        ----------
        compound : str
        n_labels : int

        Returns
        -------
        concentrations : numpy.array
        """
        return self.get_concentrations_of_n_labeled_df(compound=compound, n_labels=n_labels).values

    def get_concentrations_of_n_labeled_dict(self, compound, n_labels):
        """Get concentrations of all isotopomers that carry n labels.

        Parameters
        ----------
        compound : str
        n_labels : int

        Returns
        -------
        concentrations : dict
        """
        df = self.get_concentrations_of_n_labeled_df(compound=compound, n_labels=n_labels)
        return dict(zip(df.columns, df.values.T))

    def get_concentrations_of_n_labeled_df(self, compound, n_labels):
        """Get concentrations of all isotopomers that carry n labels.

        Parameters
        ----------
        compound : str
        n_labels : int

        Returns
        -------
        concentrations : pandas.DataFrame
        """
        isotopomers = self.model.get_compound_isotopomers_with_n_labels(compound=compound, n_labels=n_labels)
        return self.get_results_df()[isotopomers]

    def plot(
        self,
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
        """Plot all total concentrations.

        Parameters
        ----------
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
        compounds = sorted([f"{i}__total" for i in self.model.label_compounds] + self.model.nonlabel_compounds)
        x = self.get_time()
        y = self.get_full_results_df().loc[:, compounds]
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

    def _calculate_label_distribution(self, *, compound, relative):
        """Calculate the label distribution of a compound.

        Parameters
        ----------
        compound : str
        relative : bool

        Returns
        -------
        concentrations : numpy.array
        """
        total_concentration = self.get_total_concentration(compound=compound)
        concentrations = []
        for position in range(self.model.get_compound_number_of_label_positions(compound=compound)):
            concentration = self.get_concentration_at_positions(compound=compound, positions=position)
            if relative:
                concentration = concentration / total_concentration
            concentrations.append(concentration)
        return np.array(concentrations).T

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
        y = self._calculate_label_distribution(compound=compound, relative=relative)
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
        plot_groups = [
            (
                time,
                self._calculate_label_distribution(compound=compound, relative=relative),
            )
            for compound in compounds
        ]
        legend_groups = [
            [f"Pos {i}" for i in range(self.model.get_compound_number_of_label_positions(compound=compound))]
            for compound in compounds
        ]
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
        base_compounds = self.model.label_compounds
        plot_groups = [
            (
                time,
                self._calculate_label_distribution(compound=compound, relative=relative),
            )
            for compound in base_compounds
        ]
        legend_groups = [
            [f"Pos {i}" for i in range(self.model.get_compound_number_of_label_positions(compound=compound))]
            for compound in base_compounds
        ]
        if ylabels is None and relative:
            ylabels = "Relative concentration"

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
