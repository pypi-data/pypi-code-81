#! /usr/bin/env python3

'''
author: Nicolas JEANNE
email: jeanne.n@chu-toulouse.fr
Created on 24 jul. 2019
Copyright (C) PTI CHU Purpan
'''

import unittest
from Bio.Alphabet import IUPAC
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from viro_seq_utils import seq_utils


class Test_seq_utils(unittest.TestCase):
    '''Test class for the seq_utils module.'''

    def test_check_if_aa_seq_raise_value_error_with_gap(self):
        '''Test check_if_aa_seq(), if the tested sequence record contains gaps and the function is used without the option gaps_ok=True, a ValueError is raised.'''
        seq_record = SeqRecord(Seq('CTRPNNNTRKRIRIQRGPGRAFVTIGK-I-GNMRQAHC', IUPAC.protein), id='AA_seq_with_gaps')
        with self.assertRaises(ValueError):
            seq_utils.check_if_aa_seq(seq_record, gaps_ok=False)

    def test_check_if_aa_seq_raise_value_error_with_stop(self):
        '''Test check_if_aa_seq(), if the tested sequence record contains stops and the function is used without the option stops_ok=True, a ValueError is raised.'''
        seq_record = SeqRecord(Seq('CTRPNNNTRKRIRIQRGPGRAFVTIGK*IGNMRQAHC', IUPAC.protein), id='AA_seq_with_stop')
        with self.assertRaises(ValueError):
            seq_utils.check_if_aa_seq(seq_record)

    def test_check_if_aa_seq_no_value_error_raised_with_accepted_gaps(self):
        '''Test check_if_aa_seq(), if the tested sequence record contains gaps and the option gaps_ok=True, no ValueError is raised.'''
        seq_record = SeqRecord(Seq('CTRPNNNTRKRIRIQRGPGRAFVTIGK-I-GNMRQAHC', IUPAC.protein), id='AA_seq_with_gaps')
        seq_utils.check_if_aa_seq(seq_record)
        # if no error raised, get here
        self.assertTrue(True)

    def test_check_if_aa_seq_no_value_error_raised_with_accepted_stops(self):
        '''Test check_if_aa_seq(), if the tested sequence record contains stops and the option stops_ok=True, no ValueError is raised.'''
        seq_record = SeqRecord(Seq('CTRPNNNTRKRIRIQRGPGRAFVTIGKIGNMRQAHC*', IUPAC.protein), id='AA_seq_with_stop')
        seq_utils.check_if_aa_seq(seq_record, stops_ok=True)
        # if no error raised, get here
        self.assertTrue(True)

    def test_check_if_aa_seq_no_value_error_raised_with_accepted_gaps_stops(self):
        '''Test check_if_aa_seq(), if the tested sequence record contains gaps and stops and the options gaps_ok=True and stops_ok=True are set, no ValueError is raised.'''
        seq_record = SeqRecord(Seq('CTRPNNNTRKRIRIQRGPGRAFVTIGK-I-GNMRQAHCX', IUPAC.protein), id='AA_seq_with_gaps_and_stop')
        seq_utils.check_if_aa_seq(seq_record, gaps_ok=True, stops_ok=True)
        # if no error raised, get here
        self.assertTrue(True)

    def test_net_charge_no_use_H(self):
        '''Test net_charge(), check if net charge is correct without using H.'''
        seq_record = SeqRecord(Seq('CTRPHKDKEVFR', IUPAC.protein), id='seq_charge')
        expected_charge = 2
        returned_charge = seq_utils.net_charge(seq_record)
        self.assertEqual(expected_charge, returned_charge)

    def test_net_charge_use_H(self):
        '''Test net_charge(), check if net charge is correct without using H.'''
        seq_record = SeqRecord(Seq('CTRPHKDKEVFR', IUPAC.protein), id='seq_charge')
        expected_charge = 3
        returned_charge = seq_utils.net_charge(seq_record, use_H=True)
        self.assertEqual(expected_charge, returned_charge)

    def test_count_overlapping(self):
        '''Test count_overlapping(), check if the correct number of patterns is found. The string to search 'ANPTSNTTSNVTSYL' contains twice the pattern 'NTTSN' and 'NVTSY' at index 5 and 9.'''
        pattern = 'N[^P][TS][^P]'
        str_to_search = 'ANPTSNTTSNVTSYL'
        expected = (2, [5, 9])
        returned = seq_utils.count_overlapping(pattern, str_to_search)
        self.assertEqual(expected, returned)

    def test_count_N_glycosylation_site(self):
        '''Test count_N_glycosylation_site(), check if the correct number of N-glycosylation sites is found. The sequence to search 'A-NPTSN---T-TSNV-TS-YL' contains 2 N-glycosylation sites 'NTTSN' and 'NVTSY' at index 5 and 9.'''
        seq_record = SeqRecord(Seq('A-NPTSN---T-TSNV-TS-YL', IUPAC.protein), id='seq_with_2_glyco_sites')
        expected = (2, [5, 9])
        returned = seq_utils.count_N_glycosylation_site(seq_record)
        self.assertEqual(expected, returned)
