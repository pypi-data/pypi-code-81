"""
replica_exchange.py

author: C. Lockhart <clockha2@gmu.edu>
language: Python3
"""

from molecular.io import loadtxt

import numpy as np
import pandas as pd


# Class that stores exchange history, i.e., which replicas visited which configurations over time
class ExchangeHistory:
    """
    Replica-exchange and other coupled Markov chain simulations follow replicas over time as they walk across
    configuration space. Here, "configuration" is used generically and can refer to temperature (commonly), Hamiltonian
    scaling factors, etc.

    The purpose of this class is to permit easy evaluation of exchange performance. We can compute (and plot) parameters
    like the exchange rate, mosaic plot of the replica walk, the Hansmann parameter, and tunneling time.
    """

    __slots__ = '_data'

    # Initialize instance of exchange history
    def __init__(self, data, only_neighbors=True):
        """
        `data` must be a pandas DataFrame with the columns "replica", "config", and "step". Note that the elements in
        "replica" and "config" refer to indices.

        Parameters
        ----------
        data : pandas.DataFrame
            Exchange history.
        only_neighbors : bool
            Were exchanges permitted only between neighbors?
        """

        # Validate input
        if not isinstance(data, pd.DataFrame) or ~np.in1d(['replica', 'config', 'step'], data.columns).all():
            raise AttributeError('data must be DataFrame')

        # Make sure that replicas do not jump by more than 1 configuration at a time if only_neighbors is true
        # TODO is it necessary to have this validation step?
        if only_neighbors:
            n_replicas = data['replica'].nunique()
            for replica in range(n_replicas):
                tmp = data.query(f'replica == {replica}')['config'].diff().fillna(0)
                assert tmp.min() == -1
                assert tmp.max() == 1

        # Save
        self._data = data

    # Read NAMD history file (from their RE multi-copy algorithm)
    # TODO what if someone loaded .sort.history? The labels replica and config would be swapped.
    @classmethod
    def from_namd(cls, fname, n_replicas, glob=False):
        """
        Construct the exchange history from the results of NAMD replica exchange.

        Parameters
        ----------
        fname : str
            Name of the history file. The assumption is that there is one history file per replica. This method expects
            to find the variable `{replica}` to specify the file for each replica.
        n_replicas : int
            The number of replicas.
        glob : bool
            Indicates if `fname` contains extra glob-like features, such as wild-cards.

        Returns
        -------
        ExchangeHistory
            Newly-created instance of ExchangeHistory.

        Examples
        --------
        >>> ExchangeHistory.from_namd('exchange_{replica}.history', n_replicas=16, glob=False)
        >>> ExchangeHistory.from_namd('exchange_job?.{replica}.history', n_replicas=16, glob=True)
        """

        # Initialize DataFrame to hold results
        data = pd.DataFrame()

        # Loop over all replicas and read in files
        for replica in range(n_replicas):
            tmp = loadtxt(fname.format(replica=replica), glob=glob)
            data = data.append(pd.DataFrame({
                'step': tmp[:, 0],
                'replica': np.repeat(replica, len(tmp)),
                'config': tmp[:, 1].astype(int),
                'temperature': tmp[:, 2]
            }), ignore_index=True)

        # Return instantiated ExchangeHistory class. This is sorted but there's strictly no reason to do this.
        return cls(data.sort_values(['replica', 'step']))

    # Read history from parquet
    @classmethod
    def from_parquet(cls, fname):
        """
        Read exchange history from parquet.

        Parameters
        ----------
        fname : str
            Parquet file.

        Returns
        -------
        ExchangeHistory
        """

        return cls(pd.read_parquet(fname))

    # Cross-tabulate by config and replica axes
    def crosstab(self, index='config', column='replica'):
        """
        Cross-tabulate by "config" and "replica" axes. In other words, count the number of snapshots at given
        config and replica indices.

        Parameters
        ----------
        index : str
            Axis to define rows.
        column : str
            Axis to define columns.

        Returns
        -------
        pandas.DataFrame
            Cross-tabulation of the ExchangeHistory instance.
        """

        # Get the exchange history trajectory by the index
        data = self.trajectory(by=index, reset_index=True)

        # Melt the data by the column
        data_melt = data.melt(value_name=column)

        # Return pandas cross tabulation
        return pd.crosstab(index=data_melt[index], columns=data_melt[column])

    # Compute the exchange rate
    def exchange_rate(self, by='config', n_attempts=None, terminal_factor=0.5):
        """
        Compute the exchange rate.

        Parameters
        ----------
        by : str
            Default: config
        n_attempts : int
            Number of attempts per config or replica.
        terminal_factor : float
            Factor to apply to the first and last config to reduce its number of attempts.

        Returns
        -------
        pandas.Series
            Exchange rate per config or replica.
        """

        # Pull the trajectory
        trj = self.trajectory(by=by if by is not None else 'config')

        # Derive number of attempts. This is tricky because it depends on how exchange was set up. In unbiased exchange,
        # we expect that every replica/config exchanges every step. However, the terminal configs usually only exchange
        # every other attempt (because they're at a boundary) so we apply the terminal factor. In the future, I would
        # like to make this more intuitive.
        if n_attempts is None:
            n_attempts = np.repeat(len(trj), len(trj.columns))
            n_attempts[0] = np.floor(n_attempts[0] * terminal_factor)
            n_attempts[-1] = np.floor(n_attempts[-1] * terminal_factor)

        # Compute number of exchanges. The logic here is that if the index from one step to the next changes, then an
        # exchange has happened.
        n_exchanges = (trj.diff().dropna(axis=0) != 0).sum()

        # Return the rate
        return np.sum(n_exchanges) / np.sum(n_attempts) if by is None else n_exchanges / n_attempts

    def hansmann(self):
        r"""
        The Hansmann parameter :math:`h(T)` shows the residence time :math:`\tau` replica :math:`r` (of :math:`R` total
        replicas) spends at configuration :math:`T`.

        .. math:: h(T) = 1 - \frac{\sqrt{\sum_{r=1}^R \tau_r^2}}{\sum_{r=1}^R \tau_r}

        If all replicas are equally sampled across all configurations, then :math:`h(T) = 1 - 1 / \sqrt{R}`.

        Returns
        -------
        pandas.Series
            Hansmann parameter computed for all configurations.
        """

        # Cross-tabulate replica by configuration
        data = self.crosstab(index='config', column='replica')

        # Return Hansmann parameter
        return 1. - np.sqrt(np.square(data).sum(axis=1)) / data.sum(axis=1)

    def hansmann_plot(self, x_title=None, y_title=None, plot_theoretical=True):
        """
        Plot the Hansmann parameter.

        Parameters
        ----------
        x_title : str
        y_title : str
        plot_theoretical : bool
            Should the theoretical Hansmann parameter in the case of equal sampling be plotted? (Default: True)
        """

        import uplot as u

        data = self.hansmann()
        x = data.index.to_numpy()
        if x[0] == 0:  # start everything from an index of 1 for aesthetics
            x += 1
        y = data.to_numpy()

        # Build figure
        fig = u.figure(style={
            'x_title': x_title,
            'y_title': y_title,
            'y_min': 0.,
            'y_max': 1.,

        })
        fig += u.line(x, y, style={'color': 'black', 'line_style': 'solid', 'marker': 'circle'})
        if plot_theoretical:
            fig += u.line(
                x,
                np.repeat(1. - 1. / np.sqrt(len(x)), len(x)),  # noqa
                style={'color': 'black', 'line_style': 'longdash', 'line_width': 1.}
            )
        fig, ax = fig.to_mpl(show=False)
        fig.savefig('hansmann_plot.svg')

    def mosaic_plot(self, interval=100, cmap='ujet'):
        """
        Plot the mosaic function using a heatmap.

        Parameters
        ----------
        interval : int
            Interval for plotting. We usually cannot plot every single step because there is too much data.
        cmap : str or object
            The matplotlib-compatible color map.
        """

        import matplotlib.pyplot as plt
        from matplotlib.ticker import MultipleLocator, MaxNLocator
        import uplot as u

        u.core.set_mpl_theme()

        data = self.trajectory(by='config', reset_index=True)
        steps = data.index.to_numpy(dtype='int')[::interval]
        replicas = data.columns.to_numpy(dtype='int')
        if replicas[0] == 0:
            replicas = replicas + 1
            data = data + 1
        mosaic = data.to_numpy(dtype='int')[::interval, :]
        x = np.arange(mosaic.shape[0] + 1)
        y = np.arange(mosaic.shape[1] + 1)

        # Start figure and axis
        fig = plt.figure()
        ax = fig.add_subplot()
        # im = ax.pcolormesh(mosaic, cmap=cmap, edgecolors='k', linewidth=0.5)  # bwr
        if cmap == 'ujet':
            import uplot
            cmap = uplot.jet
        im = ax.pcolormesh(x - 0.5, y - 0.5, mosaic.T, cmap=cmap, edgecolors='k', linewidth=0.5)

        # Format x axis
        # TODO change this so only units of X are display
        ax.set_xticks(np.arange(len(steps)))
        ax.set_xticklabels(steps)
        ax.set_xlabel(r'$step$')

        # Format y axis
        ax.set_yticks(np.arange(len(replicas)))
        ax.set_yticklabels(replicas)
        ax.set_ylabel(r'$temperature\ index$')

        # Format tick lines
        # ax.spines['top'].set_visible(False)
        # ax.spines['right'].set_visible(False)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.tick_params(axis='both', which='both', direction='out')

        ax.xaxis.set_major_locator(MultipleLocator(10))
        ax.xaxis.set_minor_locator(MultipleLocator(10))

        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_minor_locator(MultipleLocator(1))

        # fig.colorbar()
        ax.set_aspect('auto')
        # ax.grid(which='minor', color='w', linestyle='-', linewidth=5)

        ax.grid(linestyle='')

        # plt.axis('equal')
        # Add color bar
        cbar = plt.colorbar(im, ax=ax, shrink=0.5, drawedges=False)
        cbar.outline.set_linewidth(0.5)
        # cbar.ax.spines['right'].set_visible(True)
        cbar.ax.tick_params(direction='out', length=5.)
        cbar.ax.tick_params(which='minor', length=0)
        #        cbar.ax.yaxis.set_major_locator(MultipleLocator(1))
        cbar.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        cbar.ax.set_ylabel(r'$replica\ index$')

        # Save the image
        # fig.show()
        fig.savefig('mosaic_plot.png')

    # Reset the step index?
    def reset_step(self):
        """
        Resets step from arbitrary interval to rank from 1 ... N. This operation occurs in place.
        """

        self._data['step'] = self._data['step'].rank(method='dense')

    # Save to csv
    def to_csv(self, *args, **kwargs):
        """
        Save ExchangeHistory to csv format. Follows :ref:`pandas.DataFrame.to_csv`.
        """
        self._data.to_csv(*args, **kwargs)

    # Save to parquet
    def to_parquet(self, *args, **kwargs):
        """
        Save ExchangeHistory to parquet format. Follows :ref:`pandas.DataFrame.to_parquet`.
        """

        self._data.to_parquet(*args, **kwargs)

    # TODO should this be renamed mosaic?
    def trajectory(self, by='config', reset_index=True):
        """
        Compute the walk of config or replicas. This is a pivot of the melted ExchangeHistory._data.

        Parameters
        ----------
        by : str
            Default: config.
        reset_index : bool
            Should the index be reset?

        Returns
        -------
        pandas.DataFrame
        """

        # Define the columns and values for the pivot
        columns = 'config'
        values = 'replica'
        if by == 'replica':
            columns, values = values, columns
        elif by != 'config':
            raise AttributeError(f'do not understand by = {by}')

        # Perform the pivot
        data = self._data.pivot_table(index='step', columns=columns, values=values)

        # Reset index?
        if reset_index:
            data.reset_index(drop=True, inplace=True)
            data.index.name = 'step'

        # Return
        return data


