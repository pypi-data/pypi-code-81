#! /usr/local/bin/python3

import sys


# --------------------------------------------------------------------------
# ----- Read & write -----

def readCountTable(inputFile):
    with open(inputFile, "r") as countTable:
        header = countTable.readline().strip().split()[1:]
    return header


def writeDesignMatrix(designMatrix, outputDir):
    with open(outputDir + "/design_matrix.tsv", "w") as sheet:
        for row in designMatrix:
            sheet.write('\t'.join(row) + "\n")


# --------------------------------------------------------------------------
# ----- Create sample sheet based on headers from count table -----

def createDesignMatrix(header):
    designMatrix = list()
    designMatrix.append(['sampleID', 'groupID', 'sex', 'phenotype'])
    header.sort()
    for column in header:
        designMatrix.append([column])    
    return designMatrix


# --------------------------------------------------------------------------
# ----- Start script and get arguments-----

def main(args):
    print("Start processing...")
    inputFile = args.input
    outputDir = args.output

    header = readCountTable(inputFile)
    designMatrix = createDesignMatrix(header)
    writeDesignMatrix(designMatrix, outputDir)
    print("Done!")


if __name__ == "__main__":
    main()
