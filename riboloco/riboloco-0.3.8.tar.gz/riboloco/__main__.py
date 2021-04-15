import pandas as pd
import argparse
import subprocess
import numpy as np
from scipy.stats import pearsonr
import os
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.ticker as ticker
import seaborn as sns
import matplotlib.pyplot as plt
import pysam
import math
import random
import collections
from riboloco.shared_riboloco_functions import read_fasta, read_info_file
from sklearn.decomposition import PCA


def find_A_offset(df, max_dist, min_counts_start, min_ratio_start,
                  min_counts_stop, min_ratio_stop, use_stop, args,
                  this_type, fasta_d):
    """
    This function looks for the A offset using conventional start and stop codon enrichment
    The dataframe should already have been filtered
    """
    # Find correct offset using start codon
    df = df.drop("index", axis=1)
    df["distance_from_start1"] = df["end"] - df["cds_start"]
    df["distance_from_end"] = df["end"] - df["cds_end"] + 2  # +2 because we want from the  start of the stop codon

    A_offset_start = offset_from_start(df, max_dist, min_counts_start, min_ratio_start)
    if not args.reference_use_KL:
        if use_stop:
            A_offset_end = offset_from_stop(df, max_dist, min_counts_stop, min_ratio_stop)
        else:
            A_offset_end = "Unsure"  # because we didn't check it

        if A_offset_end == "Unsure" and A_offset_start == "Unsure":
            A_offset = "Unsure"
        else:
            if A_offset_end != "Unsure" and A_offset_start == "Unsure":  # one is fine
                A_offset = A_offset_end
            if A_offset_end == "Unsure" and A_offset_start != "Unsure":  # one is fine
                A_offset = A_offset_start

            if A_offset_end != "Unsure" and A_offset_start != "Unsure":  # then check they're the same!
                if A_offset_end == A_offset_start:
                    A_offset = A_offset_end  # same as start so pick either
                else:  # inconsistent
                    A_offset = "Unsure"

    else:  # use KL
        print("Using KL to determine best offset")
        ignore, fractions, background = find_RUST_ratios(df, this_type, fasta_d, args)
        A_offset = find_A_offset_from_KL(fractions, background, this_type, args)

    return A_offset


def find_A_offset_from_KL(fractions, background, this_type, args):
    """
    Finds the best A site offset by looking for the region with strongest KL divergence
    """

    kld = {}
    for offset, this_fraction_d in fractions.items():
        if (offset + int(this_type.split("_")[1])) % 3 == 0:
            kld[offset] = find_KL(this_fraction_d, background)

    # get the (by default) di-codon sum of KL
    kl_sums = {}
    for i in range(args.kl_length - 1, len(kld.keys())):
        this_sum = 0
        for j in range(args.kl_length):
            this_sum += list(kld.values())[i - j]
        kl_sums[list(kld.keys())[i]] = this_sum

    # remove positions at the read termini
    filtered_d = {}
    read_length = int(this_type.split("_")[0])
    for pos, kl in kl_sums.items():
        if -read_length + 3 * args.kl_length + 2 < pos < -4:
            if args.max_A_offset <= pos <= args.min_A_offset:
                filtered_d[pos] = kl

    A_offset = max(filtered_d, key=filtered_d.get)
    return A_offset


def offset_from_start(df, max_dist, min_counts_start, min_ratio_start):
    """
    This function uses the standard method I've used looking for the offset
    that gives a sudden increase in reads at the start codon.
    This offset gives the P site, so subtract 3 for A site.
    """
    dfs = df[abs(df["distance_from_start1"]) <= max_dist]  # dfs == df_start
    dfs = dfs.reset_index()

    dfs["n_this_distance"] = dfs.groupby(["distance_from_start1"]).transform(len).iloc[:, 0]
    dfs = dfs[["distance_from_start1", "n_this_distance"]].drop_duplicates()

    dfs = dfs.reset_index().sort_values(by=["distance_from_start1"])

    # find biggest increase
    biggest = None  # expect 15 nt for 28 nt reads
    prev_n = 0
    biggest_diff = -100
    for dist, n in zip(dfs.distance_from_start1, dfs.n_this_distance):
        this_diff = n - prev_n
        if this_diff > biggest_diff:
            biggest = dist
            biggest_diff = this_diff
        prev_n = n

    # Check that this is high confidence
    confident = True  # assume true
    n_at_start = int(dfs[dfs["distance_from_start1"] == biggest].n_this_distance)

    if biggest_diff == n_at_start:
        A_offset = "Unsure"
    else:
        if n_at_start < min_counts_start:
            confident = False
        if n_at_start / (n_at_start - biggest_diff) < min_ratio_start:  # ratio > 1 by definition
            confident = False

        if confident:
            A_offset = -(biggest - 3)
        else:
            A_offset = "Unsure"
    return A_offset


def offset_from_stop(df, max_dist, min_counts_stop, min_ratio_stop):
    """
    This function looks for maximum enrichment at the stop codon
    """

    dfs = df[abs(df["distance_from_end"]) <= max_dist]
    dfs = dfs.reset_index()

    dfs["n_this_distance"] = dfs.groupby(["distance_from_end"]).transform(len).iloc[:, 0]
    dfs = dfs[["distance_from_end", "n_this_distance"]].drop_duplicates()

    dfs = dfs.reset_index().sort_values(by=["distance_from_end"])

    # find biggest increase
    biggest = None  # expect 12 nt for 28 nt reads
    prev_n = 0
    biggest_drop = 100  # initialise positive, actual values should be negative
    prev_dist = False
    for dist, n in zip(dfs.distance_from_end, dfs.n_this_distance):
        this_drop = n - prev_n
        if this_drop < biggest_drop:
            biggest = prev_dist
            biggest_drop = this_drop  # should be -ve
        prev_n = n
        prev_dist = dist

    # Check that this is high confidence
    confident = True  # assume true
    n_at_stop = int(dfs[dfs["distance_from_end"] == biggest].n_this_distance)

    if n_at_stop + biggest_drop == 0:
        A_offset = "Unsure"
    else:
        if n_at_stop < min_counts_stop:
            confident = False
        if n_at_stop / (n_at_stop + biggest_drop) < min_ratio_stop:  # >1 by definition
            confident = False

        if confident:
            A_offset = -biggest
        else:
            A_offset = "Unsure"
    return A_offset


def RUST_background(df, fasta_d):
    """
    This function returns the fractional abundance of each codon
    for the transcripts which are present in the data-frame
    """
    # make data-frame with transcripts of interest
    df = df[["transcript_id", "cds_start0", "cds_end"]].drop_duplicates()

    d = make_codon_dict()
    n = 0  # total number of codons
    for transcript_id, start0, end in zip(df["transcript_id"], df["cds_start0"], df["cds_end"]):
        n_codons = (end - start0) // 3 - 1
        seq = fasta_d[transcript_id]
        for x in range(n_codons):
            codon = seq[int(start0) + 3 * x:int(start0) + 3 * x + 3]
            if codon in d.keys():
                d[codon] += 1
                n += 1

    background = {}
    for key, value in d.items():
        background[key] = value / n  # fractional abundance

    return background


def make_codon_dict():
    nts = ["A", "C", "G", "T"]
    codons = {}
    for x in nts:
        for y in nts:
            for z in nts:
                codons[x + y + z] = 0
    return codons


def RUST(df, offset, background, fasta_d):
    """
    This function returns the codon RUST enrichments
    for a given offset
    """
    # Perform the "unit step transformation" and filter

    df["RUST"] = np.where(df["counts_this_type_this_tx_this_pos"] / df["mean_coverage"] >= 1, 1, 0)
    df = df[df["RUST"] == 1]

    d = make_codon_dict()
    n = 0
    e = {}
    n_missed = 0
    for a, b in zip(df["end"], df["transcript_id"]):
        seq = fasta_d[b]
        this_codon = seq[a + offset - 1:a + offset + 3 - 1]
        try:
            d[this_codon] += 1
        except KeyError:
            n_missed += 1  # likely a short transcript -> truncated codon

        n += 1

    # if d["TGA"] / n >= 0.01:
    #     print("Warning - lots of stop codons detected with a nucleotide offset of " + str(offset))

    # calculated codon fractions
    f = {}
    for codon, number in d.items():
        f[codon] = number / sum(d.values())

    # find the level of enrichment compared to background
    for key, value in d.items():
        if background[key] == 0:
            enrichment = 0
        else:
            enrichment = (value / n) / background[key]
        e[key] = enrichment

    return e, f


def generate_bed_df(args, info, fasta_d):
    """
    Reads in the bed file and info file, either choosing the biggest (monosome) file
    or using the single file given
    """

    # Check if the sample input is a csv of samples, or a single sample
    sample_dir = args.sample_dir
    if sample_dir != "":
        if sample_dir[-1] != "/":
            sample_dir = sample_dir + "/"

    if ".csv" in args.samples:
        # then it's a csv
        # First, read in the names of the samples
        samples = []
        with open(args.samples, 'r') as file:
            for line in file:
                samples.append(line.rstrip().replace(',', ''))

        # Work out which file is the biggest, and monosome
        read_nos = {}
        filenames = {}
        for sample in samples:
            if args.monosome_priority:
                if not "Mon" in sample:
                    ignore = True
                else:
                    ignore = False
            else:
                ignore = False

            if not ignore:
                file_name = sample_dir + sample + args.end_name
                filenames[sample] = file_name
                dir_path = os.path.dirname(os.path.realpath(__file__))
                read_nos[sample] = int(
                    subprocess.check_output("zcat " + dir_path + '/' + file_name + " | wc -l", shell=True))
        biggest_sample = max(read_nos, key=read_nos.get)
        print("Biggest sample is " + biggest_sample)

        df, total_counts, total_counts_cds, ss_df = read_bed_ish_file(filenames[biggest_sample], info, args,
                                                               fasta_d)

    else:  # it's a single sample
        print("Reading single sample")
        df, total_counts, total_counts_cds, ss_df = read_bed_ish_file(sample_dir + args.samples, info, args,
                                                               fasta_d)

    return df, total_counts, total_counts_cds, ss_df