# Create a temperature schedule
def temp_schedule(temp_min=300, temp_max=440, n_temps=40, mode='geometric'):
    r"""
    Create a temperature schedule that could be used, for instance, with replica exchange.

    There are several choices for `mode`. Note that :math:`T` refers to the temperature at :math:`i = 1 ... R`, where
    :math:`T_1` is `temp_min` and :math:`T_R` is `temp_max`. In total, there are :math:`R` temperatures (= `n_temps`).

    * "geometric" [#]_

    .. math :: T_i = T_1 \left( \frac{T_R}{T_1} \right)^{\frac{i-1}{R-1}}

    * "linear"

    .. math :: T_i = T_1 + (i-1) \frac{T_R-T_1}{R-1}

    * "parabolic" (Note if `n_temps` is even, `temp_max` won't directly be sampled).

    .. math :: T_i = T_1 - \frac{T_R-T_1}{\left( \frac{R-1}{2} \right) ^2} (i-1) (i-R)

    Parameters
    ----------
    temp_min : float
        Lowest temperature
    temp_max : float
        Highest temperature
    n_temps : int
        Number of temperatures
    mode : str
        Mode to produce schedule. Valid options include "geometric", "linear", "parabolic". Any substring will match,
        but the preference should be to use the full option label. (Default: "geometric")

    Returns
    -------
    numpy.ndarray
        Temperature schedule

    Examples
    --------
    .. plot::
       :include-source:

       import matplotlib.pyplot as plt
       import molecular as mol

       n_temps = 10
       geometric = mol.temp_schedule(300, 440, n_temps, 'geometric')
       linear = mol.temp_schedule(300, 440, n_temps, 'linear')
       parabolic = mol.temp_schedule(300, 440, n_temps, 'parabolic')

       plt.figure()
       plt.plot(range(n_temps), geometric, label='geometric')
       plt.plot(range(n_temps), linear, label='linear')
       plt.plot(range(n_temps), parabolic, label='parabolic')
       plt.xlabel('index')
       plt.ylabel('temperature')
       plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
       plt.show()

    References
    ----------
    .. [#] Nymeyer, H., Gnanakaran, S., & García, A. E. (2004) Atomistic simulations of protein folding, using the
       replica exchange algorithm. *Methods Enzymol.* **383**: 119-149.
    """

    mode = mode.lower()

    if mode in 'geometric':
        schedule = temp_min * np.power(temp_max / temp_min, np.arange(n_temps) / (n_temps - 1.), dtype=np.float64)

    elif mode in 'linear':
        schedule = np.linspace(start=temp_min, stop=temp_max, num=n_temps)

    elif mode in 'parabolic':
        temp_range = temp_max - temp_min
        temp_ind = np.arange(n_temps)
        schedule = temp_min - (temp_range / np.square((n_temps - 1.) / 2.)) * temp_ind * (temp_ind - n_temps + 1.)

    else:
        raise AttributeError(f'mode {mode} not supported')

    return schedule


if __name__ == '__main__':
    print(temp_schedule(temp_min=300, temp_max=440, n_temps=5, mode='geometric'))
    # print(temp_schedule(temp_min=310, temp_max=500, n_temps=5, mode='parabolic'))
