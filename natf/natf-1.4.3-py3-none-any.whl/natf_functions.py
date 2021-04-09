#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from __future__ import with_statement, print_function
import argparse
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
import math
import numpy as np
import pandas as pd
import os
from natf.mesh import Mesh
from natf.source_particle import SourceParticle
from natf.cell import Cell, get_cell_index
from natf.material import Material
from natf.part import Part
from natf.radwaste_standard import RadwasteStandard
from natf.utils import sgn, cooling_time_sec, format_single_output, str2float, \
    scale_list, is_blank_line, log
from natf.mcnp_input import is_comment
from natf.mcnp_output import get_cell_neutron_flux, get_cell_names_from_line, \
    get_cell_vol_mass, get_cell_tally_info, get_cell_vols_from_line, \
    is_cell_info_start, get_cell_icl_cellid_matid_matdensity, get_cell_basic_info


# constant variables
E_175 = (1.00001E-007, 4.13994E-007, 5.31579E-007, 6.82560E-007, 8.76425E-007,
         1.12535E-006, 1.44498E-006, 1.85539E-006, 2.38237E-006, 3.05902E-006,
         3.92786E-006, 5.04348E-006, 6.47595E-006, 8.31529E-006, 1.06770E-005,
         1.37096E-005, 1.76035E-005, 2.26033E-005, 2.90232E-005, 3.72665E-005,
         4.78512E-005, 6.14421E-005, 7.88932E-005, 1.01301E-004, 1.30073E-004,
         1.67017E-004, 2.14454E-004, 2.75364E-004, 3.53575E-004, 4.53999E-004,
         5.82947E-004, 7.48518E-004, 9.61117E-004, 1.23410E-003, 1.58461E-003,
         2.03468E-003, 2.24867E-003, 2.48517E-003, 2.61259E-003, 2.74654E-003,
         3.03539E-003, 3.35463E-003, 3.70744E-003, 4.30742E-003, 5.53084E-003,
         7.10174E-003, 9.11882E-003, 1.05946E-002, 1.17088E-002, 1.50344E-002,
         1.93045E-002, 2.18749E-002, 2.35786E-002, 2.41755E-002, 2.47875E-002,
         2.60584E-002, 2.70001E-002, 2.85011E-002, 3.18278E-002, 3.43067E-002,
         4.08677E-002, 4.63092E-002, 5.24752E-002, 5.65622E-002, 6.73795E-002,
         7.20245E-002, 7.94987E-002, 8.25034E-002, 8.65170E-002, 9.80365E-002,
         1.11090E-001, 1.16786E-001, 1.22773E-001, 1.29068E-001, 1.35686E-001,
         1.42642E-001, 1.49956E-001, 1.57644E-001, 1.65727E-001, 1.74224E-001,
         1.83156E-001, 1.92547E-001, 2.02419E-001, 2.12797E-001, 2.23708E-001,
         2.35177E-001, 2.47235E-001, 2.73237E-001, 2.87246E-001, 2.94518E-001,
         2.97211E-001, 2.98491E-001, 3.01974E-001, 3.33733E-001, 3.68832E-001,
         3.87742E-001, 4.07622E-001, 4.50492E-001, 4.97871E-001, 5.23397E-001,
         5.50232E-001, 5.78443E-001, 6.08101E-001, 6.39279E-001, 6.72055E-001,
         7.06512E-001, 7.42736E-001, 7.80817E-001, 8.20850E-001, 8.62936E-001,
         9.07180E-001, 9.61672E-001, 1.00259E+000, 1.10803E+000, 1.16484E+000,
         1.22456E+000, 1.28735E+000, 1.35335E+000, 1.42274E+000, 1.49569E+000,
         1.57237E+000, 1.65299E+000, 1.73774E+000, 1.82684E+000, 1.92050E+000,
         2.01897E+000, 2.12248E+000, 2.23130E+000, 2.30693E+000, 2.34570E+000,
         2.36533E+000, 2.38513E+000, 2.46597E+000, 2.59240E+000, 2.72532E+000,
         2.86505E+000, 3.01194E+000, 3.16637E+000, 3.32871E+000, 3.67879E+000,
         4.06570E+000, 4.49329E+000, 4.72367E+000, 4.96585E+000, 5.22046E+000,
         5.48812E+000, 5.76950E+000, 6.06531E+000, 6.37628E+000, 6.59241E+000,
         6.70320E+000, 7.04688E+000, 7.40818E+000, 7.78801E+000, 8.18731E+000,
         8.60708E+000, 9.04837E+000, 9.51229E+000, 1.00000E+001, 1.05127E+001,
         1.10517E+001, 1.16183E+001, 1.22140E+001, 1.25232E+001, 1.28403E+001,
         1.34986E+001, 1.38403E+001, 1.41907E+001, 1.45499E+001, 1.49182E+001,
         1.56831E+001, 1.64872E+001, 1.69046E+001, 1.73325E+001, 1.96403E+001)
E_709 = (1.05E-11, 1.10E-11, 1.15E-11, 1.20E-11, 1.26E-11, 1.32E-11, 1.38E-11,
         1.45E-11, 1.51E-11, 1.58E-11, 1.66E-11, 1.74E-11, 1.82E-11, 1.91E-11,
         2.00E-11, 2.09E-11, 2.19E-11, 2.29E-11, 2.40E-11, 2.51E-11, 2.63E-11,
         2.75E-11, 2.88E-11, 3.02E-11, 3.16E-11, 3.31E-11, 3.47E-11, 3.63E-11,
         3.80E-11, 3.98E-11, 4.17E-11, 4.37E-11, 4.57E-11, 4.79E-11, 5.01E-11,
         5.25E-11, 5.50E-11, 5.75E-11, 6.03E-11, 6.31E-11, 6.61E-11, 6.92E-11,
         7.24E-11, 7.59E-11, 7.94E-11, 8.32E-11, 8.71E-11, 9.12E-11, 9.55E-11,
         1.00E-10, 1.05E-10, 1.10E-10, 1.15E-10, 1.20E-10, 1.26E-10, 1.32E-10,
         1.38E-10, 1.45E-10, 1.51E-10, 1.58E-10, 1.66E-10, 1.74E-10, 1.82E-10,
         1.91E-10, 2.00E-10, 2.09E-10, 2.19E-10, 2.29E-10, 2.40E-10, 2.51E-10,
         2.63E-10, 2.75E-10, 2.88E-10, 3.02E-10, 3.16E-10, 3.31E-10, 3.47E-10,
         3.63E-10, 3.80E-10, 3.98E-10, 4.17E-10, 4.37E-10, 4.57E-10, 4.79E-10,
         5.01E-10, 5.25E-10, 5.50E-10, 5.75E-10, 6.03E-10, 6.31E-10, 6.61E-10,
         6.92E-10, 7.24E-10, 7.59E-10, 7.94E-10, 8.32E-10, 8.71E-10, 9.12E-10,
         9.55E-10, 1.00E-09, 1.05E-09, 1.10E-09, 1.15E-09, 1.20E-09, 1.26E-09,
         1.32E-09, 1.38E-09, 1.45E-09, 1.51E-09, 1.58E-09, 1.66E-09, 1.74E-09,
         1.82E-09, 1.91E-09, 2.00E-09, 2.09E-09, 2.19E-09, 2.29E-09, 2.40E-09,
         2.51E-09, 2.63E-09, 2.75E-09, 2.88E-09, 3.02E-09, 3.16E-09, 3.31E-09,
         3.47E-09, 3.63E-09, 3.80E-09, 3.98E-09, 4.17E-09, 4.37E-09, 4.57E-09,
         4.79E-09, 5.01E-09, 5.25E-09, 5.50E-09, 5.75E-09, 6.03E-09, 6.31E-09,
         6.61E-09, 6.92E-09, 7.24E-09, 7.59E-09, 7.94E-09, 8.32E-09, 8.71E-09,
         9.12E-09, 9.55E-09, 1.00E-08, 1.05E-08, 1.10E-08, 1.15E-08, 1.20E-08,
         1.26E-08, 1.32E-08, 1.38E-08, 1.45E-08, 1.51E-08, 1.58E-08, 1.66E-08,
         1.74E-08, 1.82E-08, 1.91E-08, 2.00E-08, 2.09E-08, 2.19E-08, 2.29E-08,
         2.40E-08, 2.51E-08, 2.63E-08, 2.75E-08, 2.88E-08, 3.02E-08, 3.16E-08,
         3.31E-08, 3.47E-08, 3.63E-08, 3.80E-08, 3.98E-08, 4.17E-08, 4.37E-08,
         4.57E-08, 4.79E-08, 5.01E-08, 5.25E-08, 5.50E-08, 5.75E-08, 6.03E-08,
         6.31E-08, 6.61E-08, 6.92E-08, 7.24E-08, 7.59E-08, 7.94E-08, 8.32E-08,
         8.71E-08, 9.12E-08, 9.55E-08, 1.00E-07, 1.05E-07, 1.10E-07, 1.15E-07,
         1.20E-07, 1.26E-07, 1.32E-07, 1.38E-07, 1.45E-07, 1.51E-07, 1.58E-07,
         1.66E-07, 1.74E-07, 1.82E-07, 1.91E-07, 2.00E-07, 2.09E-07, 2.19E-07,
         2.29E-07, 2.40E-07, 2.51E-07, 2.63E-07, 2.75E-07, 2.88E-07, 3.02E-07,
         3.16E-07, 3.31E-07, 3.47E-07, 3.63E-07, 3.80E-07, 3.98E-07, 4.17E-07,
         4.37E-07, 4.57E-07, 4.79E-07, 5.01E-07, 5.25E-07, 5.50E-07, 5.75E-07,
         6.03E-07, 6.31E-07, 6.61E-07, 6.92E-07, 7.24E-07, 7.59E-07, 7.94E-07,
         8.32E-07, 8.71E-07, 9.12E-07, 9.55E-07, 1.00E-06, 1.05E-06, 1.10E-06,
         1.15E-06, 1.20E-06, 1.26E-06, 1.32E-06, 1.38E-06, 1.45E-06, 1.51E-06,
         1.58E-06, 1.66E-06, 1.74E-06, 1.82E-06, 1.91E-06, 2.00E-06, 2.09E-06,
         2.19E-06, 2.29E-06, 2.40E-06, 2.51E-06, 2.63E-06, 2.75E-06, 2.88E-06,
         3.02E-06, 3.16E-06, 3.31E-06, 3.47E-06, 3.63E-06, 3.80E-06, 3.98E-06,
         4.17E-06, 4.37E-06, 4.57E-06, 4.79E-06, 5.01E-06, 5.25E-06, 5.50E-06,
         5.75E-06, 6.03E-06, 6.31E-06, 6.61E-06, 6.92E-06, 7.24E-06, 7.59E-06,
         7.94E-06, 8.32E-06, 8.71E-06, 9.12E-06, 9.55E-06, 1.00E-05, 1.05E-05,
         1.10E-05, 1.15E-05, 1.20E-05, 1.26E-05, 1.32E-05, 1.38E-05, 1.45E-05,
         1.51E-05, 1.58E-05, 1.66E-05, 1.74E-05, 1.82E-05, 1.91E-05, 2.00E-05,
         2.09E-05, 2.19E-05, 2.29E-05, 2.40E-05, 2.51E-05, 2.63E-05, 2.75E-05,
         2.88E-05, 3.02E-05, 3.16E-05, 3.31E-05, 3.47E-05, 3.63E-05, 3.80E-05,
         3.98E-05, 4.17E-05, 4.37E-05, 4.57E-05, 4.79E-05, 5.01E-05, 5.25E-05,
         5.50E-05, 5.75E-05, 6.03E-05, 6.31E-05, 6.61E-05, 6.92E-05, 7.24E-05,
         7.59E-05, 7.94E-05, 8.32E-05, 8.71E-05, 9.12E-05, 9.55E-05, 1.00E-04,
         1.05E-04, 1.10E-04, 1.15E-04, 1.20E-04, 1.26E-04, 1.32E-04, 1.38E-04,
         1.45E-04, 1.51E-04, 1.58E-04, 1.66E-04, 1.74E-04, 1.82E-04, 1.91E-04,
         2.00E-04, 2.09E-04, 2.19E-04, 2.29E-04, 2.40E-04, 2.51E-04, 2.63E-04,
         2.75E-04, 2.88E-04, 3.02E-04, 3.16E-04, 3.31E-04, 3.47E-04, 3.63E-04,
         3.80E-04, 3.98E-04, 4.17E-04, 4.37E-04, 4.57E-04, 4.79E-04, 5.01E-04,
         5.25E-04, 5.50E-04, 5.75E-04, 6.03E-04, 6.31E-04, 6.61E-04, 6.92E-04,
         7.24E-04, 7.59E-04, 7.94E-04, 8.32E-04, 8.71E-04, 9.12E-04, 9.55E-04,
         1.00E-03, 1.05E-03, 1.10E-03, 1.15E-03, 1.20E-03, 1.26E-03, 1.32E-03,
         1.38E-03, 1.45E-03, 1.51E-03, 1.58E-03, 1.66E-03, 1.74E-03, 1.82E-03,
         1.91E-03, 2.00E-03, 2.09E-03, 2.19E-03, 2.29E-03, 2.40E-03, 2.51E-03,
         2.63E-03, 2.75E-03, 2.88E-03, 3.02E-03, 3.16E-03, 3.31E-03, 3.47E-03,
         3.63E-03, 3.80E-03, 3.98E-03, 4.17E-03, 4.37E-03, 4.57E-03, 4.79E-03,
         5.01E-03, 5.25E-03, 5.50E-03, 5.75E-03, 6.03E-03, 6.31E-03, 6.61E-03,
         6.92E-03, 7.24E-03, 7.59E-03, 7.94E-03, 8.32E-03, 8.71E-03, 9.12E-03,
         9.55E-03, 1.00E-02, 1.05E-02, 1.10E-02, 1.15E-02, 1.20E-02, 1.26E-02,
         1.32E-02, 1.38E-02, 1.45E-02, 1.51E-02, 1.58E-02, 1.66E-02, 1.74E-02,
         1.82E-02, 1.91E-02, 2.00E-02, 2.09E-02, 2.19E-02, 2.29E-02, 2.40E-02,
         2.51E-02, 2.63E-02, 2.75E-02, 2.88E-02, 3.02E-02, 3.16E-02, 3.31E-02,
         3.47E-02, 3.63E-02, 3.80E-02, 3.98E-02, 4.17E-02, 4.37E-02, 4.57E-02,
         4.79E-02, 5.01E-02, 5.25E-02, 5.50E-02, 5.75E-02, 6.03E-02, 6.31E-02,
         6.61E-02, 6.92E-02, 7.24E-02, 7.59E-02, 7.94E-02, 8.32E-02, 8.71E-02,
         9.12E-02, 9.55E-02, 1.00E-01, 1.05E-01, 1.10E-01, 1.15E-01, 1.20E-01,
         1.26E-01, 1.32E-01, 1.38E-01, 1.45E-01, 1.51E-01, 1.58E-01, 1.66E-01,
         1.74E-01, 1.82E-01, 1.91E-01, 2.00E-01, 2.09E-01, 2.19E-01, 2.29E-01,
         2.40E-01, 2.51E-01, 2.63E-01, 2.75E-01, 2.88E-01, 3.02E-01, 3.16E-01,
         3.31E-01, 3.47E-01, 3.63E-01, 3.80E-01, 3.98E-01, 4.17E-01, 4.37E-01,
         4.57E-01, 4.79E-01, 5.01E-01, 5.25E-01, 5.50E-01, 5.75E-01, 6.03E-01,
         6.31E-01, 6.61E-01, 6.92E-01, 7.24E-01, 7.59E-01, 7.94E-01, 8.32E-01,
         8.71E-01, 9.12E-01, 9.55E-01, 1.00E+00, 1.05E+00, 1.10E+00, 1.15E+00,
         1.20E+00, 1.26E+00, 1.32E+00, 1.38E+00, 1.45E+00, 1.51E+00, 1.58E+00,
         1.66E+00, 1.74E+00, 1.82E+00, 1.91E+00, 2.00E+00, 2.09E+00, 2.19E+00,
         2.29E+00, 2.40E+00, 2.51E+00, 2.63E+00, 2.75E+00, 2.88E+00, 3.02E+00,
         3.16E+00, 3.31E+00, 3.47E+00, 3.63E+00, 3.80E+00, 3.98E+00, 4.17E+00,
         4.37E+00, 4.57E+00, 4.79E+00, 5.01E+00, 5.25E+00, 5.50E+00, 5.75E+00,
         6.03E+00, 6.31E+00, 6.61E+00, 6.92E+00, 7.24E+00, 7.59E+00, 7.94E+00,
         8.32E+00, 8.71E+00, 9.12E+00, 9.55E+00, 1.00E+01, 1.02E+01, 1.04E+01,
         1.06E+01, 1.08E+01, 1.10E+01, 1.12E+01, 1.14E+01, 1.16E+01, 1.18E+01,
         1.20E+01, 1.22E+01, 1.24E+01, 1.26E+01, 1.28E+01, 1.30E+01, 1.32E+01,
         1.34E+01, 1.36E+01, 1.38E+01, 1.40E+01, 1.42E+01, 1.44E+01, 1.46E+01,
         1.48E+01, 1.50E+01, 1.52E+01, 1.54E+01, 1.56E+01, 1.58E+01, 1.60E+01,
         1.62E+01, 1.64E+01, 1.66E+01, 1.68E+01, 1.70E+01, 1.72E+01, 1.74E+01,
         1.76E+01, 1.78E+01, 1.80E+01, 1.82E+01, 1.84E+01, 1.86E+01, 1.88E+01,
         1.90E+01, 1.92E+01, 1.94E+01, 1.96E+01, 1.98E+01, 2.00E+01, 2.10E+01,
         2.20E+01, 2.30E+01, 2.40E+01, 2.50E+01, 2.60E+01, 2.70E+01, 2.80E+01,
         2.90E+01, 3.00E+01, 3.20E+01, 3.40E+01, 3.60E+01, 3.80E+01, 4.00E+01,
         4.20E+01, 4.40E+01, 4.60E+01, 4.80E+01, 5.00E+01, 5.20E+01, 5.40E+01,
         5.60E+01, 5.80E+01, 6.00E+01, 6.50E+01, 7.00E+01, 7.50E+01, 8.00E+01,
         9.00E+01, 1.00E+02, 1.10E+02, 1.20E+02, 1.30E+02, 1.40E+02, 1.50E+02,
         1.60E+02, 1.80E+02, 2.00E+02, 2.40E+02, 2.80E+02, 3.20E+02, 3.60E+02,
         4.00E+02, 4.40E+02, 4.80E+02, 5.20E+02, 5.60E+02, 6.00E+02, 6.40E+02,
         6.80E+02, 7.20E+02, 7.60E+02, 8.00E+02, 8.40E+02, 8.80E+02, 9.20E+02,
         9.60E+02, 1.00E+03)
