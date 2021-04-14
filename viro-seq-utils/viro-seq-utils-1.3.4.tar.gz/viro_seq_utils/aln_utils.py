#! /usr/bin/env python3

"""
author: Nicolas JEANNE
email: jeanne.n@chu-toulouse.fr
Created on 10 apr. 2019
Copyright (C) PTI CHU Purpan
"""

from itertools import groupby
import logging
from operator import itemgetter

from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import numpy as np

from viro_seq_utils import seq_utils


NUMERIC_RESIDUES = {"-": 0, "A": 1, "C": 2, "G": 3, "T": 4, "R": 5, "N": 6,
                    "D": 7, "E": 8, "Q": 9, "H": 10, "I": 11, "L": 12,
                    "K": 13, "M": 14, "F": 15, "P": 16, "S": 17, "W": 18,
                    "Y": 19, "V": 20, "U": 21, "O": 22}


def get_last_aligned_position(aln, idx_row_aln, gap_char="-"):
    """
    Get the last position (0-indexed) of an aligned sequence which is not a gap.

    :param aln: the alignment.
    :type aln: Bio.Align.MultipleSeqAlignment
    :param idx_row_aln: the index of the sequence in the alignment.
    :type idx_row_aln: int
    :param gap_char: the gap character, default is "-".
    :type gap_char: str
    :return: the index of the last aligned position, 0-indexed.
    :rtype: int
    """
    seq = aln[idx_row_aln].seq
    idx = len(seq) - 1
    while seq[idx] == gap_char:
        idx -= 1
    return idx


def get_first_aligned_position(aln, idx_row_aln, gap_char="-"):
    """
    Get the first position (0-indexed) of an aligned sequence which is not a gap.

    :param aln: the alignment.
    :type aln: Bio.Align.MultipleSeqAlignment
    :param idx_row_aln: the index of the sequence in the alignment.
    :type idx_row_aln: int
    :param gap_char: the gap character, default is "-".
    :type gap_char: str
    :return: the index of the first aligned position, 0-indexed.
    :rtype: int
    """
    seq = aln[idx_row_aln].seq
    idx = 0
    while seq[idx] == gap_char:
        idx += 1
    return idx


def get_no_codon_deletions(record):
    """
    Get index of deletions that are not codons.

    :param Bio.SeqRecord record: the record of the sequence where the deletions that are not codons
    are searched.
    :return: the indexes of the deletions that are not codons.
    :rtype: list
    """
    del_idx = []
    for idx in range(len(record.seq)):
        if record.seq[idx] == "-":
            del_idx.append(idx)
    del_idx_no_codon = remove_codons_index(del_idx)
    return del_idx_no_codon


def remove_codons_index(idx_lst):
    """
    Detect consecutive index in a list and check if they are not codons (multiples of 3). If true,
    remove them from the list of index.

    :param list idx_lst: the list of index.
    :return: the modified list of index.
    :rtype: list
    """
    # the lambda function creates a key for the groupby function by subtracting
    # during the enumeration the integer value to the index of the list.
    # the groupby function return the key (computed in the lambda function) and
    # the group as an iterable, the group can be an iterable of one element, i.e
    # for lst = [0, 1, 2, 7]
    # if the lst is enumerated, we have the following keys for the groupby function:
    # index(lst)[0] - lst[1] -> 0-0 = 0
    # index(lst)[1] - lst[1] -> 1-1 = 0
    # index(lst)[2] - lst[2] -> 2-2 = 0
    # index(lst)[3] - lst[3] -> 3-7 = -4
    # All the keys equal to 0 will be grouped together and the key -4 will be alone.
    for _, group in groupby(enumerate(idx_lst),
                            key=lambda enum_result: enum_result[0] - enum_result[1]):
        consecutive_grp = list(map(itemgetter(1), group))
        # if the consecutive group is a multiple of 3, one or more codons are detected, they should
        # be removed from the index list.
        if len(consecutive_grp) % 3 == 0:
            idx_lst = [x for x in idx_lst if x not in consecutive_grp]

    return idx_lst