def find_APE_of_reference(args, df, fasta_d, total_counts_cds):
    """
    This function is a wrapper that calls various functions that:
        * filters for certain read types, either automatically or the reads specified
        * Uses start and stop codon to try to find offsets
        * finds APE enrichments for these reference read types
    """
    max_dist = args.max_distance
    print("Generating reference")

    if args.read_type == []:
        # Filter for read types that are abundant
        cds_reads = df[["read_type", "counts_this_type_cds"]].drop_duplicates()
        filtered_read_types = cds_reads[cds_reads["counts_this_type_cds"] > total_counts_cds * args.min_abundance_ref]
        read_types = filtered_read_types["read_type"]
    else:
        read_types = args.types_specified

    assert len(read_types) > 0, "No read types with which to build reference - reduce filtering, or manually determine"
    print("Using " + ' '.join(read_types))

    A_offsets = {}
    enrichments = {}
    for read_type in read_types:
        df2 = df[df["read_type"] == read_type]

        if read_type in args.offset_dict.keys():
            A_offset = args.offset_dict[read_type]
            print("Using user specified offset of " + str(A_offset) + " for " + read_type)
        else:
            A_offset = find_A_offset(df2, max_dist, args.min_counts_start, args.min_ratio_start,
                                     args.min_counts_stop, args.min_ratio_stop, args.use_stop, args,
                                     read_type, fasta_d)
            if A_offset == "Unsure":
                print("Offset for " + read_type + " could not be confidently determined")
                continue
            else:
                print("Best A site offset for " + read_type + " is " + str(A_offset) + " nucleotides")

        print("Finding RUST ratios for best offset...")
        enrichments[read_type], ignore, ignore2 = find_RUST_ratios(df2, this_type=read_type,
                                                                   fasta_d=fasta_d, args=args,
                                                                   A_offset=A_offset)
        A_offsets[read_type] = A_offset

    n = 0
    for offset in A_offsets.values():
        if offset != "Unsure":
            n += 1
    assert n > 0, "No offsets could be determined - either reduce stringency," \
                  " provide manual offsets, or use a reference file (eg one " \
                  "generated by a monosome experiment. Use option -g to generate the reference, then -r to read it in)"

    check_offsets_consistent(A_offsets)

    return enrichments, A_offsets


def check_offsets_consistent(A_offsets):
    """
    This function checks that the offsets appear to be consistent.
    It has a few principles:
        1. The range of offsets for the same read length should not be greater than 2
        2. Longer read lengths should not have smaller magnitude offsets (debatable...)
        3. Longer read lengths should not have dramatically longer read lengths - an x nt increase should at most result
            in a x nt increase in offset
    """
    all_consistent = True
    # Principle 1:
    p1 = {}
    for read_type, offset in A_offsets.items():
        read_length = int(read_type.split("_")[0])
        if read_type in p1.keys():
            p1[read_length].append(A_offsets[read_type])
        else:
            p1[read_length] = [A_offsets[read_type]]
    for read_length, offsets in p1.items():
        error_message = "Warning! Offsets for read length " + str(read_length) + " not consistent!"
        if not range_n(offsets) <= 2:
            print(error_message)
            all_consistent = False

    # Principles 2 & 3:
    p2 = collections.OrderedDict(sorted(p1.items()))
    counter = 0
    for read_length, offsets in p2.items():
        counter += 1
        if counter > 1:
            # calculate the lowest possible acceptable offset for this rl

            # remember, max is actually min, and min is actually max...
            lowest_acceptable_offset = -max(prev_offsets) - 2 + range_n(prev_offsets)  # -ve because -ve offsets

            rl_diff = read_length - prev_rl
            highest_acceptable_offset = -min(prev_offsets) + 2 - range_n(prev_offsets) + rl_diff

            if -max(offsets) < lowest_acceptable_offset:  # -ve because -ve offsets, max not min because -ve
                print("Warning! Some offsets for " + str(read_length) + " are smaller than for " + str(prev_rl))
                all_consistent = False
            if -min(offsets) > highest_acceptable_offset:
                print("Warning! Some offsets for " + str(read_length) + " are much larger than for " + str(prev_rl))
                all_consistent = False

        prev_offsets = offsets
        prev_rl = read_length

    # Check Principles 2 & 3 for specific frames
    for frame in range(3):
        d = {}
        for read_type, offset in A_offsets.items():
            this_frame = int(read_type.split("_")[1])
            if this_frame == frame:
                d[read_type] = -offset  # convert to positive
        d = collections.OrderedDict(sorted(d.items()))
        counter = 0
        for read_type, offset in d.items():
            read_length = int(read_type.split("_")[0])
            counter += 1
            if counter > 1:
                if offset < prev_offset:
                    print("Warning! Offset for " + read_type + " is smaller than for " + prev_read_type)
                    all_consistent = False

                rl_diff = read_length - prev_read_length
                offset_diff = offset - prev_offset  # already made them positive
                if offset_diff > rl_diff + 1:  # +1 to stop erroneous warnings
                    print("Warning! Offset for " + read_type + " is much larger than for " + prev_read_type)
                    all_consistent = False

            prev_offset = offset
            prev_read_type = read_type
            prev_read_length = read_length

    if all_consistent:
        print("All offsets are consistent.\n")


def range_n(numbers):
    return abs(max(numbers) - min(numbers))


def read_from_bam(filename, fasta_d):
    """
    This function reads + stranded reads from a bam file.
    It has the benefit that it checks whether the first nucleotide matches the transcriptome
    """
    samfile = pysam.AlignmentFile(filename, "rb")
    tx_ids = []
    start0s = []
    ends = []
    matches = []

    for read in samfile:
        tx_id = read.reference_name
        if not read.is_reverse and tx_id in fasta_d.keys():
            start0 = read.reference_start
            read_length = read.query_length
            end = start0 + read_length
            first_nt = read.query_sequence[0:1]

            tx_ids.append(tx_id)
            start0s.append(start0)
            ends.append(end)
            if first_nt == fasta_d[tx_id][start0:start0 + 1]:
                matches.append("m")
            else:
                matches.append("MM")

    df = pd.DataFrame.from_dict({'transcript_id': tx_ids, 'start0': start0s, 'end': ends, 'strand': "+",
                                 'first_nt_match': matches})
    return (df)


def read_bed_ish_file(filename, info, args, fasta_d):
    """
    This function reads a 6 column bed file and returns it as a data-frame
    after performing some initial analysis and merging with
    the info file (thus meaning it only has the longest transcripts)
    """
    # Read in the file to a pandas df and perform initial processing
    print(filename)
    if "bed" in filename:
        if args.four_column_bed:
            colnames = ["transcript_id", "start0", "end", "strand"]
            df = pd.read_csv(filename, sep='\t', names=colnames, header=None)
        else:
            colnames = ["transcript_id", "start0", "end", "read_name", "score", "strand"]
            df = pd.read_csv(filename, sep='\t', names=colnames, header=None)
            df = df[["transcript_id", "start0", "end", "strand"]]
    elif filename[-4:] == ".bam":
        df = read_from_bam(filename, fasta_d)
    else:
        assert "bed" in filename or filename[-4:0] == ".bam", "filename must best bed or bam file"

    df = df[df.strand.eq('+')]
    df["start1"] = df["start0"] + 1
    df = df.merge(info, on="transcript_id", how="inner")
    assert len(df) > 0, "No reads with information found! Check your transcript bed/bam and info file match! " \
                        "Do you need option -fcb?"
    print("File contains " + str(len(df)) + " reads for which there is information")

    # start analysing read lengths and frame
    df["read_length"] = df["end"] - df["start0"]
    df["frame"] = (df["end"] - df["cds_start"]) % 3

    if args.mismatches and filename[-4:] == ".bam":
        df["read_type"] = df["read_length"].apply(str) + "_" + df["frame"].apply(str) + "_" + df["first_nt_match"]
    else:
        df["read_type"] = df["read_length"].apply(str) + "_" + df["frame"].apply(str)


    df["counts_this_type"] = df.groupby(["read_type"]).transform(len).iloc[:, 0]

    cds = df[df["start1"] >= df["cds_start"]]
    cds = cds[cds["end"] <= cds["cds_end"]]
    cds["counts_this_type_cds"] = cds.groupby(["read_type"]).transform(len).iloc[:, 0]
    cds = cds[["read_type", "counts_this_type_cds"]].drop_duplicates()
    df = df.merge(cds, on="read_type", how="inner")

    size_df = df.groupby(["transcript_id", "read_type", "end"]).size().rename("counts_this_type_this_tx_this_pos")
    df = df.merge(size_df, on=["transcript_id", "read_type", "end"])
    df = df.drop_duplicates().reset_index()

    if args.write_full_data:
        df.drop('index', axis=1).to_csv(args.output_directory + args.output + "_full_file.csv", index=False)

    total_counts = sum(df["counts_this_type_this_tx_this_pos"])
    total_counts_cds = sum(cds["counts_this_type_cds"])

    # Get start and stop codon dfs for each read length
    ss_df = make_ss_df(df)

    # Filter for abundant read types that are periodic
    df = filter_non_periodic(df, args)
    df = df[~df["read_type"].isin(args.list_to_ignore)]

    assert len(df) > 0, "Filtering removed all reads! Trying setting less stringent parameters."
    return df, total_counts, total_counts_cds, ss_df


