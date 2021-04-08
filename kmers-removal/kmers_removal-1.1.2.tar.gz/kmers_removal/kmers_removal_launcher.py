import logging
import os
import argparse
import sys
import pandas as pd

from tqdm import tqdm

"""If kmers are entered in a file, one kmer per line, then this scripts allows to
take a .fasta assembly and remove all the concerned kmers from it by replacing them
into N"""

def load_fasta(fastafile):
    """Returns a python dict { id : sequence } for the given .fasta file"""
    with open(os.path.realpath(fastafile), 'r') as filin:
        fasta = filin.read()
        fasta = fasta.split('>')[1:]
        outputdict = {x.split('\n')[0].strip(): "".join(x.split('\n')[1:]) for x in fasta}
    return outputdict

def determinate_presence(kmers_file,genome,verbosity):
    """Returns a pd.DataFrame that indicates which kmers have been found in which
    scaffolds, and how many occurences were found for this scaffold"""

    logging.info("[INFO] Generating the report for the presence of the kmers")

    kmers = open(os.path.realpath(kmers_file),"r").read().split('\n')

    proto_df = []

    genome = load_fasta(os.path.realpath(genome))

    for scaffold in genome:

        genome[scaffold] = genome[scaffold].upper() # This is usefull because the upper and lower letters
        # are soft-encoding of repeated sequences

        logging.info('[INFO] Seeking kmers in scaffold {}'.format(scaffold))

        if verbosity in ["DEBUG","INFO"]:
            wrapper = tqdm(kmers)
        else:
            wrapper = kmers

        for kmer in wrapper:
            nb_found = genome[scaffold].count(kmer)
            proto_df.append({"scaffold":scaffold,"kmer":kmer,"nb_found":nb_found})

    return pd.DataFrame(proto_df)

def dict_to_fasta(myDict, fastafile):
    """ from a python dict {Identifier:sequence}, writes a fastafile"""
    logging.debug('[DEBUG] (dict to fasta), fastafile = {}'.format(fastafile))
    logging.info('[INFO] Wrinting outputFasta at {}'.format(fastafile))
    def divide_seq(seq, length = 60, sep = '\n'):
        """From a full-length sequence, divides it in chunks of 60 letters (most frequent.fasta format)"""
        return( str(sep).join([seq[x:x+int(length)] for x in range(0, len(seq), length)]))
        # Tricky one liner --> Splits a sequence into chunks of size "length"
    with open(os.path.realpath(fastafile), "w") as filout:
        for key in myDict:
            filout.write('>'+str(key)+'\n'+str(divide_seq(myDict[key]))+'\n')

def refactor_genome(fastain,fastaout,path_to_kmers_to_remove,verbosity):
    """The previous functions and tools allowed you to study where your kmers were in both genomes
    Here, this function allows you to remove the kmers from a .fasta input and write a new .fasta output
    removal is performed by replacing the kmers by "N" nucleotides, which means 'unknown'"""

    logging.info('[INFO] Refactoring genome')

    logging.debug('[DEBUG] fastain = {}, fastaout = {}, path_to_kmers_to_remove = {}'.format(fastain,fastaout,path_to_kmers_to_remove))

    filin = os.path.realpath(fastain)
    filout = os.path.realpath(fastaout)
    genome_in = load_fasta(filin)

    list_kmers = open(os.path.realpath(path_to_kmers_to_remove),"r").read().split('\n')

    if not list_kmers[-1]: # if the last line is \n (which is frequent)
        del list_kmers[-1]

    logging.debug('[DEBUG] List kmers to remove = {}'.format(list_kmers))

    if verbosity in ["DEBUG","INFO"]:
        wrapper = tqdm(genome_in.copy())
    else:
        wrapper = genome_in.copy()

    for scaffold in wrapper:
        logging.info("[INFO] Handling scaffold {}".format(scaffold))
        genome_in[scaffold] = genome_in[scaffold].upper()
        for kmer in list_kmers:
            genome_in[scaffold] = genome_in[scaffold].replace(kmer,"N")

    dict_to_fasta(genome_in,filout)


def main():
    """ Interprets all arguments"""

    description = "Allows to remove a given list of kmers in a genome assembly"

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--fastaFile','-f',
                        required=True,
                        help='Input .fasta file where kmers must be removed',
                        type=os.path.realpath)

    parser.add_argument('--kmerFile','-k',
                        required=True,
                        help='Path to a file with 1 kmer to remove per line (can be list of files). Must contain only'
                             'upper A, T, C or G and \\n',
                        type=os.path.realpath)

    parser.add_argument('--output',"-o",
                            help='output .fa file',
                            required=True,
                            type=os.path.realpath)

    parser.add_argument('--verbosity','-v',
                            help='Choose your verbosity on stdout. Default: INFO. If verbosity < INFO, no progress_bar is displayed.',
                            required=False,
                            default="INFO",
                            choices=["NONE","DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])

    parser.add_argument('--report','-r',
                            help='[FACULTATIVE - DEFAULT is None] Path to a report of the kmers encountered',
                            required=False,
                            default=None,
                            type=os.path.realpath)


    args = parser.parse_args()
    # sequencefile = os.path.realpath(args.sequencefile)

    ###### Handling verbosity

    if args.verbosity != "NONE": # Configure the loglevel according to user's preference
        verboselevel = "logging."+str(args.verbosity)
        logging.basicConfig(stream=sys.stdout, level=eval(verboselevel),
                            format='%(asctime)s %(message)s')
        logging.info("[INFO] Initiating filtering")

    logging.debug('[DEBUG] Listing realpaths of kmerfiles')
    args.kmerFile = os.path.realpath(args.kmerFile)

    logging.info('[INFO] Checking that the kmerfile only contains A, T, C, G or \\n characters')
    try:
        kmerfile = open(args.kmerFile).read().upper()
        for line in kmerfile.split('\n'):
            assert not any([x not in "ATCG" for x in line])
    except AssertionError:
        logging.critical('[CRITICAL] Found "N" nucleotides or unauthorized characters in the kmer list. This might corrupt the analysis. Will abort')
        exit(-1)

    logging.debug('[DEBUG] Converting fastaFile into a realpath')
    args.fastaFile = os.path.realpath(args.fastaFile)

    logging.debug('[DEBUG] Converting output into a realpath')
    args.output = os.path.realpath(args.output)

    refactor_genome(fastain=args.fastaFile,fastaout=args.output,path_to_kmers_to_remove=args.kmerFile,verbosity=args.verbosity)

    if args.report:
        logging.info('[INFO] Generating a detailed report at {}'.format(args.report))
        df = determinate_presence(args.kmerFile,args.fastaFile,verbosity=args.verbosity)
        df.to_csv(os.path.realpath(args.report),index=False)
        logging.info('[INFO] Report generated')

    logging.info('[INFO] DONE')

    return 0

if __name__ == "__main__":
    main()