def cut_on_ref_boundaries(aln, ref_id, gap_char="-"):
    """
    Cut an alignment on a reference sequence boundaries.
    Look for the first position on the reference sequence which is not a gap and look for the
    position starting from the end of the reference sequence which is not a gap.
    Cut the alignment on these positions.

    :param Bio.Align.MultipleSeqAlignment aln: the alignment
    :param str ref_id: the ID of the sequence which boundaries are searched
    :param str gap_char: the character for a gap, default is "-".
    :return: the alignment
    :rtype: Bio.Align.MultipleSeqAlignment
    """

    ref = aln[[idx for idx in range(len(aln)) if aln[idx].id == ref_id][0]]
    ref_start = 0
    for idx, item in enumerate(ref):
        if item != gap_char:
            ref_start = idx
            break
    ref_end = len(ref)-1
    for idx in reversed(range(len(ref))):
        if ref[idx] != gap_char:
            ref_end = idx
            break
    logging.debug("\treference boundary start: {} (0-indexed)".format(ref_start))
    logging.debug("\treference boundary end: {} (0-indexed)".format(ref_end))
    aln = aln[:, ref_start:ref_end+1]

    return aln


def cut_on_unaligned_ref(aln, ref_id, region_start, region_end, gap_char="-"):
    """
    Cut an alignment at start and end positions of its reference sequence using this reference on the unaligned form.

    :param Bio.Align.MultipleSeqAlignment aln: the alignment
    :param str ref_id: the ID of the sequence which boundaries are searched
    :param int region_start: the non aligned start position (0-indexed) of the region to cut
    :param int region_end: the non aligned start position (0-indexed) of the region to cut
    :param str gap_char: the character for a gap, default is "-"
    :return: the alignment
    :rtype: Bio.Align.MultipleSeqAlignment
    """

    ref = aln[[idx for idx in range(len(aln)) if aln[idx].id == ref_id][0]]
    nb_gap = 0
    cut_start = 0
    cut_end = 0
    gaps_at_ref_start = True
    for idx, item in enumerate(ref):
        idx_ungap_ref = idx - nb_gap
        if item == gap_char:
            nb_gap += 1
        # check if the ref is smaller than the other sequences, in that case the idx count of the
        # ungap ref will start at the first base of the ref.
        if gaps_at_ref_start:
            if ref[idx] != gap_char:
                gaps_at_ref_start = False
            else:
                # pass to the next idx
                continue
        # register position of start or end
        if cut_start == 0:
            if idx_ungap_ref == region_start:
                cut_start = idx
                logging.debug("\treference boundary start: {} (0-indexed)".format(cut_start))
        else:
            if idx_ungap_ref == region_end:
                cut_end = idx
                logging.debug("\treference boundary end: {} (0-indexed)".format(cut_end))
                break
    return aln[:, cut_start:cut_end+1]


def prune_aln(alignment, rows_list_idx):
    """Remove the rows of an alignment using the index positions of a list.

    :param Bio.Align.MultipleSeqAlignment alignment: the alignment
    :param list rows_list_idx : list of rows index (integers) to remove
    :return: the pruned alignment
    :rtype: Bio.Align.MultipleSeqAlignment
    """

    for index in sorted(rows_list_idx, reverse=True):
        if index == 0:
            alignment = alignment[index+1:, :]
        elif index == len(alignment)-1:
            alignment = alignment[:index, :]
        else:
            tail_alignment = alignment[index+1:, :]
            alignment = alignment[:index, :]
            for i in range(len(tail_alignment)):
                alignment.append(tail_alignment[i, :])
    return alignment


def slice_aln(alignment, cols_list_idx):
    """Remove the columns of an alignment using the index positions of a list.

    :param Bio.Align.MultipleSeqAlignment alignment: the alignment
    :param list cols_list_idx : list of columns index (integers) to remove
    :return: the sliced alignment
    :rtype: Bio.Align.MultipleSeqAlignment
    """

    for index in sorted(cols_list_idx, reverse=True):
        if index == 0:
            alignment = alignment[:, index+1:]
        elif index == alignment.get_alignment_length()-1:
            alignment = alignment[:, :index]
        else:
            tail_alignment = alignment[:, index+1:]
            alignment = alignment[:, :index] + tail_alignment
    return alignment