fispact_nuc_flag = ('?', '&', '*', '>')


@log
def check_input(filename="input"):
    """Read the 'input' file and check the variables.
    if the required variable is not given, this function will give error
    message."""

    config = ConfigParser.ConfigParser()
    config.read(filename)
    # general
    WORK_DIR = config.get('general', 'WORK_DIR')
    AIM = config.get('general', 'AIM')
    # check the input variables
    AIMS = (
        'CELL_ACT_PRE','CELL_ACT_POST', 'CELL_DPA_PRE', 'CELL_DPA_POST',
        'COOLANT_ACT_PRE', 'COOLANT_ACT_POST')
    if AIM not in AIMS:  # check AIM validate
        errormessage = ''.join(['AIM can only be the provided option\n',
                                'The AIM you input is: ', AIM, ', not in the list'])
        raise ValueError(errormessage)

    # mcnp
    MCNP_INPUT = os.path.join(WORK_DIR, config.get('mcnp', 'MCNP_INPUT'))
    MCNP_OUTPUT = os.path.join(WORK_DIR, config.get('mcnp', 'MCNP_OUTPUT'))
    try:
        CONTINUE_OUTPUT = config.get('mcnp', 'CONTINUE_OUTPUT')
        if CONTINUE_OUTPUT != '':
            CONTINUE_OUTPUT = os.path.join(WORK_DIR, config.get('mcnp', 'CONTINUE_OUTPUT'))
    except:
        CONTINUE_OUTPUT = None

    # mcnp.n_group_size
    N_GROUP_SIZE = config.getint('mcnp', 'N_GROUP_SIZE')
    if N_GROUP_SIZE not in (175, 315, 709):
        raise ValueError('N_GROUP_SIZE must be 175, 315 or 709')

    # mcnp.tally_number
    TALLY_NUMBER = config.getint('mcnp', 'TALLY_NUMBER')
    if TALLY_NUMBER < 0 or (TALLY_NUMBER % 10) != 4:
        raise ValueError(
            'TALLY_NUMBER must great than 0 and ended with 4')
    if AIM in ['CELL_DPA_PRE', 'CELL_DPA_POST'] and N_GROUP_SIZE != 709:
        raise ValueError(
            'N_GROUP_SIZE only support 709 if you want to calculate DPA')

    # coolant_flow, available only for COOLANT_ACT mode
    if AIM in ['COOLANT_ACT_PRE', 'COOLANT_ACT_POST']:
        # coolant_flow.coolant_flow_parameters, required in COOLANT_ACT mode
        COOLANT_FLOW_PARAMETERS = os.path.join(WORK_DIR,
            config.get('coolant_flow', 'COOLANT_FLOW_PARAMETERS'))
        if AIM in ['COOLANT_ACT_PRE', 'COOLANT_ACT_POST'] and COOLANT_FLOW_PARAMETERS is None:
            raise ValueError("COOLANT_FLOW_PARAMETERS must be provided in COOLANT_ACT mode")
        # coolant_flow.flux_multiplier, required in COOLANT_ACT mode
        FLUX_MULTIPLIER = float(config.get('coolant_flow', 'FLUX_MULTIPLIER'))
        if AIM in ['COOLANT_ACT_PRE', 'COOLANT_ACT_POST'] and FLUX_MULTIPLIER is None:
            raise ValueError("FLUX_MULTIPLIER must be provided in COOLANT_ACT mode")

    # fispact
    # fispact.fispact_material_list, optional
    try:
        FISPACT_MATERIAL_LIST = config.get('fispact', 'FISPACT_MATERIAL_LIST')
        if FISPACT_MATERIAL_LIST != '':
            FISACT_MATERIAL_LIST = os.path.join(WORK_DIR, FISPACT_MATERIAL_LIST)
    except:
        FISPACT_MATERIAS_LIST = ''
    # fispact.irradiation_scenario, required in CELL_ACT and CELL_DPA mode
    IRRADIATION_SCENARIO = config.get('fispact', 'IRRADIATION_SCENARIO')
    if AIM in ['CELL_ACT_PRE', 'CELL_ACT_POST', 'CELL_DPA_PRE', 'CELL_DPA_POST']:
        if IRRADIATION_SCENARIO == '':
            raise ValueError("IRRADIATION_SCENARIO must be provided in CELL_ACT and CELL_DPA mode")
    if AIM in ['COOLANT_ACT_PRE', 'COOLANT_ACT_POST']:
        if IRRADIATION_SCENARIO != '':
            raise ValueError("IRRADIATION_SCENARIO is not required in COOLANT_ACT mode")
    IRRADIATION_SCENARIO = os.path.join(WORK_DIR, config.get('fispact', 'IRRADIATION_SCENARIO'))
    try:
        NUC_TREATMENT = config.get('fispact', 'NUC_TREATMENT')
        if NUC_TREATMENT != '':
            NUC_TREATMENT = os.path.join(WORK_DIR, NUC_TREATMENT)
    except:
        NUC_TREATMENT = ''

    # model, required
    PART_CELL_LIST = os.path.join(WORK_DIR,
            config.get('model', 'PART_CELL_LIST'))
    # model.model_degree, optional
    try:
        MODEL_DEGREE = float(config.get('model', 'MODEL_DEGREE'))
        if MODEL_DEGREE < 0.0 or MODEL_DEGREE > 360.0:
            raise ValueError('MODEL_DEGREE must between 0 ~ 360')
    except:
        MODEL_DEGREE = 360.0

    return True


@log
def get_cooling_time(IRRADIATION_SCENARIO, AIM):
    """Read the irradiation_scenario, return cooling_time[]
        report error if the irradiation_scenario not fit the need of the AIM (CELL_DPA).
        CELL_DPA requirement: 1. only one pluse allowed, and this must be the FULL POWER YEAR, 1 year
                              2. no cooling time allowed."""
    # check the IRRADIATiON_SCENARIO file
    errormessage = ''.join(['IRRADIATION_SCENARIO ERROR:\n',
                            '1. Only one pulse allowed, and it must be a FPY (1 YEARS).\n',
                            '2. No cooling time allowed.'])
    # check there is only one Pulse in the content
    if AIM in ('CELL_DPA_PRE', 'CELL_DPA_POST'):
        fin = open(IRRADIATION_SCENARIO)
        time_count = 0
        for line in fin:
            line_ele = line.split()
            if line_ele == 0:  # end of the file
                continue
            if line[0] == '<' and line[1] == '<':  # this is a comment line
                continue
            if 'TIME' in line:  # this is the time information line
                time_count += 1
                if ' 1 ' not in line or ' YEARS ' not in line:  # error
                    raise ValueError(errormessage)
        fin.close()
        if time_count != 1:  # error
            raise ValueError(errormessage)

    cooling_time = []
    fin = open(IRRADIATION_SCENARIO)
    zero_flag = False
    for line in fin:
        line_ele = line.split()
        if len(line_ele) == 0:  # this is a empty line
            continue
        if line[0] == '<' and line[1] == '<':  # this is a comment line
            continue
        if 'ZERO' in line:
            zero_flag = True
            continue
        if 'TIME' in line and zero_flag:  # this is a information about the cooling time
            cooling_time.append(
                cooling_time_sec(float(line_ele[1]),line_ele[2]))
    fin.close()
    return cooling_time


def get_cooling_time_cul(cooling_time):
    """Calculate the culmulated cooling times."""
    cooling_time_cul = [0.0]*len(cooling_time)
    for i in range(len(cooling_time)):
        cooling_time_cul[i] = cooling_time_cul[i-1] + cooling_time[i]
    return cooling_time_cul


