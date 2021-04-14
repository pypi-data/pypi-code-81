#! /usr/bin/env python3

from Bio.Alphabet import IUPAC
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Align import MultipleSeqAlignment
import aln_utils
import seq_utils


aln = MultipleSeqAlignment([SeqRecord(Seq('CTRPNNNTRKRIRIQRGPGRAFVTIGK-I-GNMRQAHC', IUPAC.protein), id='HXB2_V3'),
                            SeqRecord(Seq('CTRPYQSKKRIIHI--GPGRAFYARGG-T--DIRKASC', IUPAC.protein), id='seq1_V3'),
                            SeqRecord(Seq('CTRPSANKRKSIRIHRGPGRAFVTGGI-T-GDLKQAHC', IUPAC.protein), id='seq3_V3'),
                            SeqRecord(Seq('CTRPNNNTRKSISI--GPGSAIYTTGQII-GNIRQAYC', IUPAC.protein), id='seq9_V3')])

print(aln)

idx_ref = [idx for idx in range(len(aln)) if aln[idx].id == 'HXB2_V3'][0]
print(idx_ref)

nbs = aln_utils.numbering_positions(aln, 'HXB2_V3')
print(nbs)

seq = aln_utils.get_seq_from_id_in_aln(aln, 'HXB2_V3').seq.ungap("-")
print(seq)
print(len(seq))

recoded = aln_utils.numeric_recoding_from_seqrecord(aln[idx_ref])
print(recoded)
print(len(recoded))
for idx, pos in enumerate(nbs):
    print('{}: {} {}'.format(pos, recoded[idx], aln[idx_ref].seq[idx]))

seq_ok = SeqRecord(Seq('CTRPNNNTRKRIRIQRGPGRAFVTIGKIGNMRQAHC', IUPAC.protein), id='ok')
seq_ok = SeqRecord(Seq('DLDLDD', IUPAC.protein), id='ok')
seq_utils.check_if_aa_seq(seq_ok)
seq_not_ok = SeqRecord(Seq('CTRPNNNTRKRIRIQRGPGRAFVTIGK-I-GNMRQAHC', IUPAC.protein), id='not_ok')
seq_utils.check_if_aa_seq(seq_not_ok)
try:
    print('Sequence: {}'.format(seq_ok.seq))
    charge = seq_utils.net_charge(seq_ok)
    print('charge methode heuristique: {}'.format(charge))
    charge_seqinr = seq_utils.net_charge_pk(seq_ok)
    print('charge methode seqinR: {}'.format(charge_seqinr, use_N_C_term=True))
    charge_moore = seq_utils.net_charge_pk2(seq_ok)
    print('charge methode Moore: {}'.format(charge_moore, use_N_C_term=True))
except ValueError as exc:
    print('DANS RUN: {}'.format(exc))
except TypeError as exc:
    print('DANS RUN:\n{}'.format(exc))

seq_with_count = SeqRecord(Seq('CTRPNNNTRKRIRIQRGPGRAFVTIGKIGNMRQAHC', IUPAC.protein),
                           id='seq_with_count',
                           description='count=666')
print('Count found for {}: {}'.format(seq_with_count.id, seq_utils.get_count(seq_with_count)))
