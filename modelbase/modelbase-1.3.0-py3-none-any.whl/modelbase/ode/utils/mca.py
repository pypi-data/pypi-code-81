"""Write me."""

# Standard Library
import math

# Third party
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Local code
from ...utils.plotting import get_norm as _get_norm
from ...utils.plotting import heatmap_from_dataframe as _heatmap_from_dataframe
from ..__init__ import Simulator

_DISPLACEMENT = 1e-4


def _find_steady_state(*, model, y0):
    """Simulate the system to steadt state.

    Just a convenience mapper.

    Parameters
    ----------
    model : modelbase.ode.model
    y0 : Union(dict(str: num), iterable(num))

    Returns
    -------
    t : numpy.array
    y : numpy.array
    """
    s = Simulator(model=model)
    s.initialise(y0=y0, test_run=False)
    t, y = s.simulate_to_steady_state()
    return t, y


def get_compound_elasticity(model, compound, y, t=0, normalized=True, displacement=_DISPLACEMENT):
    """Get sensitivity of all rates to a change of the concentration of a compound.

    Also called epsilon-elasticities. Not in steady state!

    Parameters
    ----------
    m: modelbase.ode.Model
    compound: str
    y: Union(dict(str: num), iterable(num))
    t: Union(num, iterable(num))
    normalized : bool
    displacement : float
        Percentage change of the value

    Returns
    -------
    elasticities: numpy.ndarray
    """
    y = model.get_full_concentration_dict(y=y, t=t)
    old_concentration = y[compound]
    fluxes = []
    for new_concentration in (
        old_concentration * (1 + displacement),
        old_concentration * (1 - displacement),
    ):
        y[compound] = new_concentration
        fluxes.append(model.get_fluxes_array(y=y, t=t))
    elasticity_coef = (fluxes[0] - fluxes[1]) / (2 * displacement * old_concentration)
    if normalized:
        y[compound] = old_concentration
        fluxes = model.get_fluxes_array(y=y, t=t)
        elasticity_coef *= old_concentration / fluxes
    return np.atleast_1d(np.squeeze(elasticity_coef))


def get_compound_elasticities_array(model, compounds, y, t=0, normalized=True, displacement=_DISPLACEMENT):
    """Get sensitivity of all rates to a change of the concentration of multiple compounds.

    Also called epsilon-elasticities. Not in steady state!

    Parameters
    ----------
    m: modelbase.ode.Model
    compounds: iterable(str)
    y: Union(dict(str: num), iterable(num))
    t: Union(num, iterable(num))
    normalized : bool
    displacement : float
        Percentage change of the value

    Returns
    -------
    elasticities: numpy.ndarray
    """
    elasticities = np.full(shape=(len(compounds), len(model.get_rate_names())), fill_value=np.nan)
    for i, compound in enumerate(compounds):
        elasticities[i] = get_compound_elasticity(
            model=model,
            compound=compound,
            y=y,
            t=t,
            normalized=normalized,
            displacement=displacement,
        )
    return elasticities


def get_compound_elasticities_df(model, compounds, y, t=0, normalized=True, displacement=_DISPLACEMENT):
    """Get sensitivity of all rates to a change of the concentration of multiple compounds.

    Also called epsilon-elasticities. Not in steady state!

    Parameters
    ----------
    m: modelbase.ode.Model
    compounds: iterable(str)
    y: Union(dict(str: num), iterable(num))
    t: Union(num, iterable(num))
    normalized : bool
    displacement : float
        Percentage change of the value

    Returns
    -------
    elasticities: pandas.DataFrame
    """
    array = get_compound_elasticities_array(
        model=model,
        compounds=compounds,
        y=y,
        t=t,
        normalized=normalized,
        displacement=displacement,
    )
    return pd.DataFrame(data=array, index=compounds, columns=model.get_rate_names())