@log
def get_fispact_material_list(FISPACT_MATERIAL_LIST, AIM=None):
    """get_fispact_material_list: read the FISPACT_MATERIAL_LIST file to get the link of
    return the fispact_material_list (of int) and fispact_material_path (of string)
    Where the fispact_material_list contains the material id
              fispact_material_path contains the material file in fispact format"""

    fispact_material_list = []
    fispact_material_path = []
    # check for the input
    if FISPACT_MATERIAL_LIST == '':
        fispact_material_list, fispact_material_path = [], []
    else:
        # read the FISPACT_MATERIAL_LIST to get the information
        fin = open(FISPACT_MATERIAL_LIST)
        try:
            for line in fin:
                line_ele = line.split()
                # is this line a comment line?
                if line_ele[0] in ['c', 'C']:
                    pass
                else:
                    material_path = line_ele[0]
                    if material_path in fispact_material_path: 
                        errormessage = ''.join(
                            ['material path:', material_path, ' defined more than once in FISPACT_MATERIAL_LIST\n'])
                        raise ValueError(errormessage)
                    else:
                        fispact_material_path.append(material_path)
                        if AIM in ['COOLANT_ACT_PRE', 'COOLANT_ACT_POST']:
                            # part name supports explicit define only
                            fispact_material_list.append(line_ele[1:])
                        else:
                            fispact_material_list.append(get_cell_ids(line_ele[1:]))
        except BaseException:
            errormessage = ''.join(
                ['Error produced when reading FISPACT_MATERIAL_LIST'])
            print(errormessage)
    check_material_list(fispact_material_list, AIM=AIM)
    return fispact_material_list, fispact_material_path


@log
def get_mesh_structure(MCNP_MESHTAL, MESH_GEOM, MESH_VEC, TALLY_NUMBER):
    """get_mesh_structure: read the meshtal to get the mesh structure.
    input parameters: MCNP_MESHTAL, the file path of the meshtal file,
                      MESH_GEOM, the geom of the mesh
                      MESH_VEC, the vector of the cyl mesh
                      TALLY_NUMBER, define which tally to read
    return value:mesh_boundaries, a tuple of 3 lists that contains the boundaries of 3 directions if MESH_GEOM is xyz
                 mesh_boundaries, a tuple of 6 lists that contains the boundaries of 3 direction and the origin, axs and vec if
                 the MESH_GEOM is cyl"""

    # input parameter check
    if MCNP_MESHTAL == '' or MESH_GEOM == '':
        raise ValueError('MCNP_MESHTAL and MESH_GEOM must be given!')
    # open meshtal file
    fin = open(MCNP_MESHTAL)
    if MESH_GEOM == 'xyz':
        x_boundary = []
        y_boundary = []
        z_boundary = []
        while True:
            line = fin.readline()
            if 'Mesh Tally Number' in line and str(
                    TALLY_NUMBER) in line:  # find the the given tally part
                while True:
                    line = fin.readline()
                    line_ele = line.split()
                    if 'X direction' in line:
                        x_boundary.extend(map(float, line_ele[2:]))
                    if 'Y direction' in line:
                        y_boundary.extend(map(float, line_ele[2:]))
                    if 'Z direction' in line:
                        z_boundary.extend(map(float, line_ele[2:]))
                    if 'R direction' in line:
                        raise ValueError(
                            'MESH_GEOM is xyz, but there are cyl mesh in meshtal!')
                    if 'Energy' in line:
                        break
                break
        mesh_boundary = (x_boundary, y_boundary, z_boundary)
    if MESH_GEOM == 'cyl':
        r_boundary = []
        z_boundary = []
        t_boundary = []
        origin = []
        axs = []
        while True:
            line = fin.readline()
            if 'Mesh Tally Number' in line and str(
                    TALLY_NUMBER) in line:  # find the the given tally part
                while True:
                    line = fin.readline()
                    line_ele = line.split()
                    if 'X direction' in line:
                        raise ValueError(
                            'MESH_GEOM is cyl, but there are xyz mesh in meshtal!')
                    if 'R direction' in line:
                        r_boundary.extend(map(float, line_ele[2:]))
                    if 'Z direction' in line:
                        z_boundary.extend(map(float, line_ele[2:]))
                    if 'Theta direction' in line:
                        t_boundary.extend(map(float, line_ele[3:]))
                    if 'Cylinder origin at' in line:
                        origin.extend(map(float, line_ele[3:5]))
                        origin.append(float(line_ele[5][:-1]))
                        axs.extend(map(int, map(float, line_ele[8:11])))
                    if 'Energy' in line:
                        break
                break
        mesh_boundary = (
            r_boundary,
            z_boundary,
            t_boundary,
            origin,
            axs,
            MESH_VEC)

    fin.close()
    return mesh_boundary


@log
def init_meshs(mesh_structure):
    """initial meshs according to the mesh_structure.
    input parameter: mesh_structure, a tuple of 3 or 6 lists.
    if geom is xyz, (tuple 3 lists), then set geom, mesh_id, xmin, xmax, ymin, ymax, zmin,, zmax, vol of the meshs;
     if geom is cyl, (tuple 6 lists), then set the geom, mesh_id, rmin,rmax, zmin, zmax, tmin, tmax,
                                                        origin, axs, vec of the meshs
     return a list of meshs : Meshes"""
    Meshes = []
    I = len(mesh_structure[0]) - 1
    J = len(mesh_structure[1]) - 1
    K = len(mesh_structure[2]) - 1
    if len(mesh_structure) == 3:  # geom is xyz
        for i in range(I):
            for j in range(J):
                for k in range(K):
                    temp_mesh = Mesh()
                    temp_mesh.geom = 'xyz'
                    temp_mesh.mesh_id = k + K * j + K * J * i
                    temp_mesh.xmin = mesh_structure[0][i]
                    temp_mesh.xmax = mesh_structure[0][i + 1]
                    temp_mesh.ymin = mesh_structure[1][j]
                    temp_mesh.ymax = mesh_structure[1][j + 1]
                    temp_mesh.zmin = mesh_structure[2][k]
                    temp_mesh.zmax = mesh_structure[2][k + 1]
                    temp_mesh.cal_vol()
                    Meshes.append(temp_mesh)
    if len(mesh_structure) == 6:  # geom is cyl
        for i in range(I):
            for j in range(J):
                for k in range(K):
                    temp_mesh = Mesh()
                    temp_mesh.geom = 'cyl'
                    temp_mesh.mesh_id = k + K * j + K * J * i
                    temp_mesh.rmin = mesh_structure[0][i]
                    temp_mesh.rmax = mesh_structure[0][i + 1]
                    temp_mesh.zmin = mesh_structure[1][j]
                    temp_mesh.zmax = mesh_structure[1][j + 1]
                    temp_mesh.tmin = mesh_structure[2][k]
                    temp_mesh.tmax = mesh_structure[2][k + 1]
                    temp_mesh.cal_vol()
                    Meshes.append(temp_mesh)
    return Meshes


def cal_pos(value, boundary):
    """cal_pos, calculate the position of a value in the boundary
    input parameter: value, a float number represents xxx, yyy or zzz
    input parameter: boundary, a list of float represents the boundary
    return: pos, a int number"""

    # value check
    pos = -1
    if value < min(boundary) or value > max(
            boundary):  # particle out of the range of mesh
        return -1
    for i in range(len(boundary) - 1):
        if i == 0:  # speacial treat for the first boundary
            if boundary[i] <= value <= boundary[i + 1]:
                pos = i
        else:
            if boundary[i] < value <= boundary[i + 1]:
                pos = i
    if pos == -1:  # check the value
        raise RuntimeError('pos mus be changed in cal_pos')
    return pos


def cal_rzt(s, mesh_structure):
    """cal_rzt, calculate the r, z, t value according to the xxx,yyy,zzz of a source and mesh_sturcture
    input parameter: s, a source particle
    input parameter: mesh_structure, a tuple contains mesh structure information
    return: r, z, t, three int number"""
    r, z, t = -1, -1, -1  # initial three number, used to check whether thay are changed
    origin = list(mesh_structure[3])
    axs = list(mesh_structure[4])
    vec = list(mesh_structure[5])
    x_d = s.xxx - origin[0]
    y_d = s.yyy - origin[1]
    z_d = s.zzz - origin[2]
    if axs == [0, 0, 1]:  # axs is 0 0 1
        r = math.sqrt(x_d ** 2 + y_d ** 2)
        z = s.zzz - origin[2]
        if vec == [1, 0, 0]:  # vec is 1 0 0
            t = (1 - sgn(y_d)) // 2 + (sgn(y_d) *
                                      (math.acos(x_d / r))) / (2 * math.pi)
        if vec == [0, 1, 0]:  # vec is 0 1 0
            t = (1 - sgn(-x_d)) // 2 + (sgn(-x_d)
                                       * (math.acos(y_d / r))) / (2 * math.pi)
    if axs == [1, 0, 0]:  # axs is 1 0 0
        r = math.sqrt(y_d ** 2 + z_d ** 2)
        z = s.xxx - origin[0]
        if vec == [0, 1, 0]:  # vec is 0 1 0
            t = (1 - sgn(z_d)) // 2 + (sgn(z_d) *
                                      (math.acos(y_d / r))) / (2 * math.pi)
        if vec == [0, 0, 1]:
            t = (1 - sgn(-y_d)) // 2 + (sgn(-y_d)
                                       * (math.acos(z_d / r))) / (2 * math.pi)
    if axs == [0, 1, 0]:  # axs is 0 1 0
        r = math.sqrt(x_d ** 2 + z_d * 2)
        z = s.yyy - origin[1]
        if vec == [1, 0, 0]:
            t = (1 - sgn(z_d)) // 2 + (sgn(z_d) *
                                      (math.acos(x_d / r))) / (2 * math.pi)
        if vec == [0, 0, 1]:
            t = (1 - sgn(-x_d)) // 2 + (sgn(-x_d)
                                       * (math.acos(z_d / r))) / (2 * math.pi)
    if r == -1 or z == -1 or t == -1:  # check r, z, t value
        raise RuntimeError('r, z, t of must be changed in  cal_rzt!')
    return r, z, t


def cal_mesh_id(s, mesh_structure):
    """cal_mesh_id, calculate the mesh_id of a source particle according to the mesh_structre
    input parameter: s, a source particle
    input parameter: mesh_structre, a tuple of mesh geomtry and boundaries
    return: mid, a int of mesh_id"""

    I = len(mesh_structure[0]) - 1
    J = len(mesh_structure[1]) - 1
    K = len(mesh_structure[2]) - 1
    mid = -1

    if len(mesh_structure) == 3:  # the mesh geom is xyz
        i = cal_pos(s.xxx, mesh_structure[0])
        j = cal_pos(s.yyy, mesh_structure[1])
        k = cal_pos(s.zzz, mesh_structure[2])
        if i == -1 or j == -1 or k == -1:  # they may particle out of mesh
            return -1
        mid = k + K * j + K * J * i
    if len(mesh_structure) == 6:  # the mesh geom is cyl
        r, z, t = cal_rzt(s, mesh_structure)
        i = cal_pos(r, mesh_structure[0])
        j = cal_pos(z, mesh_structure[1])
        k = cal_pos(t, mesh_structure[2])
        if i == -1 or j == -1 or k == -1:
            return -1
        mid = k + K * j + K * J * i

    if mid == -1:  # check the value
        raise RuntimeError('mid must be changed in cal_mesh_id')
    return mid


def get_mesh_id(value, mesh_structure):
    """get_mesh_id, calculate the mesh_id according to the x,y,z or r,z,t"""
    I = len(mesh_structure[0]) - 1
    J = len(mesh_structure[1]) - 1
    K = len(mesh_structure[2]) - 1
    mesh_id = -1
    i = cal_pos(value[0], mesh_structure[0])
    j = cal_pos(value[1], mesh_structure[1])
    k = cal_pos(value[2], mesh_structure[2])
    if i == -1 or j == -1 or k == -1:  # they may particle out of mesh
        raise ValueError('the positon not in any mesh, there must be error')
    mesh_id = k + K * j + K * J * i
    return mesh_id


@log
def match_source_particles_match(Source_Particles, Meshes, mesh_structure):
    """match_source_particles_match
    funciton: put the source partiles into meshes
    input parameters: Source_Particles, a list of SourceParticle
    input parameters: Meshes, a list of Mesh
    input parameters: mesh_structure, a tuple of mesh geometry and boundaries
    return: Source_Particles, Meshes edited"""

    count_s_m = 0
    count_s_n_m = 0
    for s in Source_Particles:
        mid = cal_mesh_id(s, mesh_structure)
        if mid == -1:  # this particle doesn't in any mesh
            count_s_n_m += 1
            continue
        if mid != -1:
            count_s_m += 1
            s.mesh_id = mid
    print('    Particles in meshes: {0}; Particles not in meshes: {1}'.format(count_s_m, count_s_n_m))

    # calculate the mesh_cell_list
    for m in Meshes:
        cell_list = []
        cell_counts = []
        mat_list = []
        mat_counts = []
        for s in Source_Particles:
            if s.mesh_id == m.mesh_id:
                cell_list.append(s.cell_id)
                mat_list.append(s.mat_id)
        cell_set = set(cell_list)
        mat_set = set(mat_list)
        for item in cell_set:
            cell_counts.append(cell_list.count(item))
        for item in mat_set:
            mat_counts.append(mat_list.count(item))
        m.mesh_cell_list = list(cell_set)
        m.mesh_cell_counts = cell_counts
        m.mesh_mat_list = list(mat_set)
        m.mesh_mat_counts = mat_counts
        for i in range(len(m.mesh_cell_list)):
            m.mesh_cell_vol_fraction.append(
                float(m.mesh_cell_counts[i]) / sum(m.mesh_cell_counts))
        for i in range(len(m.mesh_mat_list)):
            m.mesh_mat_vol_fraction.append(
                float(m.mesh_mat_counts[i]) / sum(m.mesh_mat_counts))
        # calculate the mesh packing factor
        if 0 in m.mesh_mat_list:
            m.packing_factor = 1.0 - \
                float(m.mesh_mat_counts[m.mesh_mat_list.index(0)]) / sum(m.mesh_mat_counts)

    # check the counts of the meshes
    bad_mesh_counts = 0
    for m in Meshes:
        if sum(m.mesh_cell_counts) < 100:
            bad_mesh_counts += 1
    if float(bad_mesh_counts) / len(Meshes) > 0.05:
        raise ValueError(
            'bad sample meshes larger than 5%, please enlarge the ptrac nps')

    return Source_Particles, Meshes


