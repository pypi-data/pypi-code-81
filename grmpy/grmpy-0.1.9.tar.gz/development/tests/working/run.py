"""This module contains a monte carlo example that illustrates the advantages of the grmpy estima-
tion strategy. For this purpose data and the associated parameterization from Cainero 2011 are
used. Additionally the module creates two different figures for the reliability section of the
documentation.
"""
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
import numpy as np
import json

from linearmodels.iv import IV2SLS
from grmpy.simulate.simulate_auxiliary import simulate_unobservables
from grmpy.test.random_init import print_dict
from grmpy.simulate.simulate import simulate
from grmpy.estimate.estimate import fit
from grmpy.read.read import read


def create_data(file):
    """This function creates the a data set based on the results from Caineiro 2011."""
    # Read in initialization file and the data set
    init_dict = read(file)
    df = pd.read_pickle(init_dict['SIMULATION']['source'] + '.grmpy.pkl')

    # Distribute information
    indicator, dep = init_dict['ESTIMATION']['indicator'], init_dict['ESTIMATION']['dependent']
    label_out = [init_dict['varnames'][j - 1] for j in init_dict['TREATED']['order']]
    label_choice = [init_dict['varnames'][j - 1] for j in init_dict['CHOICE']['order']]
    seed = init_dict['SIMULATION']['seed']

    # Set random seed to ensure recomputabiltiy
    np.random.seed(seed)

    # Simulate unobservables
    U, V = simulate_unobservables(init_dict)

    print(len(U[:, 0]))

    df['U1'], df['U0'], df['V'] = U[:, 0], U[:, 1], V

    # Simulate choice and output
    df[dep + '1'] = np.dot(df[label_out], init_dict['TREATED']['all']) + df['U1']
    df[dep + '0'] = np.dot(df[label_out], init_dict['UNTREATED']['all']) + df['U0']
    df[indicator] = np.array(
        np.dot(df[label_choice], init_dict['CHOICE']['all']) - df['V'] > 0).astype(int)
    df[dep] = df[indicator] * df[dep + '1'] + (1 - df[indicator]) * df[dep + '0']

    # Save the data
    df.to_pickle(init_dict['SIMULATION']['source'] + '.grmpy.pkl')

    return df


def update_correlation_structure(model_dict, rho):
    """This function takes a valid model specification and updates the correlation structure
    among the unobservables."""

    # We first extract the baseline information from the model dictionary.
    sd_v = model_dict['DIST']['all'][-1]
    sd_u1 = model_dict['DIST']['all'][0]

    # Now we construct the implied covariance, which is relevant for the initialization file.
    cov1v =  rho * sd_v * sd_u1

    model_dict['DIST']['all'][2] = cov1v

    # We print out the specification to an initialization file with the name mc_init.grmpy.ini.
    for key_ in ['TREATED', 'UNTREATED', 'CHOICE']:
        x = [model_dict['varnames'][j - 1] for j in model_dict[key_]['order']]
        model_dict[key_]['order'] = x
    print_dict(model_dict, 'mc')


def get_effect_grmpy(file):
    """This function simply returns the ATE of the data set."""
    dict_ = read('test.grmpy.ini')
    df = pd.read_pickle('mc.grmpy.pkl')
    beta_diff = dict_['TREATED']['all'] - dict_['UNTREATED']['all']
    covars = [dict_['varnames'][j - 1] for j in dict_['TREATED']['order']]
    ATE = np.dot(np.mean(df[covars]), beta_diff)

    return ATE


