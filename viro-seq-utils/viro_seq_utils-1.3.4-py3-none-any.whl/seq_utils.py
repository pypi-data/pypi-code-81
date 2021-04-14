#! /usr/bin/env python3

"""
author: Nicolas JEANNE
email: jeanne.n@chu-toulouse.fr
Created on 10 apr. 2019
Copyright (C) PTI CHU Purpan
"""

from collections import OrderedDict
import copy
import csv
import logging
import re

from viro_seq_utils import aln_utils


def get_records_wo_stops(records):
    """
    Get the records without stops codons on at least one frame.

    :param list records: the Sequence records.
    :return: the list of records without stops codons on at least one frame.
    :rtype: list
    """
    records_without_stops = []
    for rec in records:
        for i in range(3):
            # add trailing N to avoid Biopython warning during translation for
            # incomplete codon
            ungapped = rec.seq.ungap("-")
            tmp_nt_seq = ungapped[i:] + ("N" * (3 - len(ungapped[i:]) % 3))
            if "*" not in tmp_nt_seq.translate():
                # no stops in at least one ORF
                records_without_stops.append(rec)
                break
    return records_without_stops


def dereplicate_fasta(fastas, pattern="[Cc]ount=(\\d+)", verbose=True):
    """
    Dereplicate sequences by adding the count information (count=xxx) on the Sequence Record
    description.

    :param list fastas: a list of potentially replicated fasta Bio.SeqRecord.
    :param str pattern: the regular expression to retrieve the count information in the fasta
    headers. Default is [Cc]ount=(\\d+)
    :param bool verbose: display warnings.
    :return: the list of dereplicated Bio.SeqRecord.
    :rtpe: list
    """

    # create the dictionary to retrieve the sequences
    dereplicated = {}
    for record in fastas:
        count = get_count(record, pattern, verbose)
        if str(record.seq) in dereplicated:
            dereplicated[str(record.seq)]["count"] += count
        else:
            dereplicated[str(record.seq)] = {"count": count, "record": record}

    # update the final count of the SeqRecord description
    for key in dereplicated:
        dereplicated[key]["record"].description = "count={}".format(dereplicated[key]["count"])

    dereplicated = OrderedDict(sorted(dereplicated.items(), key=lambda d: d[1]["count"], reverse=True))

    return [dereplicated[key]["record"] for key in dereplicated]


def get_count(record, pattern_count="[Cc]ount=(\\d+)", verbose=True):
    """
    Get the count of a read. The count is found with the pattern and
    searched in the record ID, then in the record description.
    If the count is not found, the count is set to 1.

    :param Bio.SeqRecord record: the sequence record.
    :param re pattern_count: regular expression to retrieve the count from the fasta record.
    :param bool verbose: display warnings.
    :return: the count.
    :rtype: int
    """

    pattern = re.compile(pattern_count)
    search_count_found_id = pattern.search(record.id)
    if search_count_found_id:
        reads_count = int(search_count_found_id.group(1))
    else:
        search_count_found_description = pattern.search(record.description)
        if search_count_found_description:
            reads_count = int(search_count_found_description.group(1))
        else:
            reads_count = 1
            if verbose:
                logging.warning("Reads count set to 1 for {0}, count pattern \"{1}\" not found in the "
                                "fasta header: {0} {2}".format(record.id, pattern.pattern, record.description))
    return reads_count


def check_if_aa_seq(assumed_aa, gaps_ok=True, stops_ok=False):
    """Check if the sequence provided is a valid amino-acids sequence, if not, raise a ValueError
    Exception.

    :param str assumed_aa: the sequence record to check.
    :param boolean gaps_ok: set if gaps "-" are accepted.
    :param boolean stops_ok: set if stops "*" or "X" are accepted.
    """
    valid_aa = ["A", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "P",
                "Q", "R", "S", "T", "V", "W", "Y", "X", "U", "O",
                "a", "c", "d", "e", "f", "g", "h", "i", "k", "l", "m", "n", "p",
                "q", "r", "s", "t", "v", "w", "y", "x", "u", "o"]
    if gaps_ok:
        valid_aa.append("-")
    if stops_ok:
        valid_aa = valid_aa + ["*", "X"]
    if False in [aa in valid_aa for aa in assumed_aa.seq]:
        raise ValueError(("The sequence \"{}\" is not a valid AA sequence, it contains at least a "
                          "character which is not:\n{}").format(assumed_aa.id, ", ".join(valid_aa)))


