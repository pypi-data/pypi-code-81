#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from __future__ import print_function
import os
import numpy as np
import pandas as pd
from matplotlib.pylab import plt #load plot library
from matplotlib import rc
import seaborn as sns
from natf.natf_functions import *
from natf import utils

# set color and markers
sns.set_palette(sns.color_palette("hls", 10))
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']
markers = ['o', 's', 'v', '^', 'P', '*', 'X', 'd', 'x', 'D', 'H']

def get_labels(items, filename=None):
    """
    Get the labesl for all the parts.
    """
    if filename is not None and items == ['All']:
        # part with multiple nuc 'All'
        df = pd.read_csv(filename)
        items = list(df.columns)[1:]
    labels = []
    for i, p in enumerate(items):
        if p == 'CP':
            labels.append('CP')
        elif p in ['']:
            labels.append('PFC')
        elif p in ['Divertor_W_layer']:
            labels.append('Divertor W layer')
        elif p == 'Divertor_structure':
            labels.append("Divertor structure using SS316")
        elif p == 'Divertor_structure_eurofer':
            labels.append("Divertor structure using Eurofer")
        elif p == 'FirstWall':
            labels.append('FW')
        elif p == 'Be_U_0':
            labels.append('Be w/o U')
        else:
            labels.append(p)
    return labels

#def bz_change_to_ext(item):
#    """
#    Change the key or nuc to ext for BZ.
#    """
#    bz_convert_map = {'acts_max': 'act_ext_max',
#            'acts_max_ratio': 'acts_ext_max_ratio',
#            'ci_max': 'ci_ext_max',
#            'ci_max_ratio': 'ci_ext_max_ratio',
#            'dhv_max': 'dhv_ext_max',
#            'dhv_max_ratio': 'dhv_ext_max_ratio',
#            'act_st_t': 'act_st_t',
#            'dh_vt_t': 'dh_vt_t',
#            'total_specific_act(Bq/kg)': 'total_specific_act_ext(Bq/kg)',
#            'total_activity(Bq)': 'total_activity_ext(Bq)',
#            'total_decay_heat_vol(kW/m3)': 'total_decay_heat_ext_vol(kW/m3)',
#            'total_decay_heat(kW)': 'total_decay_heat(kW)'}
#    if item in bz_convert_map.keys():
#        return bz_convert_map[item]
#    else:
#        raise ValueError("item: {0} not in the convert map".format(item))
#
def get_filename(part, key, work_dir=None):
    """
    Get the filename for specific part and key.
    Eg. Get the act of A -> A.act
    """
    filename = os.path.join(work_dir, part, part + '.' + key)
    return filename

def get_value(filename, nucs=None, item=None):
    """
    Get the value for specific file.
    """
    df = pd.read_csv(filename)
    if nucs == ['All']:
        nucs = list(df.columns)[1:]
    if item is not None:
        # return specific item but not all
        idx = list(df['Nuclide']).index(item)
        value = np.array(df[nucs]).flatten()[idx]
    else:
        value = df[nucs]
    return value

def get_cooling_times(filename):
    "Get the cooling time."
    df = pd.read_csv(filename)
    value = df['Cooling_time(s)']
    return value

def get_values(parts, key, item=None, nucs=None, work_dir=None):
    """
    Get the value of parts for given key.
    The key could be 'act', 'acts', 'ci', ...

    Parameters:
    nucs: list
        If nucs is ['Total'], then get total value.
        If nucs is a list of specific nuc, then them.
        if nucs is ['all'], then get all the nucs
    """
    if len(parts) > 1 and len(nucs) > 1:
        raise ValueError("Multiple nucs and multiple parts mode is not supported")
    values = []
    cooling_times = []
    for i, p in enumerate(parts):
        filename = get_filename(p, key, work_dir=work_dir)
        value = get_value(filename, nucs=nucs, item=item)
        if item is None:
            if i == 0:
                cooling_times = get_cooling_times(filename)
        values.append(value)
    return values, cooling_times

def plot_example():
    """
    Example.
    """
    # create figure
    fig, ax = plt.subplots(figsize=(8,6))
    # example data
    a = np.arange(1,5)
    b = a**2
    c = a**3
    ax.plot(a, b)
    ax.plot(a, c)
    ax.legend()
    # show figure
    # save figure
    fig.savefig(fname="example.png",dpi=300)

def get_ylabel(key):
    """
    Set ylabel according to key.
    """
    if key in ['act']:
        return 'Total activity (Bq)'
    if key in ['act_st_t']:
        return 'Specific activity (Bq/kg)'
    if key in ['cdt']:
        return 'Contact dose rate (Sv/h)'

def plot_parts(parts, key=None, nucs=None, work_dir=None,
        figname='example.png', dpi=600, figtitle=None,
        xlabel='Time after shutdown (a)', ylabel=None):
    """
    Plot specific act of given parts.
    """
    # label and value
    labels = get_labels(parts)
    if ylabel is None:
        ylabel = get_ylabel(key)
    values, cooling_times = get_values(parts, key=key, nucs=nucs, work_dir=work_dir)
    # convert time from sec to year.
    for i, ct in enumerate(cooling_times):
        cooling_times[i] = utils.time_sec_to_unit(ct, 'a')
    # plots parts
    fig, ax = plt.subplots()
    for i, p in enumerate(parts):
        ax.plot(cooling_times, values[i], label=labels[i], color=colors[i], marker=markers[i])
    ax.legend()
    # style difinition
    rc('text', usetex=True)
    rc('font', family='serif')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel(xlabel=xlabel, fontsize='x-large')
    ax.set_ylabel(ylabel=ylabel, fontsize='x-large')
    ax.tick_params(axis='both', tick1On=True, tick2On=True)
    ax.grid(which='major', axis='both')
    # save file
    fig.savefig(fname=figname, dpi=dpi)

def plot_wap_distribute(parts, key=None, nucs=None, work_dir=None,
        figname='example.png', dpi=600, figtitle=None,
        xlabel='Distance from BLK to PHTS components (m)', ylabel=r'Sepcific Activity (Bq/kg$_{H2O}$)',
        x_values=None):
    """
    Plot specific activity of given nuclide in PHTS.
    """
    # label and value
    labels = get_labels(parts)