def gen_ss_df(df, cds_start_or_end, region):
    """
    Looks for number of reads at each distance from start or stop codon
    cds_start_or_end = "cds_start" or "cds_end"
    """
    df['distance'] = df['end'] - df[cds_start_or_end]
    df = df[abs(df['distance']) <= region]
    df = df[['distance', 'read_length', "counts_this_type_this_tx_this_pos"]]
    df = df.reset_index().groupby(['distance', 'read_length']).sum().drop_duplicates().reset_index()

    # need to add zero values
    lengths = df['read_length'].drop_duplicates()
    length_list = []
    dist_list = []
    counts_list = []
    for dist in range(-region, region):
        this_df = df[df["distance"] == dist]
        for length in lengths:
            df2 = this_df[this_df['read_length'] == length]
            length_list.append(length)
            dist_list.append(dist)
            if len(df2) == 1:
                counts_list.append(list(df2["counts_this_type_this_tx_this_pos"])[0])
            else:
                counts_list.append(0)

    df = pd.DataFrame.from_dict({'distance': dist_list, 'counts_this_type_this_tx_this_pos': counts_list,
                                 'read_length': length_list})

    df["frame"] = df["distance"] % 3
    return df


def make_ss_df(df, region=100):
    """
    This is a function for showing periodicity around start and stop codons
    """
    start_df = gen_ss_df(df, "cds_start", region)
    start_df['start_or_end'] = "start"
    end_df = gen_ss_df(df, "cds_end", region)
    end_df["start_or_end"] = "end"
    combined = start_df.append(end_df)
    return combined.reset_index()


def filter_non_periodic(df, args):
    """
    This function removes read lengths which are not periodic. The level of stringency can be user specified.
    """
    df2 = df[["read_type", "counts_this_type", "read_length"]].drop_duplicates().reset_index()

    df2["max_this_rl"] = df2.groupby("read_length")["counts_this_type"].transform('max')
    df2["min_this_rl"] = df2.groupby("read_length")["counts_this_type"].transform('min')
    df2["periodicity"] = df2["max_this_rl"] / df2["min_this_rl"]
    df2 = df2[df2["periodicity"] >= args.periodicity]
    df3 = df2[["read_type", "periodicity"]]
    df = df.merge(df3, on="read_type", how="inner")
    return df


def save_refs_to_file(d, args):
    """
    This function takes the double nested dictionary with the RUST
    ratios for the reference and writes it to a csv
    """
    print("Saving reference")
    to_write_to = args.output_directory + args.output + '.ref'
    with open(to_write_to, 'w') as file:
        file.write("codon,read_type,E,P,A\n")
        for read_type, enrichments in d.items():
            codons = make_codon_dict().keys()
            sites = ["E", "P", "A"]
            for codon in codons:
                this_line = codon + "," + read_type
                for site in sites:
                    this_line += "," + str(d[read_type][site][codon])
                this_line += "\n"
                file.write(this_line)

    return to_write_to, d.keys()


def read_ref(ref_file):
    """
    This function reads the file produced by save_ref_to_file()
    and converts it back into a nested dictionary
    """

    prev_read_type = "None"
    refs = {}
    with open(ref_file, 'r') as file:
        for a, line in enumerate(file):
            if a > 0:  # skip header
                split = line.rstrip().split(",")
                read_type = split[1]

                if read_type != prev_read_type:
                    if prev_read_type != "None":
                        ref = {"A": refA, "E": refE, "P": refP}
                        refs[prev_read_type] = ref
                    refE = {}
                    refA = {}
                    refP = {}

                refE[split[0]] = float(split[2])
                refP[split[0]] = float(split[3])
                refA[split[0]] = float(split[4])
                prev_read_type = read_type

    ref = {"A": refA, "E": refE, "P": refP}
    refs[read_type] = ref
    return refs


def find_RUST_ratios(df, this_type, fasta_d, args, A_offset="not_provided"):
    """
    Calculates RUST ratios at each offset.
    It is a wrapper around the RUST() function
    """

    APE = {}
    fractions = {}
    if A_offset != "final":
        df2 = df[df["read_type"] == this_type]
        # Filter for reads within CDS
        df2 = df2[df2["start1"] + args.max_offset > df2["cds_start"] + 5]
        df2 = df2[df2["end"] + args.min_offset < df2["cds_end"] - 5]
    else:  # if it is final
        df2 = df

    df2 = df2.reset_index()

    df2["total_counts"] = df2.groupby("transcript_id")["counts_this_type_this_tx_this_pos"].transform(np.sum)
    df2["mean_coverage"] = 3 * df2["total_counts"] / df2["cds_length"]

    # calculate the background for this read type
    background = RUST_background(df2, fasta_d)

    if A_offset == "not_provided":
        # calculate rust ratios at each codon for a range of positions
        for nt_offset in range(args.max_offset, args.min_offset + 1):
            APE[nt_offset], fractions[nt_offset] = RUST(df2, nt_offset, background, fasta_d)

    elif A_offset == "final":  # ie this is the final combined bed graph. Assume 15 nt
        for nt_offset in range(args.max_offset + 15, args.min_offset + 15 + 1):
            APE[nt_offset], fractions[nt_offset] = RUST(df2, nt_offset, background, fasta_d)

    else:  # then we're just looking for the APEs of the reference
        d = {-2: "E", -1: "P", 0: "A"}
        for aa_offset in range(-2, 1):  # -2 = E, 0 = A
            APE[d[aa_offset]], fractions[aa_offset] = RUST(df2, 3 * aa_offset + A_offset, background, fasta_d)

    return APE, fractions, background


def find_best_offsets(these_ratios, this_type, args, ref_APEs):
    """
    This function looks through all the RUST ratios produced. Of course, 2/3 will be out of frame. It looks for
    the best match.
    these_ratios = dictionary of RUST ratios at each position
    ref_APEs = nested dictionary of references
    """

    r_values = {}
    for E_site_test in these_ratios.keys():
        if E_site_test + 6 in these_ratios.keys():
            test_d = {}
            test_d["E"] = these_ratios[E_site_test]
            test_d["P"] = these_ratios[E_site_test + 3]
            test_d["A"] = these_ratios[E_site_test + 6]

            cors = []
            for ref in ref_APEs.keys():
                if not ref == this_type + "_added":  # ensure no self referencing
                    cors.append(round(find_cor(ref_APEs[ref], test_d), 4))

            r_values[E_site_test + 6] = max(cors)
    r_values_filtered = {}
    for key, value in r_values.items():
        if (int(this_type.split('_')[1]) + key) % 3 != 0 and not args.allow_out_of_frame:
            continue
        if args.max_A_offset <= value <= args.min_A_offset:
            r_values_filtered[key] = value
    best_nt_offset = max(r_values_filtered, key=r_values.get)

    if (int(this_type.split('_')[1]) + best_nt_offset) % 3 != 0:
        print("Warning - for " + this_type + " best offset is out of frame!")

    # check if bad or ambiguous
    bad = check_if_bad_match(r_values, args)

    return bad, best_nt_offset, r_values


def check_if_bad_match(r_values, args):
    # check if this was a bad or ambiguous match
    bad = False
    if max(r_values.values()) < args.min_score:
        bad = True  # just straight up bad
    if len([a for a in r_values.values() if a >= args.ambiguity * max(r_values.values()) and
                                            a != max(r_values.values())]):
        bad = True  # ambiguous
    return bad


def find_abundance_ratio(df, bin_width, near_start_pos, downstream_pos):
    """
    Finds the number of reads upstream and downstream
    """

    total_near_start = sum(df[(df["start0"] - df["cds_start"] > near_start_pos) &
                              (df["start0"] - df["cds_start"] <
                               near_start_pos + bin_width)].counts_this_type_this_tx_this_pos)

    total_downstream = sum(df[(df["start0"] - df["cds_start"] > downstream_pos) &
                              (df["start0"] - df["cds_start"] <
                               downstream_pos + bin_width)].counts_this_type_this_tx_this_pos)

    return total_near_start, total_downstream


def find_out_of_frameness(df, read_types, bin_width, near_start_pos=0, downstream_pos=1000):
    """
    This function finds the enrichment of a specific read type near the start, versus near the end.
    The idea is that reads with a stronger bias to near the start codon are more enriched for out of frame reads, due
    to leaky scanning and uORFs.
    This function ignores offsets, just uses the *starts* (not the ends! - better compatibility with disomes etc) of
    each read
    """
    # Find the overall read enrichment at start and end
    df = df[
        ["transcript_id", "read_type", "start0", "end", "counts_this_type_this_tx_this_pos", "cds_start", "cds_end"]]
    df = df.drop_duplicates()

    df = df[(df["start0"] > df["cds_start"]) & (df["end"] < df["cds_end"])]

    total_near_start, total_near_end = find_abundance_ratio(df, bin_width, near_start_pos, downstream_pos)
    average_ratio = total_near_start / total_near_end

    # find for each read types
    frameness_d = {}
    for read_type in read_types:
        dfr = df[df["read_type"] == read_type]
        this_near_start, this_near_end = find_abundance_ratio(dfr, bin_width, near_start_pos, downstream_pos)
        frameness_d[read_type] = (this_near_start / this_near_end) / average_ratio

    return frameness_d


def oof_enrichment(df, orf_df, offset=14):
    """
    This function finds the number of reads present in positions in frame 1, frame 2 and frame 3
    It assumes an offset of -14.
    """
    df = df[["transcript_id", "end", "counts_this_type_this_tx_this_pos"]]
    df = df.merge(orf_df, on="transcript_id", how="inner")
    df = df[(df["end"] - offset > df["orf_start"]) & (df["end"] - offset < df["orf_stop"])]

    d = {}
    for f in range(3):
        d[f] = sum(df[df["orf_frame"] == f].counts_this_type_this_tx_this_pos)

    return d