def check_if_nt_seq(assumed_nt, gaps_ok=True, ambiguity_ok=False):
    """Check if the sequence provided is a valid nucleotides sequence, if not, raise a ValueError
    Exception.

    :param str assumed_nt: the sequence record to check.
    :param boolean gaps_ok: set if gaps "-" are accepted.
    :param boolean ambiguity_ok: set if ambiguous nucleotides are accepted.
    """
    valid_nt = ["A", "C", "G", "T", "a", "c", "g", "t"]
    if gaps_ok:
        valid_nt.append("-")
    if ambiguity_ok:
        valid_nt = valid_nt + ["B", "D", "H", "K", "M", "R", "S", "V", "W", "Y",
                               "b", "d", "h", "k", "m", "r", "s", "v", "w", "y"]
    if False in [nt in valid_nt for nt in assumed_nt.seq]:
        raise ValueError(("The sequence \"{}\" is not a valid nucleotides sequence, it contains at "
                          "least a character which is not: {}").format(assumed_nt.id, ", ".join(valid_nt)))


def count_overlapping(pattern_string, string_to_search):
    """"
    Find the occurrences count of an overlapping pattern and get the counts and index positions.
    Start from left and start searching for the pattern, when found increment the counter
    and keep on search from next index position.

    :param str pattern_string: the regular expression string.
    :param str string_to_search: the string in which the pattern is searched.
    :return: a tuple of the number of occurrences and the list of their start positions.
    :rtype: tuple(int, list)
    """
    counter = 0
    start = 0
    indexes = []
    pattern = re.compile(pattern_string)
    while True:
        match = pattern.search(string_to_search, start)
        if match is None:
            return counter, indexes
        indexes.append(match.start())
        counter += 1
        start = 1 + match.start()


def compute_regions_charge_nglyco(align, regions_coord_path):
    """
    Compute the charge and the number of N-glycosylation sites by region for each sequence of an
    alignment based on a reference sequence in the alignment.
    The region reference sequence and the coordinates (0-indexed) of the regions are provided by
    a comma separated file, ex:
    <SEQUENCE_ID>
    <REGION_1_ID>,<START_COORD>,<END_COORD>
    <REGION_2_ID>,<START_COORD>,<END_COORD>
    ...
    <REGION_X_ID>,<START_COORD>,<END_COORD>

    :param Bio.Align.MultipleSeqAlignment align: the alignment of amino acids.
    :param str regions_coord_path: the path to the CSV file of the region reference coordinates.
    :return: the reference ID and the dictionary by sequence, excepted the numbering position reference sequence, by
    region of the charge and the number of N-glycosylation sites. The dictionary is:
    {<SEQ_ID>: {<REGION>: {"charge": <INT>, "nglyco": <INT>}}}
    :rtype: str, dict
    """

    # 0-indexed regions
    regions_coord = {}
    region_ref_seq_id = None
    regions_ordered = []
    with open(regions_coord_path, "r") as regions_file:
        reader = csv.reader(regions_file)
        region_ref_seq_id = reader.__next__()[0]
        for row in reader:
            regions_ordered.append(row[0])
            regions_coord[row[0]] = {"start": int(row[1]), "end": int(row[2])}

    # get the regions reference sequence
    try:
        regions_ref = aln_utils.get_seq_from_id_in_aln(align, region_ref_seq_id)
    except IndexError as exc:
        exc.message = ("{} regions reference sequence not found "
                       "in the alignment file.").format(region_ref_seq_id)
        raise exc
    # get the HXB2 regions position in the alignment
    nb_gap_ref_region = 0
    regions_in_aln = {}
    idx_reading_ref = 0
    for region in regions_ordered:
        regions_in_aln[region] = {"start": None, "end": None}
        for idx in range(idx_reading_ref, len(regions_ref.seq)):
            if regions_ref.seq[idx] == "-":
                nb_gap_ref_region += 1
            if regions_in_aln[region]["start"] is None:
                if idx - nb_gap_ref_region == regions_coord[region]["start"]:
                    regions_in_aln[region]["start"] = idx
            if idx - nb_gap_ref_region == regions_coord[region]["end"]:
                regions_in_aln[region]["end"] = idx
                idx_reading_ref = idx + 1
                break

    data = {}
    for record in align:
        if not record.id == "reference" and not record.id == "HXB2_K03455_env_AA":
            data[record.id] = {}
            for region in regions_in_aln:
                tmp = copy.copy(record)
                tmp.seq = tmp.seq[regions_in_aln[region]["start"]:regions_in_aln[region]["end"]+1]
                data[record.id].update({region: {"charge": net_charge(tmp),
                                                 "nglyco": count_N_glycosylation_site(tmp)[0]}})
    return region_ref_seq_id, data