def monte_carlo(file, grid_points):
    """This function estimates the ATE for a sample with different correlation structures between U1
     and V. Two different strategies for (OLS,LATE) are implemented.
     """

    # Define a dictionary with a key for each estimation strategy
    effects = {}
    for key_ in ['grmpy', 'ols', 'true', 'random', 'rho', 'iv', 'means']:
        effects[key_] = []

    # Loop over different correlations between V and U_1
    for rho in np.linspace(0.00, 0.99, grid_points):
        effects['rho'] += [rho]
        # Readjust the initialization file values to add correlation
        model_spec = read(file)
        X = [model_spec['varnames'][j - 1] for j in model_spec['TREATED']['order']]
        update_correlation_structure(model_spec, rho)
        model_spec = read('mc.grmpy.ini')

        # Simulate a Data set and specify exogeneous and endogeneous variables
        df_mc = create_data('mc.grmpy.ini')
        endog, exog, exog_ols = df_mc['wage'], df_mc[X], df_mc[['state'] + X]

        instr = [model_spec['varnames'][j - 1] for j in model_spec['CHOICE']['order']]
        instr = [i for i in instr if i != 'const']
        # Calculate true average treatment effect
        ATE = np.mean(df_mc['wage1'] - df_mc['wage0'])
        effects['true'] += [ATE]

        # Estimate  via grmpy
        rslt = fit('test.grmpy.ini')
        beta_diff = rslt['TREATED']['all'] - rslt['UNTREATED']['all']
        stat = np.dot(np.mean(exog), beta_diff)

        effects['grmpy'] += [stat]

        # Estimate via OLS
        ols = sm.OLS(endog, exog_ols).fit()
        stat = ols.params[0]
        effects['ols'] += [stat]

        # Estimate via 2SLS
        iv = IV2SLS(endog, exog, df_mc['state'], df_mc[instr]).fit()
        stat = iv.params['state']
        effects['iv'] += [stat]

        # Estimate via random
        random = np.mean(df_mc[df_mc.state==1]['wage']) - np.mean(df_mc[df_mc.state==0]['wage'])
        stat = random
        effects['random'] += [stat]

        # outcomes
        stat = [[np.mean(df_mc[df_mc.state==1]['wage']),df_mc[df_mc.state==1].shape[0]],[np.mean(df_mc[df_mc.state==0]['wage']),df_mc[df_mc.state==0].shape[0]]]
        effects['means'] += stat

        print(effects)

    return effects


def create_plots(effects, true):
    """The function creates the figures that illustrates the behavior of each estimator of the ATE
    when the correlation structure changes from 0 to 1."""

    fig, ax = plt.subplots(2, 2,figsize=(10,10))

    grid = np.linspace(0.00, 0.99, len(effects['ols']))

    fig.suptitle("Monte Carlo Results", fontsize=16)


    # Determine the title for each strategy plot
    for plot_num1 in [0,1]:
        for plot_num2 in [0, 1]:
            plot_num = [plot_num1, plot_num2]

            true_ = np.tile(true, len(effects['ols']))

            l1, = ax[plot_num1, plot_num2].plot(grid, true_, label="True")
            ax[plot_num1, plot_num2].set_xlim(0, 1)
            ax[plot_num1, plot_num2].set_ylim(0.35, 0.6)
            ax[plot_num1, plot_num2].set_ylabel(r"$B^{ATE}$")
            ax[plot_num1, plot_num2].set_xlabel(r"$\rho_{U_1, V}$")

            ax[plot_num1, plot_num2].yaxis.get_major_ticks()[0].set_visible(False)


            if plot_num == [0, 0]:
                color = 'orange'
                strategy = 'random'
                label = '$E[Y|D=1] - E[Y|D=0]$'
                title = 'Naive comparison'
                l2, = ax[plot_num1, plot_num2].plot(grid, effects[strategy], label=title,
                                                    color=color)

            elif plot_num == [0, 1]:
                color = 'orange'
                label = 'OLS'
                strategy = 'ols'
                title = 'Ordinary Least Squares'
                l2, = ax[plot_num1, plot_num2].plot(grid, effects[strategy], label=title,
                                                    color=color)

            elif plot_num == [1, 0]:
                color = 'orange'
                strategy = 'iv'
                label = 'IV'
                title = 'Instrumental Variables'
                l2, = ax[plot_num1, plot_num2].plot(grid, effects[strategy], label=title,
                                                    color=color)

            elif plot_num == [1, 1]:
                color = 'orange'
                strategy = 'grmpy'
                label = 'grmpy'
                title = 'grmpy'
                l2, = ax[plot_num1, plot_num2].plot(grid, effects[strategy], label=title,
                                                    color=color)
            ax[plot_num1, plot_num2].title.set_text(title)

            ax[plot_num1, plot_num2].legend([l1, l2], ['True', '{}'.format(label)], prop={'size': 8})
    file_name = 'average-effect-estimation.png'.format(strategy)
    plt.savefig(file_name)


if __name__ == '__main__':
    simulate('test.grmpy.ini')

    ATE = get_effect_grmpy('test.grmpy.ini')

    x = monte_carlo('test.grmpy.ini', 10)
    create_plots(x, ATE)


