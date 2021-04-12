'Print the input arguments to the screen.'

import argparse
import pdb

#import xarray as xr

import cmdline_provenance as cmdprov


def main(args):
    """Run the program."""

#    dset1 = xr.open_dataset(args.infile1)
#    dset2 = xr.open_dataset(args.infile2)
    new_log = cmdprov.new_log(infile_logs={'file.nc': 'file history...'},
                              code_url='https://github.com/',
                              extra_notes=['note1', 'note2'])
    print(new_log)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    
    parser.add_argument("infile1", type=str, help="Input file name")
    parser.add_argument("infile2", type=str, help="Input file name")
    parser.add_argument("outfile", type=str, help="Output file name")

    args = parser.parse_args()            
    main(args)