def numbering_positions(aln, ref_seq_id):
    r"""Numbering an alignment positions based on a reference sequence.
    The positions are registered as posX. The gaps in the reference sequence
    which are insertions in the sequences of the alignment are registered as posX_1.
    In example:
        >reference_sequence
        CTR-PQ
        >foo
        CTRAPQ
        >bar
        C-KAPQ

    aligned as:
        CTR-PQ  reference_sequence
        CTRAPQ  foo
        C-KAPQ  bar

    will produce:
        [pos1, pos2, pos3, pos3_1, pos4, pos5]

    :param Bio.Align.MultipleSeqAlignment aln: the alignment.
    :param str ref_seq_id: the ID of the reference sequence to use in the alignment.
    :return: the list of positions.
    :rtype: list of str
    """
    # get the aligned reference
    aligned_reference = get_seq_from_id_in_aln(aln, ref_seq_id)
    # numbering the positions
    positions_list = []
    position_no_gap = 0
    insertion = 1
    for item in aligned_reference.seq:
        if item != "-":
            insertion = 1
            position_no_gap += 1
            positions_list.append("pos{}".format(position_no_gap))
        else:
            positions_list.append("pos{}_{}".format(position_no_gap, insertion))
            insertion += 1
    return positions_list


def numeric_recoding_from_seqrecord(record):
    """Recode a sequence with numerics.

    :param Bio.SeqRecord record: a sequence record.
    :return: a list with the recoded sequence.
    :rtype: list of int.
    """
    recoded = []
    for item in record.seq:
        recoded.append(NUMERIC_RESIDUES[item.upper()])
    return recoded


def numeric_recoding_from_dataframe(df, col_names_to_recode):
    """Recode amino-acids or nucleotides in a dataframe with numerics.

    :param dataframe df: the dataframe containing the amino-acids to recode.
    :param list col_names_to_recode: list of columns names to recode.
    :return: the recoded dataframe.
    :rtype: dataframe.
    """
    # recode the selected columns
    tmp_df = df[col_names_to_recode]
    for item in NUMERIC_RESIDUES:
        tmp_df = tmp_df.replace(item, NUMERIC_RESIDUES[item.upper()])
    df[col_names_to_recode] = tmp_df
    return df


def get_seq_from_id_in_aln(aln, seq_id):
    """With the ID of a sequence in an alignment, retrieve the sequence record.

    :param Bio.Align.MultipleSeqAlignment aln: the alignment.
    :param str seq_id: the sequence id of the sequence to retrieve.
    :return: the sequence.
    :rtype: Bio.SeqRecord
    """
    # get the index of the sequence corresponding to the searched ID
    try:
        index = [idx for idx in range(len(aln)) if aln[idx].id == seq_id][0]
    except IndexError as exc:
        raise exc
    return aln[index]


def weighted_consensus_AA(aln, pattern="[Cc]ount=(\\d+)", ungap=True,
                          sample_id=None, sample_descr=""):
    """
    Compute the consensus sequence of an amino acids alignment using the abundance of the haplotypes.

    :param Bio.Align.MultipleSeqAlignment aln: the alignment.
    :param re pattern: regular expression for the count pattern.
    :param bool ungap: remove gaps from the consensus, default is True.
    :param str sample_id: the sample ID to add to the Bio.SeqRecord.id, default is None.
    :param str sample_descr: the sample description to add to the Bio.SeqRecord.description,
    default is an empty string.
    :return: the consensus sequence of amino acids.
    :rtype: Bio.SeqRecord
    """
    aa = ["A", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V",
          "W", "Y", "X", "U", "O", "-"]
    consensus_seq = []
    for idx_col in range(aln.get_alignment_length()):
        aln_col_aa_count = [0] * len(aa)
        for idx_row, rec in enumerate(aln):
            # get the index in AA of the current nucleotide in the current aln column
            idx_aa = aa.index(aln[idx_row, idx_col].upper())
            # update the count
            aln_col_aa_count[idx_aa] += seq_utils.get_count(rec, pattern)
        # get the maximum count value
        max_count_val = max(aln_col_aa_count)
        # find the indices of the maximum count values and sort the results
        idx_max = sorted([idx for idx, count in enumerate(aln_col_aa_count) if count == max_count_val])

        consensus_seq.append(aa[idx_max[0]])

    seq_con = Seq("".join(consensus_seq))
    # sample ID to set to the record ID
    id_rec = "consensus"
    if sample_id:
        id_rec = "{}_{}".format(id_rec, sample_id)
    # ungap the consensus sequence
    if ungap:
        seq_con = seq_con.ungap("-")

    return SeqRecord(seq=seq_con, id=id_rec, description=sample_descr)