def save_KL(fractions, background, this_type, offset, args, save):
    """
    This function calculates the KL divergence at each position compared to the background, then saves this
    """
    # We will only consider in frame KL
    offset_list = []

    if offset == "final":  # i.e. this from the final bed file where "end" now refers to end of start codon
        offset = 2  # because need to subtract 2 to get start of codon

    for this_offset in fractions.keys():
        if (offset - this_offset) % 3 == 0:
            offset_list.append(this_offset)

    kl_d = {}
    for this_offset in offset_list:
        if this_type == "final":
            kl_d[this_offset + 1] = find_KL(fractions[this_offset], background)
        else:
            kl_d[this_offset - offset] = find_KL(fractions[this_offset], background)

    filename = args.output_directory + args.output + '.kl_div.csv'

    if this_type == "final":
        this_type = "combined"  # clearer name

    if save:
        with open(filename, 'a') as file:
            for corrected_offset, kl in kl_d.items():
                file.write(','.join([this_type, str(int(corrected_offset / 3)), str(kl)]) + '\n')

    return kl_d


def find_KL(f, background):
    """
    This function returns the KL divergence of the background versus the given read
    """
    # First, convert background to fractions (wait - aren't they already?) Well...whatever.
    b = {}
    for codon, number in background.items():
        b[codon] = number / sum(background.values())

    kl = 0
    for codon in b.keys():
        # only defined when P(x) and Q(x) > 0
        if b[codon] > 0 and f[codon] > 0:
            # if codon not in ["TAG", "TAA", "TGA"]:  # ignore stops because they confuse things
            kl += f[codon] * np.log2(f[codon] / b[codon])

    return kl


def find_oof_fracs(df, orf_df, start, end, read_type="all", offset=14):
    """
    This is a wrapper around oof_enrichment()
    It takes a df, optionally filters it for a specific read type, then analyses enrichment of orfs for this df
    between 'start' and 'end'
    """
    if read_type != "all":
        df = df[df["read_type"] == read_type]

    df = df[(df["end"] > df["cds_start"] + start) &
            (df["end"] < df["cds_start"] + end + offset)]

    total_oof = oof_enrichment(df, orf_df)

    if sum(total_oof.values()) > 0:
        enrichment_d = {'total': sum(total_oof.values()),
                        0: total_oof[0] / sum(total_oof.values()),
                        1: total_oof[1] / sum(total_oof.values()),
                        2: total_oof[2] / sum(total_oof.values())}
    else:
        enrichment_d = {'total': sum(total_oof.values()),
                        0: -1,
                        1: -1,
                        2: -1}

    return enrichment_d


def append_to_ref(ref_APEs, these_ratios, offset, this_type):
    """
    This function adds to the reference list of APEs during assignment
    """
    name = this_type + "_added"
    d = {-6:"E", -3:"P", 0:"A"}
    to_add = {}
    for position, ratios_d in these_ratios.items():
        if position - offset in d.keys():
            to_add[d[position-offset]] = ratios_d
    ref_APEs[name] = to_add
    return ref_APEs


def convert_bed_to_single_codon_res(args, df, fasta_d, ref_APEs, precalculated_offsets,
                                    total_counts_cds, info, orf_df, oof_df, ss_df, oof_distance=500):
    """
    This function finds the best APE offset for each
    read length that passes filtering by comparing to the reference APE RUST
    enrichments provided.
    Then writes them out.

    refs = double nested dictionary of RUST ratios of reference
    precalculated_offsets = dictionary of offsets that were calculated already
    """

    if args.orf_search:
        background_oof_d = find_oof_fracs(df, orf_df, start=0, end=oof_distance, read_type='all')

    print("Converting to single codon resolution")

    # Remove read types with too few counts
    counts_df = df[["read_length", "read_type", "counts_this_type_cds"]].drop_duplicates()  # store for later
    df = df[df["counts_this_type_cds"] > args.min_abundance * total_counts_cds]

    # Check if user specified further filtering
    if not args.keep_all_valid:
        if len(args.conversion_types) > 0:
            df = df[df["read_type"].isin(args.conversion_types.keys())]

    # Get a list of all the types we have
    types = df[["read_type"]].drop_duplicates()

    full_d = {}  # nested dictionary of each aa offset's RUST ratios for each read type
    best_nt_offsets = {}
    all_r_values = {}
    best_r_values = {}
    oof_d = {}
    kl_d_d = {}
    ratios_d = {}
    fractions_d = {}
    background_d = {}

    frameness_d = find_out_of_frameness(df, types["read_type"], 100)
    out_of_frame = []

    done_dict = {}
    calculated = []
    for this_type in types['read_type']:
        done_dict[this_type] = 0

    while min(done_dict.values()) == 0:  # some aren't done

        # ranodomly select one that hasn't been assigned yet
        to_assign = [a for a in done_dict.keys() if done_dict[a] == 0]
        this_type = random.choice(to_assign)

        done_dict[this_type] = 1 # this one is done...for now

        assigned = False  # assume false
        print("Attempting to find match for " + this_type)

        if this_type not in calculated:  # hasn't been calculated yet
            # Calculate APE for all offsets, including those specified
            these_ratios, these_fractions, this_background = find_RUST_ratios(df, this_type, fasta_d, args)
            full_d[this_type] = these_ratios
            ratios_d[this_type] = these_ratios
            background_d[this_type] = this_background
            fractions_d[this_type] = these_fractions
            calculated.append(this_type)

        if args.use_KL:
            best_nt_offsets[this_type] = find_A_offset_from_KL(these_fractions, this_background, this_type, args)
            print("Using max KL divergence best offset is "+str(best_nt_offsets[this_type]) + " for " + this_type)
            done_dict.pop(this_type)

        # find best r values and offsets
        bad, best_nt_offset, r_values = find_best_offsets(these_ratios=ratios_d[this_type], this_type=this_type,
                                                          args=args, ref_APEs=ref_APEs)

        upstream_enrichment = frameness_d[this_type]
        if upstream_enrichment >= args.frameness_ratio:
            if args.verbose:
                print("Warning, read type " + this_type + " is enriched " + str(round(100 * (upstream_enrichment - 1))) +
                  "% near the start codon. This suggests it has a lot of out of frame reads (or is low read depth)")
            out_of_frame.append(this_type)

        if args.orf_search:
            this_oof_d = find_oof_fracs(df, orf_df, start=0, end=oof_distance, read_type=this_type)

            e1 = this_oof_d[1] / background_oof_d[1]
            e2 = this_oof_d[2] / background_oof_d[2]
            if e1 > 1.20:
                print(this_type + " is " + str(round(100 * (e1 - 1))) + "% enriched for (out of) frame 1")
            if e2 > 1.20:
                print(this_type + " is " + str(round(100 * (e2 - 1))) + "% enriched for (out of) frame 2")
            enrichment_d = {1: round(100 * (e1 - 1), 2), 2: round(100 * (e2 - 1), 2)}
            oof_d[this_type] = enrichment_d

        # If user specified offset for this then use it, else use the best match calculated
        if this_type in args.conversion_types.keys():
            if args.conversion_types[this_type] != "NA":  # ie an offset was specified
                best_nt_offsets[this_type] = args.offset_dict[this_type]
                best_r_values[this_type] = r_values[args.offset_dict[this_type]]
                assigned = True
                done_dict.pop(this_type)  # remove
                if args.offset_dict[this_type] != best_nt_offset and not args.use_KL:
                    print("Warning! For " + this_type + " user specified " + str(args.offset_dict[this_type]) + " but "
                                                                                                                "" + str(
                        best_nt_offset) + " was a better match to reference!")

        else:  # If no offset was specified...
            if not bad:  # if good
                assigned = True
                if this_type in done_dict.keys():
                    done_dict.pop(this_type)  # remove
                if this_type in precalculated_offsets.keys():  # this was in reference so best already calculated
                    best_nt_offsets[this_type] = precalculated_offsets[this_type]
                    best_r_values[this_type] = r_values[precalculated_offsets[this_type]]
                    print("Offset assigned: " + str(precalculated_offsets[this_type]))
                else:  # this was not in reference so offset was calculated in this function
                    if not args.use_KL:
                        best_nt_offsets[this_type] = best_nt_offset
                        if not args.no_iterative_improvement:
                            print("Adding " + this_type + " to reference")
                            ref_APEs = append_to_ref(ref_APEs, ratios_d[this_type], best_nt_offset, this_type)
                            # now, because reference has expanded, reset all dones
                            for key in done_dict.keys():
                                done_dict[key] = 0  # reset them all to zero
                    best_r_values[this_type] = max(r_values.values())
                    print("Offset assigned: " + str(best_nt_offset))
        all_r_values[this_type] = r_values

        if assigned:
            kl_d_d[this_type] = save_KL(fractions_d[this_type],
                                        background_d[this_type],
                                        this_type, best_nt_offsets[this_type], args,
                                        save=args.save_stats)

        if len(done_dict) == 0:
            break

    if not args.no_iterative_improvement:
        # recalculate r values
        for this_type in types['read_type']:
            _, _, r_values = find_best_offsets(these_ratios=ratios_d[this_type], this_type=this_type,
                                                              args=args, ref_APEs=ref_APEs)
            all_r_values[this_type] = r_values
            best_r_values[this_type] = max(r_values.values())

    print("\nFinal Assignments:")

    for key, value in best_nt_offsets.items():
        if key in out_of_frame:
            add = " but a significant fraction of footprints may be derived from out of frame ribosomes"
        else:
            add = ""
        print(key + " assigned " + str(value) + " with r = " + str(round(best_r_values[key], 3)) + add)

    assert len(df) > 0, "Filtering removed all reads! Try less stringent parameters, or build a better reference."

    check_offsets_consistent(best_nt_offsets)
    write_files(df, full_d, best_nt_offsets, args, all_r_values, oof_df, oof_d, frameness_d, fasta_d, counts_df,
                total_counts_cds, kl_d_d, ss_df, orf_df)

    return best_nt_offsets