#    if ylabel is None:
#        ylabel = get_ylabel(key)
#    # convert time from sec to year.
#    for i, ct in enumerate(cooling_times):
#        cooling_times[i] = utils.time_sec_to_unit(ct, 'a')
    # plots parts
    fig, ax = plt.subplots()
    if x_values is None:
        x_values = range(0, len(parts))
    for i, nuc in enumerate(nucs):
        values, cooling_times = get_values(parts, key=key, nucs=[nucs[i]], work_dir=work_dir, item='Specific act (Bq/kg)')
        ax.plot(x_values, values, label=nuc, color=colors[i], marker=markers[i])
    ax.legend()
    # style difinition
    rc('text', usetex=True)
    rc('font', family='serif')
    ax.set_xlim([20, 200])
    ax.set_xscale('linear')
    ax.set_yscale('log')
    ax.set_xlabel(xlabel=xlabel, fontsize='x-large')
    ax.set_ylabel(ylabel=ylabel, fontsize='x-large')
    ax.tick_params(axis='both', tick1On=True, tick2On=True)
    ax.grid(which='major', axis='both')
    ax.set_xticks(x_values)
#    ax.set_xticklabels(x_values)
    ax.set_xticklabels(parts, rotation = 75)
#    secax = ax.secondary_xaxis('top')
#    secax.set_xtiks(x_values)
#    secax.set_xticklabels(x_values) 
    ax2=ax.twiny()
    ax2.set_xlim([20, 200])
    ax2.set_xticks(x_values)
    ax2.set_xticklabels(x_values, rotation=75)
    plt.tight_layout()
    # save file
    fig.savefig(fname=figname, dpi=dpi)

def plot_wap_power_cmp(powers, cs, parts, key=None, nucs=None, work_dir=None,
        figname='example.png', dpi=600, figtitle=None,
        xlabel='Distance from BLK to PHTS components (m)', ylabel=r'Sepcific Activity (Bq/kg$_{H2O}$)',
        x_values=None):
    """
    Plot specific activity of given nuclide in PHTS.
    Only one nuc is allowed.
    """
    # label and value
    labels = get_labels(parts)
    # plots parts
    fig, ax = plt.subplots()
    if x_values is None:
        x_values = range(0, len(parts))
    for i, power in enumerate(powers):
        folder_name = os.path.join(work_dir, 'natf_coolant_' + cs + '_' + power)
        values, cooling_times = get_values(parts, key=key, nucs=nucs, work_dir=folder_name, item='Specific act (Bq/kg)')
        ax.plot(x_values, values, label=power, color=colors[i], marker=markers[i])
    ax.legend()
    # style difinition
    rc('text', usetex=True)
    rc('font', family='serif')
    ax.set_xlim([20, 200])
    ax.set_xscale('linear')
    ax.set_yscale('log')
    ax.set_xlabel(xlabel=xlabel, fontsize='x-large')
    ax.set_ylabel(ylabel=ylabel, fontsize='x-large')
    ax.tick_params(axis='both', tick1On=True, tick2On=True)
    ax.grid(which='major', axis='both')
    ax.set_xticks(x_values)
#    ax.set_xticklabels(x_values)
    ax.set_xticklabels(parts, rotation = 75)
#    secax = ax.secondary_xaxis('top')
#    secax.set_xtiks(x_values)
#    secax.set_xticklabels(x_values) 
    ax2=ax.twiny()
    ax2.set_xlim([20, 200])
    ax2.set_xticks(x_values)
    ax2.set_xticklabels(x_values, rotation=75)
    plt.tight_layout()
    # save file
    fig.savefig(fname=figname, dpi=dpi)


def plot_nucs(parts, key, nucs, labels=None, work_dir=None,
        figname='example.png', dpi=600, figtitle=None,
        xlabel='Time after shutdown (a)', ylabel=None, yscale='log'):
    """
    Plot the different nucs or item in the same part.
    """
    filename = get_filename(part=parts[0], key=key, work_dir=work_dir)
    # label and value
    if labels is None:
        labels = get_labels(nucs, filename=filename)
    if ylabel is None:
        ylabel = get_ylabel(key)
    values, cooling_times = get_values(parts, key=key, nucs=nucs, work_dir=work_dir)
    # convert time from sec to year.
    for i, ct in enumerate(cooling_times):
        cooling_times[i] = utils.time_sec_to_unit(ct, 'a')
    # plots parts
    ratio_fix = 0
    if 'ratio' in key:
        ratio_fix = 1
    fig, ax = plt.subplots()
    for i, item in enumerate(labels):
        ax.plot(cooling_times, values[0][item], label=labels[i], color=colors[i+ratio_fix], marker=markers[i+ratio_fix])
    ax.legend()
    # style difinition
    rc('text', usetex=True)
    rc('font', family='serif')
    ax.set_xscale('log')
    ax.set_yscale(yscale)
    ax.set_xlabel(xlabel=xlabel, fontsize='x-large')
    ax.set_ylabel(ylabel=ylabel, fontsize='x-large')
    ax.tick_params(axis='both', tick1On=True, tick2On=True)
    ax.grid(which='major', axis='both')
    # save file
    fig.savefig(fname=figname, dpi=dpi)
    plt.close()

def get_part_mass(part, work_dir=None):
    """
    Get part mass from part name.
    """
    key = 'basicinfo'
    filename = get_filename(part, key, work_dir=work_dir)
    df = pd.read_csv(filename)
    mass_info = np.array(df.loc[df[part] == 'mass(g)']).flatten()
    return float(mass_info[1])

def get_part_vol(part, work_dir=None):
    """
    Get part volume from part name.
    """
    key = 'basicinfo'
    filename = get_filename(part, key, work_dir=work_dir)
    df = pd.read_csv(filename)
    vol_info = np.array(df.loc[df[part] == 'volume(cm3)']).flatten()
    return float(vol_info[1])

def write_part_basicinfo(parts, work_dir=None, ofname='cfetr_parts_vol_mass.csv'):
    """
    Write part basic information as a csv table.
    """
    vols = [0.0]*len(parts)
    masses = [0.0]*len(parts)
    for i, p in enumerate(parts):
        vols[i] = get_part_vol(p, work_dir=work_dir)
        masses[i] = get_part_mass(p, work_dir=work_dir)
    # save the ctrs into csv
    fo = open(ofname, 'w')
    title_line = utils.data_to_line_1d(key='Components', value=['Volumes (m3)', 'Masses (ton)'])
    fo.write(title_line)
    for i, p in enumerate(parts):
        line = utils.data_to_line_1d(key=p, value=[vols[i]/1e6, masses[i]/1e6], decimals=1)
        fo.write(line)
    fo.close()

def calc_rwcs_masses(parts, key, cooling_time_s, work_dir=None):
    """
    Calcualte the mass of HLW, ILW and LLW.
    """
    rwc_dict = {'Clearance':0, 'VLLW':0, 'LLW':1, 
                'LLWC':1, 'LLWB':1, 'LLWA':1,
                'ILW':2, 'HLW':3}
    masses = np.array([0.0, 0.0, 0.0, 0.0])
    for i, p in enumerate(parts):
        filename = get_filename(p, key, work_dir=work_dir)
        rwc = get_rwc(filename, cooling_time_s=cooling_time_s) 
        masses[rwc_dict[rwc]] += get_part_mass(p, work_dir=work_dir)
    return masses

