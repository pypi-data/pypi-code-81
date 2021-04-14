import os
from camelot_frs.camelot_frs import get_kb, get_frame, get_frames, get_frame_all_parents, get_frame_all_children, frame_parent_of_frame_p
from camelot_frs.pgdb_loader import load_pgdb
from camelot_frs.pgdb_api import uniprot_links_of_reaction, potential_generic_reaction_p, get_generic_reaction_all_subs, sub_reactions_of_reaction, enzymes_of_reaction, potential_pathway_hole_p, taxon_in_pathway_taxonomic_range_p
from reactionary.reactionary_lib import ncbi_taxon_id_in_lineage_p

from collections import defaultdict

## Pathway Prediction

## This MetaCyc metadata should really be in the SQLite3 db:
def load_metacyc_pwy_data():
    metacyc_pwy_file = os.path.dirname(__file__) + '/dbs/metacyc_pwy_metadata.txt'
    pwy2name = {}
    pwy2rxns = defaultdict(list)
    pwy2taxa = defaultdict(list)
    rxn2pwys = defaultdict(list)
    pwy2key_rxns = defaultdict(list)
    pwy2key_non_rxns = defaultdict(list)
    
    with open(metacyc_pwy_file) as meta_fh:
        for line in meta_fh:
            fields = line.strip().split('|')
            pwy = fields[0]
            pwy2name[pwy] = fields[1]
            if fields[4]:
                pwy2key_rxns[pwy] = fields[4].split(',')
            if fields[5]:
                pwy2key_non_rxns[pwy] = fields[5].split(',')
            ## We use [4:] to remove the 'TAX-' prefix:
            for taxon in fields[2].split(','):
                taxon_str = taxon[4:]
                pwy2taxa[pwy].append(taxon_str)
            for rxn in fields[3].split(','):
                pwy2rxns[pwy].append(rxn)
                rxn2pwys[rxn].append(pwy)                
    return pwy2name, pwy2rxns, pwy2taxa, rxn2pwys, pwy2key_rxns, pwy2key_non_rxns
            
            
# def gen_rxn_weighting_hash(kb):
#     weights = defaultdict(int)
#     rxn_class = get_frame(kb, "Reactions")
#     for rxn in get_frame_all_children(rxn_class, frame_types="instance"):
#         weights[rxn] = len(rxn.get_slot_values("IN-PATHWAY"))
#     return weights

def compute_weighted_rxn_fraction(pwy, present_rxns, pwy2rxns, rxn2pwys):
    weighted_rxns_total   = 0
    weighted_present_rxns = 0
    for rxn in pwy2rxns[pwy]:
        weighted_rxns_total += len(rxn2pwys[rxn])
        if rxn in present_rxns:
            weighted_present_rxns += len(rxn2pwys[rxn])
    return weighted_present_rxns*1.0/weighted_rxns_total


def predict_metacyc_pathways(present_rxns,org_taxon_tuple):
    possible_pwys = defaultdict(int)
    pwy_predictions = []
    (pwy2name,
     pwy2rxns,
     pwy2taxa,
     rxn2pwys,
     pwy2key_rxns,
     pwy2key_non_rxns) = load_metacyc_pwy_data()
    #rxn_weights = gen_rxn_weighting_hash(kb)
    for rxn in present_rxns:
        for pwy in rxn2pwys[rxn]:
            possible_pwys[pwy]
    for pwy in list(possible_pwys.keys()):
        super_pathway_p = False
        for rxn in pwy2rxns[pwy]:
            if rxn in pwy2name:
                super_pathway_p = True
        if not super_pathway_p and ncbi_taxon_id_in_lineage_p(pwy2taxa[pwy],
                                                              org_taxon_tuple):
            all_key_rxns_present_p = None
            key_non_rxns_satisfied_p = None
            
            if pwy in pwy2key_rxns:
                all_key_rxns_present_p = len(set(pwy2key_rxns[pwy])
                                             & set(present_rxns)) == len(pwy2key_rxns[pwy])
            else:
                all_key_rxns_present_p = None
            
            ## "Satisfied" means that the logical expression is true, and thus
            ## the pathway should not be predicted:
            if pwy in pwy2key_non_rxns:
                key_non_rxns = pwy2key_non_rxns[pwy]
                if key_non_rxns[0] == 'AND':
                    ## AND logic: if #all# rxns listed are present, then the condition is satisfied:
                    key_non_rxns_satisfied_p = len(set(key_non_rxns[1:]) - set(present_rxns)) == 0
                else:
                    ## OR logic: if *any* of the rxns listed are present, then the condition is satisifed:
                    key_non_rxns_satisfied_p = len(set(key_non_rxns[1:]) & set(present_rxns)) > 0
            else:
                key_non_rxns = []
                key_non_rxns_satsified_p = None
            
            pwy_predictions.append([pwy,
                                    pwy2name[pwy],
                                    compute_weighted_rxn_fraction(pwy, 
                                                                  present_rxns,
                                                                  pwy2rxns,
                                                                  rxn2pwys),
                                    pwy2taxa[pwy],
                                    list(set(pwy2rxns[pwy]) & set(present_rxns)),
                                    list(set(pwy2rxns[pwy]) - set(present_rxns)),
                                    all_key_rxns_present_p,
                                    pwy2key_rxns[pwy],
                                    key_non_rxns_satisfied_p,
                                    key_non_rxns
                                    
            ])
    return pwy_predictions

def _predict_pathway(pred_data,threshold):
    if pred_data[7] == ['']:
        key_rxns_p = True
    else:
        key_rxns_p = pred_data[6]
    
    if pred_data[9] == ['']:
        key_non_rxns_p = True
    else:
        key_non_rxns_p = pred_data[8]
    
    return pred_data[2] >= threshold \
        and key_rxns_p \
        and key_non_rxns_p
            