def get_parameter_elasticity(model, parameter, y, t=0, normalized=True, displacement=_DISPLACEMENT):
    """Get sensitivity of all rates to a change of a parameter value.

    Also called pi-elasticities. Not in steady state!

    Parameters
    ----------
    m: modelbase.ode.Model
    parameter: str
    y: Union(dict(str: num), iterable(num))
    t: Union(num, iterable(num))
    normalized : bool
    displacement : float
        Percentage change of the value

    Returns
    -------
    elasticities: numpy.array
    """
    model = model.copy()
    old_value = model.get_parameter(parameter_name=parameter)
    fluxes = []
    for new_value in [old_value * (1 + displacement), old_value * (1 - displacement)]:
        model.update_parameter(parameter_name=parameter, parameter_value=new_value)
        fluxes.append(model.get_fluxes_array(y=y, t=t))
    elasticity_coef = (fluxes[0] - fluxes[1]) / (2 * displacement * old_value)
    if normalized:
        model.update_parameter(parameter_name=parameter, parameter_value=old_value)
        fluxes = model.get_fluxes_array(y=y, t=t)
        elasticity_coef *= old_value / fluxes
    return np.atleast_1d(np.squeeze(elasticity_coef))


def get_parameter_elasticities_array(model, parameters, y, t=0, normalized=True, displacement=_DISPLACEMENT):
    """Get sensitivity of all rates to a change of multiple parameter values.

    Also called pi-elasticities. Not in steady state!

    Parameters
    ----------
    m: modelbase.ode.Model
    parameters: iterable(str)
    y: Union(dict(str: num), iterable(num))
    t: Union(num, iterable(num))
    normalized : bool
    displacement : float
        Percentage change of the value

    Returns
    -------
    elasticities: numpy.array
    """
    elasticities = np.full(shape=(len(parameters), len(model.get_rate_names())), fill_value=np.nan)
    for i, parameter in enumerate(parameters):
        elasticities[i] = get_parameter_elasticity(
            model=model,
            parameter=parameter,
            y=y,
            t=t,
            normalized=normalized,
            displacement=displacement,
        )
    return elasticities


def get_parameter_elasticities_df(model, parameters, y, t=0, normalized=True, displacement=_DISPLACEMENT):
    """Get sensitivity of all rates to a change of multiple parameter values.

    Also called pi-elasticities. Not in steady state!

    Parameters
    ----------
    m: modelbase.ode.Model
    parameters: iterable(str)
    y: Union(dict(str: num), iterable(num))
    t: Union(num, iterable(num))
    normalized : bool
    displacement : float
        Percentage change of the value

    Returns
    -------
    elasticities: pandas.DataFrame
    """
    matrix = get_parameter_elasticities_array(
        model=model,
        parameters=parameters,
        y=y,
        t=t,
        normalized=normalized,
        displacement=displacement,
    )
    return pd.DataFrame(matrix, index=parameters, columns=model.get_rate_names())


def get_concentration_response_coefficient(
    model, parameter, y, t=0, normalized=True, displacement=_DISPLACEMENT
):
    """Get response of the steady state concentrations to a change of the given parameter.

    Parameters
    ----------
    m: modelbase.ode.Model
    parameter : str
    y: Union(dict(str: num), iterable(num))
    t: Union(num, iterable(num))
    normalized : bool
    displacement : float
        Percentage change of the value

    Returns
    -------
    coefficients: numpy.array
    """
    model = model.copy()
    old_value = model.get_parameter(parameter_name=parameter)
    ss = []
    for new_value in [
        old_value * (1 + displacement),
        old_value * (1 - displacement),
    ]:
        model.update_parameter(parameter_name=parameter, parameter_value=new_value)
        t_ss, y_ss = _find_steady_state(model=model, y0=y)
        ss.append(y_ss)
    resp_coef = (ss[0] - ss[1]) / (2 * displacement * old_value)
    if normalized:
        model.update_parameter(parameter_name=parameter, parameter_value=old_value)
        t_ss, y_ss = _find_steady_state(model=model, y0=y)
        resp_coef *= old_value / y_ss
    return np.atleast_1d(np.squeeze(resp_coef))


def get_concentration_response_coefficients_array(
    model, parameters, y, t=0, normalized=True, displacement=_DISPLACEMENT
):
    """Get response of the steady state concentrations to a change of the given parameters.

    Parameters
    ----------
    m: modelbase.ode.Model
    parameters: iterable(str)
    y: Union(dict(str: num), iterable(num))
    t: Union(num, iterable(num))
    normalized : bool
    displacement : float
        Percentage change of the value

    Returns
    -------
    coefficients: numpy.array
    """
    crs = np.full(shape=(len(parameters), len(model.get_compounds())), fill_value=np.nan)
    for i, parameter in enumerate(parameters):
        crs[i] = get_concentration_response_coefficient(
            model=model,
            parameter=parameter,
            y=y,
            t=t,
            normalized=normalized,
            displacement=displacement,
        )
    return crs


