"""Console script for predex."""
import sys
import argparse

import predex.designMatrix as designMatrix
import predex.annoGenerator as annoGenerator
import predex.createComparisons as createComparisons
import predex.processIPAresults as processIPAresults


"""Start called task"""
def main():
    check_args()


def check_args():
    parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50))
    parser = argparse.ArgumentParser(description = "Prepare data for expression analysis with e.g. dgeAnalysis - LUMC.")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.9.3")

    subparser = parser.add_subparsers()

    # design arguments
    a_parser = subparser.add_parser("design", help="Create design matrix template", formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50))
    a_parser.set_defaults(func=designMatrix.main)
    required = a_parser.add_argument_group('required arguments')
    required.add_argument("-i", "--input", help="Input files (count matrix, e.g., HTSeq)", required=True)
    required.add_argument("-o", "--output", help="Output directory (default = current)", default=".")

    # annotation arguments
    b_parser = subparser.add_parser("annotation", help="Create annotation file", formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50))
    b_parser.set_defaults(func=annoGenerator.main)
    b_parser.add_argument("-t", "--threads", help="Number of threads (default = 1)", default=1)
    required = b_parser.add_argument_group('required arguments')
    required.add_argument("-f", "--fasta", help="Fasta file input", required=True)
    required.add_argument("-g", "--gtf", help="GTF file input", required=True)
    required.add_argument("-o", "--output", help="Output directory (default = current)", default=".")
    
    # comparisons arguments
    c_parser = subparser.add_parser("comparison", help="Create comparisons for looped analysis", formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50))
    c_parser.set_defaults(func=createComparisons.main)
    required = c_parser.add_argument_group('required arguments')
    required.add_argument("-d", "--design", help="Design matrix with sample data", required=True)
    required.add_argument("-c", "--column", help="Column name to make comparisons with", required=True)
    required.add_argument("-o", "--output", help="Output directory (default = current)", default=".")

    # IPA output arguments
    d_parser = subparser.add_parser("ipa", help="Process IPA output in tidy tsv format", formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50))
    d_parser.set_defaults(func=processIPAresults.main)
    required = d_parser.add_argument_group('required arguments')
    required.add_argument("-i", "--input", help="Input dir with IPA downloaded table", required=True)
    required.add_argument("-o", "--output", help="Output dir to write processed data to (default = current)", default=".")
    required.add_argument("-e", "--extension", help="Extension of IPA files (default = .txt)", default=".txt")

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":    
    main()