def plot_rwcs_compare(parts, keys=['rwc_chn2018', 'rwc_usnrc', 'rwc_usnrc_fetter', 'rwc_uk'],
        cooling_time_s='1 s', work_dir=None, ofname='rwc_compare_1s.png'):
    """
    Plot the compare result of different radwaste standards.

    Parameters:
    -----------
    parts: list
        List of part names.
    keys: list
        List of keys. Eg. ['rwc_chn2018', 'rwc_usnrc']
    cooling_time: string
        The cooling time to plot.
    work_dir: string
        The working directory.
    ofname: string
        Output figure name.
    """
    rwcs_masses = np.zeros(shape=(len(keys), 4), dtype=float)
    for i, key in enumerate(keys):
        # get mass of Clearance/VLLW, LLW, ILW and HLW
        rwcs_masses[i][:] = calc_rwcs_masses(parts, key, cooling_time_s, work_dir=work_dir)
    # convert to unit t
    rwcs_masses = np.divide(rwcs_masses, 1.0e6)
    # plot
    labels = ['VLLW', 'LLW', 'ILW', 'HLW']
    x = np.arange(len(labels)) * 2
    witdh = 0.35
    fig, ax = plt.subplots()
    rects0 = ax.bar(x - 1.5 * witdh, rwcs_masses[:][0], witdh, label='CHN2018', color=colors[0], hatch='//')
    rects1 = ax.bar(x - 0.5 * witdh, rwcs_masses[:][1], witdh, label='USNRC', color=colors[1], hatch='--')
    rects2 = ax.bar(x + 0.5 * witdh, rwcs_masses[:][2], witdh, label='USNRC_FETTER', color=colors[2], hatch='xx')
    rects3 = ax.bar(x + 1.5 * witdh, rwcs_masses[:][3], witdh, label='UK', color=colors[3], hatch='++')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Mass (t)')
    ax.set_xlabel('Radioactive levels')
#    ax.set_title('')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(loc='best')

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(round(height, 1)),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', size=5)
    
    autolabel(rects0)
    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    fig.tight_layout()
    fig.savefig(fname=ofname,dpi=600)
    
def calc_rwc_cooling_requirement(parts, key, classes, standard='CHN2018', work_dir=None, out_unit='a', ofname=None):
    """
    Calculate the cooling time requirement for specific classes.
    """
    ctrs = []
    for i, p in enumerate(parts):
        filename = get_filename(p, key, work_dir)
        cooling_times = get_cooling_times(filename)
        rwcs = list(get_value(filename, nucs='Radwaste_Class'))
        ctr = utils.calc_ctr(cooling_times, rwcs, classes, out_unit=out_unit, standard=standard)
        ctrs.append(ctr)
    # save the ctrs into csv
    fo = open(ofname, 'w')
    title_line = utils.data_to_line_1d(key='Components', value=list(c + ' (' +out_unit+')' for c in classes))
    fo.write(title_line)
    for i, p in enumerate(parts):
        line = utils.data_to_line_1d(key=p, value=ctrs[i])
        fo.write(line)
    fo.close()


def get_rwc(filename, cooling_time_s=None, cooling_time=None):
    """
    Get the rwc from specific filename and cooling time.
    """
    if cooling_time_s is not None and cooling_time is not None:
        raise ValueError("only one cooling time input is supported")
    if cooling_time_s is not None:
        tokens = cooling_time_s.strip().split()
        value = tokens[0]
        unit = tokens[1]
        ct = utils.cooling_time_sec(value, unit)
    if cooling_time is not None:
        ct = cooling_time
    df = pd.read_csv(filename)
    cooling_times = np.array(df['Cooling_time(s)']).flatten()
    index = utils.get_ct_index(ct, cooling_times)
    rwc = np.array(df['Radwaste_Class']).flatten()[index]
    return rwc


def get_rwcs_by_cooling_times(parts, cooling_times_s=['1 s', '1 a', '10 a', '100 a'],
        key='rwc_chn2018', work_dir=None, ofname='cfetr_all_rwc_chn2018.csv'):
    """
    Get the radwaste classification of different cooling times.

    Parameters:
    -----------
    parts: list of string
        List of part names.
    cooling_times: list of string
        List of cooling times.
    standard: string
        Standard name. Supported standards: 'CHN2018', 'USNRC', 'USNRC_FETTER', 'UK'
    work_dir: string
        Working directory.
    ofname: string
        Output csv file name.
    """
    
    cooling_times = [0.0] * len(cooling_times_s)
    # convert cooling_times from string to float
    for i, ct in enumerate(cooling_times_s):
        tokens = ct.strip().split()
        value = tokens[0]
        unit = tokens[1]
        cooling_times[i] = utils.cooling_time_sec(value, unit)

    rwcs = np.array([['']*len(cooling_times)]*len(parts), dtype='<U8')
    for i, p in enumerate(parts):
        filename = get_filename(p, key, work_dir=work_dir)
        df = pd.read_csv(filename)
        cts = np.array(df['Cooling_time(s)']).flatten()
        for j, ct in enumerate(cooling_times):
            rwc = get_rwc(filename, cooling_time = ct)
            rwcs[i][j] = rwc

    # save the rwcs into csv
    fo = open(ofname, 'w')
    title_line = utils.data_to_line_1d(key='Components', value=cooling_times_s)
    fo.write(title_line)
    for i, p in enumerate(parts):
        line = utils.data_to_line_1d(key=p, value=rwcs[i])
        fo.write(line)
    fo.close()

if __name__ == "__main__":
#    plot_example()
#    work_dir = '/media/zxk/ZXK_SAMSUNG/ComputeData/CFETR2019/WaterActivation/natf_coolant_cs2_1500MW'
    work_dir = '/media/zxk/ZXK_SAMSUNG/ComputeData/200MW_WCCB_Update/UpdateActivation/combined_results'
