#!/usr/bin/env python3
# -*- coding:utf-8 -*- import numpy as np import re
import argparse
import collections
import re
from natf.cell import get_cell_index
from natf.utils import is_blank_line, log
from natf.mcnp_input import is_comment

def is_tally_result_start(line):
    tally_start_pattern = re.compile("^1tally .*nps =", re.IGNORECASE)
    if re.match(tally_start_pattern, line):
        return True
    else:
        return False

def is_tally_result_end(line):
    tally_end_pattern1 = re.compile(".*tfc bin check", re.IGNORECASE)
    tally_end_pattern2 = re.compile(".*===", re.IGNORECASE)
    if re.match(tally_end_pattern1, line) or re.match(tally_end_pattern2, line):
        return True
    else:
        return False

def get_tally_id(line):
    if not is_tally_result_start(line):
        raise ValueError(f"line: {line} is not tally result start")
    line_ele = line.strip().split()
    return int(line_ele[1])
   

def has_tally_result(filename, tally_num=4):
    """Check whether the file contain specific tally result"""
    if filename is None or filename == '':
        return False
    with open(filename, 'r') as fin:
        while True:
            line = fin.readline()
            if line == '':
                return False
            if is_tally_result_start(line):
                if get_tally_id(line) == tally_num:
                    return True
    return False

def get_cell_names_from_line(line):
    """
    """
    cell_names = []
    ls = line.strip().split()
    for i in range(1, len(ls)):
        cell_names.append(int(ls[i]))
    return cell_names

@log
def get_cell_neutron_flux(MCNP_OUTPUT, Cells, TALLY_NUMBER, N_GROUP_SIZE, CONTINUE_OUTPUT=None):
    """get_cell_neutron_flux: read the mcnp output file and get the neutron flux of the cell

    Parameters:
    -----------
    MCNP_OUTPUT: str
        the mcnp output file
    Cells: list
        the list of Cell
    TALLY_NUMBER: int
        tally number
    N_GROUP_SIZE: int
        Number of group size, 175 or 709.
    CONTINUE_OUTPUT: str, optional
       The output file of continue run, contains neutron flux info. Used when
       the MCNP_OUTPUT file does not contian neutron flux info.

    Returns:
    --------
    Cells: list
        Cells that have the neutron flux information in it
    """

    # check tally results
    tally_file = None
    if has_tally_result(MCNP_OUTPUT, TALLY_NUMBER) and CONTINUE_OUTPUT is None:
        tally_file = MCNP_OUTPUT
    if has_tally_result(MCNP_OUTPUT, TALLY_NUMBER) and \
            has_tally_result(CONTINUE_OUTPUT, TALLY_NUMBER):
        tally_file = CONTINUE_OUTPUT
        print(f"Tally {TALLY_NUMBER} results in {CONTINUE_OUTPUT} will be used")
    if not has_tally_result(MCNP_OUTPUT, TALLY_NUMBER) and \
            not has_tally_result(CONTINUE_OUTPUT, TALLY_NUMBER):
        raise ValueError(f"ERROR: {MCNP_OUTPUT} and {CONTINUE_OUTPUT} do not have tally result")

    fin = open(tally_file)
    while True:
        line = fin.readline()
        if line == '':
            raise ValueError(f'1tally {TALLY_NUMBER} not found in the file, wrong file!')
        if not is_tally_result_start(line):
            continue
        if get_tally_id(line) == TALLY_NUMBER:
            while True:
                line1 = fin.readline()
                line_ele1 = line1.split()
                if is_blank_line(line1):
                    continue
                # end of the cell neutron flux information part
                if is_tally_result_end(line1):
                    break
                if 'cell' in line1:
                    line2 = fin.readline()
                    if 'energy' in line2:  # the folowing 176/710 lines are neutron flux information
                        cell_id = get_cell_names_from_line(line1)
                        cell_flux = []
                        cell_error = []
                        for i in range(N_GROUP_SIZE + 1):
                            line = fin.readline()
                            # check the neutron energy group
                            if i == N_GROUP_SIZE:
                                if 'total' not in line:
                                    errormessage = ''.join(
                                        [
                                            'ERROR in reading cell neutron flux\n',
                                            'Neutron energy group is ',
                                            str(N_GROUP_SIZE),
                                            ' in input file\n',
                                            'But keyword: \'total\' not found in the end!\n',
                                            'Check the neutron energy group in the output file\n'])
                                    raise ValueError(errormessage)
                            line_ele = line.split()
                            erg_flux = []
                            erg_error = []
                            for j in range(len(cell_id)):
                                erg_flux.append(float(line_ele[2 * j + 1]))
                                erg_error.append(float(line_ele[2 * j + 2]))
                            cell_flux.append(erg_flux)
                            cell_error.append(erg_error)
                        # put the cell_flux and cell_error into
                        for i in range(len(cell_id)):
                            cell_index = get_cell_index(Cells, cell_id[i])
                            temp_flux = []
                            temp_error = []
                            for j in range(N_GROUP_SIZE + 1):
                                temp_flux.append(cell_flux[j][i])
                                temp_error.append(cell_error[j][i])
                            Cells[cell_index].neutron_flux = temp_flux
                            Cells[cell_index].neutron_flux_error = temp_error
            break
    fin.close()
    print('     read cell neutron flux over')
    return Cells