def write_combined_distinct_bedgraph(df, best_nt_offsets, args):
    """
    This function writes a single bedgraph file. Importantly, it keeps all the read types separate.
    """

    offset_df = pd.DataFrame(list(zip(best_nt_offsets.keys(), best_nt_offsets.values())),
                             columns=["read_type", "A_offset"])

    df = df.merge(offset_df, on="read_type", how="outer")

    df = df[["transcript_id", "start0", "end", "counts_this_type_this_tx_this_pos", "read_type",
             "A_offset"]].drop_duplicates()

    df["A_site_start0"] = df["end"] + df["A_offset"] - 1
    df["A_site_end"] = df["A_site_start0"] + 1

    outfile = args.output_directory + args.output + ".distinct.bedgraph"

    df.to_csv(outfile, sep="\t", header=True, index=False, na_rep="NA")


def write_rust(full_d, best_nt_offsets, args):
    """
    This function writes out the RUST ratios
    """

    outfile = args.output_directory + args.output + ".rust_values.csv"

    with open(outfile, 'w') as file:
        file.write("read_type,offset,codon,rust_ratio,in_frame\n")

    for read_type, this_d in full_d.items():
        if read_type in best_nt_offsets.keys():  # check this one was assigned
            for offset, codon_d in this_d.items():
                codon_offset = int(offset - best_nt_offsets[read_type])
                if codon_offset % 3 == 0:
                    in_frame = "True"
                else:
                    in_frame = "False"
                with open(outfile, 'a') as file:
                    for codon, ratio in codon_d.items():
                        file.write(read_type+','+str(codon_offset)+','+codon+','+str(ratio)+','+in_frame+'\n')


def plot_abundances(counts_df, total_counts_cds, best_nt_offsets, pdf_pages, min_frac):
    """
    Plot bar chart of how abundance each read type is
    """
    df = counts_df[counts_df["counts_this_type_cds"] > min_frac * total_counts_cds]
    df = df.sort_values(by="read_length")
    df["assigned"] = [a in best_nt_offsets.keys() for a in df["read_type"]]
    ax = sns.barplot(x="read_type", y="counts_this_type_cds", hue="assigned", data=df, dodge=False)

    for item in ax.get_xticklabels():
        item.set_rotation(90)

    fig = ax.get_figure()
    pdf_pages.savefig(fig)


def order_d(d):
    """
    Orders dictionary on read length and frame
    """
    length_d = {}
    for key in d.keys():
        if "combined" in key:
            length_d[key] = 1000000
        else:
            length_d[key] = int(key.split("_")[0]) + 0.1*(float(key.split("_")[1]))
    # order by lengths
    ordered = sorted(length_d, key=length_d.get)
    to_return = collections.OrderedDict()
    for key in ordered:
        to_return[key] = d[key]
    return to_return


def plot_KL_and_r(kl_d_d, pdf_pages, title, vmax=1.0, square=False, only_in_frame=False):

    read_types = []
    positions = []
    kls = []
    ordered_d = order_d(kl_d_d)

    for read_type, d in ordered_d.items():
        for pos, kl in d.items():
            if only_in_frame and (pos+int(read_type.split("_")[1])) % 3 != 0:
                continue
            read_types.append(read_type)
            positions.append(pos)
            if square:
                kls.append(kl ** 2)  # useful when "kl" is actually an r value to get r-squared
            else:
                kls.append(kl)

    df = pd.DataFrame.from_dict({'read_type':read_types, 'pos':positions, 'kl':kls})
    df = df.pivot(index="read_type", columns="pos")

    p = sns.heatmap(df.iloc[:,1:], cbar=False, vmin=0, vmax=vmax, cmap="Reds", label='small')
    p.set_yticks(range(len(df)))
    p.set_yticklabels(ordered_d.keys(), size=8)
    p.set_title(title)
    pdf_pages.savefig(p.figure)


def order_list(types):
    """
    wrapper around order_d()
    """
    d = {}
    for this_type in types:
        d[this_type] = 0

    return order_d(d).keys()


def plot_cds_metaprofile(df, best_nt_offsets, pdf_pages, min_abundance):
    df = df[df["counts_this_type_cds"] > min_abundance]
    types = df["read_type"].drop_duplicates()
    types = order_list(types)
    for this_type in types:
        plt.clf()
        cds_metaprofile(df[df["read_type"] == this_type], best_nt_offsets, pdf_pages, this_type)


def make_meta_dict():
    d = {}
    for i in range(201):
        if i < 20:
            d[i] = '5utr'
        elif 20 <= i <= 170:
            d[i] = 'cds'
        else:
            d[i] = '3utr'
    return d


def cds_metaprofile(df, best_nt_offsets, pdf_pages, this_type, offset=-13):
    """
    200 bins; the 5'utr from 0:20, CDS 20:170, 3'utr 170:200
    Uses an assumed offset
    """

    five_utr = df[df['end'] + offset < df['cds_start']]
    three_utr = df[df['end'] + offset > df['cds_end']]
    cds = df[df['cds_start'] <= df['end'] + offset]
    cds = cds[cds['cds_start'] + offset <= cds['cds_end']]

    five_utr["bin"] = round(20*(five_utr['end'] + offset)/five_utr['cds_start'])
    cds['bin'] = round(150*(cds['end']+offset-cds['cds_start'])/(cds['cds_end']-cds['cds_start'])) + 20
    three_utr['bin'] = round(30*(cds['end']+offset-cds['cds_end'])/(cds['tx_length'] - cds['cds_end'])) + 170

    meta_dict = make_meta_dict()

    df = five_utr.append(cds).append(three_utr)
    meta = df.groupby('bin', as_index=False).agg({'counts_this_type_this_tx_this_pos':'sum'})
    meta['coverage'] = meta['counts_this_type_this_tx_this_pos']
    meta['type'] = meta['bin'].map(meta_dict)
    meta = meta[meta['bin'] <= 200]

    p = sns.barplot(x="bin", y="coverage", hue='type', data=meta, dodge=False)
    if this_type in best_nt_offsets.keys():
        p.set_title('Metaplot for ' + this_type + ' (assigned)')
    else:
        p.set_title('Metaplot for ' + this_type + ' (not assigned)')
    p.set(xticklabels=[])
    pdf_pages.savefig(p.figure)


def plot_pca(full_d, best_nt_offsets, pdf_pages):

    offset_d = {-6:"E", -3:"P", 0:"A"}
    codons = make_codon_dict().keys()
    ratios_d = {}
    types = []
    for this_type, d in full_d.items():
        ratios_list = []
        if this_type in best_nt_offsets.keys():
            types.append(this_type)
            for offset, ratios in d.items():
                corrected_offset = offset - best_nt_offsets[this_type]
                if corrected_offset in offset_d.keys():
                    for codon in codons:
                        if codon not in ["TGA", "TAA", "TAG"]:
                            try:
                                ratios_list.append(ratios[codon])
                            except KeyError:
                                ratios_list.append(0)
            ratios_d[this_type] = ratios_list

    ratio_df = pd.DataFrame.from_dict(ratios_d, orient="index")
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(ratio_df)
    principalDf = pd.DataFrame(data=principalComponents, columns=['principal component 1', 'principal component 2'])
    principalDf["read_type"] = types
    p = sns.scatterplot(x='principal component 1', y='principal component 2', data=principalDf)
    p.set_title("PCA of decoding centres - 1: " + str(round(100*pca.explained_variance_[0])) + '% 2: ' +
                                                   str(round(100*pca.explained_variance_[1])) + '%')

    for read_type, x, y in zip(types, principalDf['principal component 1'], principalDf['principal component 2']):
        p.text(x, y, read_type, horizontalalignment='left', size='small', color='black', weight='semibold')

    pdf_pages.savefig(p.figure)


def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w


