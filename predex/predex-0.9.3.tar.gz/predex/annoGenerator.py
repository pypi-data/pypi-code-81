#!/usr/bin/python3

import queue
import threading
import pysam
import pandas as pd


allGeneData = dict()


# --------------------------------------------------------------------------
# ----- Monitor queue and threading -----

class startGenerator(threading.Thread):
    def __init__(self, queue):
      threading.Thread.__init__(self)
      self.queue = queue
   
    def run(self):
        while not self.queue.empty():
            reference, geneComplete = self.queue.get()
            newGene = get_geneInfo(geneComplete[0])
            gene_seq = getSequence(geneComplete[0], reference)
            allGeneData[newGene[0]] = addNewGene(geneComplete[1:], gene_seq, newGene)
            if len(allGeneData) % 5000 == 0:
                print("\tProcessed", len(allGeneData), "genes")
            self.queue.task_done()


# --------------------------------------------------------------------------
# ----- Read through gtf and call required functions -----

def readGTF(reference, gtf, threads):
    geneComplete = list()
    q = queue.Queue()
    
    with open(gtf, "r") as openFile:
        for line in openFile:
            line = line.strip().replace('\t', ';').split(";")
            if line[0][0] == "#":
                pass
            elif "gene" in line[2]:
                if geneComplete:
                    q.put([reference, geneComplete])
                geneComplete = list()
                geneComplete.append(line)
            elif "exon" in line[2]:
                exon = [int(line[3])-int(geneComplete[0][3]), int(line[4])-int(geneComplete[0][3])]
                geneComplete.append(exon)
    q.put([reference, geneComplete])

    for OneOf in range(int(threads)):
        thread = startGenerator(queue=q)
        thread.start()
    q.join()


# --------------------------------------------------------------------------
# ----- Call functions to gather exon data and merge all gene information -----

def addNewGene(exon_data, gene_seq, newGene):
    exon_data = checkExonData(exon_data)
    newGene = getExonIntron(newGene, gene_seq, exon_data)
    return newGene


# --------------------------------------------------------------------------
# ----- Create correct exon location without any overlap -----

def checkExonData(exon_data):
    exon_data = sorted(exon_data)
    correct = [exon_data[0]]
    for location in exon_data:
        if correct[-1][0] <= location[0] <= correct[-1][1] <= location[1]:
            correct[-1][1] = location[1]
        elif location[0] >= correct[-1][0] and location[1] <= correct[-1][1]:
            pass
        else:
            correct.append(location)
    return correct


# --------------------------------------------------------------------------
# ----- Get gene data from gtf -----

def get_geneInfo(line):
    try:
        geneSymbol = str(''.join([s for s in line if "gene_name" in s]).split()[-1].strip('"'))
    except IndexError as err:
        geneSymbol = str(''.join([s for s in line if "gene_id" in s]).split()[-1].strip('"'))
        print("\t geneName unavailable for", geneSymbol + ", will use geneID instead")
    newGene = [str(''.join([s for s in line if "gene_id" in s]).split()[-1].strip('"')),  # GeneID
               str(geneSymbol),  # GeneSymbol
               str(line[0]),  # Contig
               int(line[3]),  # StartPos
               int(line[4]),  # EndPos
               int(line[4]) - int(line[3]) + 1,  # Length
               str(line[6]),  # GeneStrand
               str(''.join([s for s in line if "gene_" and "type" in s]).split()[-1].strip('"'))]  # GeneType
    return newGene


# --------------------------------------------------------------------------
# ----- Get gene sequence -----

def getSequence(gene, reference):
    contig = str(gene[0])
    start = int(gene[3])
    end = int(gene[4])
    if start != end:
        genome = pysam.Fastafile(reference)
        sequence = genome.fetch(contig, start, end)
        genome.close()
    else:
        sequence = ""
    return sequence


# --------------------------------------------------------------------------
# ----- Get exon/intron data and add to gene data -----

def getExonIntron(newGene, gene_seq, exon_data):
    exon_seq = ""
    intron_seq = gene_seq
    for exon in exon_data:
        exon_seq += gene_seq[exon[0]:exon[1]]
        intron_seq = intron_seq[:exon[0]] + len(intron_seq[exon[0]:exon[1]])*"0" + intron_seq[exon[1]:]
    intron_seq = intron_seq.replace("0", "")

    exonlength = len(exon_seq)
    geneGC = getGCcontent(gene_seq)
    exonGC = getGCcontent(exon_seq)
    intronGC = getGCcontent(intron_seq)
    newGene.extend([geneGC, exonGC, intronGC, exonlength])
    return newGene


# --------------------------------------------------------------------------
# ----- Calculate GC content -----

def getGCcontent(sequence):
    if len(sequence) == 0:
        gc = 0
    else:
        gc = round(sum(map(sequence.count, ["G", "C"])) / len(sequence), 6)
    return gc


# --------------------------------------------------------------------------
# ----- Set column names and save dataframe as TSV -----

def saveDataframe(df, outputDir):
    df.columns = ["feature", "geneName", "chromosome", "startPos", "endPos",
                  "geneLength", "geneStrand", "geneType", "geneGC", "exonGC",
                  "intronGC", "exonLength"]
    df = df[["feature", "geneName", "chromosome", "startPos", "endPos",
             "geneStrand", "geneLength", "exonLength", "geneGC", "exonGC",
             "intronGC", "geneType"]]
    df[["startPos", "endPos", "geneLength", "exonLength"]] = df[
        ["startPos", "endPos", "geneLength", "exonLength"]].astype('Int64')
    df = df.sort_values("feature")
    df.to_csv(outputDir + "/annotation.tsv", sep="\t", index=False)


# --------------------------------------------------------------------------
# ----- Start script and get arguments -----

def main(args):
    print("Start processing...")
    print("\tProcessed 0 genes")

    reference = args.fasta
    gtf = args.gtf
    outputDir = args.output
    threads = args.threads

    readGTF(reference, gtf, threads)
    print("Processed", len(allGeneData), "genes")

    print("Saving data...")
    df = pd.DataFrame.from_dict(allGeneData, orient="index")
    df.columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
    saveDataframe(df, outputDir)

    print("Done!")


if __name__ == "__main__":
    main()
