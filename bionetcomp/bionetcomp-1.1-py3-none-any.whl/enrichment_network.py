import os
import pandas as pd
import numpy as np
from pandas import DataFrame
import gseapy


def enrichment_network(input_file,taxid,fdr_cutoff,output_folder,name):

	genes_list = pd.read_csv(input_file, sep='\t',header=None)
	genes = genes_list.iloc[:,0]
	my_genes = genes.tolist()

	organism_validated = [9606,10090,7227,4932,6396,7955]
	org = {9606:'Human',10090:'Mouse',7227:'Fly',4932:'Yeast',6396:'Worm',7955:'Fish'}

	if(taxid in organism_validated):

			l = my_genes
			output = output_folder + "/" + name + "_enrichment_results"
			gseapy.enrichr(gene_list=l,
				description='pathway',
				gene_sets=['KEGG_2019','GO_Biological_Process_2018','WikiPathways_2016','Reactome_2016','Panther_2016'], 
				#gene_sets = 'KEGG_2019',
				organism = org[taxid],
				outdir=output,
				 top_term=20,
				cutoff = fdr_cutoff )

	else:
		print ("Invalid Organism! Enrichment is not possible to execute for %s taxid.\n Availables:"%taxid);
		print (org)
                #sys.exit(0)	
