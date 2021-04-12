#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#author: Stephan Fuchs (Robert Koch Institute, MF-1, fuchss@rki.de)

VERSION = "0.0.9"
import os
import argparse
import subprocess
import re
import sys
import gzip
import pysam
from collections import defaultdict
from collections import Counter
import numpy as np
from Bio import SeqIO
import pandas as pd

class ampliset():
    def __init__(self, amplicon_bed_file, insert_bed_file, ref_fasta_file = None):
        # input
        self.amplicon_bed_file = amplicon_bed_file
        self.insert_bed_file = insert_bed_file
        self.ref_fasta_file = ref_fasta_file

        # data
        self.refs = self.fasta2dict(ref_fasta_file) if ref_fasta_file else None
        self.amplicons = self.init_amplicons()


    def bed2dict(self, fname):
        '''
        creates a dictionary from a BED file using DESCR as key and the following tuple as value: (CRHOM, START, END)
        BED FILE FOMRAT DEFINITION: Zero-based index; Start and end positions are identified using a zero-based index. The end position is excluded. For example, setting start-end to 1-2 describes exactly one base, the second base in the sequence.
        '''
        with open(fname, "r") as handle:
            my_dict = {}
            for line in handle:
                line = line.strip()
                if line.startswith("track name=") or len(line) == 0:
                    continue
                fields = line.split("\t")
                if fields[3] in my_dict:
                    sys.exit("error: '" + fields[3] + "' is not unique in " + fname)
                coords = sorted([int(x) for x in fields[1:3]])
                my_dict[fields[3]] = (fields[0], coords[0], coords[1])
            return my_dict

    def fasta2dict(self, fname):
        '''
        converts fasta to dict using biopython
        '''
        return SeqIO.to_dict(SeqIO.parse(fname, "fasta"))

    def init_amplicons(self):
        '''
        creates pandas df for amplicon data (coordinates 0-based, ends exclusive)
        '''
        amplicons = self.bed2dict(self.amplicon_bed_file)
        inserts = self.bed2dict(self.insert_bed_file)

        data = []
        for key in amplicons:
            amplicon = amplicons[key]
            insert = inserts[key]
            if insert[0] != amplicon[0]:
                sys.exit("error: different chromosomes linked to " + key)
            chrom = amplicon[0]
            primer1 = sorted([amplicon[1], insert[1]])
            primer2 = sorted([amplicon[2], insert[2]])
            data.append([key, insert[0], primer1[0], primer1[1], primer2[0], primer2[1]])

        df = pd.DataFrame(data, columns=["id", "chrom", "fwd_primer_start", "fwd_primer_end", "rev_primer_start", "rev_primer_end"])
        df.set_index("id", inplace=True)
        return df

    def iter_amplicons(self):
        for aid in sorted(self.amplicons.index.tolist()):
            yield aid

    def get_seq(self, chrom, start, end, rev_compl = False):
        if not self.refs:
            return None
        seq = self.refs[chrom].seq[start:end]
        if rev_compl:
            seq = seq.reverse_complement()
        return str(seq)

    def get_amplicon(self, id):
        if id not in self.amplicons.index:
            return None
        start = self.amplicons.loc[id]['fwd_primer_start']
        end = self.amplicons.loc[id]['rev_primer_end']
        chrom = self.amplicons.loc[id]['chrom']
        seq = self.get_seq(chrom, start, end)
        return (id, chrom, start, end, seq)

    def get_insert(self, id, rev_compl=False):
        start = self.amplicons.loc[id]['fwd_primer_end']
        end = self.amplicons.loc[id]['rev_primer_start']
        chrom = self.amplicons.loc[id]['chrom']
        seq = self.get_seq(chrom, start, end, rev_compl)
        return (id, chrom, start, end, seq)

    def get_fwd_primer(self, id):
        start = self.amplicons.loc[id]['fwd_primer_start']
        end = self.amplicons.loc[id]['fwd_primer_end']
        chrom = self.amplicons.loc[id]['chrom']
        seq = self.get_seq(chrom, start, end)
        return (id, chrom, start, end, seq)

    def get_rev_primer(self, id, rev_compl=True):
        start = self.amplicons.loc[id]['rev_primer_start']
        end = self.amplicons.loc[id]['rev_primer_end']
        chrom = self.amplicons.loc[id]['chrom']
        seq = self.get_seq(chrom, start, end, rev_compl)
        return (id, chrom, start, end, seq)

    def get_closest_fwd_amplicon_id(self, pos):
        try:
            key = self.amplicons[self.amplicons['fwd_primer_start'] <= pos]['fwd_primer_start'].sub(pos).abs().idxmin()
        except:
            return None
        return key

    def get_closest_rev_amplicon_id(self, pos):
        try:
            key = self.amplicons[self.amplicons['rev_primer_end'] >= pos]['rev_primer_end'].sub(pos).abs().idxmin()
        except:
            return None
        return key

    def get_covering_amplicons(self, chrom, start, end=None):
        end = start if end is not None else start
        df = self.amplicons[(self.amplicons['chrom'] == chrom) & (self.amplicons['fwd_primer_start'] <= start) & (self.amplicons['rev_primer_end'] > end)]
        out = []
        return set(df.index)

    def in_primer(self, id, start, end=None, fwd=True):
        if end is None:
            end = start + 1
        id, chrom, pstart, pend, seq = self.get_fwd_primer(id) if fwd else self.get_rev_primer(id)
        return (start >= pstart and start < pend) or (end > pstart and end <= pend)

    def draw_amplicon(self, id):
        id, chrom, start, end, seq = self.get_fwd_primer(id)
        p1 = ">" * (end - start)
        id, chrom, start, end, seq = self.get_insert(id)
        i = "-" *  (end - start)
        id, chrom, start, end, seq = self.get_rev_primer(id)
        p2 = "<" * (end - start)
        return p1 + i + p2

    def export_csv(self):
        print(self.amplicons.to_csv())

    def export_ptrimmer(self):
        lines = [] 
        for amplicon in self.iter_amplicons():
            p1 = self.get_fwd_primer(amplicon)[-1]
            p2 = self.get_rev_primer(amplicon, True)[-1]
            l = len(self.get_insert(amplicon))
            lines.append(p1 + "\t" + p2 + "\t" + str(l))
        return lines
    
    def export_bedpe(self):
        lines = [] 
        for amplicon in self.iter_amplicons():
            p1 = self.get_fwd_primer(amplicon)
            p2 = self.get_rev_primer(amplicon)
            data = list(p1[1:4]) + list(p2[1:4]) + [p1[0]]
            data = [str(x) for x in data]
            lines.append("\t".join(data))
        return lines

def main():
    parser = argparse.ArgumentParser(prog="create_bedpe.py", description="create a bedpe file used for bamclipper based on two BED files containing the amplicon and the insert coordinates, respectively.", )
    parser.add_argument('amplicons', metavar="AMPLICON_FILE", help="BED file containing amplicon data", type=str)
    parser.add_argument('inserts', metavar="INSERT_FILE", help="BED file containing insert data", type=str)
    parser.add_argument('-o', metavar="FILE", help="output file name. Please consider>: Existing file will be overwritten! (default: stdout)", type=str, default=None)
    parser.add_argument('--version', action='version', version='%(prog)s ' + VERSION)
    args = parser.parse_args()

    if not os.path.isfile(args.inserts):
        sys.exit("error: " + args.amplicons + "does not exist.")
    if not os.path.isfile(args.inserts):
        sys.exit("error: " + args.inserts + "does not exist.")

    aset = ampliset(args.amplicons, args.inserts)    
    lines = aset.export_bedpe()
    if args.o:
        with open(args.o, "w") as handle:
            handle.write("\n".join(lines))
    else:
        for line in lines:
            print(line)

if __name__ == "__main__":
        main()
