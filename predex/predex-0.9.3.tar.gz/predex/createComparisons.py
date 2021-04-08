#! /usr/local/bin/python3

import pandas as pd
import itertools
import sys
import os


# --------------------------------------------------------------------------
# ----- Make possible combinations and write temporary data to file -----

def combinations(unique, designPath, outputDir):    
    value = unique[0]
    del unique[0]        
    matrixList = list(itertools.product([value], unique))
    for design in matrixList:
        with open(outputDir + "/tmp", "a") as myfile:
            myfile.write('\tlist(\n\t\tdesign = "' + outputDir + "/" + designPath +
                '",\n\t\tmatrix_v1 = "' + design[0] +
                '",\n\t\tmatrix_v2 = "' + design[1] +
                '",\n\t\tname = "' + design[0] + 'vs' + design[1] + '"\n\t),\n')
    return unique


# --------------------------------------------------------------------------
# ----- Write final data to file -----

def write_to_file(outputDir):    
    with open(outputDir + "/tmp", 'r') as myfile:
        lines = myfile.readlines()
        lines = lines[:-1]
    with open(outputDir + "/comparisons.R", "w") as myfile:
        myfile.writelines(lines)
        myfile.write("\t)\n)")
    os.remove(outputDir + "/tmp")


def readInputFiles(designPath, compare):
    designFile = pd.read_csv(designPath)
    if len(designFile.columns) == 1:
        designFile = pd.read_csv(designPath, sep="\t")    
    if len(designFile.columns) == 1:
        print("Design matrix not tab/comma seperated")
        sys.exit()
        
    try:
        unique = sorted(set(designFile[compare]))
    except KeyError as err:
        print("Column", err, "not in design matrix!")
        sys.exit()

    return unique


# --------------------------------------------------------------------------
# ----- Load input and call functions -----

def main(args):
    designPath = args.design
    compare = args.column
    outputDir = args.output

    print("Start processing...")
    unique = readInputFiles(designPath, compare)

    with open(outputDir + "/tmp", "w") as myfile:
        myfile.write("designs <- list(\n")

    print("Making combinations...")
    for item in range(len(unique)-1):
        unique = combinations(unique, designPath, outputDir)
    write_to_file(outputDir)

    print("Done!")

if __name__ == "__main__":
    main()