def weighted_consensus(aln, pattern="[Cc]ount=(\\d+)", ungap=True, check_orfs_no_stop=True,
                       allow_iupac_ambiguous=True, sample_id=None, sample_descr=""):
    """
    Compute the consensus sequence of a nucleotides alignment using the abundance of the haplotypes.

    :param Bio.Align.MultipleSeqAlignment aln: the alignment.
    :param re pattern: regular expression for the count pattern.
    :param bool ungap: remove gaps from the consensus, default is True.
    :param bool check_orfs_no_stop: if the presence of STOP codons in at least one ORF should be
    mentioned, default is True.
    :param bool allow_iupac_ambiguous: allow ambiguous IUPAC code in the consensus if at a position
    of the alignment, the number of nucleotides are equals. If not allowed, the first nucleotide in
    alphabetical order is assigned. Default is True.
    :param str sample_id: the sample ID to add to the Bio.SeqRecord.id, default is None.
    :param str sample_descr: the sample description to add to the Bio.SeqRecord.description,
    default is an empty string.
    :return: the consensus sequence, DNA can be ambiguous or gap.
    :rtype: Bio.SeqRecord
    """
    nuc = ["A", "C", "G", "T", "-"]
    if allow_iupac_ambiguous:
        # ambiguous positions dict, keys are alphabetically sorted and values are ambiguous IUPAC code
        ambiguous = {"A": "A", "C": "C", "G": "G", "T": "T", "-": "-",
                     "AC": "M", "AG": "R", "AT": "W", "-A": "A",
                     "CG": "S", "CT": "Y", "-C": "C",
                     "GT": "K", "-G": "G",
                     "-T": "T",
                     "ACG": "V", "ACT": "H", "-AC": "M",
                     "AGT": "D", "-AG": "R",
                     "-AT": "W",
                     "CGT": "B", "-CG": "S", "-CT": "Y",
                     "-GT": "K",
                     "-ACG": "V", "-ACT": "H", "-AGT": "D",
                     "-CGT": "B",
                     "ACGT": "N", "-ACGT": "N"}
    else:
        # ambiguous positions dict, keys are alphabeticly sorted and values are in order of
        # preferences A, G, T, C, according to: van der Kuyl, A. C., & Berkhout, B. (2012).
        # The biased nucleotide composition of the HIV genome: a constant factor in a highly
        # variable virus. Retrovirology, 9, 92. doi:10.1186/1742-4690-9-92
        ambiguous = {"A": "A", "C": "C", "G": "G", "T": "T", "-": "-",
                     "AC": "A", "AG": "A", "AT": "A", "-A": "A",
                     "CG": "G", "CT": "T", "-C": "C",
                     "GT": "G", "-G": "G",
                     "-T": "T",
                     "ACG": "A", "ACT": "A", "-AC": "A",
                     "AGT": "A", "-AG": "A",
                     "-AT": "A",
                     "CGT": "G", "-CG": "G", "-CT": "T",
                     "-GT": "G",
                     "-ACG": "A", "-ACT": "A", "-AGT": "A",
                     "-CGT": "G",
                     "ACGT": "A", "-ACGT": "A"}
    consensus_seq = []
    for idx_col in range(aln.get_alignment_length()):
        aln_col_nuc_count = [0, 0, 0, 0, 0]
        for idx_row, rec in enumerate(aln):
            # get the index in NUC of the current nucleotide in the current aln column
            idx_nuc = nuc.index(aln[idx_row, idx_col].upper())
            # update the count
            aln_col_nuc_count[idx_nuc] += seq_utils.get_count(rec, pattern)
        # get the maximum count value
        max_count_val = max(aln_col_nuc_count)
        # find the indices of the maximum count values and sort the results
        idx_max = sorted([idx for idx, count in enumerate(aln_col_nuc_count) if count == max_count_val])
        # find the corresponding IUPAC character, ambiguous or not
        key_ambiguous = "".join(sorted([nuc[idx] for idx in idx_max]))
        consensus_seq.append(ambiguous[key_ambiguous])

    seq_con = Seq("".join(consensus_seq))
    # sample ID to set to the record ID
    id_rec = "consensus"
    if sample_id:
        id_rec = "{}_{}".format(id_rec, sample_id)
    # ungap the consensus sequence
    if ungap:
        seq_con = seq_con.ungap("-")
    # check for STOPs in all frames
    if check_orfs_no_stop:
        if not __check_consensus(seq_con):
            id_rec = "{}_with_stop".format(id_rec)

    return SeqRecord(seq=seq_con,
                     id=id_rec,
                     description=sample_descr)


