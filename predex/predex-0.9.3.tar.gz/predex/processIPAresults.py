#! /usr/local/bin/python3

import pandas as pd
import sys
import os

# --------------------------------------------------------------------------
# ----- Load input and call functions -----

def cleanFile(df_ipa, output):
    df_ipa.columns = ["Ingenuity Canonical Pathways", "pvalue", "ratio", "z-score", "Genes"]
    df_ipa = df_ipa.replace({"α": "a", "β": "B", "γ": "y"}, regex=True)    
    df_ipa["pvalue"] = 10 ** - df_ipa["pvalue"]
    return(df_ipa)


# --------------------------------------------------------------------------
# ----- Read input and write output to file -----

def read(input, output, extension):
    processed = 0
    for filename in os.listdir(input):
        if filename.endswith(extension):
            df_ipa = pd.read_csv(input + "/" + filename, sep="\t", decimal=",", header=1, usecols=[0,1,2,3,4])
            df_cleaned = cleanFile(df_ipa, output)
            filename = filename.replace(extension, ".tsv")
            write(df_cleaned, output, filename)
            processed += 1
            print("\tProcessed", processed, "files")
        else:
            continue


def write(df_cleaned, output, filename):
    df_cleaned.to_csv(output + "/" + filename, index=False, sep="\t")


# --------------------------------------------------------------------------
# ----- Load input and call functions -----

def main(args):
    inputDir = args.input
    outputDir = args.output
    extension = args.extension

    print("Start processing...")    

    read(inputDir, outputDir, extension)

    print("Done!")

if __name__ == "__main__":
    main()
