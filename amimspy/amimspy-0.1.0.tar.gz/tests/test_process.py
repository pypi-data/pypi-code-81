#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2020-2021 Matthew Smith, Ralf Weber
#
# This file is part of AMIMSpy.
#
# AMIMSpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# AMIMSpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with AMIMSpy.  If not, see <https://www.gnu.org/licenses/>.
#

import unittest
import os
import string
import numpy as np
import pandas as pd
from collections import OrderedDict

from dimspy.metadata import update_metadata_and_labels
from dimspy.metadata import validate_metadata
from dimspy.portals import hdf5_portal
from dimspy.portals.mzml_portal import Mzml
from dimspy.process.peak_filters import filter_attr
from dimspy.process.replicate_processing import align_peaks
from dimspy.tools import hdf5_peak_matrix_to_txt
from dimspy.tools import hdf5_peaklists_to_txt
from dimspy.tools import sample_filter

from amimspy.process import Scans

# Test data file
data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "testData1.mzML")
run = Mzml(data_path)

# Scan metadata
scans_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "testData1.txt")
df = pd.read_csv(scans_path,
                 header=None,
                 names=["barcode",
                        "date/time",
                        "row",
                        "col",
                        "scan",
                        "ejection time",
                        "NA"])

df = df[["barcode", "row", "col", "scan"]]
alphabet = list(string.ascii_uppercase)
df['well_label'] = df.apply(lambda row: "%s_%s%02d" % (
    row.barcode, alphabet[row.row - 1], row.col), axis=1)


well_scans = list(df[(df["well_label"] == "1091564525_G11")].drop_duplicates()["scan"])

#Create instance of scans
scans_instance = Scans(run, "1091564525_G11", well_scans, id_snr=15, id_tol=3)


class WorkflowTestCase(unittest.TestCase):
    def test_peaklists(self):
        scans_instance = Scans(run, "1091564525_G11", well_scans, id_snr=15, id_tol=3)

        pls = run.peaklists([36284], function_noise="median")

        self.assertEqual(pls[0].mz[0], 125.00572204589844)
        self.assertEqual(pls[0].mz[-1], 1038.25927734375)
        self.assertEqual(list(pls[0].__dict__.keys()), ['_dtable', '_id', '_metadata', '_tags', '_flags', '_flag_attrs'])
        self.assertEqual(pls[0].intensity[0], 34.0)
        self.assertEqual(pls[0].intensity[-1], 27.0)
        self.assertEqual(pls[0].to_str()[0:16], "mz,intensity,snr")
        self.assertEqual(len(pls[0].to_str()), 3975)

    def test_dict(self):
        expected = OrderedDict([(36284, 0), (36285, 0), (36286, 0), (36287, 1), (36288, 1), (36289, 1), (36290, 1), (36291, 0),
            (36292, 0), (36293, 0), (36294, 1), (36295, 1), (36296, 1), (36297, 0), (36298, 0), (36299, 0), (36300, 1), (36301, 1),
            (36302, 1), (36303, 1), (36304, 0), (36305, 0), (36306, 0), (36307, 1), (36308, 1), (36309, 1), (36310, 0), (36311, 0),
            (36312, 0), (36313, 0), (36314, 1), (36315, 1)])
        self.assertEqual(scans_instance.dictionary(), expected)

    def test_padding(self):
        expected = "000001111000111000111100011100001100"
        self.assertEqual(scans_instance.padding(), expected)

    def test_extract_all_scans(self):
        expected = [36284, 36285, 36286, 36287, 36288, 36289, 36290, 36291, 36292, 36293, 36294, 36295, 36296,
        36297, 36298, 36299, 36300, 36301, 36302, 36303, 36304, 36305, 36306, 36307, 36308, 36309, 36310, 36311,
        36312, 36313, 36314, 36315]
        self.assertEqual(list(scans_instance.extract("all_scans")), expected)

    def test_extract_off_scans(self):
        expected = [36284, 36285, 36286, 36287, 36288, 36289, 36290, 36291, 36292, 36293, 36294, 36295, 36296,
        36297, 36298, 36299, 36300, 36301, 36302, 36303, 36304, 36305, 36306, 36307, 36308, 36309, 36310, 36311,
        36312, 36313, 36314]
        self.assertEqual(list(scans_instance.extract("off_scans")), expected)

    def test_extract_on_scans(self):
        expected_on = [36287, 36288, 36289, 36290, 36294, 36295, 36296, 36300, 36301, 36302, 36303, 36307, 36308,
        36309, 36314, 36315]
        self.assertEqual(list(scans_instance.extract("on_scans")), expected_on)

    def test_extract_on_scans_no_edge(self):
        expected = [36288, 36289, 36295, 36301, 36302, 36308, 36315]
        self.assertEqual(list(scans_instance.extract("on_scans_no_edge")), expected)

if __name__ == '__main__':
    unittest.main()