def consensus(aln, check_orfs_no_stop=True, allow_iupac_ambiguous=True, sample_id=None,
              sample_descr=""):
    """
    Compute the consensus sequence of a nucleotides alignment using only the haplotype without using
    its abundance.

    :param Bio.Align.MultipleSeqAlignment aln: the alignment.
    :param bool check_orfs_no_stop: if the presence of STOP codons in at least one ORF should be
    mentioned, default is True.
    :param bool allow_iupac_ambiguous: allow ambiguous IUPAC code in the consensus if at a position
    of the alignment, the number of nucleotides are equals. If not allowed, the first nucleotide in
    alphabetical order is assigned. Default is True.
    :param str sample_id: the sample ID to add to the Bio.SeqRecord.id, default is None.
    :param str sample_descr: the sample description to add to the Bio.SeqRecord.description,
    default is an empty string.
    :return: the consensus sequence, DNA can be ambiguous or gap.
    :rtype: Bio.SeqRecord
    """
    nuc = ["A", "C", "G", "T", "-"]
    if allow_iupac_ambiguous:
        # ambiguous positions dict, keys are alphabetically sorted and values are ambiguous IUPAC code
        ambiguous = {"A": "A", "C": "C", "G": "G", "T": "T", "-": "-",
                     "AC": "M", "AG": "R", "AT": "W", "-A": "A",
                     "CG": "S", "CT": "Y", "-C": "C",
                     "GT": "K", "-G": "G",
                     "-T": "T",
                     "ACG": "V", "ACT": "H", "-AC": "M",
                     "AGT": "D", "-AG": "R",
                     "-AT": "W",
                     "CGT": "B", "-CG": "S",
                     "-GT": "K",
                     "-ACG": "V", "-ACT": "H", "-AGT": "D",
                     "-CGT": "B",
                     "ACGT": "N", "-ACGT": "N"}
    else:
        # ambiguous positions dict, keys are alphabetically sorted and values are in order of
        # preferences A, G, T, C, according to: van der Kuyl, A. C., & Berkhout, B. (2012).
        # The biased nucleotide composition of the HIV genome: a constant factor in a highly
        # variable virus. Retrovirology, 9, 92. doi:10.1186/1742-4690-9-92
        ambiguous = {"A": "A", "C": "C", "G": "G", "T": "T", "-": "-",
                     "AC": "A", "AG": "A", "AT": "A", "-A": "A",
                     "CG": "G", "CT": "T", "-C": "C",
                     "GT": "G", "-G": "G",
                     "-T": "T",
                     "ACG": "A", "ACT": "A", "-AC": "A",
                     "AGT": "A", "-AG": "A",
                     "-AT": "A",
                     "CGT": "G", "-CG": "G",
                     "-GT": "G",
                     "-ACG": "A", "-ACT": "A", "-AGT": "A",
                     "-CGT": "G",
                     "ACGT": "A", "-ACGT": "A"}
    consensus_seq = []
    for idx_col in range(aln.get_alignment_length()):
        aln_col_nuc_count = [0, 0, 0, 0, 0]
        for idx_row, _ in enumerate(aln):
            # get the index in nuc of the current nucleotide in the current aln column
            idx_nuc = nuc.index(aln[idx_row, idx_col].upper())
            # update the count
            aln_col_nuc_count[idx_nuc] += 1
        # get the maximum count value
        max_count_val = max(aln_col_nuc_count)
        # find the indices of the maximum count values
        idx_max = sorted([idx for idx, count in enumerate(aln_col_nuc_count) if count == max_count_val])
        # find the corresponding IUPAC character, ambiguous or not
        key_ambiguous = "".join(sorted([nuc[idx] for idx in idx_max]))
        consensus_seq.append(ambiguous[key_ambiguous])
    # ungap the consensus sequence
    seq_con = Seq("".join(consensus_seq)).ungap("-")
    # sample ID to set to the record ID
    id_rec = "consensus"
    if sample_id:
        id_rec = "{}_{}".format(id_rec, sample_id)
    # check for STOPs in all frames
    if check_orfs_no_stop:
        if not __check_consensus(seq_con):
            id_rec = "{}_with_stop".format(id_rec)

    return SeqRecord(seq=seq_con,
                     id=id_rec,
                     description=sample_descr)


