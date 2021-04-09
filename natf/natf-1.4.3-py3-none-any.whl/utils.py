#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from __future__ import with_statement, print_function
import math
import numpy as np
import os

def log(func):
    def wrapper(*args, **kw):
        print('running {0}:'.format(func.__name__))
        return func(*args, **kw)
    return wrapper

def cooling_time_sec(value, unit):
    """cooling_time_sec convert the time of cooling time to the unit of sec.
    input parameters:value, a float number of time,
                     unit, a string of time unit, like SECS, MINS, HOURS, DAYS, YEARS
    return value: value, a float number of time in unit of sec"""
    # convert value to float incase of it's a string
    value = float(value)
    # unit check
    if unit.lower() not in ('s', 'sec', 'secs','second', 'seconds',
                            'm', 'min', 'mins', 'minute', 'minutes',
                            'h', 'hr', 'hour', 'hours',
                            'd', 'day', 'days',
                            'y', 'a', 'year', 'years'):
        raise ValueError('unit of time must in given value, not aribitary one')
    if unit.lower() in ('s', 'sec', 'secs','second', 'seconds'):
        return value * 1.0
    if unit.lower() in ('m', 'min', 'mins', 'minute', 'minutes'):
        return value * 60.0
    if unit.lower() in ('h', 'hr', 'hour', 'hours'):
        return value * 3600.0
    if unit.lower() in ('d', 'day', 'days'):
        return value * 3600 * 24.0
    if unit.lower() in ('y', 'a', 'year', 'years'):
       return value * 3600 * 24 * 365.25

def time_sec_to_unit(value, unit):
    """
    Convert time from unit (s) to another unit.
    """
    value = float(value)
    # unit check
    if unit.lower() not in ('s', 'sec', 'secs','second', 'seconds',
                            'm', 'min', 'mins', 'minute', 'minutes',
                            'h', 'hr', 'hour', 'hours',
                            'd', 'day', 'days',
                            'y', 'a', 'year', 'years'):
        raise ValueError('unit of time must in given value, not aribitary one')
    if unit.lower() in ('s', 'sec', 'secs','second', 'seconds'):
        return value / 1.0
    if unit.lower() in ('m', 'min', 'mins', 'minute', 'minutes'):
        return value / 60.0
    if unit.lower() in ('h', 'hr', 'hour', 'hours'):
        return value / 3600.0
    if unit.lower() in ('d', 'day', 'days'):
        return value / (3600 * 24.0)
    if unit.lower() in ('y', 'a', 'year', 'years'):
       return value / (3600 * 24 * 365.25)

def sgn(value):
    """sgn return 1 for number greater than 0.0, return -1 for number smaller than 0"""
    if not isinstance(value, (int, float)):
        raise ValueError('value for sgn must a number of int or float')
    if value == 0:
        sgn = 0
    if value < 0.0:
        sgn = -1
    if value > 0.0:
        sgn = 1
    return sgn

def ci2bq(value):
    """Convert unit from Ci to Bq."""
    # input check
    if not isinstance(value, float):
        raise ValueError("Input value for Ci must be float")
    if value < 0:
        raise ValueError("Negtive input for Ci")
    return value * 3.7e+10


def scale_list(value):
    """scale_list: scale a list of float, normalized to 1"""
    # check the input
    if not isinstance(value, list):
        raise ValueError('scale_list can only apply to a list')
    for item in value:
        if not isinstance(item, float):
            raise ValueError('scale_list can only apply to a list of float')
    # scale the list
    t = sum(value)
    for i in range(len(value)):
        value[i] /= t
    return value


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

def get_ct_index(ct, cts):
    """
    Get the index of a cooling time in cooling_times. As there is roundoff
    error in data.

    Parameters:
    -----------
    ct: float
        The cooling time to find.
    cts: list of float
        The cooling times.
    """
    for i in range(len(cts)):
        if is_close(ct, cts[i], rel_tol=1e-2):
            return i
    raise ValueError("ct {0} not found".format(ct))