def get_material_index(Materials, mat_id):
    """get_material_index, return material index of the Materials according to the mat_id"""
    mat_index = -1
    for i in range(len(Materials)):
        if Materials[i].mat_id == mat_id:
            mat_index = i
    # check value
    if mat_index == -1:
        raise ValueError('material not  found!')
    return mat_index


@log
def get_material_info(MCNP_OUTPUT):
    """get_material_info, read the MCNP_OUTPUT file and returns the Materials"""

    Materials = []
    # read the MCNP_OUTPUT first time to get the numbers of material
    mat_list = []
    fin = open(MCNP_OUTPUT)
    while True:
        line = fin.readline()
        if line == '':
            raise ValueError('1cells not found in the file, wrong file!')
        if '1cells' in line:  # read 1cells
            # read the following line
            line = fin.readline()
            line = fin.readline()
            line = fin.readline()
            line = fin.readline()
            while True:
                line = fin.readline()
                if ' total' in line:  # end of the cell information part
                    break
                line_ele = line.split()
                if len(line_ele) == 0:
                    continue
                mat_id, atom_density, gram_density = int(
                    line_ele[2]), float(
                    line_ele[3]), float(
                    line_ele[4])
                mat_list.append((mat_id, atom_density, gram_density))
            break
    fin.close()
    mat_list = list(set(mat_list))

    # initial the Materials
    for i in range(len(mat_list)):
        m = Material()
        m.mat_id = mat_list[i][0]
        m.atom_density = mat_list[i][1]
        m.density = mat_list[i][2]
        Materials.append(m)

    # get the nuclide of the mcnp material
    fin = open(MCNP_OUTPUT)
    mat_id = -1
    nuc_list = []
    atom_fraction_list = []
    while True:
        line = fin.readline()
        if 'component nuclide, atom fraction' in line:  # read atom fraction
            # read the following line
            line = fin.readline()
            mat_flag = False
            while True:
                line = fin.readline()
                if 'material' in line:  # end of the material atom fraction part
                    mat_index = get_material_index(Materials, mat_id)
                    Materials[mat_index].mcnp_material_nuclide = list(nuc_list)
                    Materials[mat_index].mcnp_material_atom_fraction = scale_list(
                        atom_fraction_list)
                    break
                line_ele = line.split()
                if len(line_ele) == 0:
                    continue
                if len(line_ele) % 2 == 1:  # this line contains material id
                    if mat_flag:
                        mat_index = get_material_index(Materials, mat_id)
                        Materials[mat_index].mcnp_material_nuclide = list(
                            nuc_list)
                        Materials[mat_index].mcnp_material_atom_fraction = scale_list(
                            atom_fraction_list)
                        nuc_list = []  # reset
                        atom_fraction_list = []  # reset
                    mat_id = int(line_ele[0])
                    mat_flag = True
                    for i in range(len(line_ele) // 2):
                        nuc, atom_fraction = line_ele[2 * i +
                                                      1][:-1], float(line_ele[2 * i + 2])
                        if nuc not in nuc_list:
                            nuc_list.append(nuc)
                            atom_fraction_list.append(atom_fraction)
                            continue
                        if nuc in nuc_list:
                            nuc_index = nuc_list.index(nuc)
                            atom_fraction_list[nuc_index] += atom_fraction
                if len(line_ele) % 2 == 0:
                    for i in range(len(line_ele) // 2):
                        nuc, atom_fraction = line_ele[2 *
                                                      i][:-1], float(line_ele[2 * i + 1])
                        if nuc not in nuc_list:
                            nuc_list.append(nuc)
                            atom_fraction_list.append(atom_fraction)
                            continue
                        if nuc in nuc_list:
                            nuc_index = nuc_list.index(nuc)
                            atom_fraction_list[nuc_index] += atom_fraction
            break
    fin.close()

    # get the mass fraction of the nuclide
    fin = open(MCNP_OUTPUT)
    mat_id = -1
    nuc_list = []
    mass_fraction_list = []
    while True:
        line = fin.readline()
        if 'component nuclide, mass fraction' in line:  # read mass fraction
            # read the following line
            line = fin.readline()
            mat_flag = False
            while True:
                line = fin.readline()
                if ' warning.' in line or '1cell' in line:  # end of the material atom fraction part
                    mat_index = get_material_index(Materials, mat_id)
                    Materials[mat_index].mcnp_material_nuclide = list(nuc_list)
                    Materials[mat_index].mcnp_material_mass_fraction = scale_list(
                        mass_fraction_list)
                    break
                line_ele = line.split()
                if len(line_ele) == 0:
                    continue
                if len(line_ele) % 2 == 1:  # this line contains material id
                    if mat_flag:
                        mat_index = get_material_index(Materials, mat_id)
                        Materials[mat_index].mcnp_material_nuclide = list(
                            nuc_list)
                        Materials[mat_index].mcnp_material_mass_fraction = scale_list(
                            mass_fraction_list)
                        nuc_list = []  # reset
                        mass_fraction_list = []  # reset
                    mat_id = int(line_ele[0])
                    mat_flag = True
                    for i in range(len(line_ele) // 2):
                        nuc, mass_fraction = line_ele[2 * i +
                                                      1][:-1], float(line_ele[2 * i + 2])
                        if nuc not in nuc_list:
                            nuc_list.append(nuc)
                            mass_fraction_list.append(mass_fraction)
                            continue
                        if nuc in nuc_list:
                            nuc_index = nuc_list.index(nuc)
                            mass_fraction_list[nuc_index] += mass_fraction
                if len(line_ele) % 2 == 0:
                    for i in range(len(line_ele) // 2):
                        nuc, mass_fraction = line_ele[2 *
                                                      i][:-1], float(line_ele[2 * i + 1])
                        if nuc not in nuc_list:
                            nuc_list.append(nuc)
                            mass_fraction_list.append(mass_fraction)
                            continue
                        if nuc in nuc_list:
                            nuc_index = nuc_list.index(nuc)
                            mass_fraction_list[nuc_index] += mass_fraction
            break
    fin.close()
    return Materials


@log
def convert_material_M2F(Materials):
    """convert_material_M2F: convert the mcnp material to FISPACT material"""
    for m in Materials:
        m.mat_mcnp2fispact()
    return Materials


@log
def match_cells_materials(Cells, Materials):
    """match the cells and materials"""
    for c in Cells:
        mid = get_material_index(Materials, c.mat_id)
        c.mat = Materials[mid]
    return Cells


def cal_mesh_material_list(m, Materials):
    """cal_material_list: calculate the materials for a specific mesh
    input:m, a mesh
    input:Materials, the list of all the materials
    return: materials_list, a list a materials in the given mesh"""
    material_list = []
    for i in range(len(m.mesh_mat_list)):
        mat_index = get_material_index(Materials, m.mesh_mat_list[i])
        material_list.append(Materials[mat_index])
    return material_list


def mix_mesh_material(m, material_list):
    """mix_mesh_material: calculate the mixture material of the mesh
    input:m, the mesh
    input:materials_list, a list of the materials
    return: mesh_mat, a Material represent the material of given mesh"""

    mesh_mat = Material()  # initial a material
    density = 0.0
    atom_density = 0.0
    mcnp_material_nuclide = []
    mcnp_material_atom_fraction = []
    mcnp_material_mass_fraction = []

    for i in range(len(m.mesh_mat_list)):  # fill the material
        density += material_list[i].density * m.mesh_mat_vol_fraction[i]
        atom_density += material_list[i].atom_density * \
            m.mesh_mat_vol_fraction[i]
    mesh_mat.density, mesh_mat.atom_density = density, atom_density

    # calculate the mcnp nuclide information
    for i in range(len(m.mesh_mat_list)):
        mat = material_list[i]
        fraction = m.mesh_mat_vol_fraction[i]
        for j in range(len(mat.mcnp_material_nuclide)):
            # in the list, then add the nuc data
            if mat.mcnp_material_nuclide[j] in mcnp_material_nuclide:
                # get the index of the nuc in the nuc_list
                nid = mcnp_material_nuclide.index(mat.mcnp_material_nuclide[j])
                mcnp_material_atom_fraction[nid] += mat.mcnp_material_atom_fraction[j] * fraction
                mcnp_material_mass_fraction[nid] += mat.mcnp_material_mass_fraction[j] * fraction
            # not in the list, add it into the list
            if mat.mcnp_material_nuclide[j] not in mcnp_material_nuclide:
                mcnp_material_nuclide.append(
                    mat.mcnp_material_nuclide[j])  # add it into list
                # get the index of the nuc in the nuc_list
                nid = mcnp_material_nuclide.index(mat.mcnp_material_nuclide[j])
                mcnp_material_atom_fraction.append(
                    mat.mcnp_material_atom_fraction[j] * fraction)
                mcnp_material_mass_fraction.append(
                    mat.mcnp_material_mass_fraction[j] * fraction)
    mesh_mat.mcnp_material_nuclide = mcnp_material_nuclide
    mesh_mat.mcnp_material_atom_fraction = scale_list(
        mcnp_material_atom_fraction)
    mesh_mat.mcnp_material_mass_fraction = scale_list(
        mcnp_material_mass_fraction)
    # convert it into fispact format
    mesh_mat.mat_mcnp2fispact()
    return mesh_mat


@log
def cal_mesh_material(Meshes, Materials):
    """cal_mesh_material: calculate the mesh material according to the Meshes, Cells, and Materials"""
    for m in Meshes:
        material_list = cal_mesh_material_list(
            m, Materials)  # make a materials list for this mesh
        m.mat = mix_mesh_material(m, material_list)
    return Meshes


def get_energy_index(energy, energy_group):
    """return energy index according to the energy and energy_group"""
    e_index = -1
    if energy == 'Total':
        return len(energy_group)
    else:
        energy = float(energy)
    for i in range(len(energy_group)):
        if abs(energy - energy_group[i]) / energy_group[i] < 1e-3:
            e_index = i
    if e_index == -1:
        raise ValueError(
            'energy not found in the energy group! Only 175/709 group supported!')
    return e_index


@log
def get_mesh_neutron_flux(
        Meshes,
        MCNP_MESHTAL,
        TALLY_NUMBER,
        mesh_structure,
        N_GROUP_SIZE):
    """get_mesh_neutron_flux: get the neutron flux according to the meshtal"""
    fin = open(MCNP_MESHTAL)
    data = []
    while True:
        line = fin.readline()
        if line == '':
            raise ValueError(
                'Mesh Tally Number %s not found in the file, wrong file!',
                str(TALLY_NUMBER))
        if 'Mesh Tally Number' in line and str(
                TALLY_NUMBER) in line:  # find the the given tally part
            while True:
                line = fin.readline()
                if 'Energy' in line and 'Result' in line and 'Rel Error' in line:  # read
                    while True:
                        line = fin.readline()
                        line_ele = line.split()
                        if len(line_ele) == 0:
                            break
                        data.append(line_ele)  # put all the data into the
                    break
            break
    # initial a empty list to store the neutron flux and error data
    neutron_flux, neutron_flux_error = [], []
    for i in range(len(Meshes)):
        neutron_flux.append([])
        neutron_flux_error.append([])
        for j in range(N_GROUP_SIZE + 1):
            neutron_flux[i].append(-1.0)
            neutron_flux_error[i].append(-1.0)
    # put data of each line into nuetron flux and error
    for item in data:
        energy, x, y, z, result, error = item[0], float(
            item[1]), float(
            item[2]), float(
            item[3]), float(
                item[4]), float(
            item[5])
        e_index = get_energy_index(energy, E_175)
        mesh_id = get_mesh_id([x, y, z], mesh_structure)
        neutron_flux[mesh_id][e_index] = result
        neutron_flux_error[mesh_id][e_index] = error
    # treat the total neutron flux in case of version 1.2
    for i in range(len(neutron_flux)):
        if neutron_flux[i][-1] < 0.0:
            neutron_flux[i][-1] = sum(neutron_flux[i][:-1])
            neutron_flux_error[i][-1] = sum(neutron_flux_error[i]
                                            [:-1]) / N_GROUP_SIZE
    # put the neutron flux and error data into Meshes
    for i in range(len(Meshes)):
        Meshes[i].neutron_flux = list(neutron_flux[i])
        Meshes[i].neutron_flux_error = list(neutron_flux_error[i])
    fin.close()
    return Meshes


def write_fispact_file(material, IRRADIATION_SCENARIO, MODEL_DEGREE,
        neutron_flux, file_prefix, tab4flag, endf_lib_flag,
        fispact_material_list, fispact_material_path, AIM=None):
    """write_fispact_file: write fispact file, input .i the flux .flx files
    input: material, a Material
    input: IRRADIATION_SCENARIO, the irradiation_scenario file
    input: MODEL_DEGREE, a float number of model, this used to multiply the total neutron flux
    input: neutron_flux, neutron flux of a mesh or a cell
    input: fispact_material_list, the list of the materials that defined by user to use another one
    input: fispact_material_path, the list of the materials pathes that need to use"""

    # write the input file
    file_name = ''.join([file_prefix, '.i'])
    fo = open(file_name, 'w')
    fo.write('<< ----get nuclear data---- >>\n')
    fo.write('NOHEADER\n')
    # endf lib used? ---------
    if endf_lib_flag:
        fo.write('EAFVERSION 8\n')
        fo.write('COVAR\n')
    # ------------------------
    fo.write(' '.join(['GETXS 1', str(len(neutron_flux) - 1), '\n']))
    fo.write('GETDECAY 1\n')
    fo.write('FISPACT\n')
    fo.write('* Irradiation start\n')
    fo.write('<< ----set initial conditions---- >>\n')
    # material part start
    if AIM in ['COOLANT_ACT_PRE']:
        if any(material in sublist for sublist in fispact_material_list):
            material_path = get_material_path(fispact_material_list,
                    fispact_material_path, material)
            fo.write(
                '<< ----material info. defined by user in the separate file below ---->>\n')
            fo.write(''.join(['<< ----', material_path, '---->>\n']))
            # read the files in fispact_material_list and write it here
            fin = open(material_path)
            for line in fin:
                if line.strip().split() == []:
                    continue
                fo.write(line)
    elif any(material.mat_id in sublist for sublist in fispact_material_list):
        material_path = get_material_path(fispact_material_list,
                fispact_material_path, material.mat_id)
        fo.write(
            '<< ----material info. defined by user in the separate file below ---->>\n')
        fo.write(''.join(['<< ----', material_path, '---->>\n']))
        # read the files in fispact_material_list and write it here
        fin = open(material_path)
        for line in fin:
            if line.strip().split() == []:
                continue
            fo.write(line)
    else:
        fo.write('<< ----material info. converted from MCNP output file ---->>\n')
        fo.write(
            ' '.join(['DENSITY', str(format(material.density, '.5e')), '\n']))
        fo.write(
            ' '.join(['FUEL', str(len(material.fispact_material_nuclide)), '\n']))
        for i in range(len(material.fispact_material_nuclide)
                       ):  # write nuclide and atoms information
            fo.write(' '.join([material.fispact_material_nuclide[i], str(
                format(material.fispact_material_atom_kilogram[i], '.5e')), '\n']))
    # material part end
    fo.write('MIND 1.E5\n')
    fo.write('HAZARDS\n')
    fo.write('CLEAR\n')
    if tab4flag:
        fo.write('TAB4 44\n')
    fo.write('ATWO\n')
    fo.write('HALF\n')
    fo.write('NOSTABLE\n')
    fo.write('UNCERT 2\n')
    fo.write('TOLERANCE 0 5.0E3 1.0E-4\n')
    fo.write('TOLERANCE 1 1.0E2 1.0E-4\n')
    # irradiation scenario part
    if AIM == 'COOLANT_ACT_PRE':
        fo.write(IRRADIATION_SCENARIO)
    else:
        fin = open(IRRADIATION_SCENARIO)
        for line in fin:
            line_ele = line.split()
            if len(line.strip()) == 0:  # end of the file
                #fo.write('\n')
                break
            if 'FLUX' in line:  # this is the irradiation part that defines flux
                try:
                    real_flux = float(
                        line_ele[1]) * MODEL_DEGREE / 360.0 * neutron_flux[len(neutron_flux) - 1]
                    fo.write(
                        ' '.join(['FLUX', str(format(real_flux, '.5e')), '\n']))
                except BaseException:
                    errormessage = ''.join(
                        [
                            'Neutron flux length inconsistance with the given Group number',
                            '\n',
                            'Please check the data'])
                    raise ValueError(errormessage)
            else:
                fo.write(line)
        fin.close()
    fo.write('END\n')
    fo.write('*END of RUN \n')
    fo.close()

    # write .flx file
    file_name = ''.join([file_prefix, '.flx'])
    fo = open(file_name, 'w')
    for i in range(len(neutron_flux) - 1):  # reverse the neutron flux
        fo.write(
            ''.join([format_single_output(neutron_flux[len(neutron_flux) -2 -i]), '\n']))
    fo.write('1.0\n')
    fo.write(' '.join(['Neutron energy group', str(
        len(neutron_flux) - 1), 'G, TOT = ', format_single_output(neutron_flux[-1])]))
    fo.close()


@log
def mesh_fispact_cal_pre(
        AIM,
        WORK_DIR,
        Meshes_need_cal,
        MODEL_DEGREE,
        IRRADIATION_SCENARIO,
        fispact_material_list,
        fispact_material_path):
    """fispact_cal_pre, write .flx and .i files for fispact according to the AIM"""
    # check the input data
    if AIM not in ('MESH_PRE'):  # PRE mode
        raise RuntimeError(
            'mesh_fispact_cal_pre can only called in MESH_PRE mode')

    # when writing fispact input and flx file, material, irradiation scenario (inputed),
    # model_degree (inputed), neutron_flux and prefix are required
    tab4flag = True
    endf_lib_flag = False
    if AIM == 'MESH_PRE':
        for m in Meshes_need_cal:
            file_prefix = ''.join([WORK_DIR, '/m', str(m.mesh_id)])
            material = m.mat
            neutron_flux = m.neutron_flux
            write_fispact_file(
                material,
                IRRADIATION_SCENARIO,
                MODEL_DEGREE,
                neutron_flux,
                file_prefix,
                tab4flag,
                endf_lib_flag,
                fispact_material_list,
                fispact_material_path)


@log
def mesh_post_process(Meshes, WORK_DIR, AIM, cooling_time):
    """mesh_post_process: check the data of the meshes and then output the ptrans file."""
    # check the AIM
    if AIM not in ('MESH_POST',):
        raise ValueError(
            'mesh_post_process can only be called when AIM is MESH_POST')
    # check the gamma_emit_rate of meshes
    for m in Meshes:
        if m.gamma_emit_rate.shape != (len(cooling_time), 24):
            # this mesh is not calculated, set it's data to zero
            m.gamma_emit_rate = np.zeros((len(cooling_time), 24), dtype=float)
    # write the ptrans file of mesh
    # make a new director for the output files
    dirname = ''.join([WORK_DIR, '/', 'ptrans'])
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    # check the GEOM if the meshes
    GEOM = ''
    origin = []
    axs = []
    vec = []
    if Meshes[0].geom == 'xyz':
        GEOM = 'xyz'
    if Meshes[0].geom == 'cyl':
        GEOM = 'cyl'
        origin = Meshes[0].origin
        axs = Meshes[0].axs
        vec = Meshes[0].vec
    # write content
    for intv in range(len(cooling_time)):
        filename = os.path.join(dirname, ''.joine([str(intv), '.ptrans']))
        fo = open(filename, 'w')
        # section 1: mode CELL/MESH_XYZ/MESH_CYL
        if GEOM == 'xyz':
            fo.write('MESH_XYZ\n')
        if GEOM == 'cyl':
            fo.write('MESH_CYL\n')
            line = ' '.join([str(format(origin[0], '.5e')),
                             str(format(origin[1], '.5e')),
                             str(format(origin[2], '.5e')), '\n'])
            fo.write(line)
            line = ' '.join([str(axs[0]), str(axs[1]), str(axs[2]), '\n'])
            fo.write(line)
            line = ' '.join([str(vec[0]), str(vec[1]), str(vec[2]), '\n'])
            fo.write(line)
        # section 2: number of meshes
        line = ''.join([str(len(Meshes)), '\n'])
        fo.write(line)
        # section 3: mesh geometry, packing_factor and  total gamma emit rate
        if GEOM == 'xyz':
            for m in Meshes:
                line = ' '.join([str(format(m.xmin, '.5e')), str(format(m.xmax, '.5e')),
                                 str(format(m.ymin, '.5e')), str(format(m.ymax, '.5e')),
                                 str(format(m.zmin, '.5e')), str(format(m.zmax, '.5e')),
                                 str(format(m.packing_factor, '.5e')),
                                 str(format(sum(m.gamma_emit_rate[intv, :]), '.5e'))])
                line = ''.join([line, '\n'])
                fo.write(line)
        if GEOM == 'cyl':
            for m in Meshes:
                line = ' '.join([str(format(m.rmin, '.5e')), str(format(m.rmax, '.5e')),
                                 str(format(m.zmin, '.5e')), str(format(m.zmax, '.5e')),
                                 str(format(m.tmin, '.5e')), str(format(m.tmax, '.5e')),
                                 str(format(m.packing_factor, '.5e')),
                                 str(format(sum(m.gamma_emit_rate[intv, :]), '.5e'))])
                line = ''.join([line, '\n'])
                fo.write(line)
        # section 4: photon spectra of the meshes
        for m in Meshes:
            for j in range(24):
                if j == 0:
                    line = str(format(m.gamma_emit_rate[intv, 0], '.5e'))
                else:
                    line = ' '.join(
                        [line, str(format(m.gamma_emit_rate[intv, j], '.5e'))])
            line = ''.join([line, '\n'])
            fo.write(line)


@log
def cell_fispact_cal_pre(
        AIM,
        WORK_DIR,
        Cells_need_cal,
        MODEL_DEGREE,
        IRRADIATION_SCENARIO,
        fispact_material_list,
        fispact_material_path):
    """fispact_cal_pre, write .flx and .i files for fispact according to the AIM"""
    if AIM not in (
        'CELL_ACT_PRE',
        'CELL_ACT_POST',
        'CELL_DPA_PRE',
            'CELL_DPA_POST'):
        raise RuntimeError('cell_fispact_cal_pre can only called in CELL MODE')
    tab4flag = False
    # endf libaries used, then need keyword EAFVERSION 8
    if AIM in ('CELL_DPA_PRE', 'CELL_DPA_POST'):
        endf_lib_flag = True
    else:
        endf_lib_flag = False

    for c in Cells_need_cal:
        file_prefix = ''.join([WORK_DIR, '/c', str(c.cell_id)])
        material = c.mat
        neutron_flux = c.neutron_flux
        try:
            write_fispact_file(
                material,
                IRRADIATION_SCENARIO,
                MODEL_DEGREE,
                neutron_flux,
                file_prefix,
                tab4flag,
                endf_lib_flag,
                fispact_material_list,
                fispact_material_path)
        except BaseException:
            errormessage = ' '.join(
                ['Encounter Error when writing fispact file of cell:', str(c.cell_id), '\n'])
            raise ValueError(errormessage)

def get_irr_and_cooling_times(part_name, COOLANT_FLOW_PARAMETERS):
    """
    Get irradiation time and cooling times according to part name and
    coolant flow parameters.
    """
    df = pd.read_csv(COOLANT_FLOW_PARAMETERS)
    cols = df.columns
    part_info = np.array(df.loc[df['Parts'] == part_name]).flatten()
    irr_time = float(part_info[2])
    cooling_times_s = []
    for i in range(3, len(cols), 2):
        cooling_times_s.append(part_info[i])
    cooling_times = [float(x) for x in cooling_times_s]
    return irr_time, cooling_times

def construct_irradiation_scenario(irr_time, cooling_times, irr_total_flux):
    """
    Construct FISPACT-II format irradiation scenario.
    """
    irr_snr = '<<-----------Irradiation Scenario--------------->>\n'
    irr_snr += 'FLUX ' + format_single_output(irr_total_flux) + '\n'
    irr_snr += 'TIME ' + format_single_output(irr_time) + ' SECS ATOMS\n'
    irr_snr += 'ZERO\n'
    irr_snr += '<<-----------End of Irradiation --------------->>\n'
    irr_snr += '<<-----------Cooling Times--------------->>\n'
    for i, ct in enumerate(cooling_times):
        irr_snr += 'TIME ' + format_single_output(ct) + ' SECS ATOMS\n'
    return irr_snr


def calc_part_irradiation_scenario(part_name, COOLANT_FLOW_PARAMETERS,
        FLUX_MULTIPLIER, n_total_flux, MODEL_DEGREE=360.0):
    """
    Calculate the irradiation scenario according to the coolant flow parameters.

    Parameters:
    -----------
    part_name: str
        The name of the part.
    COOLANT_FLOW_PARAMETERS: str
        The file path of the coolant flow parameters.
    FLUX_MULTIPLIER: float
        The total neutron emitting rate of the fusion device.
        Eg: for CFETR 200 MW case, the value is 7.09e19.
    n_total_flux: float
        Total flux of the part.equal_cell.
    MODEL_DEGREE: float
        Default 360.

    Returns:
    --------
    irradiation_scenario: str
    """
    irr_time, cooling_times = get_irr_and_cooling_times(part_name, COOLANT_FLOW_PARAMETERS)
    irr_total_flux = MODEL_DEGREE / 360.0 * FLUX_MULTIPLIER * n_total_flux
    irradiation_scenario = construct_irradiation_scenario(irr_time, cooling_times, irr_total_flux)
    return irradiation_scenario

@log
def parts_fispact_cal_pre(AIM, WORK_DIR, Parts, MODEL_DEGREE,
        fispact_material_list, fispact_material_path, COOLANT_FLOW_PARAMETERS,
        FLUX_MULTIPLIER):
    """fispact_cal_pre, write .flx and .i files for fispact according to the AIM"""
    tab4flag = False
    endf_lib_flag = False
    # endf libaries used, then need keyword EAFVERSION 8
    for p in Parts:
        file_prefix = os.path.join(WORK_DIR, 'p' + p.name)
        neutron_flux = p.equal_cell.neutron_flux
        material = p.equal_cell.name
        IRRADIATION_SCENARIO = calc_part_irradiation_scenario(p.name,
                COOLANT_FLOW_PARAMETERS, FLUX_MULTIPLIER, p.equal_cell.neutron_flux[-1], MODEL_DEGREE)
        try:
            write_fispact_file(material, IRRADIATION_SCENARIO, MODEL_DEGREE,
                    neutron_flux, file_prefix, tab4flag, endf_lib_flag,
                    fispact_material_list, fispact_material_path, AIM=AIM)
        except BaseException:
            errormessage = ' '.join(
                ['Encounter Error when writing fispact file of part: ', p.name, '\n'])
            raise ValueError(errormessage)


def get_cell_ids_sub(value):
    """get_cells_id_sub, used to interpret a string of cell list to int list of cell ids"""
    cell_ids_sub = []
    if '~' in value:  # this string need to expand
        cell_ele = value.split('~')
        pre_cell, post_cell = int(cell_ele[0]), int(cell_ele[-1])
        for i in range(pre_cell, post_cell + 1, 1):
            cell_ids_sub.append(i)
    else:
        cell_ids_sub.append(int(value))
    return cell_ids_sub


def get_cell_ids(value):
    """get_cell_ids, used to get cell ids from the context read from PART_CELL_LIST
    input: value, this is a list of string, that need to interpret to cell ids
    return: a list of int that represent the cell ids"""
    cell_ids = []
    for item in value:
        cell_ids_sub = get_cell_ids_sub(item)
        cell_ids.extend(cell_ids_sub)
    return cell_ids


def get_part_index(Parts, p):
    """get the index of part p in the Parts"""
    part_index = -1
    for i in range(len(Parts)):
        if p.name == Parts[i].name:  # found it
            part_index = i
    # check value
    if part_index == -1:
        raise RuntimeError('part %s not found in the Parts', p.name)
    return part_index


def match_cell_part(part, Cells, cell_ids):
    """ put the cells defined int the cell_ids to the part"""
    for item in cell_ids:
        cid = get_cell_index(Cells, item)
        part.part_cell_list.append(Cells[cid])
    return part


@log
def get_part(Cells, PART_CELL_LIST, COOLANT_FLOW_PARAMETERS=None):
    """get_part, read PART_CELL_LIST and form the Parts"""
    Parts = []
    part_name = ''
    pid = -1
    if PART_CELL_LIST == '':  # PART_CELL_LIST not given
        return Parts
    fin = open(PART_CELL_LIST, 'r')
    line = ' '
    while line != '':
        try:
            line = fin.readline()
        except:
            line = fin.readline().encode('ISO-8859-1')
        line_ele = line.split()
        if is_blank_line(line):  # this is a empty line
            continue
        if is_comment(line):  # this is a comment line
            continue
        # otherwise, this is a line that contains information
        if line[:5] == '     ':  # this is a continue line
            cell_ids = get_cell_ids(line_ele)
            Parts[pid] = match_cell_part(Parts[pid], Cells, cell_ids)
        else:  # this line contains a part name
            part_name = line_ele[0]
            part = Part()
            part.name = part_name
            Parts.append(part)
            cell_ids = get_cell_ids(line_ele[1:])
            pid = get_part_index(Parts, part)
            Parts[pid] = match_cell_part(Parts[pid], Cells, cell_ids)
    fin.close()
    # init equal_cell for each part
    for i, p in enumerate(Parts):
        p.init_equal_cell()
    # read part mass flow rate if COOLANT_FLOW_PARAMETERS is provided
    if COOLANT_FLOW_PARAMETERS is not None:
        df = pd.read_csv(COOLANT_FLOW_PARAMETERS)
        for i, p in enumerate(Parts):
            part_info = np.array(df.loc[df['Parts'] == p.name]).flatten()
            p.mass_flow_rate = float(part_info[1])
    return Parts

@log
def get_nodes(COOLANT_FLOW_PARAMETERS):
    """Get nodes, read COOLNAT_FLOW_PARAMETERS to define nodes"""
    nodes = []
    df = pd.read_csv(COOLANT_FLOW_PARAMETERS)
    cols = df.columns
    for i in range(3, len(cols), 2):
        node_name = cols[i].split('(s)')[0].strip()
        node = Part()
        node.name = node_name
        node.init_equal_cell()
        node.node_part_count = list(np.array(df[node_name + ' counts']))
        nodes.append(node)
    return nodes

@log
def get_cell_need_cal(AIM, Parts, Cells):
    """calculate the cell need to cal according to the AIM and Parts
        input: AIM, the aim of the run
        input: Parts, the parts that need to run
        input: Cells, the lists of all the cells in the mcnp model
        return: cell_need_cal, a list of cells that need to perform FISPACt run
        CONDITION 1: if the AIM is 'CELL_DPA_PRE/POST' or the 'CELL_ACT_PRE/POST', then the Parts must be given
               and then the cell_need_cal will be the cells listed in the Parts."""
    # judge the condition
    cell_need_cal = []
    if AIM in ('CELL_DPA_PRE', 'CELL_DPA_POST', 'CELL_ACT_PRE',
               'CELL_ACT_POST'):  # Parts should be given
        if len(Parts) == 0:
            raise ValueError(
                "if the AIM is 'CELL_DPA_PRE/POST' or the 'CELL_ACT_PRE/POST', then the Parts must be given")
        else:
            for p in Parts:
                for c in p.part_cell_list:
                    if c not in cell_need_cal:
                        cell_need_cal.append(c)
    return cell_need_cal


@log
def get_mesh_need_cal(Meshes):
    """get_mesh_need_cal: get meshes that need to do the fispact calculate
    input:Meshes, the list of all the meshes
    return: Meshes_need_cal, the list of meshes that need calculate
    GUIDE: meshes that satisfy two condition need cal
    1. non-void material, use mat.density to judge
    2. non-zero total neutron flux, use neutron_flux to judge"""
    Meshes_need_cal = []
    for m in Meshes:
        if m.mat.density > 0 and m.neutron_flux[len(m.neutron_flux) - 1] > 0:
            Meshes_need_cal.append(m)
    return Meshes_need_cal


@log
def check_fispact_output_files(itemlist, WORK_DIR, AIM):
    """check_fispact_output_files, check whether all the output files needed are available
    input: itemlist, a list of cells/meshes that contains all the items needed to calculate
    WORK_DIR, the working directory
    content, what files are checked, a tuple of '.out','.tab4'
    raise a error when some file are missing, return nothing if all the files are OK."""
    if AIM not in ['CELL_ACT_POST', 'CELL_DPA_POST', 'COOLANT_ACT_POST']:
        raise RuntimeError(
                'check_fispact_output_files not support AIM: {0}'.format(AIM))
    if AIM in ['CELL_ACT_POST', 'CELL_DPA_POST', 'COOLANT_ACT_POST']:
        content = ('.out',)
    for item in itemlist:
        for cnt in content:
            if isinstance(item, Cell):
                check_file_name = os.path.join(WORK_DIR, 'c'+str(item.cell_id)+cnt)
            if isinstance(item, Part):
                check_file_name = os.path.join(WORK_DIR, 'p'+item.name+cnt)
            try:
                f = open(check_file_name)
                f.close()
            except IOError:
                error_message = ''.join(
                    ['File:', check_file_name, ' not accessible'])
                raise RuntimeError(error_message)


def contain_fispact_nuc_flag(line):
    """return True if the line contains a fispact_nuc_flag: ?,&,*,>
    otherwise, return False"""
    for item in fispact_nuc_flag:
        if item in line:
            return True
    return False


def get_fispact_out_line_info(line):
    """return nuc, act,dose_rate, ci, half_life of a line
    # a line of fispact output of nuclides, contains several information, a sample line like below
    #  NUCLIDE        ATOMS         GRAMS        Bq       b-Energy    a-Energy   g-Energy    DOSE RATE   INGESTION  INHALATION   CLEARANCE     Bq/A2     HALF LIFE
    #                                                    kW          kW         kW         Sv/hr      DOSE(Sv)    DOSE(Sv)     INDEX       Ratio      seconds
    #H   3       6.72510E+21   3.368E-02   1.198E+13   1.095E-05   0.00E+00   0.000E+00   0.000E+00   5.032E+02   3.115E+03   1.198E+08   2.995E-01   3.891E+08
    #K  40     > 5.85721E+17   3.887E-05   1.017E+01   7.387E-16   0.00E+00   2.538E-16   3.850E-10   6.306E-08   2.136E-08   1.017E-03   1.130E-11   3.992E+16
    #Rh104m      2.85761E+14   4.931E-08   7.607E+11   1.051E-05   0.00E+00   5.548E-06   7.358E-01   6.694E+00   6.009E+00   4.226E+07   3.803E+01   2.604E+02
    #Rh104m    > 2.85761E+14   4.931E-08   7.607E+11   1.051E-05   0.00E+00   5.548E-06   7.358E-01   6.694E+00   6.009E+00   4.226E+07   3.803E+01   2.604E+02
    # if a line doesn't contain a flag of ?,&,*,>, then the nuclide should be in the first one or two element
    # if a first element of a line contains less than 3 character, that means the nuclide distributed in two parts
    # there are 4 kinds of conditons,
    # case A: nuclide name in two part, no flag
    # case B: nuclide name in two part, with flag
    # case C: nuclide name in one part, no flag
    # case D: nuclide name in one part, with flag
    checked in 20170802, by Xiaokang Zhang"""
    line_ele = line.split()
    if len(line_ele) < 12:  # this line must be wrong
        errormessage = ''.join(
            ['line:', line, 'have wrong information, check!'])
        raise ValueError(errormessage)
    if len(line_ele[0]) < 3 and contain_fispact_nuc_flag(
            line) == False:  # case A
        nuc = ''.join([line_ele[0], line_ele[1]])
        act, contact_dose, ci, half_life = map(
            float, [line_ele[4], line_ele[8], line_ele[11], line_ele[13]])
        decay_heat = sum(map(float, [line_ele[5], line_ele[6], line_ele[7]]))
    if len(line_ele[0]) < 3 and contain_fispact_nuc_flag(line):  # case B
        nuc = ''.join([line_ele[0], line_ele[1]])
        act, contact_dose, ci, half_life = map(
            float, [line_ele[5], line_ele[9], line_ele[12], line_ele[14]])
        decay_heat = sum(map(float, [line_ele[6], line_ele[7], line_ele[8]]))
    if len(line_ele[0]) >= 3 and contain_fispact_nuc_flag(
            line) == False:  # case C
        nuc = line_ele[0]
        act, contact_dose, ci, half_life = map(
            float, [line_ele[3], line_ele[7], line_ele[10], line_ele[12]])
        decay_heat = sum(map(float, [line_ele[4], line_ele[5], line_ele[6]]))
    if len(line_ele[0]) >= 3 and contain_fispact_nuc_flag(line):  # case D
        nuc = line_ele[0]
        act, contact_dose, ci, half_life = map(
            float, [line_ele[4], line_ele[8], line_ele[11], line_ele[13]])
        decay_heat = sum(map(float, [line_ele[5], line_ele[6], line_ele[7]]))
    return nuc, act, contact_dose, ci, half_life, decay_heat



def found_interval_line(line, interval_list):
    """found_interval_line: judege whether this line is the line we need according to the interval list"""
    found_flag = False
    if 'TIME INTERVAL' not in line or 'ELAPSED TIME IS' not in line:
        return False
    else:
        # judge the interval in the interval_list in line?
        for interval in interval_list:
            if ''.join([' ', str(interval), ' ']) in line:
                found_flag = True
                return found_flag
    return found_flag


def check_cooling_start(line, cooling_start=False):
    """
    Check wether the cooling started.
    """
    if "of steps" in line:
        return True
    else:
        return cooling_start

def read_fispact_out_act(c, filename, interval_list):
    """read_fispact_out_act, read the act information,
     include: nuclide, half_life, specific activity, decay heat density, ci, contact dose.
    Parameters:
    c : cell
    filename: FISPACT output file of this cell
    interval_list : clumulated cooling times
     """
    # read the file first time to get the nuclide and half_life
    nuclide = []
    half_life = []
    fin = open(filename)
    while True:
        line = fin.readline()
        if 'fispact run time' in line:  # end of the file information
            break
        if found_interval_line(line, interval_list):  # found a interval
            line = fin.readline()
            line = fin.readline()
            line = fin.readline()
            while True:
                line = fin.readline()
                if 'TOTAL NUMBER' in line:  # found the end of this interval part
                    break
                nuc, act, contact_dose, ci, hf_lf, dh = get_fispact_out_line_info(
                    line)
                if nuc not in nuclide:
                    nuclide.append(nuc)
                    half_life.append(hf_lf)
    fin.close()
    c.nuclide = nuclide
    c.half_life = half_life
    # read the information in each interval, then get the  act, contact_dose,
    # ci of each nuclide
    c.act = np.resize(c.act, (len(interval_list), len(nuclide)))
    c.contact_dose = np.resize(
        c.contact_dose, (len(interval_list), len(nuclide)))
    c.decay_heat = np.resize(c.decay_heat, (len(interval_list), len(nuclide)))
    c.ci = np.resize(c.ci, (len(interval_list), len(nuclide)))
    c.total_alpha_act = np.resize(c.total_alpha_act, (len(interval_list)))
    for intv in range(len(interval_list)):
        fin = open(filename)
        while True:
            line = fin.readline()
            if is_interval_in_line(interval_list[intv], line):
                line = fin.readline()
                line = fin.readline()
                line = fin.readline()
                while True:
                    line = fin.readline()
                    if 'TOTAL NUMBER' in line:  # end of this interval of nuclide information
                        line = fin.readline()
                        line = fin.readline()
                        line = fin.readline()
                        line = fin.readline()
                        line = fin.readline()
                        if 'ALPHA BECQUERELS' in line:
                            c.total_alpha_act[intv] = get_total_alpha_act(line)
                        else:
                            raise ValueError("line does not contain total alpha act")
                        break
                    nuc, act, contact_dose, ci, hf_lf, dh = get_fispact_out_line_info(
                        line)
                    nuc_index = nuclide.index(nuc)
                    c.act[intv][nuc_index] = act
                    c.decay_heat[intv][nuc_index] = dh
                    c.contact_dose[intv][nuc_index] = contact_dose
                    c.ci[intv][nuc_index] = ci
                break
        fin.close()

def read_fispact_out_sdr(c, filename, interval_list):
    """read_fispact_out_sdr, read the sdr information of a cell or a mesh
    include: gamma emit rate at different cooling time"""
    c.gamma_emit_rate = np.resize(c._gamma_emit_rate, (len(interval_list), 24))
    for intv in range(len(interval_list)):
        fin = open(filename)
        while True:
            line = fin.readline()
            if is_interval_in_line(interval_list[intv], line):
                while True:
                    line = fin.readline()
                    if 'GAMMA SPECTRUM AND ENERGIES' in line:
                        line = fin.readline()
                        line = fin.readline()
                        line = fin.readline()
                        line = fin.readline()
                        line = fin.readline()
                        line = fin.readline()
                        for i in range(24):  # read 24 group photon emmit rate
                            line = fin.readline()
                            line_ele = line.split()
                            c.gamma_emit_rate[intv][i] = str2float(line_ele[-1])
                        break # end of gamma emit rate data
                break
        fin.close()

def read_fispact_out_dpa(c, filename, interval_list):
    """read_fispact_out_dpa, read the dpa information of a cell
    include:dpa, and gas production"""
    # judge the interval_list
    if len(interval_list) != 0:
        errormessage = ''.join(['IRRADIATION_SCENARIO ERROR:\n',
                                '1. Only one pulse allowed, and it must be a FPY (1 year).\n',
                                '2. No cooling time allowed.'])
        raise ValueError(errormessage)
    # read the dpa information
    fin = open(filename)
    H_pro = 0.0
    He_pro = 0.0
    while True:
        line = fin.readline()
        line_ele = line.split()
        if line == '':  # end of the file, but not found the key word
            raise ValueError(
                'Total Displacement Rate (n,Dtot ) not found in the file, check')
        if 'Total Displacement Rate (n,Dtot )' in line:
            c.dpa = float(line_ele[-2])
        if 'APPM OF He  4' in line:
            He_pro += float(line_ele[-1])
        if 'APPM OF He  3' in line:
            He_pro += float(line_ele[-1])
        if 'APPM OF H   3' in line:
            H_pro += float(line_ele[-1])
        if 'APPM OF H   2' in line:
            H_pro += float(line_ele[-1])
        if 'APPM OF H   1' in line:
            H_pro += float(line_ele[-1])
        if 'COMPOSITION  OF  MATERIAL  BY  ELEMENT' in line:
            break
    fin.close()
    c.He_production = He_pro
    c.H_production = H_pro

@log
def get_interval_list(filename, cooling=True):
    """get_interval_list, returns the cooling interval number of the irradiation scenario.
                          it could used to check both cell and mesh files"""
    ## check the mode CELL/MESH
    # start to get the information
    interval_list = []
    cooling_start = False
    with open(filename) as fin:
        #file_interval_number = 0
        for line in fin:
            if line == '':
                errormessage = ''.join(
                    ['File: ', filename, ' does not have interval message, incomplete file!'])
                raise ValueError(errormessage)
            cooling_start = check_cooling_start(line, cooling_start)
            if 'TIME INTERVAL' in line and 'ELAPSED TIME IS' in line:
                if cooling:
                    if 'COOLING TIME' in line and cooling_start:
                        interval_list.append(get_interval_from_line(line))
                else:
                    interval_list.append(get_interval_from_line(line))
            if 'fispact run time=' in line:
                break

    return interval_list


def check_interval_list(item_list, WORK_DIR):
    """
    Check the interval lists in the different output files.
    Parameters:
    item_list: list of cells or meshes
    """
    # check the mode CELL/PART
    mode = ''
    if (len(item_list) == 0):
        raise ValueError(
            'numbers of files to check is zero, there must be error, check!')
    if isinstance(item_list[0], Cell):
        mode = 'CELL'
        cooling = True
    if isinstance(item_list[0], Part):
        mode = 'PART'
        cooling = False
    if (mode == ''):
        raise ValueError('item_list to be checked not belong to Cell or Part')

    ref_interval_list = []
    # read the interval list for each item
    for i, item in enumerate(item_list):
        if mode == 'CELL':
            filename = os.path.join(WORK_DIR, ''.join(['c', str(item.cell_id), '.out']))
        if mode == 'PART':
            filename = os.path.join(WORK_DIR, ''.join(['p', item.name, '.out']))
        if i == 0:
            ref_interval_list = get_interval_list(filename)
            ref_filename = filename
        interval_list = get_interval_list(filename)
        if interval_list != ref_interval_list:
            raise ValueError("File {0} has different interval list from the {1}".format(filename, ref_filename))
    # no different found, get cooling interval
    interval_list = get_interval_list(filename, cooling=cooling)
    return interval_list
         
@log
def read_fispact_output_cell(Cells_need_cal, WORK_DIR, AIM, cooling_time_cul):
    """read_fispact_output_act: read the fispact output file to get activation information of cells
    input: Cells_need_cal, list a cells that need to calculate and analysis
    input: WORK_DIR, the working director
    return: Cells_need_cal, changed list of cells"""
    interval_list = check_interval_list(Cells_need_cal, WORK_DIR)
    print('     the intervals need to read are {0}'.format(interval_list))
    for c in Cells_need_cal:
        print('       reading cell {0} start'.format(c.cell_id))
        if AIM == 'CELL_ACT_POST':  # read output information
            filename = os.path.join(WORK_DIR, ''.join(['c', str(c.cell_id), '.out']))
            read_fispact_out_act(c, filename, interval_list)
        if AIM == 'CELL_DPA_POST':  # read DPA information
            filename = os.path.join(WORK_DIR, ''.join(['c', str(c.cell_id), '.out']))
            read_fispact_out_dpa(c, filename, interval_list)

@log
def read_fispact_output_part(Parts, WORK_DIR, AIM):
    """read_fispact_output_part: read the fispact output file to get
    activation information of parts in PHTS.

    Parameters:
    -----------
    Parts:  list of parts
        Parts that need to calculate and analysis
    WORK_DIR: string
        The working director

    Returns:
    --------
    Parts:
        Changed list of parts
    """
    interval_list = check_interval_list(Parts, WORK_DIR)
    print('     the intervals need to read are {0}'.format(interval_list))
    for i, p in enumerate(Parts):
        print('       reading part {0} start'.format(p.name))
        if AIM == 'COOLANT_ACT_POST':  # read output information
            filename = os.path.join(WORK_DIR, ''.join(['p', p.name, '.out']))
            read_fispact_out_act(p.equal_cell, filename, interval_list)
            read_fispact_out_sdr(p.equal_cell, filename, interval_list)

@log
def read_fispact_output_mesh(Meshes_need_cal, WORK_DIR, AIM, cooling_time):
    """read_fispact_output_mesh: read the tab4 files of meshes to get the gamma emit rate of the meshes
    input: Meshes_need_cal, a list of meshes that need to calculate and analysis
    input: WORK_DIR, the working director
    input: AIM, it must be MESH_POST
    input: cooling time, the cooling interval times
    return: Meshes_need_cal, changed list of meshes"""
    # check the AIM
    if AIM not in ('MESH_POST',):
        raise ValueError(
            'read_fispact_output_mesh can only be called when AIM is MESH_POST')

    interval_list = get_interval_list(Meshes_need_cal, WORK_DIR, cooling_time)
    print('     the interval need read is {0}'.format(interval_list))
    for m in Meshes_need_cal:
        print('       reading mesh {0} start'.format(m.mesh_id))
        filename = ''.join([WORK_DIR, '/m', str(m.mesh_id), '.tab4'])
        m = read_fispact_out_sdr(m, filename, interval_list)
    return Meshes_need_cal


def cell_act_post_process(Parts, WORK_DIR, MODEL_DEGREE, AIM,
        cooling_time_cul, rws=None):
    """
    cell_act_post_process: treat the parts, analysis the data and output results

    Parameters:
    -----------
    ...
    rws: RadwasteStandard, optional
        Radwsate standard used.
    """
    # first, merge the cells in the part to get the euqal_cell
    if AIM in ('CELL_ACT_POST', 'CELL_DPA_POST'):
        for p in Parts:
            p.merge_cell(AIM)

    # if the AIM is CELL_ACT_POST, then there should perform analysis
    if AIM == 'CELL_ACT_POST':
        for p in Parts:
            p.part_act_analysis(AIM, rws=rws)
    # if the AIM is CELL_DPA_POST, don't do anything
    # output the data
    for p in Parts:
        p.output_data(WORK_DIR, MODEL_DEGREE, AIM, cooling_time_cul=cooling_time_cul, rws=rws)
        
def coolant_act_post_process(Parts, nodes, WORK_DIR, MODEL_DEGREE, AIM):
    """
    coolant_act_post_process: treat the parts and coolant, analysis the data
    and output results
    """
    # merge nodes data
    for i, node in enumerate(nodes):
        merge_node_parts(node, Parts, i)

    # output the data
    for p in Parts:
        p.output_data(WORK_DIR, MODEL_DEGREE, AIM)
    for node in nodes:
        node.output_data(WORK_DIR, MODEL_DEGREE, AIM)
 
def is_close(a, b, rel_tol=1e-9, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def is_float(s):
    """
    This function checks whether a string can be converted as a float number.
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_cooling_time_in_line(ct, line):
    """
    Check whether the cooling time (ct) in line.
    """
    if  ('TIME INTERVAL' not in line) or ('COOLING TIME' not in line) or ('ELAPSED TIME' not in line):
        return False
    else:
        elapsed_time = get_elapsed_time_from_line(line)
        if is_close(elapsed_time, ct):
            return True
        else:
            return False


def get_elapsed_time_from_line(line):
    """
    Get the elapsed time (s) for a line contain 'ELAPSED TIME IS'.
    """
    ls = line.strip().split('*')
    ls = [i for i in ls if (i and i != ' ')]
    elapsed_time = ls[-1].strip().split('ELAPSED TIME IS')[-1].strip()
    elapsed_time = cooling_time_sec(elapsed_time.split()[0], elapsed_time.split()[-1])
    return elapsed_time


def get_interval_from_line(line):
    """
    Get interval index (an integer number) from line.
    """
    ls = line.strip().split('*')
    ls = [i for i in ls if  (i and i != ' ')]
    interval = ls[1].strip().split('TIME INTERVAL')[-1].strip()
    return int(interval)

def is_interval_in_line(interval, line):
    """Check whether an interval number in line."""
    if  ('TIME INTERVAL' not in line) or ('ELAPSED TIME' not in line):
        return False
    if get_interval_from_line(line) == interval:
        return True
    else:
        return False

def is_short_live(half_life):
    """
    Check whether the nuclide is short live (half live <= 30 years) nuclide.
    """
    # input check
    if not isinstance(half_life, float):
        raise ValueError("half_life must be a float")
    if half_life < 0:
        raise ValueError("half_life < 0, invalide")
    # 30 year 
    threshold = 60.0 * 60 * 24 * 365.25 * 30
    if half_life <= threshold:
        return True
    else:
        return False

def get_total_alpha_act(line):
    """
    Read the total alpha activity from line.
    """
    ls = line.strip().split()
    alpha_act = str2float(ls[4])
    return alpha_act

def get_material_path(mat_chain_list, path_list, mat_id):
    """
    Find the material path to replace.
    """
    for i, item in enumerate(mat_chain_list):
        if mat_id in item:
            return path_list[i]
    raise ValueError("Material path not found")

def check_material_list(mat_chain_list, AIM=None):
    """
    Check material list.
    Raise ValueError when these happens:
    - mat_id is not int.
    - mat_id is negtive. (mat_id could be 0, enable He to replace it)
    - mat_id is shown in more than one sublist of mat_chain_list.
    """

    extend_list = []
    # check type
    for i, sublist in enumerate(mat_chain_list):
        for j, item in enumerate(sublist):
            if AIM in ['COOLANT_ACT_PRE', 'COOLANT_ACT_POST']:
                if not isinstance(item, str):
                    raise ValueError("part name {0} has wrong type or value.".format(str(item)))
            else:
                if not isinstance(item, int) or item < 0:
                    raise ValueError("mat_id {0} has wrong type or value.".format(str(item)))
        extend_list.extend(sublist)

    # check repeat
    extend_set = set(extend_list)
    if len(extend_set) != len(extend_list):
        # there is duplicate in the list
        for i, item in enumerate(extend_list):
            count = extend_list.count(item)
            if count > 1:
                raise ValueError("mat_id {0} defined more than once.".format(str(item)))
    return True
   
def merge_node_parts(node, parts, node_index):
    """
    Merge the data of different parts to node according to cooling interval.
    The merged data are stored in node.equal_cell.
    """
    # get the total mass flow rate
    for i, p in enumerate(parts):
        node.mass_flow_rate += p.mass_flow_rate * node.node_part_count[i]
    # treat the nuclide and half-life
    for i, p in enumerate(parts):
        for j, nuc in enumerate(p.equal_cell.nuclide):
            if nuc in node.equal_cell.nuclide:
                pass
            else:
                # add the nuc into node
                node.equal_cell.nuclide.append(nuc)
                node.equal_cell.half_life.append(p.equal_cell.half_life[j]) 
    # treat the act, decay heat, contact_dose and ci
    NUC = len(node.equal_cell.nuclide)
    INTV = len(parts[0].equal_cell.act)
    node.equal_cell.act = np.resize(node.equal_cell.act, (1, NUC))
    node.equal_cell.total_alpha_act = np.resize(node.equal_cell.total_alpha_act, (INTV-1))
    node.equal_cell.decay_heat = np.resize(node.equal_cell.decay_heat, (1, NUC))
    node.equal_cell.contact_dose = np.resize(node.equal_cell.contact_dose, (1, NUC))
    node.equal_cell.ci = np.resize(node.equal_cell.ci, (1, NUC))
    node.equal_cell.gamma_emit_rate = np.resize(node.equal_cell.gamma_emit_rate, (1, 24))
    # merge the data
    for i, p in enumerate(parts):
        for j, nuc in enumerate(p.equal_cell.nuclide):
            nid = node.equal_cell.nuclide.index(nuc)
            node.equal_cell.act[0][nid] += p.equal_cell.act[node_index+1][j] * (p.mass_flow_rate*node.node_part_count[i]/node.mass_flow_rate) # unit: Bq/kg
            node.equal_cell.decay_heat[0][nid] += p.equal_cell.decay_heat[node_index+1][j] * (p.mass_flow_rate*node.node_part_count[i]/node.mass_flow_rate) # kW/kg
            node.equal_cell.contact_dose[0][nid] += p.equal_cell.contact_dose[node_index+1][j] * (p.mass_flow_rate*node.node_part_count[i]/node.mass_flow_rate)  # Sv/h
            node.equal_cell.ci[0][nid] += p.equal_cell.ci[node_index+1][j] * (p.mass_flow_rate*node.node_part_count[i]/node.mass_flow_rate) # 
        for intv in range(INTV-1):
            node.equal_cell.total_alpha_act[intv] += p.equal_cell.total_alpha_act[node_index+1] * (p.mass_flow_rate*node.node_part_count[i]/node.mass_flow_rate) # kW/kg
        for eb in range(24):
            node.equal_cell.gamma_emit_rate[0][eb] += p.equal_cell.gamma_emit_rate[node_index+1][eb] * (p.mass_flow_rate*node.node_part_count[i]/node.mass_flow_rate) # 

def get_nuc_treatments(value):
    """
    Get list of the [nuc, treatment].
    """
    nuc_treatments = []
    for i, item in enumerate(value):
        nuc = item.split()[0]
        treatment = float(item.split()[1])
        nuc_treatments.append([nuc, treatment])
    return nuc_treatments

def get_cell_nuc_treatments(NUC_TREATMENT):
    """
    Read the file NUC_TREATMENT and get information.
    
    Parameters:
    -----------
    NUC_TREATMENT: str
        The filename of NUC_TREATMENT.

    Returns:
    --------
    cell_list: list
        List of the cells need to treat.
    treatments: list of list
        List of treatments. Eg.: [['H3', 0.001], ['C14', 0.01']]
    """

    cell_nuc_treatments = []
    fin = open(NUC_TREATMENT, 'r')
    line = ' '
    while line != '':
        try:
            line = fin.readline()
        except:
            line = fin.readline().encode('ISO-8859-1')
        if is_blank_line(line):  # this is a empty line
            continue
        if is_comment(line):  # this is a comment line
            continue
        line_ele = line.split(',')
        # otherwise, this is a line that contains information
        cell_ids = get_cell_ids(line_ele[0].split())
        nuc_treatments = get_nuc_treatments(line_ele[1:])
        # put the pair: cell, nuc, treatment to list
        for i, c in enumerate(cell_ids):
            for j, n_t in enumerate(nuc_treatments):
                cell_nuc_treatments.append([c, n_t[0], n_t[1]])
    fin.close()
    return cell_nuc_treatments


def treat_nuc(cells, NUC_TREATMENT):
    """
    Treat the nuclide in cells. Such as extract the H3 by a factor of 99.9%.
    """
    if NUC_TREATMENT == '':
        return cells
    cell_nuc_treatments = get_cell_nuc_treatments(NUC_TREATMENT)
    for i, cnt in enumerate(cell_nuc_treatments):
        cid = get_cell_index(cells, cnt[0]) # find cell index
        nid = cells[cid].nuclide.index(cnt[1]) # find nuc index
        for intv in range(len(cells[cid].act)):
            cells[cid].act[intv, nid] = cells[cid].act[intv, nid] * cnt[2]
            cells[cid].decay_heat[intv, nid] = cells[cid].decay_heat[intv, nid] * cnt[2]
            cells[cid].contact_dose[intv, nid] = cells[cid].contact_dose[intv, nid] * cnt[2]
            cells[cid].ci[intv, nid] = cells[cid].ci[intv, nid] * cnt[2]
    return cells

def natf_run():
    # first check the input file to get running information
    input_filename = "input"
    check_input(filename=input_filename)
    config = ConfigParser.ConfigParser()
    config.read(input_filename)
    # general
    WORK_DIR = config.get('general', 'WORK_DIR')
    AIM = config.get('general', 'AIM')
    
    # [mcnp]
    MCNP_INPUT = os.path.join(WORK_DIR, config.get('mcnp', 'MCNP_INPUT'))
    MCNP_OUTPUT = os.path.join(WORK_DIR, config.get('mcnp', 'MCNP_OUTPUT'))
    CONTINUE_OUTPUT = None
    try:
        CONTINUE_OUTPUT = config.get('mcnp', 'CONTINUE_OUTPUT')
        if CONTINUE_OUTPUT != '':
            CONTINUE_OUTPUT = os.path.join(WORK_DIR, config.get('mcnp', 'CONTINUE_OUTPUT'))
    except:
        pass

    # mcnp.tally_number
    TALLY_NUMBER = config.getint('mcnp', 'TALLY_NUMBER')
    # mcnp.n_group_size
    N_GROUP_SIZE = config.getint('mcnp', 'N_GROUP_SIZE')
    
    # [coolant_flow]
    if AIM in ['COOLANT_ACT_PRE', 'COOLANT_ACT_POST']:
        COOLANT_FLOW_PARAMETERS = os.path.join(WORK_DIR,
                config.get('coolant_flow', 'COOLANT_FLOW_PARAMETERS'))
        FLUX_MULTIPLIER = float(config.get('coolant_flow', 'FLUX_MULTIPLIER'))
    
    # [fispact]
    # fispact.fispact_material_list, optional
    try:
        FISPACT_MATERIAL_LIST = config.get('fispact', 'FISPACT_MATERIAL_LIST')
        if FISPACT_MATERIAL_LIST != '':
            FISACT_MATERIAL_LIST = os.path.join(WORK_DIR, FISPACT_MATERIAL_LIST)
    except:
        FISPACT_MATERIAS_LIST = ''
    
    try:
        NUC_TREATMENT = config.get('fispact', 'NUC_TREATMENT')
    except:
        NUC_TREATMENT = ''
    # fispact.irradiation_scenario, required in CELL_ACT and CELL_DPA mode
    if AIM in ['CELL_ACT_PRE', 'CELL_ACT_POST', 'CELL_DPA_PRE', 'CELL_DPA_POST']:
        IRRADIATION_SCENARIO = os.path.join(WORK_DIR,
                config.get('fispact', 'IRRADIATION_SCENARIO'))
    
    # [model], required
    PART_CELL_LIST = os.path.join(WORK_DIR,
            config.get('model', 'PART_CELL_LIST'))
    # model.model_degree, optional
    try:
        MODEL_DEGREE = float(config.get('model', 'MODEL_DEGREE'))
    except:
        MODEL_DEGREE = 360.0
    
    # [radwaste] standard
    try:
        RADWASTE_STANDARD = config.get('radwaste', 'RADWASTE_STANDARD')
    except:
        RADWASTE_STANDARD = None
    
    # read the fispact material list
    fispact_material_list, fispact_material_path = get_fispact_material_list(FISPACT_MATERIAL_LIST, AIM)
    
    # ---------------------ACT and DPA calculation----------------------
    # read the irradiation scenario. If the AIM is CELL_DPA,then only
    if AIM in ['CELL_ACT_PRE', 'CELL_DPA_PRE', 'CELL_ACT_POST', 'CELL_DPA_POST']:
        # one irradiation pulse allowed, the pulse must be a FULL POWER YEAR.
        cooling_time = get_cooling_time(IRRADIATION_SCENARIO, AIM)
        cooling_time_cul = get_cooling_time_cul(cooling_time)
    
    if AIM in ['CELL_ACT_PRE', 'CELL_DPA_PRE', 'CELL_ACT_POST', 'CELL_DPA_POST']:
        # read mcnp output file, get cell information:
        # icl, cid, mat_id, vol (cm3), mass (g)
        Cells = get_cell_basic_info(MCNP_OUTPUT)
        Cells = get_cell_tally_info(MCNP_OUTPUT, Cells, TALLY_NUMBER, N_GROUP_SIZE,
                                    CONTINUE_OUTPUT=CONTINUE_OUTPUT)
        Materials = get_material_info(MCNP_OUTPUT)
        Materials = convert_material_M2F(Materials)
        Cells = match_cells_materials(Cells, Materials)
        Parts = get_part(Cells, PART_CELL_LIST)
        Cells_need_cal = get_cell_need_cal(AIM, Parts, Cells)
    if AIM in ('CELL_ACT_PRE', 'CELL_DPA_PRE'):
        cell_fispact_cal_pre(AIM, WORK_DIR, Cells_need_cal, MODEL_DEGREE,
                             IRRADIATION_SCENARIO, fispact_material_list,
                             fispact_material_path)
    if AIM in ('CELL_ACT_POST', 'CELL_DPA_POST'):
        # first, check whether all the fispact output files are available
        check_fispact_output_files(Cells_need_cal, WORK_DIR, AIM)
        # then read the output information
        read_fispact_output_cell(Cells_need_cal, WORK_DIR, AIM, cooling_time_cul)
        treat_nuc(Cells_need_cal, NUC_TREATMENT)
        if RADWASTE_STANDARD is not None:
            rws = RadwasteStandard(RADWASTE_STANDARD)
        else:
            rws = None
        cell_act_post_process(Parts, WORK_DIR, MODEL_DEGREE, AIM, cooling_time_cul, rws=rws)
    
    if AIM in ['COOLANT_ACT_PRE', 'COOLANT_ACT_POST']:
        Cells = get_cell_basic_info(MCNP_OUTPUT)
        Cells = get_cell_tally_info(MCNP_OUTPUT, Cells, TALLY_NUMBER, N_GROUP_SIZE)
        Parts = get_part(Cells, PART_CELL_LIST, COOLANT_FLOW_PARAMETERS)
        nodes = get_nodes(COOLANT_FLOW_PARAMETERS)
    if AIM == 'COOLANT_ACT_PRE':
        parts_fispact_cal_pre(AIM, WORK_DIR, Parts, MODEL_DEGREE,
                fispact_material_list, fispact_material_path,
                COOLANT_FLOW_PARAMETERS, FLUX_MULTIPLIER)
    if AIM == 'COOLANT_ACT_POST':
        # first, check whether all the fispact output files are available
        check_fispact_output_files(Parts, WORK_DIR, AIM)
        read_fispact_output_part(Parts, WORK_DIR, AIM)
        coolant_act_post_process(Parts, nodes, WORK_DIR, MODEL_DEGREE, AIM)
    
    print('End of NATF: {0}'.format(AIM))
 
# codes for test functions
if __name__ == '__main__':
    pass
