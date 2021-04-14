#! /usr/bin/env python3

'''
author: Nicolas JEANNE
email: jeanne.n@chu-toulouse.fr
Created on 10 jul. 2019
Copyright (C) PTI CHU Purpan
'''

import unittest
import pandas
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Align import MultipleSeqAlignment
from viro_seq_utils import aln_utils


class Test_aln_utils(unittest.TestCase):
    '''Test class for the aln_utils module.'''

    def setUp(self):
        '''Set up for testing'''
        self.aln = MultipleSeqAlignment([SeqRecord(Seq('CTRPNNNTRKRIRIQRGPGRAFVTIGK-I-GNMRQAHC', IUPAC.protein), id='HXB2_V3'),
                                         SeqRecord(Seq('CTRPYQSKKRIIHI--GPGRAFYARGG-T--DIRKASC', IUPAC.protein), id='seq1_V3'),
                                         SeqRecord(Seq('CTRPSANKRKSIRIHRGPGRAFVTGGI-T-GDLKQAHC', IUPAC.protein), id='seq3_V3'),
                                         SeqRecord(Seq('CTRPNNNTRKSISI--GPGSAIYTTGQII-GNIRQAYC', IUPAC.protein), id='seq9_V3')])
        self.idx_to_remove = [0, 3]

    def test_numeric_recoding_from_dataframe(self):
        '''Test numeric_recoding_from_dataframe(), if returns the awaited list of recoded AA'''
        df = pandas.DataFrame(data={'id': ['HXB2_V3', 'seq1_V3', 'seq3_V3', 'seq9_V3'],
                                    'pos35': ['H', 'S', 'H', 'Y'],
                                    'pos36': ['C', 'C', 'C', 'C']})
        expected_df = pandas.DataFrame(data={'id': ['HXB2_V3', 'seq1_V3', 'seq3_V3', 'seq9_V3'],
                                             'pos35': [9, 16, 9, 19],
                                             'pos36': [5, 5, 5, 5]})
        columns_to_recode = ['pos35', 'pos36']
        returned_df = aln_utils.numeric_recoding_from_dataframe(df, columns_to_recode)
        self.assertEqual(returned_df['pos35'].tolist(), expected_df['pos35'].tolist())
        self.assertEqual(returned_df['pos36'].tolist(), expected_df['pos36'].tolist())

    def test_numeric_recoding_from_seqrecord(self):
        '''Test numeric_recoding_from_seqrecord(), if returns the awaited list of recoded AA'''
        expected = [5, 17, 2, 15, 3, 3, 3, 17, 2, 12, 2, 10, 2, 10, 7, 2, 8, 15, 8, 2, 1, 14, 20,
                    17, 10, 8, 12, 21, 10, 21, 8, 3, 13, 2, 7, 1, 9, 5]
        idx_ref = [idx for idx in range(len(self.aln)) if self.aln[idx].id == 'HXB2_V3'][0]
        returned = aln_utils.numeric_recoding_from_seqrecord(self.aln[idx_ref])
        self.assertEqual(returned, expected)

    def test_get_seq_from_id_in_aln(self):
        '''Test numeric_recoding_from_seqrecord(), if returns the awaited list of recoded AA.'''
        expected = self.aln[0]
        returned = aln_utils.get_seq_from_id_in_aln(self.aln, 'HXB2_V3')
        self.assertEqual(returned.seq, expected.seq)
        self.assertEqual(returned.id, expected.id)

    def test_numbering_positions(self):
        '''Test numbering_positions(), if returns the awaited list of position numbering.'''
        expected_pos = ['pos1', 'pos2', 'pos3', 'pos4', 'pos5', 'pos6', 'pos7', 'pos8', 'pos9',
                        'pos10', 'pos11', 'pos12', 'pos13', 'pos14', 'pos15', 'pos16', 'pos17',
                        'pos18', 'pos19', 'pos20', 'pos21', 'pos22', 'pos23', 'pos24', 'pos25',
                        'pos26', 'pos27', 'pos27_1', 'pos28', 'pos28_1', 'pos29', 'pos30', 'pos31',
                        'pos32', 'pos33', 'pos34', 'pos35', 'pos36']
        returned_pos = aln_utils.numbering_positions(self.aln, 'HXB2_V3')
        self.assertEqual(returned_pos, expected_pos)

    def test_prune_aln_nb_removed_row(self):
        '''Test for prune_aln(), if the number of rows after pruning the alignment plus the length
        of the index list to remove is equal to the number of initail rows of the alignment.'''
        pruned_aln = aln_utils.prune_aln(self.aln, self.idx_to_remove)
        self.assertEqual(len(self.aln), len(self.idx_to_remove) + len(pruned_aln))

    def test_prune_aln_correct_removed_rows(self):
        '''Test for prune_aln(), if the removed rows are not present in the alignment.'''
        ids_to_remove = [self.aln[idx].id for idx in self.idx_to_remove]
        pruned_aln = aln_utils.prune_aln(self.aln, self.idx_to_remove)
        ids_present = [record.id for record in pruned_aln]
        # get intersection of the 2 lists of ids
        intersection = list(set(ids_to_remove).intersection(ids_present))
        self.assertEqual(len(intersection), 0)