def dissimilarity(aln, gap_penalty=0.5):
    """
    Compute the dissimilarity percentage score matrix between the sequences of an alignment.

    :param Bio.Align.MultipleSeqAlignment aln: the alignment.
    :param float gap_penalty: the penalty for a gap in the alignment.
    :return: the dissimilarity matrix.
    :rtype: np.array of dissimilarity percentage
    """

    mat = np.zeros((len(aln), len(aln)))

    nb_col = aln.get_alignment_length()
    for idx_i, record_i in enumerate(aln):
        for idx_j in range(idx_i + 1, len(aln)):
            record_j = aln[idx_j]
            dist = []
            col_idx = 0
            # browse the alignment to search differences
            while col_idx != nb_col:
                if record_i.seq[col_idx] == record_j.seq[col_idx]:
                    dist.append(0)
                elif record_i.seq[col_idx] == "-" and record_j.seq[col_idx] != "-":
                    dist, col_idx = __dist_gap_extension(record_i,
                                                         record_j,
                                                         dist,
                                                         col_idx,
                                                         gap_penalty)
                elif record_i.seq[col_idx] != "-" and record_j.seq[col_idx] == "-":
                    dist, col_idx = __dist_gap_extension(record_j,
                                                         record_i,
                                                         dist,
                                                         col_idx,
                                                         gap_penalty)
                else:
                    dist.append(1)
                col_idx += 1

            mat[idx_i, idx_j] = sum(dist) / nb_col
            mat[idx_j, idx_i] = sum(dist) / nb_col

    return mat


def remove_column_gaps(align):
    """
    Remove columns of gaps in the alignment.

    :param Bio.MultipleSeqAlignment align: the alignment with columns of gaps.
    :return: the alignment without columns of gaps.
    :rtype: Bio.MultipleSeqAlignment
    """
    # get index of columns of gaps
    idx_to_remove = []
    for idx in range(align.get_alignment_length()):
        if set(align[:, idx]) == set("-"):
            idx_to_remove.append(idx)

    # remove the columns of gaps
    initial_aln_length = align.get_alignment_length()
    for idx in reversed(idx_to_remove):
        if idx == 0:
            align = align[:, 1:]
        else:
            if idx == initial_aln_length - 1:
                align = align[:, :initial_aln_length]
            else:
                align = align[:, :idx] + align[:, idx+1:]
    return align


def __dist_gap_extension(rec1, rec2, d, idx, gap_pen):
    """When a gap is detected in the alignment, get the number of consecutive gaps
    and if the number of gaps is multiple of 3, the nucleotides insertions or deletions
    of codons are considered as variants and not gaps.

    :param Bio.SeqRecord rec1: the sequence where a gap was detected.
    :param Bio.SeqRecord rec2: the sequence to compare.
    :param list d: the list of distances.
    :param int idx: the index where the gap was detected.
    :param float gap_pen: the gap penalty.
    :return: updated distances list, index of the last consecutive gap
    :rtype: list, int
    """

    # one gap has already been detected
    nb_gap = 1
    # get the index value out of range
    idx_out_range = len(rec1.seq)
    # get the number of consecutive gaps on the same sequence
    if idx + nb_gap != idx_out_range:
        while rec1.seq[idx + nb_gap] == "-" and rec2.seq[idx + nb_gap] != "-":
            nb_gap += 1
            if idx + nb_gap == idx_out_range:
                break

    # check for codon inserted
    if nb_gap % 3 == 0:
        # if one or more codon set distances as variant value
        gap_dist = [1] * nb_gap
    else:
        # if not codons set distances as gap penalties.
        gap_dist = [gap_pen] * nb_gap
    d.extend(gap_dist)

    return d, idx + nb_gap - 1


def __check_consensus(con):
    """
    Check if the consensus translation contains STOPs in all the ORF.

    :param Bio.Seq con: the nucleotides consensus sequence.
    :return: if at least an ORF has no stop
    :rtype: boolean
    """
    valid_orf = []
    for i in range(3):
        # add trailing N to avoid Biopython warning during translation for non complete codon
        tmp_nt_seq = con[i:] + ("N" * (3 - len(con[i:]) % 3))
        if "*" in tmp_nt_seq.translate():
            valid_orf.append(False)
        else:
            valid_orf.append(True)
    return True in valid_orf


def __is_aa_seq(sequence):
    """
    Check if a sequence is an amino acids or nucleotides sequence.

    :param iterable sequence: an iterable of the alphabet of sequences.
    :return: if the sequence is an amino acid sequence.
    :rtype: boolean
    """
    is_aa = False
    for x in set(sequence):
        if x.upper() not in ["A", "C", "G", "T", "-", "X"]:
            is_aa = True
            break
    return is_aa