#    # basic info, vol and mass
#    write_part_basicinfo(parts=['PFC', 'FW', 'Be', 'BZ', 'BP', 'CP', 'rpSP', 'SW', 'Divertor_W_layer', 'Divertor_structure', 'Shield'], work_dir=work_dir, ofname='cfetr_parts_vol_mass.csv')
#    # -------------- main components ------------------------------
#    plot_parts(parts=['BLK', 'Divertor', 'Shield'], key='act_st_t', nucs=['total_specific_act(Bq/kg)'], work_dir=work_dir, figname='main_components_act_st_t.png', ylabel=r'Specific activity (Bq/kg)')
#    plot_parts(parts=['BLK', 'Divertor', 'Shield'], key='act_st_t', nucs=['total_activity(Bq)'], work_dir=work_dir, figname='main_components_act_t.png', ylabel=r'Total activity (Bq)')
#    plot_parts(parts=['BLK', 'Divertor', 'Shield'], key='rwc_chn2018', nucs=['Decay_heat(kW/m3)'], work_dir=work_dir, figname='main_components_dhv.png', ylabel=r'Decay heat density (kW/m$^3$)')
#    plot_parts(parts=['BLK', 'Divertor', 'Shield'], key='cdt', nucs=['total_contact_dose(Sv/hr)'], work_dir=work_dir, figname='main_components_cdt.png', ylabel=r'Contact dose rate (Sv/h)')
#   # --------------- blanket, total--------------------------------------
#    plot_parts(parts=['BLK', 'PFC', 'FW', 'Be', 'BZ', 'CP', 'BP', 'Cover', 'SW', 'rpSP'], key='act_st_t', nucs=['total_specific_act(Bq/kg)'], work_dir=work_dir, figname='blanket_comp_act_st_t.png')
#    plot_parts(parts=['BLK', 'PFC', 'FW', 'Be', 'BZ', 'CP', 'BP', 'Cover', 'SW', 'rpSP'], key='act_st_t', nucs=['total_activity(Bq)'], work_dir=work_dir, figname='blanket_comp_act_t.png', ylabel='Total activity (Bq)')
#    plot_parts(parts=['BLK', 'PFC', 'FW', 'Be', 'BZ', 'CP', 'BP', 'Cover', 'SW', 'rpSP'], key='dh_vt_t', nucs=['total_decay_heat_vol(kW/m3)'], work_dir=work_dir, figname='blanket_comp_dhv.png', ylabel=r'Decay heat density (kw/m$^3$)')
#    plot_parts(parts=['BLK', 'PFC', 'FW', 'Be', 'BZ', 'CP', 'BP', 'Cover', 'SW', 'rpSP'], key='dh_vt_t', nucs=['total_decay_heat(kW)'], work_dir=work_dir, figname='blanket_comp_dht.png', ylabel='Decay heat (kW)')
#    plot_parts(parts=['BLK', 'PFC', 'FW', 'Be', 'BZ', 'CP', 'BP', 'Cover', 'SW', 'rpSP'], key='cdt', nucs=['total_contact_dose(Sv/hr)'], work_dir=work_dir, figname='blanket_comp_cdt.png', ylabel='Contact dose rate (Sv/h)')
#    plot_nucs(parts=['BLK'], key='acts_max', nucs=['All'], work_dir=work_dir, figname='blanket_acts_max.png', ylabel='Specific activity (Bq/kg)')
#    plot_nucs(parts=['BLK'], key='acts_max_ratio', nucs=['All'], work_dir=work_dir, figname='blanket_acts_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['BLK'], key='dhv_max', nucs=['All'], work_dir=work_dir, figname='blanket_dhv_max.png', ylabel=r'Decay heat density (kW/m$^{3}$)', yscale='log')
#    plot_nucs(parts=['BLK'], key='dhv_max_ratio', nucs=['All'], work_dir=work_dir, figname='blanket_dhv_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['BLK'], key='cd_max', nucs=['All'], work_dir=work_dir, figname='blanket_cd_max.png', ylabel=r'Contact dose rate (Sv/h)', yscale='log')
#    plot_nucs(parts=['BLK'], key='cd_max_ratio', nucs=['All'], work_dir=work_dir, figname='blanket_cd_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#   # --------------- blanket, PFC -----------------------------------
#    plot_nucs(parts=['PFC'], key='acts_max', nucs=['All'], work_dir=work_dir, figname='blk_pfc_acts_max.png', ylabel=r'Specific activity (Bq/kg)', yscale='log')
#    plot_nucs(parts=['PFC'], key='acts_max_ratio', nucs=['All'], work_dir=work_dir, figname='blk_pfc_acts_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['PFC'], key='dhv_max', nucs=['All'], work_dir=work_dir, figname='blk_pfc_dhv_max.png', ylabel=r'Decay heat density (kW/m$^{3}$)', yscale='log')
#    plot_nucs(parts=['PFC'], key='dhv_max_ratio', nucs=['All'], work_dir=work_dir, figname='blk_pfc_dhv_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['PFC'], key='cd_max', nucs=['All'], work_dir=work_dir, figname='blk_pfc_cd_max.png', ylabel=r'Contact dose rate (Sv/h)', yscale='log')
#    plot_nucs(parts=['PFC'], key='cd_max_ratio', nucs=['All'], work_dir=work_dir, figname='blk_pfc_cd_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#   # --------------- blanket, FW -----------------------------------
#    plot_nucs(parts=['FW'], key='acts_max', nucs=['All'], work_dir=work_dir, figname='blk_fw_acts_max.png', ylabel=r'Specific activity (Bq/kg)', yscale='log')
#    plot_nucs(parts=['FW'], key='acts_max_ratio', nucs=['All'], work_dir=work_dir, figname='blk_fw_acts_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['FW'], key='dhv_max', nucs=['All'], work_dir=work_dir, figname='blk_fw_dhv_max.png', ylabel=r'Decay heat density (kW/m$^{3}$)', yscale='log')
#    plot_nucs(parts=['FW'], key='dhv_max_ratio', nucs=['All'], work_dir=work_dir, figname='blk_fw_dhv_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['FW'], key='cd_max', nucs=['All'], work_dir=work_dir, figname='blk_fw_cd_max.png', ylabel=r'Contact dose rate (Sv/h)', yscale='log')
#    plot_nucs(parts=['FW'], key='cd_max_ratio', nucs=['All'], work_dir=work_dir, figname='blk_fw_cd_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    # --------------- blanket, Be -----------------------------------
#    plot_nucs(parts=['Be'], key='acts_max',       nucs=['All'], work_dir=work_dir, figname='blk_be_acts_max.png', ylabel=r'Specific activity (Bq/kg)', yscale='log')
#    plot_nucs(parts=['Be'], key='acts_max_ratio', nucs=['All'], work_dir=work_dir, figname='blk_be_acts_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['Be'], key='dhv_max',        nucs=['All'], work_dir=work_dir, figname='blk_be_dhv_max.png', ylabel=r'Decay heat density (kW/m$^{3}$)', yscale='log')
#    plot_nucs(parts=['Be'], key='dhv_max_ratio',  nucs=['All'], work_dir=work_dir, figname='blk_be_dhv_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['Be'], key='cd_max',         nucs=['All'], work_dir=work_dir, figname='blk_be_cd_max.png', ylabel=r'Contact dose rate (Sv/h)', yscale='log')
#    plot_nucs(parts=['Be'], key='cd_max_ratio',   nucs=['All'], work_dir=work_dir, figname='blk_be_cd_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    # --------------- blanket, BZ -----------------------------------
#    plot_nucs(parts=['BZ'], key='acts_max',       nucs=['All'], work_dir=work_dir, figname='blk_bz_acts_max.png', ylabel=r'Specific activity (Bq/kg)', yscale='log')
#    plot_nucs(parts=['BZ'], key='acts_max_ratio', nucs=['All'], work_dir=work_dir, figname='blk_bz_acts_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['BZ'], key='dhv_max',        nucs=['All'], work_dir=work_dir, figname='blk_bz_dhv_max.png', ylabel=r'Decay heat density (kW/m$^{3}$)', yscale='log')
#    plot_nucs(parts=['BZ'], key='dhv_max_ratio',  nucs=['All'], work_dir=work_dir, figname='blk_bz_dhv_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    # --------------- blanket, CP -----------------------------------
#    plot_nucs(parts=['CP'], key='acts_max',       nucs=['All'], work_dir=work_dir, figname='blk_cp_acts_max.png', ylabel=r'Specific activity (Bq/kg)', yscale='log')
#    plot_nucs(parts=['CP'], key='acts_max_ratio', nucs=['All'], work_dir=work_dir, figname='blk_cp_acts_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['CP'], key='dhv_max',        nucs=['All'], work_dir=work_dir, figname='blk_cp_dhv_max.png', ylabel=r'Decay heat density (kW/m$^{3}$)', yscale='log')
#    plot_nucs(parts=['CP'], key='dhv_max_ratio',  nucs=['All'], work_dir=work_dir, figname='blk_cp_dhv_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['CP'], key='cd_max',         nucs=['All'], work_dir=work_dir, figname='blk_cp_cd_max.png', ylabel=r'Contact dose rate (Sv/h)', yscale='log')
#    plot_nucs(parts=['CP'], key='cd_max_ratio',   nucs=['All'], work_dir=work_dir, figname='blk_cp_cd_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    # --------------- blanket, BP -----------------------------------
#    plot_nucs(parts=['BP'], key='acts_max',       nucs=['All'], work_dir=work_dir, figname='blk_bp_acts_max.png', ylabel=r'Specific activity (Bq/kg)', yscale='log')
#    plot_nucs(parts=['BP'], key='acts_max_ratio', nucs=['All'], work_dir=work_dir, figname='blk_bp_acts_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['BP'], key='dhv_max',        nucs=['All'], work_dir=work_dir, figname='blk_bp_dhv_max.png', ylabel=r'Decay heat density (kW/m$^{3}$)', yscale='log')
#    plot_nucs(parts=['BP'], key='dhv_max_ratio',  nucs=['All'], work_dir=work_dir, figname='blk_bp_dhv_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['BP'], key='cd_max',         nucs=['All'], work_dir=work_dir, figname='blk_bp_cd_max.png', ylabel=r'Contact dose rate (Sv/h)', yscale='log')
#    plot_nucs(parts=['BP'], key='cd_max_ratio',   nucs=['All'], work_dir=work_dir, figname='blk_bp_cd_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    # --------------- blanket, Cover -----------------------------------
#    plot_nucs(parts=['Cover'], key='acts_max',       nucs=['All'], work_dir=work_dir, figname='blk_cover_acts_max.png', ylabel=r'Specific activity (Bq/kg)', yscale='log')
#    plot_nucs(parts=['Cover'], key='acts_max_ratio', nucs=['All'], work_dir=work_dir, figname='blk_cover_acts_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['Cover'], key='dhv_max',        nucs=['All'], work_dir=work_dir, figname='blk_cover_dhv_max.png', ylabel=r'Decay heat density (kW/m$^{3}$)', yscale='log')
#    plot_nucs(parts=['Cover'], key='dhv_max_ratio',  nucs=['All'], work_dir=work_dir, figname='blk_cover_dhv_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['Cover'], key='cd_max',         nucs=['All'], work_dir=work_dir, figname='blk_cover_cd_max.png', ylabel=r'Contact dose rate (Sv/h)', yscale='log')
#    plot_nucs(parts=['Cover'], key='cd_max_ratio',   nucs=['All'], work_dir=work_dir, figname='blk_cover_cd_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    # --------------- blanket, SW -----------------------------------
#    plot_nucs(parts=['SW'], key='acts_max',       nucs=['All'], work_dir=work_dir, figname='blk_sw_acts_max.png', ylabel=r'Specific activity (Bq/kg)', yscale='log')
#    plot_nucs(parts=['SW'], key='acts_max_ratio', nucs=['All'], work_dir=work_dir, figname='blk_sw_acts_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['SW'], key='dhv_max',        nucs=['All'], work_dir=work_dir, figname='blk_sw_dhv_max.png', ylabel=r'Decay heat density (kW/m$^{3}$)', yscale='log')
#    plot_nucs(parts=['SW'], key='dhv_max_ratio',  nucs=['All'], work_dir=work_dir, figname='blk_sw_dhv_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['SW'], key='cd_max',         nucs=['All'], work_dir=work_dir, figname='blk_sw_cd_max.png', ylabel=r'Contact dose rate (Sv/h)', yscale='log')
#    plot_nucs(parts=['SW'], key='cd_max_ratio',   nucs=['All'], work_dir=work_dir, figname='blk_sw_cd_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    # --------------- blanket, rpSP -----------------------------------
#    plot_nucs(parts=['rpSP'], key='acts_max',       nucs=['All'], work_dir=work_dir, figname='blk_rpsp_acts_max.png', ylabel=r'Specific activity (Bq/kg)', yscale='log')
#    plot_nucs(parts=['rpSP'], key='acts_max_ratio', nucs=['All'], work_dir=work_dir, figname='blk_rpsp_acts_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['rpSP'], key='dhv_max',        nucs=['All'], work_dir=work_dir, figname='blk_rpsp_dhv_max.png', ylabel=r'Decay heat density (kW/m$^{3}$)', yscale='log')
#    plot_nucs(parts=['rpSP'], key='dhv_max_ratio',  nucs=['All'], work_dir=work_dir, figname='blk_rpsp_dhv_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['rpSP'], key='cd_max',         nucs=['All'], work_dir=work_dir, figname='blk_rpsp_cd_max.png', ylabel=r'Contact dose rate (Sv/h)', yscale='log')
#    plot_nucs(parts=['rpSP'], key='cd_max_ratio',   nucs=['All'], work_dir=work_dir, figname='blk_rpsp_cd_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#
#    # -----------Divertor ----------------------
#    plot_parts(parts=['Divertor', 'Divertor_W_layer', 'Divertor_structure'], key='act_st_t', nucs=['total_specific_act(Bq/kg)'], work_dir=work_dir, figname='div_comp_act_st_t.png')
#    plot_parts(parts=['Divertor', 'Divertor_W_layer', 'Divertor_structure'], key='act_st_t', nucs=['total_activity(Bq)'], work_dir=work_dir, figname='div_comp_act_t.png', ylabel='Total activity (Bq)')
#    plot_parts(parts=['Divertor', 'Divertor_W_layer', 'Divertor_structure'], key='rwc_chn2018', nucs=['Decay_heat(kW/m3)'], work_dir=work_dir, figname='div_comp_dhv.png', ylabel=r'Decay heat density (kw/m$^3$)')
#    plot_parts(parts=['Divertor', 'Divertor_W_layer', 'Divertor_structure'], key='dh_vt_t', nucs=['total_decay_heat(kW)'], work_dir=work_dir, figname='div_comp_dht.png', ylabel='Decay heat (kW)')
#    plot_parts(parts=['Divertor', 'Divertor_W_layer', 'Divertor_structure'], key='cdt', nucs=['total_contact_dose(Sv/hr)'], work_dir=work_dir, figname='div_comp_cdt.png', ylabel='Contact dose rate (Sv/h)')
#    # --------------- Divertor , Divertor W layer -----------------------------------
#    plot_nucs(parts=['Divertor_W_layer'], key='acts_max',       nucs=['All'], work_dir=work_dir, figname='div_w_acts_max.png', ylabel=r'Specific activity (Bq/kg)', yscale='log')
#    plot_nucs(parts=['Divertor_W_layer'], key='acts_max_ratio', nucs=['All'], work_dir=work_dir, figname='div_w_acts_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['Divertor_W_layer'], key='dhv_max',        nucs=['All'], work_dir=work_dir, figname='div_w_dhv_max.png', ylabel=r'Decay heat density (kW/m$^{3}$)', yscale='log')
#    plot_nucs(parts=['Divertor_W_layer'], key='dhv_max_ratio',  nucs=['All'], work_dir=work_dir, figname='div_w_dhv_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['Divertor_W_layer'], key='cd_max',         nucs=['All'], work_dir=work_dir, figname='div_w_cd_max.png', ylabel=r'Contact dose rate (Sv/h)', yscale='log')
#    plot_nucs(parts=['Divertor_W_layer'], key='cd_max_ratio',   nucs=['All'], work_dir=work_dir, figname='div_w_cd_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    # --------------- Divertor , Divertor structure -----------------------------------
#    plot_nucs(parts=['Divertor_structure'], key='acts_max',       nucs=['All'], work_dir=work_dir, figname='div_struct_acts_max.png', ylabel=r'Specific activity (Bq/kg)', yscale='log')
#    plot_nucs(parts=['Divertor_structure'], key='acts_max_ratio', nucs=['All'], work_dir=work_dir, figname='div_struct_acts_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['Divertor_structure'], key='dhv_max',        nucs=['All'], work_dir=work_dir, figname='div_struct_dhv_max.png', ylabel=r'Decay heat density (kW/m$^{3}$)', yscale='log')
#    plot_nucs(parts=['Divertor_structure'], key='dhv_max_ratio',  nucs=['All'], work_dir=work_dir, figname='div_struct_dhv_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['Divertor_structure'], key='cd_max',         nucs=['All'], work_dir=work_dir, figname='div_struct_cd_max.png', ylabel=r'Contact dose rate (Sv/h)', yscale='log')
#    plot_nucs(parts=['Divertor_structure'], key='cd_max_ratio',   nucs=['All'], work_dir=work_dir, figname='div_struct_cd_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    # ----------------Shield-------------------------------
#    plot_nucs(parts=['Shield'], key='acts_max',       nucs=['All'], work_dir=work_dir, figname='shield_acts_max.png', ylabel=r'Specific activity (Bq/kg)', yscale='log')
#    plot_nucs(parts=['Shield'], key='acts_max_ratio', nucs=['All'], work_dir=work_dir, figname='shield_acts_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['Shield'], key='dhv_max',        nucs=['All'], work_dir=work_dir, figname='shield_dhv_max.png', ylabel=r'Decay heat density (kW/m$^{3}$)', yscale='log')
#    plot_nucs(parts=['Shield'], key='dhv_max_ratio',  nucs=['All'], work_dir=work_dir, figname='shield_dhv_max_ratio.png', ylabel=r'Contribution', yscale='linear')
#    plot_nucs(parts=['Shield'], key='cd_max',         nucs=['All'], work_dir=work_dir, figname='shield_cd_max.png', ylabel=r'Contact dose rate (Sv/h)', yscale='log')
#    plot_nucs(parts=['Shield'], key='cd_max_ratio',   nucs=['All'], work_dir=work_dir, figname='shield_cd_max_ratio.png', ylabel=r'Contribution', yscale='linear')
# 
#   # -------------- rwc chn2018 blanket----------------------------
#    plot_nucs(parts=['BLK'], key='rwc_chn2018', nucs=['Clearance', 'VLLW', 'LLW', 'ILW'], work_dir=work_dir, figname='blk_rwc_chn2018.png', ylabel=r'Classfication indices', yscale='log')
#    plot_nucs(parts=['Divertor'], key='rwc_chn2018', nucs=['Clearance', 'VLLW', 'LLW', 'ILW'], work_dir=work_dir, figname='div_rwc_chn2018.png', ylabel=r'Classfication indices', yscale='log')
#    plot_nucs(parts=['Shield'], key='rwc_chn2018', nucs=['Clearance', 'VLLW', 'LLW', 'ILW'], work_dir=work_dir, figname='shield_rwc_chn2018.png', ylabel=r'Classfication indices', yscale='log')
#   # blanket chn2018 clearance
#    plot_parts(parts=['BLK', 'PFC', 'FW', 'Be', 'BZ', 'CP', 'BP', 'Cover', 'SW', 'rpSP'], key='rwc_chn2018', nucs=['Clearance'], work_dir=work_dir, figname='blanket_comp_ci.png', ylabel='Clearance index (CHN2018)')
#    plot_parts(parts=['BLK', 'PFC', 'FW', 'Be', 'BZ', 'CP', 'BP', 'Cover', 'SW', 'rpSP'], key='rwc_chn2018', nucs=['VLLW'], work_dir=work_dir, figname='blanket_comp_vllw.png', ylabel='VLLW index (CHN2018)')
#    plot_parts(parts=['BLK', 'PFC', 'FW', 'Be', 'BZ', 'CP', 'BP', 'Cover', 'SW', 'rpSP'], key='rwc_chn2018', nucs=['LLW'], work_dir=work_dir, figname='blanket_comp_llw.png', ylabel='LLW index (CHN2018)')
#    plot_parts(parts=['BLK', 'PFC', 'FW', 'Be', 'BZ', 'CP', 'BP', 'Cover', 'SW', 'rpSP'], key='rwc_chn2018', nucs=['ILW'], work_dir=work_dir, figname='blanket_comp_ilw.png', ylabel='ILW index (CHN2018)')
#    calc_rwc_cooling_requirement(parts=['BLK', 'PFC', 'FW', 'Be', 'BZ', 'CP', 'BP', 'Cover', 'SW', 'rpSP'], key='rwc_chn2018', classes=['ILW', 'LLW', 'VLLW', 'Clearance'], work_dir=work_dir, ofname='blk_comp_rwc_chn2018_ctr.csv')
#    # --------------rwc chn2018 divertor
#    plot_parts(parts=['Divertor', 'Divertor_W_layer', 'Divertor_structure'], key='rwc_chn2018', nucs=['Clearance'], work_dir=work_dir, figname='div_comp_ci.png', ylabel='Clearance index (CHN2018)')
#    plot_parts(parts=['Divertor', 'Divertor_W_layer', 'Divertor_structure'], key='rwc_chn2018', nucs=['VLLW'], work_dir=work_dir, figname='div_comp_vllw.png', ylabel='VLLW index (CHN2018)')
#    plot_parts(parts=['Divertor', 'Divertor_W_layer', 'Divertor_structure'], key='rwc_chn2018', nucs=['LLW'], work_dir=work_dir, figname='div_comp_llw.png', ylabel='LLW index (CHN2018)')
#    plot_parts(parts=['Divertor', 'Divertor_W_layer', 'Divertor_structure'], key='rwc_chn2018', nucs=['ILW'], work_dir=work_dir, figname='div_comp_ilw.png', ylabel='ILW index (CHN2018)')
#    calc_rwc_cooling_requirement(parts=['Divertor', 'Divertor_W_layer', 'Divertor_structure'], key='rwc_chn2018', classes=['ILW', 'LLW', 'VLLW', 'Clearance'], work_dir=work_dir, ofname='div_comp_rwc_chn2018_ctr.csv')
#    # --------------rwc chn2018 Shield
#    plot_nucs(parts=['Shield'], key='rwc_chn2018', nucs=['Clearance', 'VLLW', 'LLW', 'ILW'], work_dir=work_dir, figname='shield_rwc_chn2018.png', ylabel=r'Classfication indices', yscale='log')
#    calc_rwc_cooling_requirement(parts=['Shield'], key='rwc_chn2018', classes=['ILW', 'LLW', 'VLLW', 'Clearance'], work_dir=work_dir, ofname='shield_rwc_chn2018_ctr.csv')
#    # ---------------rwc chn2018, all, 1 s, 1 a, 10 a, 100 a
#    get_rwcs_by_cooling_times(parts=['PFC', 'FW', 'Be', 'BZ', 'CP', 'BP', 'Cover', 'SW', 'rpSP', 'Divertor_W_layer', 'Divertor_structure', 'Shield'], cooling_times_s=['1 s', '1 a', '10 a', '100 a'], key='rwc_chn2018', work_dir=work_dir, ofname='cfetr_all_rwcs_chn2018.csv')

    # --------------rwc usnrc --------------------------------------
