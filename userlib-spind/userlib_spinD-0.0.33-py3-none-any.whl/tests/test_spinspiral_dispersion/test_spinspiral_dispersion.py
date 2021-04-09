import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, NullFormatter
from mpl_toolkits.axes_grid1.inset_locator import (inset_axes, InsetPosition, mark_inset)
from python3.magnetisations import SpinLattice
from python3.inputs_simulation import InputPhys
from python3.routines_analytic import *
from python3.visualizations import *
from python3.shell_commands import *
from python3.spinD_kiel_jobs import *
from pathlib import Path


def test_ssdispersion(inputs):
    # global settings
    para = InputPhys(file=inputs / 'inp')
    size = 100
    key = 'hex'
    magmom = 1.0
    if not os.path.isdir('test_calculations'):
        make_directory('test_calculations')
    if not os.path.isdir('test_calculations/GM'):
        make_directory('test_calculations/GM')
    if not os.path.isdir('test_calculations/GK'):
        make_directory('test_calculations/GK')

    num_energies = []
    ana_energies = []
    dif_energies = []
    qq = []
    qs = np.linspace(0.0, 0.49, 50)

    # GM-direction
    Rq = [0.0, 0.0, 1.0]
    Iq = [1.0, 0.5, 0.0]
    for q in qs:
        # begin with lowest q
        q = round(max(qs) - q, 2)
        sl = SpinLattice(size=size, key=key, path=None, magmom=magmom)
        Q = np.asarray([1.0, 0.0, 0.0]) * q
        sl.add1qstate(Rq, Iq, -Q)
        num = numeric_energy(sl, Path.cwd() / 'test_calculations' / 'GM'/ ('image_q_' + str(q)), inputs)
        ana = energy_SS(-q * 2. / 3. ** .5, para)
        num_energies.append(num)
        ana_energies.append(ana)
        # dif_energies.append(ana-num)
        qq.append(-q * 2. / 3. ** .5)

    # GK-direction
    Rq = [0.0, 0.0, 1.0]
    Iq = [1.0, 1.0, 0.0]
    for q in qs:
        q = round(q, 2)
        sl = SpinLattice(size=size, key=key, path=None, magmom=magmom)
        Q = np.asarray([1.0, 1.0, 0.0]) * q
        sl.add1qstate(Rq, Iq, -Q)
        num = numeric_energy(sl, 'test_calculations/GK/image_q_' + str(q), inputs)
        ana = energy_SS(q * 2., para)
        num_energies.append(num)
        ana_energies.append(ana)
        # dif_energies.append(ana-num)
        qq.append(q * 2.)

    # if any(dif_energies[0][n] <= 1e-9 for n in range(len(qs))) :
    #    print '====================================================='
    #    print ' ERROR: discrepancy of numerical and analytic results'
    #    print '        for the spinspiral dispersion exceeded < 1e-9'
    #    print '====================================================='

    return qq, np.asarray(ana_energies).transpose(), np.asarray(
        num_energies).transpose()  # , np.asarray(dif_energies).transpose()


