import numpy as np
import pandas as pd
import logging
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import beta
from tqdm import tqdm
import logging


def manplot(gwas_res_file, chro, pos, p, color_vec=("gray", "dimgray"), sig_color='red',
            threshold=1.0e-7, logp=True, out_file='man.png'):
    """
    Draw the Manhattan plot from GWAS result file.
    :param gwas_res_file: the GWAS result file with header
    :param chro: the column name for chromosome
    :param pos: the column name for position
    :param p: the column name for P values
    :param color_vec: color for different chromosomes.
    :param sig_color: the color for point pass the threshold. Default is 'red'.
    :param threshold: the threshold value. Default is 1.0e-7.
    :param logp: Whether to log transform the p values. Default is True.
    :param out_file: the output file. Default is "man.png".
    :return:
    """
    p_dct = {}
    pos_dct = {}
    chro_vec = []
    with open(gwas_res_file) as fin:
        head_line = fin.readline()
        arr = head_line.split()
        chro_ind = arr.index(chro)
        pos_ind = arr.index(pos)
        p_ind = arr.index(p)
        line_num = 0
        for line in fin:
            line_num += 1
            arr = line.split()
            try:
                pi = float(arr[p_ind])
            except Exception as e:
                del e
                logging.info('The p value in Line {} is not numerical.'.format(line_num))
                continue
            try:
                posi = float(arr[pos_ind])
            except Exception as e:
                del e
                logging.info('The position value in Line {} is not numerical.'.format(line_num))
                continue
            chroi = arr[chro_ind]
            if chroi not in chro_vec:
                chro_vec.append(chroi)
            try:
                p_dct[chroi].append(pi)
            except Exception as e:
                del e
                p_dct[chroi] = [pi]
            try:
                pos_dct[chroi].append(posi)
            except Exception as e:
                del e
                pos_dct[chroi] = [posi]
    plt.figure(figsize=(10, 3.5), dpi=600)
    plt.rc('font', family='Times New Roman', size=10)
    pos_accum = [0.0]
    xtick_vec = []
    for i in range(len(chro_vec)):
        posx = np.array(pos_dct[chro_vec[i]]) + pos_accum[-1]
        if logp:
            pvaly = -np.log10(p_dct[chro_vec[i]])
            threshold_line = -np.log10(threshold)
        else:
            pvaly = np.array(p_dct[chro_vec[i]])
            threshold_line = threshold
        plt.scatter(posx, pvaly, s=1.5, c=color_vec[i%len(color_vec)])
        p_line = np.array([threshold_line] * len(posx))
        plt.plot(posx, p_line, 'b')
        posx_sig = posx[pvaly > threshold_line]
        pvaly_sig = pvaly[pvaly > threshold_line]
        plt.scatter(posx_sig, pvaly_sig, s=1.5, c=sig_color)
        pos_accum.append(pos_accum[-1] + np.max(pos_dct[chro_vec[i]]))
        xtick_vec.append((pos_accum[-1] + pos_accum[-2])/2)
    plt.xticks(xtick_vec, chro_vec, fontsize=7)
    plt.savefig(out_file)
    return 0