#    plot_nucs(parts=['BLK'], key='rwc_usnrc', nucs=['LLWA_LL', 'LLWC_LL', 'LLWA_SL', 'LLWB_SL', 'LLWC_SL'], work_dir=work_dir, figname='blk_rwc_usnrc.png', ylabel=r'Classfication indices', yscale='log')
#    calc_rwc_cooling_requirement(parts=['BLK'], key='rwc_usnrc', classes=['LLWC', 'LLWB', 'LLWA'], standard='USNRC', work_dir=work_dir, ofname='blk_rwc_usnrc_ctr.csv')
#    plot_nucs(parts=['Divertor'], key='rwc_usnrc', nucs=['LLWA_LL', 'LLWC_LL', 'LLWA_SL', 'LLWB_SL', 'LLWC_SL'], work_dir=work_dir, figname='div_rwc_usnrc.png', ylabel=r'Classfication indices', yscale='log')
#    calc_rwc_cooling_requirement(parts=['Divertor'], key='rwc_usnrc', classes=['LLWC', 'LLWB', 'LLWA'], standard='USNRC', work_dir=work_dir, ofname='div_rwc_usnrc_ctr.csv')
#    plot_nucs(parts=['Shield'], key='rwc_usnrc', nucs=['LLWA_LL', 'LLWC_LL', 'LLWA_SL', 'LLWB_SL', 'LLWC_SL'], work_dir=work_dir, figname='shield_rwc_usnrc.png', ylabel=r'Classfication indices', yscale='log')
#    calc_rwc_cooling_requirement(parts=['Shield'], key='rwc_usnrc', classes=['LLWC', 'LLWB', 'LLWA'], standard='USNRC', work_dir=work_dir, ofname='shield_rwc_usnrc_ctr.csv')
#    get_rwcs_by_cooling_times(parts=['PFC', 'FW', 'Be', 'BZ', 'CP', 'BP', 'Cover', 'SW', 'rpSP', 'Divertor_W_layer', 'Divertor_structure', 'Shield'], cooling_times_s=['1 s', '1 a', '10 a', '100 a'], key='rwc_usnrc', work_dir=work_dir, ofname='cfetr_all_rwcs_usnrc.csv')