def plot_ssdispersion(inputs, qs, ana, num):
    para = InputPhys(file=inputs + '/inp')
    FM = energy_SS(0, para)

    # build figure
    fig = plt.figure()
    fig.set_size_inches(8, 8)
    ax0 = plt.subplot2grid((5, 2), (0, 0), rowspan=3)
    ax1 = plt.subplot2grid((5, 2), (3, 0))
    ax2 = plt.subplot2grid((5, 2), (4, 0))
    ax0e = plt.subplot2grid((5, 2), (0, 1), rowspan=3)
    ax1e = plt.subplot2grid((5, 2), (3, 1))
    ax2e = plt.subplot2grid((5, 2), (4, 1))
    plt.subplots_adjust(wspace=0.001, hspace=0.05, left=0.11, right=0.84)

    # add labels
    ax2.set_xlabel(r'q / $\frac{2\pi}{a}$', fontsize=20)
    ax0.set_ylabel(r'$E(q)-E_{FM}$ /(meV/atom)', fontsize=20)

    # make brillouin-like xaxis
    ax0.yaxis.set_minor_locator(MultipleLocator(10))
    ax0.xaxis.set_minor_locator(MultipleLocator(0.1))
    ax0.xaxis.set_major_formatter(NullFormatter())
    ax0.xaxis.set_minor_formatter(NullFormatter())
    ax0e.xaxis.set_major_formatter(NullFormatter())
    ax0e.xaxis.set_minor_formatter(NullFormatter())
    ax0.xaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax0.yaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax0e.xaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax0e.yaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax1.yaxis.set_minor_locator(MultipleLocator(10))
    ax1.xaxis.set_minor_locator(MultipleLocator(0.1))
    ax1e.xaxis.set_minor_locator(MultipleLocator(0.1))
    ax1.xaxis.set_major_formatter(NullFormatter())
    ax1.xaxis.set_minor_formatter(NullFormatter())
    ax1e.xaxis.set_major_formatter(NullFormatter())
    ax1e.xaxis.set_minor_formatter(NullFormatter())
    ax2.yaxis.set_minor_locator(MultipleLocator(10))
    ax2.xaxis.set_minor_locator(MultipleLocator(0.1))
    ax1.xaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax1.yaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax2.xaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax2.yaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax1e.xaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax1e.yaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax2e.xaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax2e.yaxis.set_tick_params(labelsize=15, direction='in', which='both')
    ax2.set_xticks(np.array([-0.577, 0, 0.666, 1]))
    ax2.set_xticklabels(['M', '$\Gamma$', 'K', 'M'])
    ax2e.set_xticks(np.array([-0.577, 0, 0.666, 1]))
    ax2e.set_xticklabels(['M', '$\Gamma$', 'K', 'M'])

    ax0.set_xlim(-0.577, 1.0)
    ax1.set_xlim(-0.577, 1.0)
    ax2.set_xlim(-0.577, 1.0)

    ax0.plot(qs, (ana[0] - FM[0]) * 1000.0, c='b', ls='-', marker='')
    ax0.plot(qs, (num[0] - num[0][50]) * 1000.0, c='b', ls='', marker='+')
    ax1.plot(qs, (ana[4] - FM[4]) * 1000.0, c='r', ls='-', marker='')
    ax1.plot(qs, (num[4] - num[4][50]) * 1000.0, c='r', ls='', marker='+')
    ax1.plot(qs, (ana[3] - FM[3]) * 1000.0, c='m', ls='-', marker='')
    ax1.plot(qs, (num[3] - num[3][50]) * 1000.0, c='m', ls='', marker='+')
    ax2.plot(qs, (ana[5] - FM[5]) * 1000.0, c='lime', ls='-', marker='')
    ax2.plot(qs, (num[5] - num[5][50]) * 1000.0, c='lime', ls='', marker='+')
    ax2.plot(qs, (ana[6] - FM[6]) * 1000.0, c='g', ls='-', marker='')
    ax2.plot(qs, (num[6] - num[6][50]) * 1000.0, c='g', ls='', marker='+')
    ax2.plot(qs, (ana[7] - FM[7]) * 1000.0, c='k', ls='-', marker='')
    ax2.plot(qs, (num[7] - num[7][50]) * 1000.0, c='k', ls='', marker='+')

    ax0e.plot(qs, ana[0] - FM[0] - num[0] + num[0][50], c='b', marker='+', ls='', label=r'E$_{tot}$')
    ax0e.plot(qs, ana[1] - FM[1] - num[1] + num[1][50], c='g', marker='+', ls='', label=r'E$_{exc}$')
    ax1e.plot(qs, ana[4] - FM[4] - num[4] + num[4][50], c='r', marker='+', ls='', label=r'E$_{dmi}$')
    ax1e.plot(qs, ana[3] - FM[3] - num[3] + num[3][50], c='m', marker='+', ls='', label=r'E$_{ani}$')
    ax2e.plot(qs, ana[5] - FM[5] - num[5] + num[5][50], c='lime', marker='+', ls='', label=r'E$_{3sp}$')
    ax2e.plot(qs, ana[6] - FM[6] - num[6] + num[6][50], c='g', marker='+', ls='', label=r'E$_{4sp}$')
    ax2e.plot(qs, ana[7] - FM[7] - num[7] + num[7][50], c='k', marker='+', ls='', label=r'E$_{biq}$')

    # draw borders
    ax0.arrow(0.0, ax0.get_ylim()[0], 0.0, ax0.get_ylim()[1], head_width=0, head_length=0, color='k', ls='-',
              width=0.00002)
    ax0e.arrow(0.0, ax0e.get_ylim()[0], 0.0, ax0e.get_ylim()[1], head_width=0, head_length=0, color='k', ls='-',
               width=0.00002)
    ax0.arrow(0.666, ax0.get_ylim()[0], 0.0, ax0.get_ylim()[1], head_width=0, head_length=0, color='k', ls='-',
              width=0.00002)
    ax0e.arrow(0.666, ax0e.get_ylim()[0], 0.0, ax0e.get_ylim()[1], head_width=0, head_length=0, color='k', ls='-',
               width=0.00002)
    ax0.arrow(-0.577, 0.0, 0.577 + 1, 0.0, head_width=0, head_length=0, color='k', ls='-', width=0.00002)
    ax1.arrow(0.0, ax1.get_ylim()[0], 0.0, ax1.get_ylim()[1], head_width=0, head_length=0, color='k', ls='-',
              width=0.00002)
    ax1e.arrow(0.0, ax1e.get_ylim()[0], 0.0, ax1e.get_ylim()[1], head_width=0, head_length=0, color='k', ls='-',
               width=0.00002)
    ax1.arrow(0.666, ax1.get_ylim()[0], 0.0, ax1.get_ylim()[1], head_width=0, head_length=0, color='k', ls='-',
              width=0.00002)
    ax1e.arrow(0.666, ax1e.get_ylim()[0], 0.0, ax1e.get_ylim()[1], head_width=0, head_length=0, color='k', ls='-',
               width=0.00002)
    ax1.arrow(-0.577, 0.0, 0.577 + 1, 0.0, head_width=0, head_length=0, color='k', ls='-', width=0.00002)
    ax2.arrow(0.0, ax2.get_ylim()[0], 0.0, ax2.get_ylim()[1], head_width=0, head_length=0, color='k', ls='-',
              width=0.00002)
    ax2.arrow(0.666, ax2.get_ylim()[0], 0.0, ax2.get_ylim()[1], head_width=0, head_length=0, color='k', ls='-',
              width=0.00002)
    ax2e.arrow(0.0, ax2e.get_ylim()[0], 0.0, ax2e.get_ylim()[1], head_width=0, head_length=0, color='k', ls='-',
               width=0.00002)
    ax2e.arrow(0.666, ax2e.get_ylim()[0], 0.0, ax2e.get_ylim()[1], head_width=0, head_length=0, color='k', ls='-',
               width=0.00002)
    ax2.arrow(-0.577, 0.0, 0.577 + 1, 0.0, head_width=0, head_length=0, color='k', ls='-', width=0.00002)

    ax0e.yaxis.tick_right()
    ax1e.yaxis.tick_right()
    ax2e.yaxis.tick_right()

    # color the area beneath 0
    ulim0 = ax0.get_ylim()[0]
    ax0.fill_between(qs, [ulim0 for i in range(len(qs))], color='k', alpha=0.1)
    ulim1 = ax1.get_ylim()[0]
    ax1.fill_between(qs, [ulim1 for i in range(len(qs))], color='k', alpha=0.1)
    ulim2 = ax2.get_ylim()[0]
    ax2.fill_between(qs, [ulim2 for i in range(len(qs))], color='k', alpha=0.1)

    ax0e.legend(bbox_to_anchor=(0, 1), loc=2, borderaxespad=0., fontsize=8)
    ax1e.legend(bbox_to_anchor=(0, 1), loc=2, borderaxespad=0., fontsize=8)
    ax2e.legend(bbox_to_anchor=(0, 1), loc=2, borderaxespad=0., fontsize=8)
    plt.savefig('test_spinspiral_energydispersion.png')
    plt.show()


if __name__ == '__main__':
    inputs = Path.cwd().parent / 'input_data'
    qs, ana, num = test_ssdispersion(inputs)
    plot_ssdispersion(inputs, qs, ana, num)
