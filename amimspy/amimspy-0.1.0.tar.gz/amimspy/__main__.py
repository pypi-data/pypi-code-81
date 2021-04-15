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


import argparse
import os
import string

from dimspy.metadata import update_metadata_and_labels
from dimspy.metadata import validate_metadata
from dimspy.portals import hdf5_portal
from dimspy.portals.mzml_portal import Mzml
from dimspy.process.peak_filters import filter_attr
from dimspy.process.replicate_processing import align_peaks
from dimspy.tools import hdf5_peak_matrix_to_txt
from dimspy.tools import hdf5_peaklists_to_txt
from dimspy.tools import sample_filter

import numpy as np

import pandas as pd

from .process import Scans


def map_delimiter(delimiter: str):  # pragma: no cover
    seps = {"comma": ",", "tab": "\t"}
    if delimiter in seps:
        return seps[delimiter]
    else:
        return delimiter

def main():

    # Create ArgumentParser object
    parser = argparse.ArgumentParser(
        description='Python package for processing acoustic mist ionisation-mass spectrometry -based metabolomics and lipidomics data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # subparsers
    subparsers = parser.add_subparsers(dest='step')

    parser_scans = subparsers.add_parser(
        'process-scans', help='Process and align scans within samples.')
    parser_samples = subparsers.add_parser('process-samples',
                                           help='Process and align samples.')
    parser_hpmt = subparsers.add_parser(
        'hdf5-pm-to-txt',
        help='Write HDF5 output (peak matrix) to text format.')
    parser_hplt = subparsers.add_parser(
        'hdf5-pls-to-txt',
        help='Write HDF5 output (peak lists) to text format.')

    #####################
    # Process Scans
    #####################

    parser_scans.add_argument(
        "-i",
        "--input",
        type=str,
        nargs='+',
        required=True,
        metavar='source',
        help="Absolute or relative path to the *.mzml file(s). Must be in same order as 'metascans *txt files'")

    parser_scans.add_argument(
        '-ms',
        '--metascans',
        type=str,
        nargs='+',
        required=True,
        metavar='source',
        help="Absolute or relative path to the comma-delimited *.txt metadata file. Must be in same order and 'input' *mzml files. Header names must contain and be in the following order names =['barcode', 'date/time', 'row', 'col', 'scan', 'ejection time', 'NA'] as output by MS-Parser tool")

    parser_scans.add_argument(
        "-o",
        "--output",
        help="Absolute or relative path to the output file",
        action="store",
        type=str,
        required=True)

    parser_scans.add_argument(
        "-f",
        "--failed-wells",
        help="Absolute or relative path to the *.txt output of which well failed",
        action="store",
        type=str,
        required=True)

    parser_scans.add_argument(
        "-pr",
        "--processed_scans",
        help="Absolute or relative path to the *.txt output of which well failed",
        action="store",
        type=str,
        required=True)

    parser_scans.add_argument(
        "-m",
        "--method",
        help="Method to define which scans to extract data from. DEFAULT = on_scans_no_edge",
        action="store",
        type=str,
        choices=[
            "all_scans",
            "on_scans",
            "off_scans",
            "on_scan_no_edge"],
        default="on_scans_no_edge")

    parser_scans.add_argument(
        "-d",
        "--id-snr",
        help="For identifying on/off scans: Hard SNR threshold for differentiating between on/off scans. DEFAULT = 15",
        action="store",
        type=int,
        default=15)

    parser_scans.add_argument(
        "-t",
        "--id-tol",
        help="For identifying on/off scans: Number of features with SNR > threshold to tolerate in off scans. DEFAULT = 3",
        action="store",
        type=int,
        default=3)

    parser_scans.add_argument(
        "-s",
        "--snr-threshold",
        help="SNR threshold to remove noise features. DEFAULT = 2",
        action="store",
        type=int,
        default=3)

    parser_scans.add_argument(
        "-n",
        "--min-scans",
        help="Minimum number of scans required to be labelled on within a well for sample to be taken forward. DEFAULT = 0",
        action="store",
        type=int,
        default=0)

    parser_scans.add_argument(
        "-r",
        "--rsd-threshold",
        help="RSD filter (scan level): Threshold of RSD of features across scans in sample for it to be retained. DEFAULT = None",
        action="store",
        type=int,
        default=None)

    parser_scans.add_argument(
        "-fr",
        "--min-fraction",
        help="Minimum fraction a peak has to be present. Use 0.0 to not apply this filter.",
        action="store",
        type=float,
        default=None)

    parser_scans.add_argument(
        "-p",
        "--ppm",
        help="Aligning scans: m/z precision (ppm) to align scans in sample - REQUIRED PARAMETER!",
        action="store",
        type=int,
        required=True)

    parser_scans.add_argument(
        '-l',
        '--metalist',
        type=str,
        required=False,
        help="Absolute or relative path to the tab-delimited *.txt file that include the name of the data files (*.mzml) and meta data. "
        "Column names: filename, replicate, batch, injectionOrder, classLabel.")

    #################################
    # Process Samples
    #################################

    parser_samples.add_argument(
        "-i",
        "--input",
        help="Absolute or relative path to the *.hdf5 file containing all peaklists from process scans",
        action="store",
        type=str,
        required=True)

    parser_samples.add_argument(
        "-o",
        "--output",
        help="Absolute or relative path to the output file",
        action="store",
        type=str,
        required=True)

    parser_samples.add_argument(
        "-p",
        "--ppm",
        help="Aligning samples: m/z precision (ppm) to align samples in study - REQUIRED PARAMETER!",
        action="store",
        type=int,
        required=True)

    parser_samples.add_argument(
        "-b",
        "--block-size",
        help="Aligning samples: Number peaks in each centre clustering block for alignment of samples. DEFAULT = 5000 (should increase for large studies)",
        action="store",
        type=int,
        default=5000)

    parser_samples.add_argument(
        "-fr",
        "--min-fraction",
        help="Minimum percentage of samples a peak has to be present.",
        action="store",
        type=float,
        required=False,
        default=None)

    parser_samples.add_argument(
        '-r',
        '--rsd-threshold',
        default=None,
        type=float,
        required=False,
        help="Peaks where the associated QC peaks are above this threshold will be removed.")

    parser_samples.add_argument(
        '-w',
        '--within',
        type=bool,
        nargs='?',
        const=True,
        default=False,
        help="Apply sample filter within each sample class.")

    parser_samples.add_argument('-q', '--qc-label',
                                default=None, type=str, required=False,
                                help="Class label for QCs")

    #################################
    # HDF5 peaklists to text
    #################################

    parser_hplt.add_argument(
        '-i',
        '--input',
        type=str,
        required=True,
        help="Absolute or relative path to the HDF5 file that contains a list of peaklist objects from one of the processing steps.")

    parser_hplt.add_argument("-o", "--output", help="Directory to write to.",
                             action="store", type=str, default=os.getcwd())

    parser_hplt.add_argument(
        '-d',
        '--delimiter',
        default="tab",
        choices=[
            "tab",
            "comma"],
        help="Values on each line of the file are separated by this character.")

    #################################
    # HDF5 peak matrix to text
    #################################

    parser_hpmt.add_argument(
        '-i',
        '--input',
        type=str,
        required=True,
        help="Absolute or relative path to the HDF5 file that contains a peak matrix object from one of the processing steps.")

    parser_hpmt.add_argument('-o', '--output', type=str, required=True,
                             help="Directory to write to.")

    parser_hpmt.add_argument(
        '-a',
        '--attribute_name',
        default="intensity",
        choices=[
            "intensity",
            "mz",
            "snr"],
        required=False,
        help="Type of matrix to print.")

    parser_hpmt.add_argument(
        '-l',
        '--class-label-rsd',
        action='append',
        required=False,
        default=(),
        help="Class label to select samples for RSD calculatons (e.g. QC).")

    parser_hpmt.add_argument(
        '-d',
        '--delimiter',
        default="tab",
        choices=[
            "tab",
            "comma"],
        help="Values on each line of the file are separated by this character.")

    parser_hpmt.add_argument(
        '-s',
        '--representation-samples',
        default="rows",
        choices=[
            "rows",
            "columns"],
        help="Should the rows or columns respresent the samples?")

    parser_hpmt.add_argument(
        '-c',
        '--comprehensive',
        action='store_true',
        required=False,
        help="Whether to output simple or comprehensive version of the peak matrix. Do not use argument if want simple output, use -c or --comprehensive for comprehensive output")

    args = parser.parse_args()

    print(args)

    if args.step == "process-scans":

        peaklists = []
        failed_wells = []
        scans_processed = {}

        for i in range(len(args.input)):

            print("Acquisition; {}".format(args.input[i]))
            # Store spectral data
            run = Mzml(args.input[i])

            # Define which wells scans are associated with
            df = pd.read_csv(args.metascans[i],
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

            if args.metalist is not None:
                metadata = validate_metadata(args.metalist)

            for index, well in df[["well_label"]].drop_duplicates(
            ).iterrows():

                well_scans = list(df[(df["well_label"] == well["well_label"])]["scan"])

                wellInfo = Scans(run, well, well_scans, args.id_snr, args.id_tol)

                scan_ids = wellInfo.extract(args.method)

                if isinstance(scan_ids, str):
                    scans_processed[well[0]] = scan_ids

                else:
                    scans_processed[well[0]] = scan_ids

                if len(scan_ids) < args.min_scans:
                    line = "Well: {}, failed due to: < {} scans in well taken forward. Scan_ids for well: {}".format(
                        well, args.min_scans, scan_ids)
                    failed_wells.append(line)

                else:
                    # Regenerates peak lists for each well (pl is individual
                    # scan) with user defined snr, rsd and min fraction
                    # thresholds
                    # pls is the spectral data (mz, intensity, snr, flags) for
                    # all scans
                    pls = run.peaklists(scan_ids, function_noise="median")

                    pls = [filter_attr(pl, "snr", min_threshold=args.snr_threshold) if len(
                        pl.mz) > 0 else pl for pl in pls]  # Filters out noise using SNR
                    # dataframe with only extracted scans/peaklists
                    pls = [pl for pl in pls if int(pl.ID) in scan_ids]

                    try:
                        # Forms aligned peak matrix from peakLists
                        pm = align_peaks(pls,
                                         ppm=args.ppm,
                                         block_size=5000,
                                         edge_extend=(2 * args.ppm))

                    except ValueError as e:
                        line = "Well: {}, failed due to: {}.".format(well, e)
                        failed_wells.append(line)
                        continue

                    # Generates peakLists from aligned peak matrix
                    pl_aligned = pm.to_peaklist(ID="{}".format(well["well_label"]))

                    if "snr" in pm.attributes:
                        pl_aligned.add_attribute("snr",
                                                 pm.attr_mean_vector("snr"),
                                                 on_index=2)

                    pl_aligned.add_attribute("rsd",
                                             pm.rsd(flagged_only=False),
                                             on_index=4)

                    pl_aligned.add_attribute('snr_flag',
                                             np.ones(pl_aligned.full_size),
                                             flagged_only=False,
                                             is_flag=True)

                    if args.rsd_threshold is not None:
                        rsd_flag = map(lambda x: not np.isnan(x) and x < args.rsd_threshold,
                                       pl_aligned.get_attribute("rsd", flagged_only=False))
                        pl_aligned.add_attribute("rsd_flag",
                                                 rsd_flag,
                                                 flagged_only=False,
                                                 is_flag=True)

                    if args.min_fraction is not None:
                        pl_aligned.add_attribute("internal_fraction_flag",
                                                 (pm.present / float(pm.shape[0])) >= args.min_fraction,
                                                 flagged_only=False,
                                                 is_flag=True)

                    if args.metalist is not None:
                        pl_aligned = update_metadata_and_labels(
                            [pl_aligned], metadata)
                    peaklists.append(pl_aligned[0])

        with open(args.failed_wells, "w") as out:
            for well in failed_wells:
                out.write("{}\n".format(well))

        out_df = pd.DataFrame.from_dict(scans_processed, orient='index')
        out_df.to_csv(args.processed_scans, sep='\t')

        hdf5_portal.save_peaklists_as_hdf5(
            peaklists, "{}.hdf5".format(args.output))

    if args.step == "process-samples":

        peaklists = hdf5_portal.load_peaklists_from_hdf5(args.input)

        peakmatrix = align_peaks(peaklists,
                                 ppm=args.ppm,
                                 block_size=args.block_size,
                                 edge_extend=(2 * args.ppm))  # align peaks into mz bins... ppm = ppm_precision

        peakmatrix = sample_filter(peakmatrix,
                                   min_fraction=args.min_fraction,
                                   within=args.within,
                                   qc_label=args.qc_label,
                                   rsd_thres=args.rsd_threshold)

        hdf5_portal.save_peak_matrix_as_hdf5(peakmatrix, args.output)

    if args.step == 'hdf5-pls-to-txt':
        hdf5_peaklists_to_txt(
            args.input,
            path_out=args.output,
            delimiter=map_delimiter(
                args.delimiter))

    if args.step == 'hdf5-pm-to-txt':
        if args.representation_samples == "rows":
            samples_in_rows = True
        else:
            samples_in_rows = False

        hdf5_peak_matrix_to_txt(args.input,
                                path_out=args.output,
                                attr_name=args.attribute_name,
                                delimiter=map_delimiter(args.delimiter),
                                rsd_tags=args.class_label_rsd,
                                samples_in_rows=samples_in_rows,
                                comprehensive=args.comprehensive)


if __name__ == '__main__':
    main()