#    # --------------rwc USNRC_FETTER
#    calc_rwc_cooling_requirement(parts=['BLK', 'PFC', 'FW', 'Be', 'BZ', 'CP', 'BP', 'Cover', 'SW', 'rpSP', 'Divertor', 'Divertor_W_layer', 'Divertor_structure', 'Shield'], key='rwc_usnrc_fetter', classes=['LLWC', 'LLWB', 'LLWA'], standard='USNRC_FETTER', work_dir=work_dir, ofname='cfetr_all_rwc_usnrc_fetter_ctr.csv')
#    get_rwcs_by_cooling_times(parts=['PFC', 'FW', 'Be', 'BZ', 'CP', 'BP', 'Cover', 'SW', 'rpSP', 'Divertor_W_layer', 'Divertor_structure', 'Shield'], cooling_times_s=['1 s', '1 a', '10 a', '100 a'], key='rwc_usnrc_fetter', work_dir=work_dir, ofname='cfetr_all_rwcs_usnrc_fetter.csv')

#    # --------------rwc UK --------------------------------------
#    calc_rwc_cooling_requirement(parts=['BLK', 'PFC', 'FW', 'Be', 'BZ', 'CP', 'BP', 'Cover', 'SW', 'rpSP', 'Divertor', 'Divertor_W_layer', 'Divertor_structure', 'Shield'], key='rwc_uk', classes=['ILW', 'LLW'], standard='UK', work_dir=work_dir, ofname='cfetr_all_rwc_uk_ctr.csv')
#    get_rwcs_by_cooling_times(parts=['PFC', 'FW', 'Be', 'BZ', 'CP', 'BP', 'Cover', 'SW', 'rpSP', 'Divertor_W_layer', 'Divertor_structure', 'Shield'], cooling_times_s=['1 s', '1 a', '10 a', '100 a'], key='rwc_uk', work_dir=work_dir, ofname='cfetr_all_rwcs_uk.csv')

