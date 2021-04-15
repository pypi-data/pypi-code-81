import pandas as pd

def read_info_file(filename):
    # Read in the info file
    info = pd.read_csv(filename, sep="\t")
    info["cds_start0"] = info["cds_start"] - 1
    return info


def read_fasta(filename):
    """
    This is a simple function written in base python that
    returns a dictionary made from a fasta file
    """
    # Read in the transcript fasta
    fasta = {}
    with open(filename, 'r') as file:
        for line in file:
            if line.rstrip()[0:1] == ">":
                this_tx_name = line.rstrip().replace(">", "")
            else:
                try:
                    fasta[this_tx_name] += line.rstrip()
                except KeyError:
                    fasta[this_tx_name] = line.rstrip()
    return fasta