def is_short_live(half_life):
    """
    Check whether the nuclide is short life (half life <= 30 years) nuclide.
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

def data_to_line_1d(key, value, delimiter=',', postfix='\n', decimals=5):
    """
    Create a print line for given key and value.
    """
    data_content = ''
    if isinstance(value, list) or isinstance(value, np.ndarray):
        for i, item in enumerate(value):
            if i == 0:
                data_content = format_single_output(item, decimals=decimals)
            else:
                data_content = delimiter.join([data_content, format_single_output(item, decimals=decimals)])
    else:
        data_content = format_single_output(value, decimals=decimals)

    if key is not None:
        line = delimiter.join([format_single_output(key, decimals=decimals), data_content])
    else:
        line = data_content
    return line+postfix

def format_single_output(value, decimals=5):
    """
    Format a single item for output.
    """
    if isinstance(value, float):
        if decimals is None:
            return str(value)
        else:
            style = "{0:."+str(decimals)+"E}"
            return style.format(value)
    else:
        return str(value)

def str2float(s):
    """
    Convert string to float. Including some strange value.
    """
    try:
        value = float(s)
        return value
    except:
        if '-' in s:
            base = s.split('-')[0]
            index = s.split('-')[1]
            s_fix = ''.join([base, 'E-', index])
            return float(s_fix)
        else:
            raise ValueError("{0} can't convert to float".format(s))

def calc_ctr_flag_chn2018(rwc, rwcs):
    """
    Calculate the flat '>' or '<' for a specific radwaste class.
    Eg: rwc='Clearance', rwcs=['HLW', 'ILW'], flag is '>'.
    Eg: rwc='ILW', rwcs=['LLW', 'VLLW'], flag is '<'.
    """
    class_dict = {'Clearance': 0, 'VLLW': 1, 'LLW': 2, 'ILW': 3, 'HLW': 4}
    min_level = len(class_dict) - 1
    max_level = 0
    for i, item in enumerate(rwcs):
        if min_level > class_dict[item]:
            min_level = class_dict[item]
        if max_level < class_dict[item]:
            max_level = class_dict[item]

    if class_dict[rwc] < min_level:
        return '>'
    else:
        return '<'

def calc_ctr_flag_usnrc(rwc, rwcs):
    """
    Calculate the flat '>' or '<' for a specific radwaste class.
    Supprted standard: 'USNRC' and 'USNRC_FETTER'.
    Eg: rwc='LLWA', rwcs=['LLWC', 'LLWB'], flag is '>'.
    Eg: rwc='ILW', rwcs=['LLWC', 'LLWB'], flag is '<'.
    """
    class_dict = {'LLWA': 0, 'LLWB': 1, 'LLWC': 2, 'ILW': 3}
    min_level = len(class_dict) - 1
    max_level = 0
    for i, item in enumerate(rwcs):
        if min_level > class_dict[item]:
            min_level = class_dict[item]
        if max_level < class_dict[item]:
            max_level = class_dict[item]

    if class_dict[rwc] < min_level:
        return '>'
    else:
        return '<'

def calc_ctr_flag_uk(rwc, rwcs):
    """
    Calculate the flat '>' or '<' for a specific radwaste class.
    Eg: rwc='LLW', rwcs=['HLW', 'ILW'], flag is '>'.
    Eg: rwc='HLW', rwcs=['ILW', 'LLW'], flag is '<'.
    """
    class_dict = {'LLW': 0, 'ILW': 1, 'HLW': 2}
    min_level = len(class_dict) - 1
    max_level = 0
    for i, item in enumerate(rwcs):
        if min_level > class_dict[item]:
            min_level = class_dict[item]
        if max_level < class_dict[item]:
            max_level = class_dict[item]

    if class_dict[rwc] < min_level:
        return '>'
    else:
        return '<'


def calc_ctr(cooling_times, rwcs, classes, standard='CHN2018', out_unit='a', decimals=2):
    """
    Calculate cooling time requirement for specific rwc.

    Parameters:
        cooling_times: list or pandas DataFrame series
            Cooling times, unit: s.
        rwcs: list
            Radwaste classes for each cooling time.
        classes: list
            Radwaste types.
            Eg: for CHN2018: ['HLW', 'ILW', 'LLW', 'VLLW', 'Clearance']
        standard: string
            Radwaste standard used. Supported standards: 'CHN2018', 'USNRC', 'UK'.
        out_unit: string
            Unit of output unit of cooling time. Supported value: 's', 'a'.
    
    Returns:
        ctr: list of strings
            Required cooling times (in string).
    """
    cooling_times = list(cooling_times)
    if out_unit == 'a':
        # unit conversion
        for i, ct in enumerate(cooling_times):
            cooling_times[i] = time_sec_to_unit(ct, 'a')
    
    exist_rwcs = list(set(rwcs))
    # find rwc in rwcs
    ctr = [] 
    for i, item in enumerate(classes):
        try:
            index = rwcs.index(item)
            ctr.append(format_single_output(cooling_times[index], decimals=decimals))
        except:
            if standard == 'CHN2018':
                flag = calc_ctr_flag_chn2018(item, exist_rwcs)
            if standard in ['USNRC', 'USNRC_FETTER']:
                flag = calc_ctr_flag_usnrc(item, exist_rwcs)
            if standard == 'UK':
                flag = calc_ctr_flag_uk(item, exist_rwcs)
            if flag == '>':
                ctr.append(''.join([flag, format_single_output(cooling_times[-1], decimals=decimals)]))
            else:
                ctr.append(''.join([flag, format_single_output(cooling_times[0], decimals=decimals)]))
    return ctr
    

def mcnp_style_str_append(s, value, indent_length=6):
    """append lines as mcnp style, line length <= 80"""
    indent_str = ' '*indent_length
    s_tmp = ''.join([s, ' ', format_single_output(value, decimals=None)])
    if len(s_tmp.split('\n')[-1]) >= 80:
        s_tmp = ''.join([s, '\n', indent_str, ' ', format_single_output(value, decimals=None)])
    s = s_tmp
    return s


def is_blank_line(line):
    """check blank line"""
    line_ele = line.split()
    if len(line_ele) == 0:
        return True
    else:
        return False


def scale_list(value):
    """scale_list: scale a list of float, normalized to 1"""
    # check the input
    if not isinstance(value, list):
        raise ValueError('scale_list can only apply to a list')
    for i, item in enumerate(value):
        try:
            value[i] = float(item)
        except:
            raise ValueError('scale_list can only apply to a list of float')
    # scale the list
    t = sum(value)
    for i in range(len(value)):
        value[i] /= t
    return value

def diff_check_file(f1, f2):
    command = ''.join(["diff ", "--strip-trailing-cr ", f1, " ", f2])
    flag = os.system(command)
    return flag

def compare_lists(l1, l2):
    """
    Compare two lists.
    """
    if len(l1) != len(l2):
        return False
    for i in range(len(l1)):
        if l1[i] != l2[i]:
            return False
    return True


# codes for test functions
if __name__ == '__main__':
    pass