#    # ------------- plot rwc compare
#    plot_rwcs_compare(parts=['PFC', 'FW', 'Be', 'BZ', 'CP', 'BP', 'Cover', 'SW', 'rpSP', 'Divertor_W_layer', 'Divertor_structure', 'Shield'], keys=['rwc_chn2018', 'rwc_usnrc', 'rwc_usnrc_fetter', 'rwc_uk'], cooling_time_s='1 s', work_dir=work_dir, ofname='rwc_compare_1s.png')
#    plot_rwcs_compare(parts=['PFC', 'FW', 'Be', 'BZ', 'CP', 'BP', 'Cover', 'SW', 'rpSP', 'Divertor_W_layer', 'Divertor_structure', 'Shield'], keys=['rwc_chn2018', 'rwc_usnrc', 'rwc_usnrc_fetter', 'rwc_uk'], cooling_time_s='1 a', work_dir=work_dir, ofname='rwc_compare_1a.png')
#    plot_rwcs_compare(parts=['PFC', 'FW', 'Be', 'BZ', 'CP', 'BP', 'Cover', 'SW', 'rpSP', 'Divertor_W_layer', 'Divertor_structure', 'Shield'], keys=['rwc_chn2018', 'rwc_usnrc', 'rwc_usnrc_fetter', 'rwc_uk'], cooling_time_s='10 a', work_dir=work_dir, ofname='rwc_compare_10a.png')
#    plot_rwcs_compare(parts=['PFC', 'FW', 'Be', 'BZ', 'CP', 'BP', 'Cover', 'SW', 'rpSP', 'Divertor_W_layer', 'Divertor_structure', 'Shield'], keys=['rwc_chn2018', 'rwc_usnrc', 'rwc_usnrc_fetter', 'rwc_uk'], cooling_time_s='100 a', work_dir=work_dir, ofname='rwc_compare_100a.png')