def plot_oof_heatmap(df, pdf_pages, window):
    positions = df["position"].drop_duplicates()
    background_df = df[df["read_type"] == "background"]
    read_types = df["read_type"].drop_duplicates()

    back1s = []
    back2s = []
    diffs1 = {}
    diffs2 = {}
    ra_diffs1 = {}
    ra_diffs2 = {}

    for position in positions:
        back1s.append(float(background_df[background_df["position"] == position].frame1_fraction))
        back2s.append(float(background_df[background_df["position"] == position].frame2_fraction))

        this_df = df[df["position"] == position]

        # find the difference to background
        for read_type in read_types:
            if read_type in diffs1.keys():
                diffs1[read_type].append(float(this_df[this_df["read_type"] == read_type].frame1_fraction - back1s[-1]))
            else:
                diffs1[read_type] = [float(this_df[this_df["read_type"] == read_type].frame1_fraction - back1s[-1])]

            if read_type in diffs2.keys():
                diffs2[read_type].append(float(this_df[this_df["read_type"] == read_type].frame2_fraction - back2s[-1]))
            else:
                diffs2[read_type] = [float(this_df[this_df["read_type"] == read_type].frame2_fraction - back2s[-1])]

    for read_type in read_types:
        if read_type != "background":
            ra_diffs1[read_type] = moving_average(diffs1[read_type], window)
            ra_diffs2[read_type] = moving_average(diffs2[read_type], window)

    ra_diffs1 = order_d(ra_diffs1)
    ra_diffs2 = order_d(ra_diffs2)

    df1 = pd.DataFrame.from_dict(ra_diffs1, orient="index")
    df1.columns = positions[window // 2:window // 2 + len(df1.columns)]
    df2 = pd.DataFrame.from_dict(ra_diffs2, orient="index")
    df2.columns = positions[window // 2:window // 2 + len(df2.columns)]

    p1 = sns.heatmap(df1, vmin=-0.1, vmax=0.1, cmap="bwr", label='small')
    p1.set_title("Enrichment for altORFs in frame 1")
    pdf_pages.savefig(p1.figure)
    plt.clf()
    p2 = sns.heatmap(df2, vmin=-0.1, vmax=0.1, cmap="bwr", label='small')
    p2.set_title("Enrichment for altORFs in frame 2")
    pdf_pages.savefig(p2.figure)


def plot_around_start_or_stop(ss_df, best_nt_offsets, pdf_pages):
    # find which read lengths are of interest
    lengths = []
    for read_type in best_nt_offsets.keys():
        read_length = int(read_type.split("_")[0])
        if read_length not in lengths:
            lengths.append(read_length)
    lengths.sort()
    for start_or_end in ['start', 'end']:
        for this_length in lengths:
            this_ss_df = ss_df[ss_df["start_or_end"] == start_or_end]
            this_ss_df = this_ss_df[this_ss_df["read_length"] == this_length]
            this_ss_df["counts"] = this_ss_df["counts_this_type_this_tx_this_pos"]
            plt.clf()
            p = sns.barplot(x="distance", y="counts", hue="frame", data=this_ss_df, dodge=False)
            p.set_title(str(this_length) + 'nt reads around ' + start_or_end)
            p.xaxis.set_major_locator(ticker.MultipleLocator(base=20))
            pdf_pages.savefig(p.figure)


def write_files(df, full_d, best_nt_offsets, args, r_values, oof_df, oof_d, frameness_d, fasta_d, counts_df,
                total_counts_cds, kl_d_d, ss_df, orf_df):
    print("Writing files...")

    if args.save_stats:
        print("Saving data files")
        save_stats(r_values, args, oof_d, frameness_d, df)
        write_rust(full_d, best_nt_offsets, args)
        if args.oof_plot:
            read_types_each_orf(df, orf_df, filename=(args.output_directory+args.output+'.read_enrichment.csv'))

    if args.plot_graphs:
        with PdfPages(args.output_directory + args.output + "_plots.pdf") as pdf_pages:
            print("Saving graphs")
            plt.clf()
            plot_abundances(counts_df, total_counts_cds, best_nt_offsets, pdf_pages, args.min_abundance)
            plt.clf()
            print("Saving KL heatmap")
            df2 = df[df["read_type"].isin(best_nt_offsets.keys())]
            kl_d_d['combined'] = write_combined_bedgraph(df2, best_nt_offsets, args, fasta_d)
            plot_KL_and_r(kl_d_d, pdf_pages, title="K-L divergences of assigned reads", vmax=0.5)
            plt.clf()
            print("Saving R values heatmaps")
            plot_KL_and_r(r_values, pdf_pages, title="R-squared values", square=True)
            plt.clf()
            plot_KL_and_r(r_values, pdf_pages, title="R-squared values (in frame only)",
                          square=True, only_in_frame=True)
            plt.clf()
            print("Saving RUST codon heatmaps")
            plot_RUST_enrichments(full_d, best_nt_offsets, pdf_pages)
            plt.clf()
            print("Saving metaprofiles")
            plot_cds_metaprofile(df, best_nt_offsets, pdf_pages, args.min_abundance)
            plt.clf()
            plot_around_start_or_stop(ss_df, best_nt_offsets, pdf_pages)
            plt.clf()
            print("Saving PCA")
            plot_pca(full_d, best_nt_offsets, pdf_pages)
            plt.clf()
            if args.oof_plot:
                print("Saving oof heatmap")
                plot_oof_heatmap(oof_df, pdf_pages, args.oof_smooth_window)

    if args.keep_read_types_distinct:
        write_combined_distinct_bedgraph(df, best_nt_offsets, args)

    if args.write_individual_files:
        write_individual_bedgraphs(df, best_nt_offsets, args)

    print("Complete!")


def read_types_each_orf(df, orf_df, filename, offset=-14):
    """
    This function goes through each orf in orf_d and finds the number of each read type. It assumes an offset
    of -14
    """
    df["est"] = df["end"] + offset  # estimated position
    df = df.reset_index()[["transcript_id", "read_type", "est", "counts_this_type_this_tx_this_pos", 'gene_name']]

    orf_df['orf_id'] = orf_df["transcript_id"]+"_"+orf_df["orf_start"].apply(str)+"_"+orf_df["orf_stop"].apply(str)

    combined = df.merge(orf_df, on="transcript_id", how='inner')
    combined = combined[combined["est"] >= combined["orf_start"]]
    combined = combined[combined["est"] <= combined["orf_stop"]]

    # find the number of each read type
    numbers = combined.groupby(["orf_id", "read_type", "annotated", "gene_name"]).sum()["counts_this_type_this_tx_this_pos"]
    numbers = numbers.to_frame().reset_index().drop_duplicates()
    totals = numbers.reset_index().groupby("orf_id").sum().drop_duplicates()
    totals["total_counts_orf"] = totals["counts_this_type_this_tx_this_pos"]

    totals = totals.drop(["counts_this_type_this_tx_this_pos"], axis=1).reset_index()
    numbers = numbers.merge(totals, on="orf_id")
    numbers['fraction'] = numbers["counts_this_type_this_tx_this_pos"]/numbers["total_counts_orf"]

    numbers.to_csv(filename, index=False)


def save_stats(r_values, args, oof_d, frameness_d, df):
    if len(oof_d) > 0:
        header = ["read_type", "offset", "r_value", "n_cds", "upstream_enrichment", "frame1_enrich", "frame2_enrich"]
    else:
        header = ["read_type", "offset", "r_value", "n_cds", "upstream_enrichment"]

    read_numbers = df[["read_type", "counts_this_type_cds"]].drop_duplicates()

    outfile = args.output_directory + args.output + ".r_values.csv"

    with open(outfile, 'w') as file:
        file.write(','.join(header) + "\n")
        for read_type, d in r_values.items():
            n_cds = str(read_numbers[read_numbers["read_type"] == read_type].counts_this_type_cds.iloc[0])
            for offset, r_value in d.items():
                line = [read_type, str(offset), str(r_value), n_cds, str(frameness_d[read_type])]
                if len(oof_d) > 0:
                    line += [str(oof_d[read_type][1]), str(oof_d[read_type][2])]
                file.write(','.join(line) + "\n")


def write_combined_bedgraph(df, best_nt_offsets, args, fasta_d):
    counter = 0
    for key, value in best_nt_offsets.items():
        counter += 1
        df2 = df[df["read_type"] == key]
        df2 = df2.drop("index", axis=1)
        df2["A_start0"] = df2["end"] + value
        df2["A_end"] = df2["A_start0"] + 1

        df2 = df2[["transcript_id", "A_start0", "A_end", "start1", "end",
                   "cds_start0", "cds_end", "cds_length", "counts_this_type_this_tx_this_pos"]]

        if counter == 1:
            df3 = df2
        else:
            df3 = df3.append(df2)

    # combined counts
    size_df = df3[["transcript_id", "A_start0", "counts_this_type_this_tx_this_pos"]].reset_index().groupby(
        ["transcript_id", "A_start0"]).sum().rename(columns={"counts_this_type_this_tx_this_pos": "counts_this_pos"})
    df3 = df3.merge(size_df, on=["transcript_id", "A_start0"])
    df4 = df3[["transcript_id", "A_start0", "A_end", "counts_this_pos"]]
    df4 = df4.reset_index().drop_duplicates()
    df4.to_csv(args.output_directory + args.output + ".bedgraph", sep="\t", header=False, index=False)

    df3 = df3.rename({'counts_this_pos': "counts_this_type_this_tx_this_pos"})

    # -6 to avoid stop codons
    df3 = df3[(df3['start1'] + args.max_offset > df3['cds_start0'] + 3) & (df3['end'] +
                                                                           args.min_offset < df3['cds_end'] - 6)]

    df3 = df3[["transcript_id", 'A_end', "cds_start0", "cds_end",
               "cds_length", "counts_this_type_this_tx_this_pos"]].reset_index().drop_duplicates()
    df3 = df3.rename(columns={'A_end': "end"})  # trick the function... *evil laugh*

    APE, fractions, background = find_RUST_ratios(df3, "final", fasta_d, args, A_offset="final")

    final_kl = save_KL(fractions=fractions, background=background, this_type="final", offset="final", args=args,
                       save=args.save_stats)

    return final_kl


def write_individual_bedgraphs(df, best_nt_offsets, args):
    """
    Writes individual bed style files with the A site
    """
    for key, value in best_nt_offsets.items():
        df2 = df[df["read_type"] == key]
        df2["A_start0"] = df2["end"] + value
        df2["A_end"] = df2["A_start0"] + 1

        df2 = df2[["transcript_id", "A_start0", "A_end", "counts_this_type_this_tx_this_pos"]]

        df2.to_csv(args.output_directory + args.output + key + ".bedgraph", sep="\t", header=False, index=False)


def plot_RUST_enrichments(full_d, best_nt_offsets, pdf_pages):
    """
    this function generates heatmaps of the RUST enrichments at each position
    for the different read types

    full_d is a double nested dictionary with all the RUST enrichments
    for each read type and each position

    best_aa_offsets is a dict with the A site offsets for each read type
    """

    # First, work out what types we have
    types = best_nt_offsets.keys()
    types = order_list(types)

    # Create a pandas dataframe with all data for this sample
    for this_type in types:
        this_dict_for_df = {"codon": make_codon_dict().keys()}  # this will contain all the columns for this type

        d = full_d[this_type]  # dictionary with a bunch of positions
        for nt_offset, e in d.items():  # e is the dictionary of codon enrichments
            rel_offset = nt_offset - best_nt_offsets[this_type]
            if rel_offset % 3 == 0:
                this_dict_for_df[int(rel_offset)] = [np.log2(a + 0.00001) for a in
                                                e.values()]  # add each rust ratio to dictionary

        # convert to numpy and generate heatmap
        this_df = pd.DataFrame.from_dict(this_dict_for_df)
        # remove stop codons
        this_df = this_df[~this_df["codon"].isin(["TAG", "TAA", "TGA"])]

        # create plot
        p = sns.heatmap(this_df.drop("codon", axis=1), cbar=False, vmin=-2, vmax=2, cmap="bwr", label='small')
        p.set_yticks(range(len(this_df)))
        p.set_yticklabels(this_df["codon"], size=5)

        p.set_title("Codon RUST heatmap for " + this_type)

        for item in p.get_yticklabels():
            item.set_rotation(0)

        _, xlabels = plt.xticks()
        p.set_xticklabels(xlabels, size=5)
        pdf_pages.savefig(p.figure)
    plt.clf()


def find_cor(ref, test_d):
    """
    This function returns the correlation between the EPA site
    rust ratios for the reference versus a given test set
    of rust ratios for a given offset.

    This function takes two nested dictionaries, one for the
    reference, and one for the offset being tested
    """
    sites = ["A", "P", "E"]
    codons = make_codon_dict().keys()
    refs = []
    tests = []
    for site in sites:
        for codon in codons:
            if not (codon == "TGA" or codon == "TAA" or codon == "TAG"):
                refs.append(np.log2(ref[site][codon] + 0.0001))
                tests.append(np.log2(test_d[site][codon] + 0.0001))
    diff = pearsonr(refs, tests)
    return diff[0]


def check_args(args):

    if args.orf_file != "none_provided":
        args.oof_plot = True
        args.orf_search = True
    else:
        args.oof_plot = False
        args.orf_search = False

    if args.orf_search or args.oof_plot:
        assert args.orf_file != "None_provded", "Need to provide orf file generated with riboloco_find_orfs!"

    if len(args.output_directory) > 0:
        if args.output_directory[-1] != "/":
            args.output_directory += "/"

    assert args.max_offset <= args.min_offset, "Max offset must be more negative than min offset."

    if args.ignore != "None":
        args.list_to_ignore = [a for a in args.ignore.split(":")]
        print("Ignoring " + ' '.join(args.list_to_ignore))
    else:
        args.list_to_ignore = []

    if args.keep_all_valid:
        assert args.generate_reference == False, "Cannot use keep_all_valid mode when generating a reference"
        assert args.offset != "None", "Must specify at least one offset when using keep_all_valid mode"

    if len(args.read_type) > 0 and args.reference != "None":
        print("Warning - ignoring offsets specified because you have supplied a reference!")

    args.offset_dict = {}  # for reference offsets
    if len(args.read_type) > 0 and args.reference == "None":
        args.types_specified = []
        for entry in args.read_type:
            # check if an offset was specified
            this_type = entry.split(":")[0]
            if len(entry.split(":")) > 1:
                offset = entry.split(":")[1]
                args.offset_dict[this_type] = int(offset)

            args.types_specified.append(this_type)

        check_in_frame(args.offset_dict)
        for key, value in args.offset_dict.items():
            print(" ".join(["Using an offset of", str(value), "for", str(key), "during reference generation"]))

    args.conversion_types = {}
    if len(args.conversion_types_list) > 0:
        for entry in args.conversion_types:
            this_type = entry.split(":")[0]
            if len(this_type.split(":")) > 0:
                this_offset = this_type.split(":")[1]
            else:
                this_offset = "NA"
            args.conversion_types[this_type] = this_offset
        check_in_frame(args.conversion_types)

    if args.orf_file != "none_provided":
        args.orf_search = True

    assert 1 >= args.ambiguity >= 0, "Ambiguity must be between 0 and 1"

    return args


def check_in_frame(d):
    for ts, offset in d.items():
        if offset != "NA":
            frame = int(ts.split("_")[1])
            if (frame + offset) % 3 != 0:
                print("Specified offset for " + ts + " is out of frame!")


def gen_oof_plot(df, orf_df, start, end, stride, output, min_abundance, total_counts_cds,
                 args):
    """
    This function generates a heatmap of out of frame enrichment, and also saves the raw values to csv
    """
    #
    print("Generating out of frame heatmap")
    df = df[df["counts_this_type_cds"] > min_abundance * total_counts_cds]

    types = df[["read_type"]].drop_duplicates()

    # Check if user specified further filtering
    if not args.keep_all_valid:
        if len(args.conversion_types) > 0:
            df = df[df["read_type"].isin(args.conversion_types.keys())]

    windows = math.ceil((end - start) / stride)

    pos = []
    read_types = []
    total_orfs = []
    frame0_frac = []
    frame1_frac = []
    frame2_frac = []
    enrichment_1 = []
    enrichment_2 = []

    for i in range(windows):
        this_start = start + stride * i
        this_end = this_start + stride - 1
        print("Analysing " + str(this_start) + " to " + str(this_end))

        background_oof_d = find_oof_fracs(df, orf_df, start=this_start,
                                          end=this_end, read_type='all')
        pos.append(this_start)
        read_types.append("background")
        total_orfs.append(background_oof_d["total"])
        frame0_frac.append(background_oof_d[0])
        frame1_frac.append(background_oof_d[1])
        frame2_frac.append(background_oof_d[2])
        enrichment_1.append(0)  # by definition
        enrichment_2.append(0)  # by definition

        for this_type in types["read_type"]:
            this_oof_d = find_oof_fracs(df, orf_df, start=this_start,
                                        end=this_end, read_type=this_type)

            if this_oof_d['total'] > 0:
                e1 = this_oof_d[1] / background_oof_d[1]
                e2 = this_oof_d[2] / background_oof_d[2]
            else:  # if no reads of this type in this window
                # assume same as background
                e1 = 1
                e2 = 1

            pos.append(this_start)
            read_types.append(this_type)
            total_orfs.append(this_oof_d["total"])
            frame0_frac.append(this_oof_d[0])
            frame1_frac.append(this_oof_d[1])
            frame2_frac.append(this_oof_d[2])
            enrichment_1.append(e1 - 1)
            enrichment_2.append(e2 - 1)

    out_df = pd.DataFrame.from_dict({'position': pos,
                                     'stride': stride,
                                     'read_type': read_types,
                                     'total_orfs': total_orfs,
                                     'frame0_fraction': frame0_frac,
                                     'frame1_fraction': frame1_frac,
                                     'frame2_fraction': frame2_frac,
                                     'frame1_enrichment': enrichment_1,
                                     'frame2_enrichment': enrichment_2})

    out_df.to_csv(output + ".oof_csv.csv", index=False)

    return out_df


def main():
    pd.options.mode.chained_assignment = None  # default='warn'
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--samples", type=str, required=False,
                        help="In reference generation mode this may either be a .csv file of samples "
                             "(you MUST ensure that the file is of '.csv' otherwise it will not be recognised) "
                             "or a single bed file. \n"
                             "In conversion mode it must be a single bed file. "
                             "Bed files should be transcriptome-aligned; only reads in the + strand are used. "
                             "\nBed files should be 6 column, with transcript_id, start, end, and strand in "
                             "columns 1, 2, 3 and 6 respectively (the default output from bedtools' 'bamtobed'). "
                             "Bed files can be in .gzip format if desired.")
    parser.add_argument("-i", "--info", type=str, required=False, help="Info file on transcripts. This should be "
                                                                      "a tab separated file with details on the CDS "
                                                                      "within each transcript. It should contain the "
                                                                      "columns 'transcript_id', 'cds_start' and "
                                                                      "'cds_stop'. The coordinates MUST be 1-based!")
    parser.add_argument("-f", "--transcript_fasta", type=str, required=False, help="Fasta file of transcripts")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output file")
    parser.add_argument("--orf_file", type=str, default="none_provided",
                        help="An orf csv generated with riboloco_find_orfs. Supplying this will activate more "
                             "intensive searching for out of frame ribosomes.")
    parser.add_argument("-a", "--min_abundance", required=False, type=float, default=0.01,
                        help="Minimum abundance of read length/frame to be included in final output. "
                             "Default is 0.01. Set to zero to disable. This can me lower than --min_abundance_ref, "
                             "the rationale being that you want to use abundant read lengths to build the reference,"
                             " but any read length that matches the reference well should be included in the final "
                             "file.")
    parser.add_argument("-ar", "--min_abundance_ref", required=False, type=float, default=0.1,
                        help="Minimum fraction of total reads that a read type must represent for calculation of "
                             "a reference offset (using start and stop codon enrichment) to be attempted. Default=0.1 "
                             "(10pc). Warning - using low values may promote inclusion of reads which are primarily "
                             "out of frame. Recommended to keep above 0.05. Read fractions are calculated for reads "
                             "within the annotated CDS - UTRs are ignored.")
    parser.add_argument("-t", "--read_type", nargs="+", type=str, default=[],
                        help="Set the read type for which the reference is calculated in reference generation mode."
                             "Additionally, you can specify the offset with a colon, eg 28_0:-12.")
    parser.add_argument("-pg", "--plot_graphs", action="store_true", required=False, default=False,
                        help="When selected, dislocate plots various graphs and heatmaps which may be useful for "
                             "downstream analysis, or to verify accuracy of offset assignments.")
    parser.add_argument("-ms", "--min_score", required=False, type=float, default=0.7,
                        help="The minimum correlation between the reference and the RUST ratios for the "
                             "assigned offset for the file to be written. Default = 0.7")
    parser.add_argument("-g", "--generate_reference", required=False, action="store_true", default=False,
                        help="Activates reference generation mode - use this mode to make a reference "
                             "before converting bed files to single nucleotide resolution")
    parser.add_argument("-r", "--reference", required=False, type=str, default="None",
                        help="Pre-computed reference file csv, generated by dislocate in 'generate reference' mode. "
                             "Multiple references can be specified by adding a colon between files. "
                             "Optional when running in conversion mode.")
    parser.add_argument("--allow_out_of_frame", required=False, action="store_true", default=False,
                        help="Allow out of frame offsets to be assigned")
    parser.add_argument("-ct", "--conversion_types_list", nargs="+", default=[],
                        help="Types to output. Can specify an offset with colon, eg 28_0:-12. Using this command "
                             "will cause other types to be ignored, unless you also use --keep_all_valid")
    parser.add_argument("-k", "--keep_all_valid", required=False, action="store_true", default=False,
                        help="This option (only applicable during conversion mode) keeps all valid read types "
                             "(i.e. all those that pass periodicity and abundance filters) even when specific "
                             "read lengths and offsets are set.")
    parser.add_argument("-rkl", "--reference_use_KL", action="store_true", default=False,
                        help="Use KL divergence to find best offset during reference generation")
    parser.add_argument("-ukl", "--use_KL", action="store_true", default=False,
                        help="Use KL divergence to determine best A site offset during assignment")
    parser.add_argument("-p", "--periodicity", type=float, required=False, default=2,
                        help="Periodicity filter - the minimum ratio of reads in the major frame to the minor frame "
                             "for a given read length to pass filtering. Default is 2; higher numbers are more "
                             "stringent. Set to 1 to remove filtering")
    parser.add_argument("-kll", "--kl_length", type=int, default=2, required=False,
                        help="The number of codons to use for KL-based determination of offsets. By default = 2 "
                             "i.e. the P and A sites.")
    parser.add_argument("-us", "--use_stop", action="store_true", default=False, required=False,
                        help="If argument is used, riboloco will attempt to assign offsets based on stop codon as well "
                             "as the start codon. Riboloco will use this value during reference generation if either "
                             "it is consistent with the start codon determined offset, or if no start codon-based "
                             "offset could be determined (e.g. with disomes)")
    parser.add_argument("-minao", "--min_A_offset", type=int, default=3, required=False,
                        help="The miniumum offset length from the 3' end of the E site. (Not the A site) "
                             "Length is measured in nt. Default = 3")
    parser.add_argument("-maxao", "--max_A_offset", type=int, default=-22, required=False,
                        help="The maximum offset length from the 3' end of the E site (not the A site). "
                             "Length is measured in nt. Default = -22")
    parser.add_argument("-mino", "--min_offset", type=int, default=10, required=False,
                        help="The miniumum which is analysed when plotting "
                             "Length is measured in nt. Default = 10")
    parser.add_argument("-maxo", "--max_offset", type=int, default=-40, required=False,
                        help="The maximum offset which is analysed when plotting. "
                             "Length is measured in nt. Default = -40")
    parser.add_argument("-ig", "--ignore", required=False, default="None", type=str,
                        help="Read types to ignore. Can add multiple with a colon separator. Eg -ig 27_2:23_1.") # TODO convert to list
    parser.add_argument("-wif", "--write_individual_files", action="store_true", required=False, default=False,
                        help="When selected, dislocate also writes individual bedgraph files for each read "
                             "length/frame. This could be useful for downstream analysis.")
    parser.add_argument("-krd", "--keep_read_types_distinct", action="store_true", default=False,
                        help="Write out a single bedgraph, but keep the read types distinct (useful for downstream"
                             "analysis). Default = False")
    parser.add_argument("-ss", "--save_stats", action="store_true", required=False, default=False,
                        help="Save a csv of the r values for each type, read and offset.")
    parser.add_argument("--min_counts_start", type=int, default=25, required=False,
                        help="The minimum number of counts of a given read type at the start codon for a read's "
                             "offset to be confidently assigned. Default=25")
    parser.add_argument("--min_ratio_start", type=float, default=4, required=False,
                        help="The minimum ratio of the start codon counts of a given read type "
                             "versus the previous position for an "
                             "offset based on the start codon to be confidently assigned. Default=4")
    parser.add_argument("--min_counts_stop", type=int, default=25, required=False,
                        help="The minimum number of counts of a given read type at the stop codon for a read's "
                             "offset to be confidently assigned. Default=25. To block stop offsets being used, "
                             "set to large number eg 100000")
    parser.add_argument("--min_ratio_stop", type=float, default=4, required=False,
                        help="The minimum ratio of the stop codon counts of a given read type "
                             "versus the next position for an "
                             "offset based on the stop codon to be confidently assigned. Default=4")
    parser.add_argument("--max_distance", type=int, default=20, required=False,
                        help="Maximum distance in nucleotides around start and stop codons for which offsets "
                             "are attempted to be calculated. Default is 20. Twenty is plenty.")
    parser.add_argument("--frameness_ratio", type=float, default=1.2, required=False,
                        help="The level of enrichment near the start codon versus downstream for a read type to be "
                             "reported as potentially having strong bias towards out of frame ribosomes. "
                             "Default = 1.2 i.e. 20percent")
    parser.add_argument("-mm", "--mismatches", action="store_true", default=False,
                        help="Whether to consider first nt mismatches. Only available when a bam file is provided")
    parser.add_argument("--ambiguity", type=float, default=0.8,
                        help="Much much better the best r value must be compared to the second best for an offset "
                             "to be confidently assigned. Default = 0.8, i.e. the r value of second best offset must "
                             "be less than 0.8x the value of the best offset. Lower values are more stringent. Should "
                             "be less than 1, and more than 0")
    parser.add_argument("--oof_plot_start", type=int, default=0,
                        help="How far downstream of the annotated start to look for out of frame reads. Default=0. "
                             "Set to negative values to search for uORFs")
    parser.add_argument("--oof_plot_end", type=int, default=2000,
                        help="How far downstream of the annotated start to look for out of frame reads. Default=2000.")
    parser.add_argument("--oof_plot_stride", type=int, default=50,
                        help="How wide each of the windows in the oof heatmap should be in nucleotides. Default=50nt")
    parser.add_argument("-nii", "--no_iterative_improvement", action="store_true", default=False,
                        help="By default, when using RUST ratio correlations to determine offsets, when new matches"
                             " are found they are added to the reference. This option stops this behaviour")
    parser.add_argument("--verbose", default=False, action="store_true")
    parser.add_argument("--oof_smooth_window", default=1, type=int, help="Rolling average smoothing for oof heatmap")
    parser.add_argument("-sd", "--sample_dir", type=str, required=False, default="",
                        help="Directory of the input files. This optional argument can be useful when passing a "
                             "csv of filenames to -s in reference generation mode.")
    parser.add_argument("-d", "--output_directory", type=str, required=False, default="",
                        help="The directory to save outputs.")
    parser.add_argument("-m", "--monosome_priority", required=False,
                        default=False, action="store_true",
                        help="During reference generation mode, and if a .csv of sample files is passed to the "
                             "function, this option ensures that only monosome files, i.e. those with 'Mon' "
                             "in the sample name(!), are used for reference generation.")
    parser.add_argument("-fcb", "--four_column_bed", action="store_true", required=False, default=False,
                        help="select if using a four column bed with the strand in the 4th column")
    parser.add_argument("--write_full_data", action="store_true", default=False,
                        help="Write out the raw bed/bam file reads with read type and info")


    args = parser.parse_args()
    args = check_args(args)

    # Read in the bed file, fasta file and info file
    fasta_d = read_fasta(args.transcript_fasta)
    info = read_info_file(args.info)

    if args.save_stats:
        with open(args.output_directory + args.output + '.kl_div.csv', 'w') as file:
            file.write(','.join(['read_type', 'offset', 'kl']) + '\n')

    # read bed/bam file
    df, total_counts, total_counts_cds, ss_df = generate_bed_df(args,
                                                         info,
                                                         fasta_d)  # if a csv of files is provided, will read the biggest
    # Generate a reference, or read it in
    if args.reference == "None":
        ref_APEs, precalculated_offsets = find_APE_of_reference(args, df, fasta_d, total_counts_cds)
        if args.generate_reference:
            print("Saving references to file")
            save_refs_to_file(ref_APEs, args)
    else:  # if a reference is provided
        print("Reading reference provided...")
        ref_APEs = read_ref(args.reference)
        precalculated_offsets = {}

    # Now, find offsets and write out files
    if not args.generate_reference:

        if args.orf_search or args.oof_plot:
            orf_df = pd.read_csv(args.orf_file)
        else:  # if not doing an ORF search
            orf_df = "None"

        if args.oof_plot:
            oof_df = gen_oof_plot(df=df, orf_df=orf_df, start=args.oof_plot_start, end=args.oof_plot_end,
                         stride=args.oof_plot_stride, output=args.output_directory+args.output,
                         min_abundance=args.min_abundance, total_counts_cds=total_counts_cds,
                         args=args)
        else:
            oof_df = None

        # Convert bed file to single codons
        convert_bed_to_single_codon_res(args=args, df=df, fasta_d=fasta_d, ref_APEs=ref_APEs,
                                        precalculated_offsets=precalculated_offsets, total_counts_cds=total_counts_cds,
                                        info=info, orf_df=orf_df, oof_df=oof_df, ss_df=ss_df)


if __name__ == "__main__":
    main()