def net_charge(aa_record, use_h=False):
    """Compute the net charge of an amino-acids sequence (BioPython SeqRecord) using the heuristic:
        R, K and optionaly H residues: +1
        D, E residues: -1

    :param Bio.SeqRecord aa_record: the biopython amino-acids sequence record.
    :param boolean use_h: use H residues as +1 for the net charge computation, default is False.
    :return: the net charge of the amino acids sequence.
    :rtype: int
    """

    try:
        # check if it is a valid AA sequence
        check_if_aa_seq(aa_record)
        # remove the gaps from the sequence
        seq = aa_record.seq.ungap("-").upper()
    except ValueError as exc:
        raise exc
    except TypeError as exc:
        raise exc

    # compute the net charge
    computed_charge = 0
    positive_aa = ["R", "K"]
    if use_h:
        positive_aa.append("H")
    negative_aa = ["D", "E"]
    for aa in seq:
        if aa in positive_aa:
            computed_charge += 1
        elif aa in negative_aa:
            computed_charge -= 1

    return computed_charge


def net_charge_pk(aa_record, use_n_c_term=False):
    """Compute the net charge of an amino-acids sequence using
    the dissociation constants of the amino-acids and the physiological pH (7.4).

    :param Bio.SeqRecord aa_record: the biopython amino-acids sequence record.
    :param bool use_n_c_term: the boolean to use the N and C terminal amino acids in the net charge computation.
    :return: the net charge of the amino acids sequence.
    :rtype: float
    """

    # Methode SeqinR
    # REF: https://www.rdocumentation.org/packages/seqinr/versions/3.1-3/topics/pk
    print("""[WARNING] net_charge_pk(), charge Net calculée à partir de la méthode SeqinR (https://www.rdocumentation.org/packages/seqinr/versions/3.1-3/topics/pk)
          Différente de la méthode MOORE net_charge_pk2(), reste à déterminer laquelle est la plus adaptée.""")

    try:
        # check if it is a valid AA sequence
        check_if_aa_seq(aa_record)
        # remove the gaps from the sequence
        seq = aa_record.seq.ungap("-").upper()
    except ValueError as exc:
        raise exc
    except TypeError as exc:
        raise exc

    # compute the net charge
    ph = 7.4
    positive_aa = ["R", "K", "H"]
    negative_aa = ["D", "E", "C", "Y"]

    pk = {"NH3": {"A": 9.69, "R": 9.04, "N": 8.8, "D": 9.6, "C": 10.28, "E": 9.67,
                  "Q": 9.13, "G": 9.6, "H": 9.17, "O": 9.65, "I": 9.6, "L": 9.6,
                  "K": 8.95, "M": 9.21, "F": 9.13, "P": 10.6, "S": 9.15, "T": 9.1,
                  "W": 9.39, "Y": 9.11, "V": 9.62, "U": 0.0},
          "COOH": {"A": 2.34, "R": 2.17, "N": 2.02, "D": 1.88, "C": 1.96, "E": 2.19,
                   "Q": 2.17, "G": 2.34, "H": 1.82, "O": 1.82, "I": 2.36, "L": 2.36,
                   "K": 2.18, "M": 2.28, "F": 1.83, "P": 1.99, "S": 2.21, "T": 2.09,
                   "W": 2.83, "Y": 2.2, "V": 2.32, "U": 0.0},
          "lateral": {"R": 12.48, "H": 6, "K": 10.53, "D": 3.65, "E": 4.25, "C": 8.18, "Y": 10.07}}

    # initialize positive and negative charges
    positive_charge = 0.0
    negative_charge = 0.0

    if use_n_c_term:
        # get the N-Terminal AA pk, if it is a X (unknown AA from ambiguous codon), pk = 0 otherwise compute it.
        if seq[0] != "X":
            pk_nh3 = pk["NH3"][seq[0]]
        else:
            pk_nh3 = 0.0
        # compute the positive charge
        positive_charge = 10.0**(-ph) / (10.0**(-pk_nh3) + 10.0**(-ph))

        # get the C-Terminal AA), if it is a X (unknown AA from ambiguous codon), pk_cooh = 0 else compute it.
        if seq[-1] != "X":
            pk_cooh = pk["COOH"][seq[-1]]
        else:
            pk_cooh = 0.0
        # compute the negative charge
        negative_charge = 10.0**(-pk_cooh) / (10.0**(-pk_cooh) + 10.0**(-ph))

    # for each positive AA get the number of occurrences and its pk charge, then
    # compute the charge for this AA and add it to the positive charge
    for aa in positive_aa:
        nb_aa = len([aa for aa in seq[1:-1] if aa in positive_aa])
        pk_lateral = pk["lateral"][aa]
        positive_charge += nb_aa * 10.0**(-ph) / (10.0**(-pk_lateral) + 10.0**(-ph))

    # for each negative AA get the number of occurrences and its pk charge, then
    # compute the charge for this AA and add it to the negative charge
    for aa in negative_aa:
        nb_aa = len([aa for aa in seq[1:-1] if aa in negative_aa])
        pk_lateral = pk["lateral"][aa]
        negative_charge += nb_aa * 10.0**(-pk_lateral) / (10.0**(-pk_lateral) + 10.0**(-ph))

    # return the net charge
    return round(positive_charge - negative_charge, 2)