#    plot_parts(parts=['Divertor_structure', 'Divertor_structure_eurofer'], key='act_st_t', nucs=['total_specific_act(Bq/kg)'], work_dir=work_dir, figname='div_cmp_act_st_t.png', ylabel=r'Specific activity (Bq/kg)')
#    calc_rwc_cooling_requirement(parts=['Divertor_structure', 'Divertor_structure_eurofer'], key='rwc_chn2018', classes=['ILW', 'LLW', 'VLLW', 'Clearance'], work_dir=work_dir, ofname='div_comp_rwc_chn2018_ctr.csv')

#    plot_nucs(parts=['BZ'], key='act_st_t',       nucs=['total_specific_act(Bq/kg)', 'total_specific_act_ext(Bq/kg)'], labels=[r'With $^{3}$H', 'Without $^{3}$H'], work_dir=work_dir, figname='blk_bz_h3_cmp_act_st_t.png', ylabel=r'Specific activity (Bq/kg)', yscale='log')
#    plot_nucs(parts=['BZ'], key='acts_ext_max',       nucs=['All'], work_dir=work_dir, figname='blk_bz_ext_acts_max.png', ylabel=r'Specific activity (Bq/kg)', yscale='log')

#    work_dir = '/media/zxk/ZXK_SAMSUNG/ComputeData/CFETR2019/WaterActivation/natf_coolant_cs2_200MW'
#    plot_wap_distribute(parts=['BSS','Seg-C','Sec-C','OHR','H-leg','Hoop-Seal','C-leg','IHR','Sec-D','Seg-D','BSS-in'], key='coolant_response', nucs=['N16', 'N17'], work_dir=work_dir, figname='PHTS_cs2_200MW.png', ylabel=r'Sepcific Activity (Bq/kg$_{H2O}$)', x_values=[28.93,34.02,45.02,80.37,90.37,99.32,107.32,142.66,153.66,158.75,187.68])
#    work_dir = '/media/zxk/ZXK_SAMSUNG/ComputeData/CFETR2019/WaterActivation/natf_coolant_cs2_500MW'
#    plot_wap_distribute(parts=['BSS','Seg-C','Sec-C','OHR','H-leg','Hoop-Seal','C-leg','IHR','Sec-D','Seg-D','BSS-in'], key='coolant_response', nucs=['N16', 'N17'], work_dir=work_dir, figname='PHTS_cs2_500MW.png', ylabel=r'Sepcific Activity (Bq/kg$_{H2O}$)', x_values=[28.93,34.02,45.02,80.37,90.37,99.32,107.32,142.66,153.66,158.75,187.68])
#    work_dir = '/media/zxk/ZXK_SAMSUNG/ComputeData/CFETR2019/WaterActivation/natf_coolant_cs2_1000MW'
#    plot_wap_distribute(parts=['BSS','Seg-C','Sec-C','OHR','H-leg','Hoop-Seal','C-leg','IHR','Sec-D','Seg-D','BSS-in'], key='coolant_response', nucs=['N16', 'N17'], work_dir=work_dir, figname='PHTS_cs2_1000MW.png', ylabel=r'Sepcific Activity (Bq/kg$_{H2O}$)', x_values=[28.93,34.02,45.02,80.37,90.37,99.32,107.32,142.66,153.66,158.75,187.68])
#    work_dir = '/media/zxk/ZXK_SAMSUNG/ComputeData/CFETR2019/WaterActivation/natf_coolant_cs2_1500MW'
#    plot_wap_distribute(parts=['BSS','Seg-C','Sec-C','OHR','H-leg','Hoop-Seal','C-leg','IHR','Sec-D','Seg-D','BSS-in'], key='coolant_response', nucs=['N16', 'N17'], work_dir=work_dir, figname='PHTS_cs2_1500MW.png', ylabel=r'Sepcific Activity (Bq/kg$_{H2O}$)', x_values=[28.93,34.02,45.02,80.37,90.37,99.32,107.32,142.66,153.66,158.75,187.68])

#    work_dir = '/media/zxk/ZXK_SAMSUNG/ComputeData/CFETR2019/WaterActivation'
#    plot_wap_power_cmp(powers=['200MW', '500MW', '1000MW', '1500MW'], cs='cs2', parts=['BSS','Seg-C','Sec-C','OHR','H-leg','Hoop-Seal','C-leg','IHR','Sec-D','Seg-D','BSS-in'], key='coolant_response', nucs=['N17'], work_dir=work_dir, figname='PHTS_cs2_power_cmp_n17.png', ylabel=r'Sepcific Activity (Bq/kg$_{H2O}$)', x_values=[28.93,34.02,45.02,80.37,90.37,99.32,107.32,142.66,153.66,158.75,187.68])
