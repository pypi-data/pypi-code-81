import numpy as np
import pandas as pd
import logging
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import beta


def qqplot(gwas_res_file, p_colname, CI=True, out_file='QQ.png'):
    """
    Q-Q plot from the GWAS results
    :param gwas_res_file: the result file of GWAS
    :param p_colname: the column name of p values
    :param CI: Whether to draw the confidence interval. Default is True.
    :param out_file: the output file. Default is QQ.png
    :return: 0
    """
    df = pd.read_csv(gwas_res_file, header=0, sep='\s+')
    p_obs = np.sort(df[p_colname])
    p_obs = p_obs[~np.isnan(p_obs)]
    arr = np.arange(1, len(p_obs) + 1)
    p_exp = (arr-0.5)/len(arr)
    logging.info("The median of p values is: {}".format(np.median(p_obs)))
    plt.figure(figsize=(3.5, 3.5), dpi=600)
    plt.rc('font', family='Times New Roman')
    plt.xlabel('Expected -log10($P$)', fontsize=10)
    plt.ylabel('Observed -log10($P$)', fontsize=10)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    if CI:
        p_up = beta.ppf(0.025, arr, arr[::-1])
        p_low = beta.ppf(0.975, arr, arr[::-1])
        plt.fill_between(-np.log10(p_exp), -np.log10(p_up), -np.log10(p_low), color='grey')
    plt.scatter(-np.log10(p_exp), -np.log10(p_obs), s=1.5, c='red')
    plt.plot(-np.log10(p_exp), -np.log10(p_exp), 'k')
    plt.savefig(out_file)
    return 0
