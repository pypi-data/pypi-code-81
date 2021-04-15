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

import re
from collections import OrderedDict

from dimspy.process.peak_filters import filter_attr


class Scans:
    """
    The Scans class.

    This class is used to extract high quality scan data from a given sample using a user defined method.

    :param run: Spectral data from multiple samples contained in a single *.mzML file
    :param well: Well label as provided in the corresponding metadata *.txt file
    :param well_scans: Scan IDs for all scans in a given well
    :param id_snr: User provided SNR threshold for differentiating between on and off scans
    :param id_tol: User provided number of features with SNR > id_snr to tolerate in off scans for labelling the scan type

    """

    def __init__(self, run, well, well_scans, id_snr, id_tol):
        self.dat = run
        self.well = well
        self.id_snr = id_snr
        self.id_tol = id_tol
        self.pls = self.peaklists(well_scans)
        # Dictionary of scan IDs in well and whether they are on/off scans
        self.binary_dict = self.dictionary()
        # String of the binary on/off scans in order. To search for on/off
        # cycle patterns
        self.binary_str = self.padding()
        self.method = "on_scans_no_edge"

    def peaklists(self, well_scans):
        """
        Peak lists are generated for all scan IDs provided as input. The peak lists include the spectral data (mz, intensity, snr, flags) for each scan.
        The peak lists havea hard SNR filter applied to diffeentiate between scan types - this is set to 15 by default.

        :param method: well_scans: List of scan IDs from all scans in the given well.

        :return: List of peaklist objects

        """

        self.pls = self.dat.peaklists(well_scans, function_noise="median")
        # adds snr flag col to data (mz, intensity, snr, flags)
        self.pls = [filter_attr(pl, "snr", min_threshold=self.id_snr) if len(pl.mz) > 0 else pl for pl in self.pls]
        return self.pls

    def dictionary(self):
        """
        A dictionary is generated using the scan IDs as keys and a binary identifier of the scan types as values (1 = 'on-scan' and  0 = 'off-scan').
        The scan type is dertemined by the number of features with SNR above the applied SNR, by default >3 features needed to be labelled as 'on-scan'.

        :return: Dictionary object

        """

        si_binary = [(int(pl.ID), int(len(pl.mz) > self.id_tol)) for pl in self.pls]
        self.binary_dict = OrderedDict(si_binary)
        return self.binary_dict

    def padding(self):
        """
        Converts the binary values in the dictionary  to a string of binary values and adds padding (00) to either side. This padding enables on/off cycles to be identified at the start and end of each well.

        :return String object

        """

        self.binary_str = "".join(map(str, self.binary_dict.values()))
        self.binary_str = "00{}00".format(self.binary_str)
        return self.binary_str

    def extract(self, method):
        """
        Generates a dictionary of possible on/off scan cycles (as binary patterns) from AMI-MS data as keys and the indices of the scans within each cycle to be extracted
        for the user defined method.
        The dictionary is then used to search the AMI-MS data for the provided scan cycles and extract the scan IDs required for downstream processing
        by calling the relavent function for the defined method. The scan IDs are returned as a list object.

        :param method: Method to define which scans to extract data from. The following options are available:

            * **all_scans** - Extracts data from all scans from the given well.

            * **on_scans** - Extracts data from only the on scans from the given well.

            * **off_scans** - Extracts data from only the off scans from the given well.

            * **on_scan_no_edge** - Extracts data from only the on scans from the given well that are not immediately preceded or followed by an off-scan. For the unusual case of only two consecutive on scans, the single scan with the highest intensity is extracted. This is the default method.


        :return: List object

        """

        self.method = method
        if self.method == "all_scans":
            return self._extract_all_scans()

        elif self.method == "off_scans":
            return self._extract_off_scans()

        else:

            # Index for the position of on scans minus the edge scans in sample pattern
            on_scans_no_edge = [[2, 3],
                                [2, 4],
                                [3, 4],
                                [3, 5],
                                [3, 6],
                                [3, 7],
                                [3, 8],
                                [3, 9],
                                [3, 10]]

            # Min and max index for all on scans in sample pattern
            on_scans = [[2, 3],
                        [2, 4],
                        [2, 5],
                        [2, 6],
                        [2, 7],
                        [2, 8],
                        [2, 9],
                        [2, 10],
                        [2, 11]]

            # Median indices for on scans within each on_scans cycle
            temporal_median_on = [[2],
                                  [3],
                                  [3],
                                  [4],
                                  [4],
                                  [5],
                                  [5],
                                  [6],
                                  [6]]


            self.methods_dict = {'on_scans_no_edge': on_scans_no_edge,
                                 'on_scans' : on_scans,
                                 'temporal_median_on': temporal_median_on}

            extract_method = self.methods_dict[method]

            # Dictionary of on scan binary pattern (keys = pattern, values = scans to extract from pattern)
            pattern_idx = OrderedDict([("00100", extract_method[0]),
                                       ("001100", extract_method[1]),
                                       ("0011100", extract_method[2]),
                                       ("00111100", extract_method[3]),
                                       ("001111100", extract_method[4]),
                                       ("0011111100", extract_method[5]),
                                       ("00111111100", extract_method[6]),
                                       ("001111111100", extract_method[7]),
                                       ("0011111111100", extract_method[8])])

            if self.method == "on_scans_no_edge":
                print(pattern_idx)
                print(self._extract_on_scans_no_edge(pattern_idx))
                return self._extract_on_scans_no_edge(pattern_idx)

            elif self.method == "on_scans":
                return self._extract_on_scans(pattern_idx)

    def _extract_all_scans(self):
        """
        Extracts the scan IDs for all scans from the given well.

        :return: List object

        """

        scan_ids = self.binary_dict.keys()
        return scan_ids

    def _extract_off_scans(self):
        """
        Extracts the scan IDs for all scans for only the off scans from the given well.

        :return: List object

        """

        scan_ids = self.extract("all_scans")
        on_scan_ids = self.extract("on_scans")
        for scan in scan_ids:
            if scan in on_scan_ids:
                scan_ids = filter(lambda a: a != scan, scan_ids)
        return scan_ids

    def _extract_on_scans(self, pattern_idx):
        """
        Uses the dictionary of on/off cycle patterns to search the AMI-MS data and identify the on scans.
        The scan IDs for only the on scans from the given well are returned.

        :param pattern_idx: Dictionary of possible on/off scan cycles from AMI-MS data as keys and the indices
            of the scans within each cycle to be extracted for the 'on_scans' method.

        :return: List object

        """

        scan_ids = []

        for k in pattern_idx:  # k is the iterator over binary patterns
            for m in re.finditer(r'(?=(' + k + '))', self.binary_str):
                start = m.start()  # Scan to start searching for the pattern from
                try:
                    if len(pattern_idx[k]) > 1:

                        # scan where binary pattern OF INTEREST starts (the
                        # first off scan) - 2 to account for synthetic off
                        # scans
                        idx_s = start + pattern_idx[k][0] - 2

                        # scan where binary pattern OF INTEREST ends
                        idx_e = start + pattern_idx[k][1] - 2

                        # Store scan IDs to process
                        scan_ids.extend(list(self.binary_dict.keys())[idx_s:idx_e])

                    # if only 1 index (for median on scans for instance)
                    elif len(pattern_idx[k]) == 1:
                        # scan of median on scan ('1') in binary pattern
                        idx = start + pattern_idx[k][0] - 2

                        # Store scan IDs to process
                        scan_ids.append(list(self.binary_dict.keys())[idx])
                    else:
                        raise Exception("Incorrect format")

                except ValueError as e:
                    line = "Extract failed for well: {}, failed due to: {}.".format(self.well, e)
                    return line

        scan_ids.sort()
        return scan_ids

    def _extract_on_scans_no_edge(self, pattern_idx):

        """
        Uses the dictionary of on/off cycle patterns to search the AMI-MS data and identify the on scans that are not immediately preceded or followed by an off-scan.
        For the unusual case of only two consecutive on scans, the single scan with the highest intensity is extracted.
        The scan IDs for these scans from the given well are returned.

        :param pattern_idx: Dictionary of possible on/off scan cycles from AMI-MS data as keys and the indices
            of the scans within each cycle to be extracted for the 'on_scans_no_edge' method.

        :return: List object

        """

        scan_ids = []

        for i in range(len(pattern_idx)):

            # k is the iterator over binary patterns
            k = [pattern for pattern in pattern_idx][i]

            # Looks for pattern k in the list of binary patterns
            for m in re.finditer(r'(?=(' + k + '))', self.binary_str):

                start = m.start()  # start scan

                try:
                    # scan where binary pattern OF INTEREST starts (the
                    # first off scan) - 2 to account for synthetic off
                    # scans
                    idx_s = start + pattern_idx[k][0] - 2

                    # scan where binary pattern OF INTEREST ends
                    idx_e = start + pattern_idx[k][1] - 2

                    # If only two consecutive on scans
                    if i == 1:
                        on_scans = list(self.binary_dict.keys())[idx_s:idx_e]
                        d = {}
                        for pl in self.pls:
                            if int(pl.ID) in on_scans:
                                d[pl.ID] = pl.metadata.tic

                        # Take the single scan with the highest intensity
                        take_scan = int(max(d, key=d.get))
                        scan_ids.append(take_scan)

                    else:
                        # Store scan IDs to process
                        scan_ids.extend(list(self.binary_dict.keys())[idx_s:idx_e])

                except ValueError as e:
                    line = "Extract failed for well: {}, failed due to: {}.".format(self.well, e)
                    return line

        scan_ids.sort()
        return scan_ids