def get_concentration_response_coefficients_df(
    model, parameters, y, t=0, normalized=True, displacement=_DISPLACEMENT
):
    """Get response of the steady state concentrations to a change of the given parameter m.

    Parameters
    ----------
    m: modelbase.ode.Model
    parameters: iterable(str)
    y: Union(dict(str: num), iterable(num))
    t: Union(num, iterable(num))
    normalized : bool
    displacement : float
        Percentage change of the value

    Returns
    -------
    coefficients: pandas.DataFrame
    """
    array = get_concentration_response_coefficients_array(
        model=model,
        parameters=parameters,
        y=y,
        t=t,
        normalized=normalized,
        displacement=displacement,
    )
    return pd.DataFrame(data=array, index=parameters, columns=model.get_compounds())


def get_flux_response_coefficient(model, parameter, y, t=0, normalized=True, displacement=_DISPLACEMENT):
    """Get response of the steady state fluxes to a change of the given parameter.

    Parameters
    ----------
    m: modelbase.ode.Model
    parameters: iterable(str)
    y: Union(dict(str: num), iterable(num))
    t: Union(num, iterable(num))
    normalized : bool
    displacement : float
        Percentage change of the value

    Returns
    -------
    coefficients: numpy.array
    """
    model = model.copy()
    old_value = model.get_parameter(parameter_name=parameter)
    fluxes = []
    for new_value in [
        old_value * (1 + displacement),
        old_value * (1 - displacement),
    ]:
        model.update_parameter(parameter_name=parameter, parameter_value=new_value)
        t_ss, y_ss = _find_steady_state(model=model, y0=y)
        fluxes.append(model.get_fluxes_array(y=y_ss, t=t_ss))
    resp_coef = (fluxes[0] - fluxes[1]) / (2 * displacement * old_value)
    if normalized:
        model.update_parameter(parameter_name=parameter, parameter_value=old_value)
        t_ss, y_ss = _find_steady_state(model=model, y0=y)
        fluxes = model.get_fluxes_array(y=y_ss, t=t_ss)
        resp_coef *= old_value / fluxes
    return np.atleast_1d(np.squeeze(resp_coef))


def get_flux_response_coefficients_array(
    model, parameters, y, t=0, normalized=True, displacement=_DISPLACEMENT
):
    """Get response of the steady state fluxes to a change of the given parameters.

    Parameters
    ----------
    m: modelbase.ode.Model
    parameters: iterable(str)
    y: Union(dict(str: num), iterable(num))
    t: Union(num, iterable(num))
    normalized : bool
    displacement : float
        Percentage change of the value

    Returns
    -------
    coefficients: numpy.array
    """
    frc = np.full(shape=(len(parameters), len(model.get_rate_names())), fill_value=np.nan)
    for i, parameter in enumerate(parameters):
        frc[i] = get_flux_response_coefficient(
            model=model,
            parameter=parameter,
            y=y,
            t=t,
            normalized=normalized,
            displacement=displacement,
        )
    return frc


def get_flux_response_coefficients_df(model, parameters, y, t=0, normalized=True, displacement=_DISPLACEMENT):
    """Get response of the steady state fluxes to a change of the given parameters.

    Parameters
    ----------
    m: modelbase.ode.Model
    parameters: iterable(str)
    y: Union(dict(str: num), iterable(num))
    t: Union(num, iterable(num))
    normalized : bool
    displacement : float
        Percentage change of the value

    Returns
    -------
    coefficients: numpy.array
    """
    array = get_flux_response_coefficients_array(
        model=model,
        parameters=parameters,
        y=y,
        t=t,
        normalized=normalized,
        displacement=displacement,
    )
    return pd.DataFrame(data=array, index=parameters, columns=model.get_rate_names())


