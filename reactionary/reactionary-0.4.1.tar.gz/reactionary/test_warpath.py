from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from builtins import range
from past.utils import old_div
from camelot_frs.pgdb_loader import load_pgdb
from camelot_frs.camelot_frs import get_kb, get_frame, get_frames, get_frame_all_children
from .reactionary.reactionary_lib import load_eggnog_rxn_mapping_file, mapOG2rxn, find_og_in_annot_line
from .reactionary.warpath import predict_metacyc_pathways
from .reactionary.reactionary import coerce_taxonid_to_metacyc_taxon_frame, augment_eggnog_annotation
from Bio import Entrez
from collections import defaultdict
import sys, gzip, os
import matplotlib.pyplot as plt
import numpy as np

def eval_warpath(eggnog_rxn_annot_file, tax_id, metaKB):
    
    rxn_ids = defaultdict(int)
    
    ## Collect reaction IDs:
    with open(eggnog_rxn_annot_file) as annot_fh:
        for line in annot_fh:
            if not line.startswith('#'):
                fields = line.strip().split('\t')
                if len(fields) == (rxn_field+1) and len(fields[rxn_field]) > 0:
                    curr_rxn_ids = fields[rxn_field].split(',')
                    for curr_rxn in curr_rxn_ids:
                        rxn_ids[curr_rxn]
    
    ## Send off to warpath:
    pwy_predictions = predict_metacyc_pathways(get_frames(metaKB, list(rxn_ids.keys())),
                                               tax_id,
                                               metaKB)
    return pwy_predictions


rxn_field              = 22

eggnog_annot_file = os.path.dirname(__file__) + '/../test/ecocyc-annots/annot.emapper.annotations'

eggnog_rxn_annot_file = os.path.dirname(__file__) + '/../test/ecocyc-annots/annot.emapper.annotations.reactionary'

load_pgdb('/home/ubuntu/data/metacyc/23.1/data')
metaKB = get_kb('META')

tax_id = get_frame(metaKB, 'TAX-511145')

TODO: load annot_taxon2tuple

## Run EggNOG-Mapper over EcoCyc proteins:
augment_eggnog_annotation(eggnog_annot_file,
                          annot_taxon2tuple,
                          metaKB,
                          tax_id)

## Run predictions over EcoCyc EggNOG-Mapper output:
pwy_predictions = eval_warpath(eggnog_rxn_annot_file,
                               tax_id,
                               metaKB)

## Compute the true Pathways present in EcoCyc:
load_pgdb('/home/ubuntu/data/ecocyc/23.1/data')
ecoliKB = get_kb('ECOLI')

ecoli_pwys = [ pwy.frame_id for pwy in get_frame_all_children(get_frame(ecoliKB,'Pathways'),
                                                              frame_types='instance') ]

## Compute the TPR & FPR:
## TPR = TP/True = TP/(TP+FN)
## FPR = FP/False = FP/(FP+TN)

TP = defaultdict(int)
FP = defaultdict(int)
TN = defaultdict(int)
FN = defaultdict(int)
TPR = defaultdict(int)
FPR = defaultdict(int)
possible_metacyc_pwys = defaultdict(int)
threshold = defaultdict(int)
acc = defaultdict(int)
F1_score = defaultdict(int)

num_samples = 40
for i in range(0,num_samples+1):
    threshold[i] = i*1.0/num_samples
    for pwy, rxn_frac, _ in pwy_predictions:
        possible_metacyc_pwys[pwy.frame_id]
        if pwy.frame_id in ecoli_pwys:
            if rxn_frac >= threshold[i]:            
                TP[i] += 1
            else:
                FN[i] += 1
        else:
            if rxn_frac >= threshold[i]:
                FP[i] += 1
            else:
                TN[i] += 1
    TPR[i] = TP[i]*1.0/(TP[i]+FN[i])
    FPR[i] = FP[i]*1.0/(FP[i]+TN[i])
    acc[i] = old_div(1.0*(TP[i]+TN[i]),(TP[i]+TN[i]+FP[i]+FN[i]))
    F1_score[i] = old_div(2.0*TP[i],(2*TP[i]+FP[i]+FN[i]))


print(list(TPR.values()))
print(list(FPR.values()))

## ROC Curve:
plt.plot(list(FPR.values())+[0], list(TPR.values())+[0])
plt.ylim(0,1.0)
plt.xlim(0,1.0)
plt.show()

## Accuracy vs. threshold:
plt.plot(list(threshold.values()),list(F1_score.values()))
plt.ylim(0,1.0)
plt.xlim(0,1.0)
plt.show()
auc=np.trapz(list(TPR.values())+[0],list(FPR.values())+[0])
            
    
    
