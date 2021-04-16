#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test neutral file generated wiith MYSTRAN
"""

import os
import tempfile

import numpy as np
import pytest
from click.testing import CliRunner

from femap_neutral_parser import Parser, blocks

from .test_utils import datadir, tempdir  # fixtrures


@pytest.fixture(scope="module")
def neutral(datadir):
    fpath = os.path.join(datadir, "mystran_00.NEU")
    return Parser(fpath)


@pytest.fixture(scope="module")
def f_neutral(datadir):
    fpath = os.path.join(datadir, "FEMAP_v8-2.neu")
    return Parser(fpath)


def test_basics(neutral):
    assert neutral.header["femap_version"] == "8.2"
    assert neutral.header["db_title"] == "323152540, bulk_model.F06"
    assert neutral.femap_version == "8.2"
    assert neutral.db_title == "323152540, bulk_model.F06"
    # test table of content
    assert neutral._toc == {
        100: [[3, 5]],
        450: [[8, 13], [907, 912]],
        451: [[16, 904], [915, 1598]],
    }
    # check available blocks
    assert neutral.available_blocks() == {
        "header": 100,
        "output_sets": 450,
        "output_vectors": 451,
    }


# =============================================================================
# Block 450 {{1
# =============================================================================
def test_b450_raw_data(neutral):
    """test Block 450 parsing. Since several Blocks 450 are usually found,
    `_get_block_raw_data` yields a file-like objecy containing each of this
    block
    """
    expected = [
        [
            "       1,\n",
            "Analyse. NASTRAN SPC 1 - NASTRAN SPC 1 - NASTRAN SPC 1 - lc1. test,          \n",
            "0,1,\n",
            "0.,\n",
            "0,\n",
        ],
        [
            "       2,\n",
            "Analyse. NASTRAN SPC 1 - NASTRAN SPC 1 - NASTRAN SPC 1 - lc2. test,     \n",
            "0,1,\n",
            "0.,\n",
            "0,\n",
        ],
    ]

    # =========================================================================
    # test raw parsing
    # =========================================================================
    b450s = neutral._get_block_raw_data(450, as_file_like=False)
    for i, b450 in enumerate(b450s):
        # b450 = b450.readlines()
        assert b450 == expected[i]
    # =========================================================================
    # also test file-like parsing
    # =========================================================================
    b450s = neutral._get_block_raw_data(450, as_file_like=True)
    for i, b450 in enumerate(b450s):
        b450 = b450.readlines()
        assert b450 == expected[i]


def test_b450_data(neutral):
    """test Block 450 parsing.     """
    expected = [
        {
            "ID": 1,
            "anal_type": 1,
            "from_prog": 0,
            "notes": "",
            "title": "Analyse. NASTRAN SPC 1 - NASTRAN SPC 1 - NASTRAN SPC 1 - lc1. test",
            "value": 0.0,
        },
        {
            "ID": 2,
            "anal_type": 1,
            "from_prog": 0,
            "notes": "",
            "title": "Analyse. NASTRAN SPC 1 - NASTRAN SPC 1 - NASTRAN SPC 1 - lc2. test",
            "value": 0.0,
        },
    ]
    parsed_block = neutral._parse_blocks(450)
    assert parsed_block.data == expected


def test_b450_get(neutral):
    """test Block 450 parsing.     """
    expected = {
        1: {
            "anal_type": "Static",
            "from_prog": "Unknown",
            "integer_format": None,
            "notes": "",
            "process_type": None,
            "title": "Analyse. NASTRAN SPC 1 - NASTRAN SPC 1 - NASTRAN SPC 1 - lc1. test",
            "value": 0.0,
        },
        2: {
            "anal_type": "Static",
            "from_prog": "Unknown",
            "integer_format": None,
            "notes": "",
            "process_type": None,
            "title": "Analyse. NASTRAN SPC 1 - NASTRAN SPC 1 - NASTRAN SPC 1 - lc2. test",
            "value": 0.0,
        },
    }

    assert neutral.output_sets == expected


# =============================================================================
# Block 451 {{1
# =============================================================================


def test_b451_data(neutral):
    """test Block 451 parsing.     """
    expected = [
        {
            "ID": 1,
            "anal_type": 1,
            "from_prog": 0,
            "notes": "",
            "title": "Analyse. NASTRAN SPC 1 - NASTRAN SPC 1 - NASTRAN SPC 1 - lc1. test",
            "value": 0.0,
        },
        {
            "ID": 2,
            "anal_type": 1,
            "from_prog": 0,
            "notes": "",
            "title": "Analyse. NASTRAN SPC 1 - NASTRAN SPC 1 - NASTRAN SPC 1 - lc2. test",
            "value": 0.0,
        },
    ]
    parsed_block = neutral._parse_blocks(451)
    data = parsed_block.data
    assert len(data) == 84
    assert set(data[0].keys()) == {
        "abs_max",
        "calc_warn",
        "cent_total",
        "comp_dir",
        "component_vec",
        "ent_type",
        "id_max",
        "id_min",
        "max_val",
        "min_val",
        "out_type",
        "record",
        "setID",
        "title",
        "vecID",
    }

    assert data[0]["vecID"] == 10001
    assert data[1]["vecID"] == 10002
    # ...
    assert data[-1]["vecID"] == 50212
    # -------------------------------------------------------------------------
    # full check for last vector
    expected = {
        "abs_max": 45.04958,
        "calc_warn": True,
        "cent_total": True,
        "comp_dir": 3,
        "component_vec": [50201.0, 50202.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "ent_type": 8,
        "id_max": 1,
        "id_min": 4,
        "max_val": 45.04958,
        "min_val": -2.221523,
        "out_type": 3,
        "setID": 2,
        "title": "BAR EndB Plane1 Moment",
        "vecID": 50202,
    }
    # we drop the array frm data structure since it requires a specific test
    act_without_array = data[-11].copy()
    actual_records = act_without_array.pop("record")
    assert act_without_array == expected
    expected_records = np.array(
        [
            (1, 4.504958e01),
            (2, 5.241556e-01),
            (3, 1.331676e01),
            (4, -2.221523e00),
            (5, 1.318767e-11),
            (6, -1.419975e-14),
            (9, -2.878763e-01),
            (10, 6.273498e-01),
            (11, 5.241556e-01),
        ],
        dtype=[("entityID", "<i8"), ("value", "<f8")],
    )
    np.testing.assert_array_equal(actual_records, expected_records)


def test_b451_get(neutral, f_neutral):
    """test Block 451 parsing.     """
    expected = {
        1: {
            "anal_type": "Static",
            "from_prog": "Unknown",
            "integer_format": None,
            "notes": "",
            "process_type": None,
            "title": "Analyse. NASTRAN SPC 1 - NASTRAN SPC 1 - NASTRAN SPC 1 - lc1. test",
            "value": 0.0,
        },
        2: {
            "anal_type": "Static",
            "from_prog": "Unknown",
            "integer_format": None,
            "notes": "",
            "process_type": None,
            "title": "Analyse. NASTRAN SPC 1 - NASTRAN SPC 1 - NASTRAN SPC 1 - lc2. test",
            "value": 0.0,
        },
    }
    # -------------------------------------------------------------------------
    # check lazy loading
    assert "output_vectors" not in dir(neutral)
    rss_translation_LCID2 = neutral.output_vectors["Total Translation"][2]
    assert "output_vectors" in dir(neutral)
    values = rss_translation_LCID2.pop("record")
    assert rss_translation_LCID2 == {
        "abs_max": 2.578386,
        "calc_warn": True,
        "cent_total": True,
        "comp_dir": 1,
        "component_vec": [10002.0, 10003.0, 10004.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "id_max": 7,
        "id_min": 1,
        "max_val": 2.578386,
        "min_val": 0.0,
        "vecID": 1,
    }
    expected_values = np.array(
        [
            (1, 0.000000e00),
            (2, 2.045391e-01),
            (3, 0.000000e00),
            (4, 1.468270e-02),
            (5, 9.231050e-05),
            (6, 6.276400e-01),
            (7, 2.578386e00),
            (8, 1.025100e-01),
            (9, 2.578363e00),
            (10, 1.916094e00),
            (11, 1.100510e00),
            (12, 2.389742e00),
        ],
        dtype=[("nodeID", "<i8"), ("Total Translation", "<f8")],
    )
    np.testing.assert_array_equal(values, expected_values)


def test_vectors_agg(neutral, f_neutral):
    expected = np.array(
        [
            (1, 0.0, 0.0, 0.0000000e00, 1),
            (2, -0.1870816, 0.0, 0.0000000e00, 1),
            (3, 0.0, 0.0, 0.0000000e00, 1),
            (4, 0.07011177, 0.0, 0.0000000e00, 1),
            (5, 0.0, 0.0, -5.7721190e-03, 1),
            (6, 0.0, 0.0, -5.6935130e-01, 1),
            (7, 0.0, 0.0, -1.2992963e00, 1),
            (8, -0.0937607, 0.0, -5.7549970e-03, 1),
            (9, 0.03555086, 0.0, -1.2992791e00, 1),
            (10, 0.0, 0.0, -1.5645016e00, 1),
            (11, 0.0, 0.0, -9.5607290e-01, 1),
            (12, 0.0, 0.0, -1.6029116e00, 1),
            (1, 0.0, 0.0, 0.0000000e00, 2),
            (2, -0.2045391, 0.0, 0.0000000e00, 2),
            (3, 0.0, 0.0, 0.0000000e00, 2),
            (4, -0.0146827, 0.0, 0.0000000e00, 2),
            (5, 0.0, 0.0, -9.2310500e-05, 2),
            (6, 0.0, 0.0, -6.2763990e-01, 2),
            (7, 0.0, 0.0, -2.5783863e00, 2),
            (8, -0.1025099, 0.0, -9.2036680e-05, 2),
            (9, -0.00744509, 0.0, -2.5783525e00, 2),
            (10, 0.0, 0.0, -1.9160941e00, 2),
            (11, 0.0, 0.0, -1.1005101e00, 2),
            (12, 0.0, 0.0, -2.3897419e00, 2),
        ],
        dtype=[
            ("nodeID", "<i8"),
            ("T1 Translation", "<f8"),
            ("T2 Translation", "<f8"),
            ("T3 Translation", "<f8"),
            ("subcaseID", "<i8"),
        ],
    )
    expected = np.rec.array(expected)
    vec = neutral.vectors(("T1 Translation", "T2 Translation", "T3 Translation"))
    f_vec = neutral.vectors(("T1 Translation", "T2 Translation", "T3 Translation"))
    np.testing.assert_array_almost_equal(f_vec.view(None), expected.view(None))
    np.testing.assert_array_almost_equal(vec.view(None), expected.view(None))


def test_info(neutral):
    info = neutral.info(doprint=False)
    expected = [
        "\nAnalysis",
        "========",
        " * subcase 1: Analyse. NASTRAN SPC 1 - NASTRAN SPC 1 - NASTRAN SPC 1 - lc1. test (Static)",
        " * subcase 2: Analyse. NASTRAN SPC 1 - NASTRAN SPC 1 - NASTRAN SPC 1 - lc2. test (Static)",
        "\nOutputs",
        "=======",
        "access to one of them using `.output_vectors[<title>][<subcaseid>]['record']\n",
        " * Total Translation",
        " * T1 Translation",
        " * T2 Translation",
        " * T3 Translation",
        " * Total Rotation",
        " * R1 Rotation",
        " * R2 Rotation",
        " * R3 Rotation",
        " * Total Applied Force",
        " * T1 Applied Force",
        " * T2 Applied Force",
        " * T3 Applied Force",
        " * Total Applied Moment",
        " * R1 Applied Moment",
        " * R2 Applied Moment",
        " * R3 Applied Moment",
        " * Total Constraint Force",
        " * T1 Constraint Force",
        " * T2 Constraint Force",
        " * T3 Constraint Force",
        " * Total Constraint Moment",
        " * R1 Constraint Moment",
        " * R2 Constraint Moment",
        " * R3 Constraint Moment",
        " * Bar EndA Plane1 Moment",
        " * Bar EndB Plane1 Moment",
        " * Bar EndA Plane2 Moment",
        " * Bar EndB Plane2 Moment",
        " * Bar EndA Pl1 Shear Force",
        " * BAR EndB Pl1 Shear Force",
        " * Bar EndA Pl2 Shear Force",
        " * BAR EndB Pl2 Shear Force",
        " * Bar EndA Axial Force",
        " * BAR EndB Axial Force",
        " * Bar EndA Torque",
        " * BAR EndB Torque",
        " * Bar EndA Pt1 Bend Stress",
        " * Bar EndB Pt1 Bend Stress",
        " * Bar EndA Pt2 Bend Stress",
        " * Bar EndB Pt2 Bend Stress",
        " * Bar EndA Pt3 Bend Stress",
        " * Bar EndB Pt3 Bend Stress",
        " * Bar EndA Pt4 Bend Stress",
        " * Bar EndB Pt4 Bend Stress",
        " * Bar EndA Max Comb Stress",
        " * Bar EndB Max Comb Stress",
        " * Bar EndA Min Comb Stress",
        " * Bar EndB Min Comb Stress",
    ]
    assert info == expected