def net_charge_pk2(aa_record, use_n_c_term=False):
    """Compute the net charge of an amino-acids sequence (BioPython SeqRecord) using
    the dissociation constants of the amino-acids and the physiological pH (7.4).

    :param SeqRecord aa_record: the biopython amino-acids sequence record.
    :param bool use_n_c_term: the boolean to use the N and C terminal amino acids in the net charge computation.
    :return: the net charge of the amino acid sequence.
    :rtype: float
    """

    # Methode MOORE
    # REF: https://onlinelibrary.wiley.com/doi/epdf/10.1016/0307-4412%2885%2990114-1
    print("""[WARNING] net_charge_pk2(), charge Net calculée à partir de la méthode MOORE (https://onlinelibrary.wiley.com/doi/epdf/10.1016/0307-4412%2885%2990114-1)
          Différente de la méthode SeqinR net_charge_pk(), reste à déterminer laquelle est la plus adaptée.""")

    try:
        # check if it is a valid AA sequence
        check_if_aa_seq(aa_record)
        # remove the gaps from the sequence
        seq = aa_record.seq.ungap("-").upper()
    except ValueError as exc:
        raise exc
    except TypeError as exc:
        raise exc

    # compute the net charge
    ph = 7.4
    positive_aa = ["R", "K", "H"]
    negative_aa = ["D", "E"]

    pk = {"NH3": {"A": 9.69, "R": 9.04, "N": 8.8, "D": 9.6, "C": 10.28, "E": 9.67,
                  "Q": 9.13, "G": 9.6, "H": 9.17, "O": 9.65, "I": 9.6, "L": 9.6,
                  "K": 8.95, "M": 9.21, "F": 9.13, "P": 10.6, "S": 9.15, "T": 9.1,
                  "W": 9.39, "Y": 9.11, "V": 9.62, "U": 0.0},
          "COOH": {"A": 2.34, "R": 2.17, "N": 2.02, "D": 1.88, "C": 1.96, "E": 2.19,
                   "Q": 2.17, "G": 2.34, "H": 1.82, "O": 1.82, "I": 2.36, "L": 2.36,
                   "K": 2.18, "M": 2.28, "F": 1.83, "P": 1.99, "S": 2.21, "T": 2.09,
                   "W": 2.83, "Y": 2.2, "V": 2.32, "U": 0.0},
          "lateral": {"R": 12.48, "H": 6, "K": 10.53, "D": 3.65, "E": 4.25}}

    # initialize positive and negative charges
    positive_charge = 0.0
    negative_charge = 0.0

    if use_n_c_term:
        # get the N-Terminal AA pk, if it is a X (unknown AA from ambiguous codon), pk = 0 otherwhise compute it.
        if seq[0] != "X":
            pk_nh3 = pk["NH3"][seq[0]]
        else:
            pk_nh3 = 0.0
        # compute the positive charge
        positive_charge = 1.0 / (1.0 + 10.0**(ph - pk_nh3))

        # get the C-Terminal AA), if it is a X (unknown AA from ambiguous codon), pk_cooh = 0 else compute it.
        if seq[-1] != "X":
            pk_cooh = pk["COOH"][seq[-1]]
        else:
            pk_cooh = 0.0
        # compute the negative charge
        negative_charge = -1.0 / (1.0 + 10.0**(-ph + pk_cooh))

    # for each positive AA get the number of occurrences and its pk charge, then
    # compute the charge for this AA and add it to the positive charge
    for aa in positive_aa:
        nb_aa = len([aa for aa in seq[1:-1] if aa in positive_aa])
        pk_lateral = pk["lateral"][aa]
        positive_charge += nb_aa / (1.0 + 10.0**(ph - pk_lateral))

    # for each negative AA get the number of occurrences and its pk charge, then
    # compute the charge for this AA and add it to the negative charge
    for aa in negative_aa:
        nb_aa = len([aa for aa in seq[1:-1] if aa in negative_aa])
        pk_lateral = pk["lateral"][aa]
        negative_charge += -nb_aa / (1.0 + 10.0**(-ph + pk_lateral))

    # return the net charge
    return round(positive_charge - negative_charge, 2)


def count_N_glycosylation_site(aa_record):
    """Count the number of N glycosilation sites in the amino-acids sequence using
    the pattern N[^P][TS][^P] defined from https://www.hiv.lanl.gov/content/sequence/GLYCOSITE/glycosite.html

    :param Bio.SeqRecord aa_record: the biopython amino-acids sequence record.
    :return: a tuple of the number N-glycosylation sites and the list of their start positions on the ungapped sequence.
    :rtype: tuple(int, list)
    """
    try:
        # check if it is a valid AA sequence
        check_if_aa_seq(aa_record)
        # remove the gaps from the sequence
        seq = aa_record.seq.ungap("-").upper()
    except ValueError as exc:
        raise exc
    except TypeError as exc:
        raise exc

    pattern_nglyco = "N[^P][TS][^P]"
    return count_overlapping(pattern_nglyco, str(seq))
