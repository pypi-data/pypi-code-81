#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains unit tests for the powerneedsaggr module.
"""

import epw

import os
import pytest


DIR_PATH = os.path.abspath(os.path.dirname(__file__))
CUBE1_ORIG_IDF_PATH = os.path.join(DIR_PATH, "cube1.idf")
CUBE2_ORIG_IDF_PATH = os.path.join(DIR_PATH, "cube2.idf")


def test_sub_one_field_1():

    sub_dict = {
        ("Material", "BETON 18CM", "Conductivity"): 0.5
    }

    returned_idf_str = epw.core.sub_one_field(CUBE1_ORIG_IDF_PATH, sub_dict=sub_dict)

    with open(os.path.join(DIR_PATH, "expected_test_sub_one_field_1.idf")) as fd:
        expected_idf_str = fd.read()

    assert returned_idf_str == expected_idf_str



def test_sub_one_field_1_int():

    sub_dict = {
        ("Material", "BETON 18CM", "Conductivity"): 1
    }

    returned_idf_str = epw.core.sub_one_field(CUBE1_ORIG_IDF_PATH, sub_dict=sub_dict)

    with open(os.path.join(DIR_PATH, "expected_test_sub_one_field_1b.idf")) as fd:
        expected_idf_str = fd.read()

    assert returned_idf_str == expected_idf_str



def test_sub_one_field_1_float_without_decimal():

    sub_dict = {
        ("Material", "BETON 18CM", "Conductivity"): 1.
    }

    returned_idf_str = epw.core.sub_one_field(CUBE1_ORIG_IDF_PATH, sub_dict=sub_dict)

    with open(os.path.join(DIR_PATH, "expected_test_sub_one_field_1c.idf")) as fd:
        expected_idf_str = fd.read()

    assert returned_idf_str == expected_idf_str


def test_sub_one_field_1_float_without_int():

    sub_dict = {
        ("Material", "BETON 18CM", "Conductivity"): .5
    }

    returned_idf_str = epw.core.sub_one_field(CUBE1_ORIG_IDF_PATH, sub_dict=sub_dict)

    with open(os.path.join(DIR_PATH, "expected_test_sub_one_field_1.idf")) as fd:
        expected_idf_str = fd.read()

    assert returned_idf_str == expected_idf_str


def test_sub_one_field_1_list_of_len_1():

    sub_dict = {
        ("Material", "BETON 18CM", "Conductivity"): [0.5]
    }

    returned_idf_str = epw.core.sub_one_field(CUBE1_ORIG_IDF_PATH, sub_dict=sub_dict)

    with open(os.path.join(DIR_PATH, "expected_test_sub_one_field_1.idf")) as fd:
        expected_idf_str = fd.read()

    assert returned_idf_str == expected_idf_str



def test_sub_one_field_2_semicolon():

    sub_dict = {
        ("InternalMass", "Inertia", "Total area exposed to zone"): 100
    }

    returned_idf_str = epw.core.sub_one_field(CUBE2_ORIG_IDF_PATH, sub_dict=sub_dict)

    with open(os.path.join(DIR_PATH, "expected_test_sub_one_field_2.idf")) as fd:
        expected_idf_str = fd.read()

    assert returned_idf_str == expected_idf_str



def test_sub_one_field_3():

    sub_dict = {
        ("Material", "BETON 18CM", "Conductivity"): 0.5,
        ("Material", "BETON 20CM", "Conductivity"): 0.6
    }

    returned_idf_str = epw.core.sub_one_field(CUBE1_ORIG_IDF_PATH, sub_dict=sub_dict)

    with open(os.path.join(DIR_PATH, "expected_test_sub_one_field_3.idf")) as fd:
        expected_idf_str = fd.read()

    assert returned_idf_str == expected_idf_str



def test_sub_one_field_4_str_value():

    sub_dict = {
        ("BuildingSurface", "PLANCHER", "Sun Exposure"): "SunExposed"
    }

    returned_idf_str = epw.core.sub_one_field(CUBE1_ORIG_IDF_PATH, sub_dict=sub_dict)

    with open(os.path.join(DIR_PATH, "expected_test_sub_one_field_4.idf")) as fd:
        expected_idf_str = fd.read()

    assert returned_idf_str == expected_idf_str



def test_sub_one_field_5_colon_and_curly_bracket():

    sub_dict = {
        ("WindowMaterial:SimpleGlazingSystem", "VITRE", "U-Factor {W/m2-K}"): 1.0
    }

    returned_idf_str = epw.core.sub_one_field(CUBE1_ORIG_IDF_PATH, sub_dict=sub_dict)

    with open(os.path.join(DIR_PATH, "expected_test_sub_one_field_5.idf")) as fd:
        expected_idf_str = fd.read()

    assert returned_idf_str == expected_idf_str



def test_sub_one_field_6_special_char_in_value():

    sub_dict = {
        ("ZoneInfiltration:DesignFlowRate", "Infiltrations", "Design Flow Rate Calculation Method"): "Flow*Area"
    }

    returned_idf_str = epw.core.sub_one_field(CUBE1_ORIG_IDF_PATH, sub_dict=sub_dict)

    with open(os.path.join(DIR_PATH, "expected_test_sub_one_field_6.idf")) as fd:
        expected_idf_str = fd.read()

    assert returned_idf_str == expected_idf_str


def test_sub_one_field_7():

    sub_dict = {
        ("Zone", "", "Ceiling Height"): 20.
    }

    returned_idf_str = epw.core.sub_one_field(CUBE1_ORIG_IDF_PATH, sub_dict=sub_dict)

    with open(os.path.join(DIR_PATH, "expected_test_sub_one_field_7.idf")) as fd:
        expected_idf_str = fd.read()

    assert returned_idf_str == expected_idf_str