def plot_coefficient_heatmap(
    df,
    title,
    cmap="RdBu_r",
    rows=None,
    columns=None,
    vmax=None,
    vmin=None,
    norm=None,
    annotate=True,
    colorbar=True,
    xlabel=None,
    ylabel=None,
    ax=None,
    cax=None,
):
    df = df.T.round(2)
    if rows is None:
        rows = df.index
    if columns is None:
        columns = df.columns
    fig, ax, hm = _heatmap_from_dataframe(
        df=df.loc[rows, columns],
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        annotate=annotate,
        colorbar=colorbar,
        cmap=cmap,
        norm=norm,
        vmax=vmax,
        vmin=vmin,
        ax=ax,
        cax=cax,
    )
    ax.set_xticklabels(ax.get_xticklabels(), **{"rotation": 45, "ha": "right"})
    return fig, ax, hm


def plot_multiple(dfs, titles, cmap="RdBu_r", annotate=True, colorbar=True, figsize=None):
    vmin = min(i.values.min() for i in dfs)
    vmax = max(i.values.max() for i in dfs)

    n_cols = 2
    n_rows = math.ceil(len(dfs) / n_cols)

    norm = _get_norm(vmin=vmin, vmax=vmax)

    if figsize is None:
        figsize = (n_cols * 4, n_rows * 4)

    fig, axs = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=figsize)
    for ax, df, title in zip(axs.ravel(), dfs, titles):
        plot_coefficient_heatmap(
            df=df,
            title=title,
            cmap=cmap,
            annotate=annotate,
            colorbar=False,
            norm=norm,
            ax=ax,
        )

    # Add a colorbar+
    if colorbar:
        cb = fig.colorbar(
            cm.ScalarMappable(norm=norm, cmap=cmap),
            ax=axs.ravel()[-1],
        )
        cb.outline.set_linewidth(0)
    fig.tight_layout()
    return fig, axs


def plot_concentration_response_coefficients(
    model,
    parameters,
    y,
    t=0,
    normalized=True,
    displacement=_DISPLACEMENT,
    cmap="RdBu_r",
    rows=None,
    columns=None,
    vmax=None,
    vmin=None,
    annotate=True,
    colorbar=True,
    xlabel=None,
    ylabel=None,
    ax=None,
    cax=None,
):
    """Plot response of the steady state concentration to a change of the given parameters.

    Parameters
    ----------
    m: modelbase.ode.Model
    parameters: iterable(str)
    y: Union(dict(str: num), iterable(num))
    t: Union(num, iterable(num))
    normalized : bool
    displacement : float
        Percentage change of the value

    Returns
    -------
    fig : matplotlib figure
    ax : matplotlib axes
    hm : matplotlib heatmap
    """
    df = get_concentration_response_coefficients_df(
        model=model,
        parameters=parameters,
        y=y,
        t=t,
        normalized=normalized,
        displacement=displacement,
    )
    return plot_coefficient_heatmap(
        df=df,
        title="Concentration Response Coefficients",
        rows=rows,
        columns=columns,
        xlabel=xlabel,
        ylabel=ylabel,
        annotate=annotate,
        colorbar=colorbar,
        cmap=cmap,
        vmax=vmax,
        vmin=vmin,
        ax=ax,
        cax=cax,
    )


def plot_flux_response_coefficients(
    model,
    parameters,
    y,
    t=0,
    normalized=True,
    displacement=_DISPLACEMENT,
    cmap="RdBu_r",
    rows=None,
    columns=None,
    vmax=None,
    vmin=None,
    annotate=True,
    colorbar=True,
    xlabel=None,
    ylabel=None,
    ax=None,
    cax=None,
):
    """Plot response of the steady state fluxes to a change of the given parameters.

    Parameters
    ----------
    m: modelbase.ode.Model
    parameters: iterable(str)
    y: Union(dict(str: num), iterable(num))
    t: Union(num, iterable(num))
    normalized : bool
    displacement : float
        Percentage change of the value

    Returns
    -------
    fig : matplotlib figure
    ax : matplotlib axes
    hm : matplotlib heatmap
    """
    df = get_flux_response_coefficients_df(
        model=model,
        parameters=parameters,
        y=y,
        t=t,
        normalized=normalized,
        displacement=displacement,
    )
    return plot_coefficient_heatmap(
        df=df,
        title="Flux Response Coefficients",
        rows=rows,
        columns=columns,
        xlabel=xlabel,
        ylabel=ylabel,
        annotate=annotate,
        colorbar=colorbar,
        cmap=cmap,
        vmax=vmax,
        vmin=vmin,
        ax=ax,
        cax=cax,
    )
