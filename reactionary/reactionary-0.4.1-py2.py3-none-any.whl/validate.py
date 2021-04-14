from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from builtins import str
from past.utils import old_div
from reactionary.reactionary_lib import load_eggnog_rxn_mapping_file, load_metacyc_effective_orphan_reactions, load_eggnog_annotation, mapOG2rxn_tuples, tax_dist2root, fetch_taxon_info, fetch_taxa_of_annotation, load_annot_file, eggnog_annot2rxns
from reactionary.reactionary import coerce_taxonid_to_metacyc_taxon_frame, augment_eggnog_annotation, predict_pathways
from reactionary.warpath import predict_metacyc_pathways

from camelot_frs.camelot_frs import get_kb, get_frame, get_frames, get_frame_all_parents, get_frame_all_children, frame_parent_of_frame_p
from camelot_frs.pgdb_loader import load_pgdb
from camelot_frs.pgdb_api import uniprot_links_of_reaction, potential_generic_reaction_p, get_generic_reaction_all_subs, sub_reactions_of_reaction, enzymes_of_reaction, potential_pathway_hole_p, protein_complex_p, monomers_of_complex, get_dblinks, reactions_of_protein, complexes_of_monomer

from Bio import Entrez
from ete3 import NCBITaxa
from collections import defaultdict, namedtuple
from random import shuffle
import sys, gzip, time, os, sqlite3

"""
validate.py: Compare Reactionary predictions against PGDB:
"""



'''
Interactively:
load_pgdb("/home/taltman/data/biocyc-24.0/ecoli/24.0/data")

ecoliKB = get_kb('ECOLI')




env_tuple = load_env("/home/taltman/data/biocyc-24.0/meta/24.0/data", "/home/taltman/data/nog2rxn_v5.gz", "/home/taltman/repos/reactionary/reactionary/dbs/effective-metacyc-orphan-rxns_2020-07-21", "/home/taltman/repos/reactionary/test/ecoli-24-0-annot.emapper.annotations")

taxon2tuple = fetch_taxa_of_annotation("/home/taltman/repos/reactionary/test/ecoli-24-0-annot.emapper.annotations")

metaKB = get_kb('META')

pgdb_env_list = load_pgdb_env("/home/taltman/data/biocyc-24.0/ecoli/24.0/data", 'ECOLI', env_list[1])

env_list = load_env("/home/taltman/data/biocyc-24.0/meta/24.0/data", "/home/taltman/data/nog2rxn_v5.gz", "/home/taltman/repos/reactionary/reactionary/dbs/effective-metacyc-orphan-rxns_2020-07-21", "/home/taltman/repos/reactionary/test/ecoli-24-0-annot.emapper.annotations")

start_time = time.time(); val_list = pgdb_validate(env_list[2], '511145', env_list[0], taxon2tuple, env_list[4], pgdb_env_list[0], tax_restrict=False); print(str(time.time() - start_time))


### Debugging Bsub:

bsub_env_list = load_pgdb_env("/home/taltman/data/biocyc-24.0/bsub/42/data", 'BSUB', '/home/taltman/repos/reactionary/test/bsub-24-0-annot.emapper.annotations', env_list[0], env_list[1])

## Predicted rxns:
bsub_val_list = pgdb_validate(bsub_env_list[1], '2', env_list[0], bsub_taxon2tuple, env_list[4], bsub_env_list[0], tax_restrict=False)

## Rxns MetaCyc says should be there:
meta_bsub_rxns=[ enzrxn.get_slot_values('REACTION')[0].frame_id for enzrxn in get_frame_all_children(get_frame(metaKB, 'Enzymatic-Reactions'), frame_types = 'instance' ) if 'Bacillus subtilis 168' in enzrxn.get_slot_values('ENZYME')[0].get_slot_values('SPECIES') ]

## Differences:
len(set(meta_bsub_rxns) - set(bsub_val_list[0]))

bsub_manual_rxns = { enzrxn.get_slot_values('REACTION')[0].frame_id for enzrxn in get_frame_all_children(get_frame(bsub_kb, 'Enzymatic-Reactions'), frame_types = 'instance' ) if 'BASIS-FOR-ASSIGNMENT' in enzrxn.slots and enzrxn.get_slot_values('BASIS-FOR-ASSIGNMENT')[0] == ':MANUAL' }

bsub_val_list = pgdb_validate(bsub_env_list[1], '2', env_list[0], taxon2tuple, env_list[4], bsub_env_list[0], tax_restrict=True)

len(set(bsub_manual_rxns) - set(bsub_val_list[0]))
## Still 122 rxns not found, why?

## Removing rxns not in MetaCyc, and ones that don't have a enzymatic reaction, we're left with 49:
fn_rxns  = [rxn for rxn in list(set(bsub_manual_rxns) - set(bsub_val_list[0])) if get_frame(metaKB, rxn) and 'ENZYMATIC-REACTION' in get_frame(metaKB, rxn).slots ]

## Making sure that the reactions to scrutinize are 'testable':
len(set(fn_rxns) & set(bsub_env_list[0]))
# 27 reactions
fn_rxns = list(set(fn_rxns) & set(bsub_env_list[0]))


### New workflow:

env_tuple = load_env("/home/taltman/data/biocyc-24.0/meta/24.0/data",'/home/taltman/data/')

# ECOLI:
ecoli_env_list = load_pgdb_env('/home/taltman/data/biocyc-24.0/ecoli/24.0/data', 'ECOLI', '/home/taltman/repos/reactionary/test/ecoli-24-0-annot.emapper-annotations', env_tuple.orphan_dict, env_tuple.nog2rxn_conn)

# BSUB
bsub_env_list = load_pgdb_env("/home/taltman/data/biocyc-24.0/bsub/42/data", 'BSUB', '/home/taltman/repos/reactionary/test/bsub-24-0-annot.emapper.annotations', env_tuple.orphan_dict, env_tuple.nog2rxn_conn)

'''




## Load in MetaCyc2GO:
def load_metacyc2go(metacyc2go_file):
    metacyc2go_rxns = defaultdict(int)
    go2metacyc_rxn  = defaultdict(list)
    num_mappings = 0
    with open(metacyc2go_file) as metacyc2go_fh:
        for line in metacyc2go_fh:
            if not line.startswith('!'):
                num_mappings += 1
                metacyc_token = line.split(' > ')[0]
                metacyc_rxn = metacyc_token.split(':')[1].strip()
                metacyc2go_rxns[metacyc_rxn] = 1
                go_term = line.split(' ; ')[1].strip()            
                go2metacyc_rxn[go_term].append(metacyc_rxn)
    return metacyc2go_rxns, go2metacyc_rxn

## Load in go2metacyc mappings from MetaCyc

def load_metacyc2go_inhouse(go2metacyc_inhouse_file):
    go2metacyc_rxn_inhouse = defaultdict(list)
    metacyc_rxns_inhouse = defaultdict(int)
    with open(go2metacyc_inhouse_file) as go2metacyc_inhouse_fh:
        for line in go2metacyc_inhouse_fh:
            parts = line.strip().split('\t')
            go2metacyc_rxn_inhouse[parts[0]].append(parts[1])
            metacyc_rxns_inhouse[parts[1]]
    return metacyc_rxns_inhouse, go2metacyc_rxn_inhouse





def load_known_rxn_file(known_rxn_file):
    known_rxns = defaultdict(int)
    with open(known_rxn_file) as rxns_fh:
        for line in rxns_fh:
            known_rxns[line.strip()]
    return list(known_rxns.keys())





    


### Load Reactions from EcoCyc and select ones valid for comparison:

# Spot checking, I see that there are EcoCyc reactions that are not spontaneous nor orphans, yet have no associated enzyme information:
# Examples: RXN0-286, RXN-19340 (these are bad examples, for  they are protein reactions that would not be included.
# I should consider filtering out reactions for which there is little hope of annotating.

def rxn_classes_with_no_enzymatic_reactions():
    
    rxn_classes = get_frame_all_children(get_frame(metaKB, 'Reactions'), frame_types='class')
    rxn_class_size_list = []
    
    for rxn_class in rxn_classes:
        rxn_class_instances = get_frame_all_children(rxn_class, frame_types='instance')
        catalyzed_rxns = [ rxn for rxn in rxn_class_instances if 'ENZYMATIC-REACTION' in rxn.slots ]
        if rxn_class_instances:
            rxn_class_size_list.append([rxn_class, len(rxn_class_instances), len(catalyzed_rxns), len(catalyzed_rxns)*1.0/len(rxn_class_instances)])
        else:
            rxn_class_size_list.append([rxn_class, len(rxn_class_instances), len(catalyzed_rxns), None])
    
    return rxn_class_size_list


def get_testable_rxn_list(rxn_list, metacyc_orphans_dict):
    
    testable_rxns = []
    metaKB = get_kb('META')
    rxn_class         = get_frame(metaKB, 'Chemical-Reactions')
    rxns              = [ rxn for rxn in get_frame_all_children(rxn_class) if not rxn.class_p() ]
    meta_rxns         = [ rxn.frame_id for rxn in rxns ]
    spontaneous_rxns  = [ rxn.frame_id for rxn in rxns if rxn.get_slot_values('SPONTANEOUS?') == ['T'] ]
    super_rxns        = [ rxn.frame_id for rxn in rxns if rxn.get_slot_values('REACTION-LIST') ]
    protein_substrate_rxns = []
    
    for rxn in rxns:
        for cpd in rxn.get_slot_values('LEFT') + rxn.get_slot_values('RIGHT'):
            if type(cpd) is not str and frame_parent_of_frame_p(get_frame(metaKB, 'Proteins'), cpd):
                protein_substrate_rxns.append(rxn.frame_id)
    
    testable_rxns = ( set(rxn_list) & set(meta_rxns) ) \
        - set(metacyc_orphans_dict.keys()) \
        - set(spontaneous_rxns) \
        - set(super_rxns) \
        - set(protein_substrate_rxns)
    
    return testable_rxns



## When we are working with PGDBs, we can use this:
def get_pgdb_testable_reactions(orgKB, metacyc_orphans_dict,restrict_xport_p=True):
    rxn_class         = get_frame(orgKB, 'Chemical-Reactions')
    xport_rxn_class   = get_frame(orgKB, 'Transport-Reactions')
    rxns              = [ rxn for rxn in get_frame_all_children(rxn_class) if not rxn.class_p() ]
    if restrict_xport_p:
        xport_rxns        = [ rxn for rxn in get_frame_all_children(xport_rxn_class) if not rxn.class_p() ]
    else:
        xport_rxns = []
    orphan_rxns       = [ rxn for rxn in rxns if rxn.get_slot_values('ORPHAN?') == [':YES-CONFIRMED'] ]
    spontaneous_rxns  = [ rxn for rxn in rxns if rxn.get_slot_values('SPONTANEOUS?') == ['T'] ]
    pathway_holes     = [ rxn for rxn in rxns if potential_pathway_hole_p(rxn) ]
    super_rxns        = [ rxn for rxn in rxns if rxn.get_slot_values('REACTION-LIST') ]
    instantiated_rxns = [ rxn for rxn in rxns if 'COMMENT' in rxn.slots and 'instantiat' in rxn.get_slot_values('COMMENT')[0] ]
    metacyc_orphans   = get_frames(orgKB, list(metacyc_orphans_dict.keys()))
    protein_substrate_rxns = []

    ## Why are protein substrate reactions excluded?
    ## There are issues where the generic reaction and the specific reaction classify
    ## their substrates differently. Here is a quote from Amanda
    ## Mackey in an email sent on 2018-10-25:
    ## "In this case the substrate and product in RXN0-6542 are
    ## proteins (CheA and phosphorylated CheA) whereas in 2.7.13.2-RXN
    ## the substrates and products are all classified as
    ## compounds. I’m not sure how to resolve this given that
    ## RXN0-6542 is used in several two-component pways"
    ## This is a difference between MetaCyc and EcoCyc.
    ## There is also a smaller set of these reactions than
    ## small-molecule reactions. 
    ## To simplify testing, we are skipping them for now.
    
    for rxn in rxns:
        for cpd in rxn.get_slot_values('LEFT') + rxn.get_slot_values('RIGHT'):
            if type(cpd) is not str and frame_parent_of_frame_p(get_frame(orgKB, 'Proteins'), cpd):
                protein_substrate_rxns.append(rxn)
    
    testable_rxns = \
        set(rxns) \
        - set(xport_rxns) \
        - set(orphan_rxns) \
        - set(spontaneous_rxns) \
        - set(pathway_holes) \
        - set(protein_substrate_rxns) \
        - set(super_rxns) \
        - set(instantiated_rxns) \
        - set(metacyc_orphans)
    
    
    return [ rxn.frame_id for rxn in testable_rxns ]


## We should also print out all remaining reactions that are not found in MetaCyc for whatever reason:

# load_pgdb(metacyc_dir)
#metaKB = get_kb('META')
# meta_rxn_class        = get_frame(metaKB, 'Chemical-Reactions')
# meta_rxns             = [ rxn for rxn in get_frame_all_children(rxn_class) if not rxn.class_p() ]
# unanswerable_eco_rxns = list(set(testable_rxns) - set(meta_rxns))
# print "Testable EcoCyc reactions that are not found in MetaCyc:"
# print len(unanswerable_eco_rxns)
# print '\n'.join(unanswerable_eco_rxns)


def test_reactome_predictions_against_gold_standard(metacyc_predictable_rxns, reaction_set, known_rxns, metacyc_complex_enz_reactions):
    true_positives  = 0
    num_false_negatives = 0
    num_false_positives = 0
    false_positives = []
    false_negatives = []
    
    reaction_set = set(reaction_set) & set(metacyc_predictable_rxns)
    
    for rxn in known_rxns:
        if rxn not in reaction_set:
            num_false_negatives += 1
            false_negatives.append(rxn)
        else:
            true_positives += 1
    
    for rxn in reaction_set:
        if rxn not in known_rxns:
            num_false_positives += 1
            false_positives.append(rxn)
    
    print("# Known reactions (gold standard): ", len(known_rxns))
    print("# predicted reactions: ", len(reaction_set))
    print("# Known reactions not predicted: ", len(set(known_rxns)-set(reaction_set)))
    print("# TP: ", true_positives)
    print("# FP: ", num_false_positives)
    print("# FN: ", num_false_negatives)
    precision = true_positives*1.0/len(reaction_set)
    recall = true_positives*1.0/len(known_rxns)
    f1_score = old_div(2.0*(precision*recall),(precision+recall))
    print("Precision: ", precision)
    print("Recall:    ", recall)
    print("F1 score:  ", f1_score)
    shuffle(false_negatives)
    shuffle(false_positives)
    print("False Positive Report:")
    print("# FPs that are 'complex enzyme' reactions:", len(set(false_positives) & set(metacyc_complex_enz_reactions)))
    print("  Sample false positives:")
    print("  ", false_positives[0:9])
    print("False Negative Report:")
    print("  Sample false negatives:")
    print("  ", false_negatives[0:9])
    
    return [ false_positives, false_negatives ]



def load_ecocyc_metacyc(ecocyc_dir,metacyc_dir):
    load_pgdb(ecocyc_dir)
    load_pgdb(metacyc_dir)



def gen_metacyc_complex_all_rxns():
    metaKB = get_kb('META')
    
    metacyc_complex_direct_rxns = [ enzrxn.get_slot_values('REACTION')[0] for enzrxn in get_frame_all_children(get_frame(metaKB, 'Enzymatic-Reactions'), frame_types = 'instance') if 'COMPONENTS' in enzrxn.get_slot_values('ENZYME')[0].slots and len(enzrxn.get_slot_values('ENZYME')[0].get_slot_values('COMPONENTS')) > 1 ]
    metacyc_complex_indirect_rxns = []
    metacyc_complex_all_rxns = [ rxn.frame_id for rxn in metacyc_complex_direct_rxns ]
    
    for rxn in metacyc_complex_direct_rxns:
        for sub_rxn in sub_reactions_of_reaction(rxn):
            metacyc_complex_indirect_rxns.append(sub_rxn.frame_id)
            metacyc_complex_all_rxns.append(sub_rxn.frame_id)
    
    return metacyc_complex_all_rxns


### Scripts for testing particular mapping files/approaches:
def test_metacyc2go():
    
    metaKB  = get_kb('META')
    
    metacyc2go_rxns, go2metacyc_rxn = load_metacyc2go(metacyc2go_file)
    metacyc_rxns_inhouse, go2metacyc_rxn_inhouse = load_metacyc2go_inhouse(go2metacyc_inhouse_file)
    
    ecocyc_rxns = gen_pgdb_predictable_rxns('ECOLI', orphan_file)
    
    metacyc_predictable_rxns = gen_pgdb_predictable_rxns('META', orphan_file)
    
    annot_ogs, annot_go_terms = load_ecoli_eggnog_annotation(annot_file)
    
    ## Reactions directly catalyzed by an enzymatic reaction:
    
    metacyc_complex_all_rxns = gen_metacyc_complex_all_rxns()
    ## Load the predicted rxns using the GO project's metacyc2go resource:
    eggnog_rxns = defaultdict(int)
    
    for go_term in list(annot_go_terms.keys()):
        for rxn in go2metacyc_rxn[go_term]:
            eggnog_rxns[rxn]
    
    print("Predictions using GO project's metacyc2go reaction file:")
    test_reactome_predictions_against_gold_standard(metacyc_predictable_rxns, list(eggnog_rxns.keys()), ecocyc_rxns, metacyc_complex_all_rxns)



## 2113 1004 1203 646 358 1467
## Ergo, the biggest problem is that relying solely on metacyc2go to get reaction IDs is not sufficient; 1203 reactions cannot even be mapped!
## Need to explore mapping via EC numbers as an intermediary.
## I am suspicious of how the metacyc2go mapping is created, I should investigate when able to polish this tool...

def test_new_metacyc2go():
    
    metacyc_predictable_rxns = gen_pgdb_predictable_rxns('META', orphan_file)
    ecocyc_rxns = gen_pgdb_predictable_rxns('ECOLI', orphan_file)
    metacyc_complex_all_rxns = gen_metacyc_complex_all_rxns()
    
    ## Evaluate predicted rxns using my own metacyc2go mapping resource:
    eggnog_rxns = defaultdict(int)
    for go_term in list(annot_go_terms.keys()):
        for rxn in go2metacyc_rxn_inhouse[go_term]:
            eggnog_rxns[rxn]
    
    
    print("Predictions using hand-rolled GO 2 MetaCyc reaction file:")
    test_reactome_predictions_against_gold_standard(metacyc_predictable_rxns, list(eggnog_rxns.keys()), ecocyc_rxns, metacyc_complex_all_rxns)




## tax_id: like 'TAX-511145'
def pgdb_validate(annot_ogs,
                  tax_id,
                  nog2rxn_conn,
                  taxon2tuple,
                  metacyc_predictable_rxn,
                  org_rxns,
                  tax_restrict=False,
                  per_annot_p=True,
                  annot_struct_dict={},
                  max_rxns=10,
                  enclosing_rank='superkingdom'):
    
    ## Local definitions
    ##eggnog_rxns = defaultdict(int)
    ##ogs_no_hits = defaultdict(int)
    
    #metacyc_predictable_rxns = get_pgdb_testable_reactions(get_kb('META'), orphan_dict, restrict_xport_p=False)
    #org_rxns = get_pgdb_testable_reactions(orgKB, orphan_dict)
    
    org_taxon = fetch_taxon_info([tax_id])[tax_id]
    
    # else:
    #     org_rxns = get_testable_rxn_list(org_rxn_list, orphan_dict)
    
    
    #metaKB = get_kb('META')
    
    
    ## Predicted reactions using EggNog mapping:
    prediction_list = []
    all_predicted_rxns = []
    num_ogs = len(list(annot_ogs.keys()))
    cursor = nog2rxn_conn.cursor()
    all_nog2rxn_nogs = [ row['OG'] for row in cursor.execute('select distinct(OG) from nog2rxn') ]
    num_findable_ogs = len(set(annot_ogs.keys()) & set(all_nog2rxn_nogs))
    
    print("Reachability report: ")
    print("Reachable OGs: ", num_findable_ogs)
    print("Out of # predicted OGs:", num_ogs)
    
    if per_annot_p:
        for prot_id in annot_struct_dict.keys():
            reactions,_,_,_ = eggnog_annot2rxns(annot_struct_dict[prot_id],
                                                org_taxon,
                                                nog2rxn_conn,
                                                taxon2tuple,
                                                max_rxns = max_rxns,
                                                enclosing_rank = enclosing_rank )
            all_predicted_rxns.extend(reactions)
    else:
        
        for og in list(annot_ogs.keys()):
            og_hits = 0
            
            og_reactions = mapOG2rxn(og, nog2rxn_conn, taxon2tuple, org_taxon, tax_restrict=tax_restrict)
            
            all_predicted_rxns.extend(og_reactions)
            #        for rxn in eggnog2rxns[og]:            
            #            rxn_obj = get_frame(metaKB, rxn)
            # if tax_restrict == True:
            #     if 'ENZYMATIC-REACTION' not in rxn_obj.slots or thereis_enzyme_of_taxon_p(get_frame(metaKB, tax_id), enzymes_of_reaction(rxn_obj, include_composites=True)):
            #         eggnog_rxns[rxn] += 1
            #         annot_ogs[og] += 1
            #         og_hits += 1
            #         prediction_list.append([og, rxn])
            # else:
            #     eggnog_rxns[rxn] += 1
            #     annot_ogs[og] += 1
            #     og_hits += 1
            #     prediction_list.append([og, rxn])
    
    all_predicted_rxns = list(set(all_predicted_rxns))
    
            # if og_hits == 0:
            # ogs_no_hits[og]
        
    
    
    print("Predictions using UniProt-EggNOG mapping:")
    metacyc_complex_all_rxns = gen_metacyc_complex_all_rxns()
    #fp, fn = [], []
    fp, fn = test_reactome_predictions_against_gold_standard(metacyc_predictable_rxns, all_predicted_rxns, org_rxns, metacyc_complex_all_rxns)
    return [all_predicted_rxns, fp, fn, annot_ogs]



### Debugging utils:
def is_subreaction_p(rxn_id, eggnog_rxn_mapping):
    is_subreaction_p = False
    for nog, uni_acc, rxn_id, enzrxn_id, annot, subrxn in eggnog_rxn_mapping:
        if subrxn == rxn_id:
            is_subreaction_p = True
    return is_subreaction_p

def fp_report(fp_rxn, annot_ogs, org_rxn_list, rxn2map, nog2rxn_conn):
    rxn_map_entries = rxn2map[fp_rxn]
    mapped_ogs      = list(set([ map_entry[0] for map_entry in rxn_map_entries ]))
    ogs_in_annot    = [ og for og in mapped_ogs if og in annot_ogs ]
    maps = []
    prots = set()
    rxns_from_ogs = set()
    for og in ogs_in_annot:
        for map_entry in eggnog2rxns[og]:
            maps.append(map_entry)
            prots.add(map_entry[1])
            rxns_from_ogs.add(map_entry[2])
        
    
    print("False Positive report for reaction: " + fp_rxn)
    print("# map entries: " + str(len(rxn_map_entries)))
    print("# mapped OGs: " + str(len(mapped_ogs)))
    print("# mapped OGs in annotation: " + str(len(ogs_in_annot)))
    print("# prots from ogs: " + str(len(prots)))
    print("# rxns from ogs: " + str(len(rxns_from_ogs)))
    print("# rxns from ogs in org: " + str(len(set(rxns_from_ogs) & set(org_rxn_list))))
    return prots, rxns_from_ogs, set(rxns_from_ogs) & set(org_rxn_list), mapped_ogs, ogs_in_annot

    
    

'''
I want a function that, given a fp, will:
* Find the annotation entries that might have lead to that prediction
* Display the chain of inference that might have been used
* Display the genes, proteins, enzymes, reactions for the annotation entry, as found in EcoCyc
^^^ All of these is what I'm doing manually, and it takes a long time

Another function: predicate to test whether a reaction is of a certain taxon,
based on the lineage of the enzymes that catalyze the reaction. 
For example, test whether a reaction has at least a single enzyme that is found in a bacterial genome.
'''

def trace_rxn_fn(kb, rxn_id):
    rxn = get_frame(kb, rxn_id)
    print(rxn_id, rxn.get_slot_values('EC-NUMBER')[0])
    for enzrxn in rxn.get_slot_values('ENZYMATIC-REACTION'):
        print("\t", enzrxn.frame_id, enzrxn.get_slot_values('COMMON-NAME')[0])
        for enz in monomers_of_complex(enzrxn.get_slot_values('ENZYME')[0]):
            print("\t\t\t",
                  enz.frame_id,
                  enz.get_slot_values('COMMON-NAME')[0] if 'COMMON-NAME' in enz.slots else '',
                  enz.get_slot_values('SPECIES')[0] if 'SPECIES' in enz.slots else '',
                  get_dblinks(enz, 'UNIPROT'))

                    

def trace_prot(prot_id,annot_dict,eggnog2rxns, taxon2tuple, metaKB):
    if prot_id in annot_dict:
        print(prot_id)
        for og in annot_dict[prot_id].eggnog_ids:
            print("\t" + og + ":")
            for rxn in mapOG2rxn(og, eggnog2rxns, taxon2tuple, metaKB, '', tax_restrict=False):
                print("\t\t" + rxn)
    else:
        print(prot_id + ": No match")

envData = namedtuple('envData', ['nog2rxn_conn',
                                 'orphan_dict',
                                 'metacyc_predictable_rxns'])

### Print report for a single entry in the annotation dictionary:
## This needs to handle generic-specific rxns, and sub-reactions:
def pp_annot(prot_id,
             annot_struct_dict,             
             pgdb_kb,
             org_taxon,
             nog2rxn_conn,
             taxon2tuple,
             max_rxns = 100,
             verbose_p=True,
             enclosing_rank='superkingdom'):
    
    prot_frame = get_frame(pgdb_kb, prot_id)
    pgdb_rxns  = reactions_of_protein(prot_frame)
    prot_complexes = complexes_of_monomer(prot_frame)
    cplx_rxns = [rxn for cplx in prot_complexes
                     for rxn in reactions_of_protein(cplx) ]
    prot_rxns = [ rxn.frame_id for rxn in (pgdb_rxns + cplx_rxns)]
    (pred_reactions,
     mapped_rank,
     mapped_taxon,
     prot_id,
     og) = eggnog_annot2rxns(annot_struct_dict[prot_id],
                                             org_taxon,
                                             nog2rxn_conn,
                                             taxon2tuple,
                                             max_rxns = max_rxns,
                                             enclosing_rank=enclosing_rank)

    if verbose_p:
        print('# Report for protein ' + prot_id)
        print('## Annotation:')
        print(annot_struct_dict[prot_id])
        print('')
        print('## PGDB Stats:')
        print('### Direct Reactions of Protein:')
        print('- ' + ','.join([ rxn.frame_id for rxn in pgdb_rxns ]))
        if len(prot_complexes) > 0:
            print('### Complexes of Protein:')
            for cplx in prot_complexes:
                print('--- ' + cplx.frame_id)
                cplx_rxns = reactions_of_protein(cplx)
                if len(cplx_rxns) > 0:
                    print('#### Complex Reactions')
                    print('---- ' + ','.join([rxn.frame_id for rxn in cplx_rxns]))
        print('')
        print('## Predictions')
        if(enclosing_rank != mapped_rank):
            print('### Modified taxonomic constraint:')
            print('--- enclosing rank: ' + mapped_rank)
            print('--- enclosing taxon: ' + mapped_taxon)
        print('### Basis for Predictions:')
        print('--- OG: ' + og)
        print('### Predicted Reactions:')
        print('--- ' + ','.join(pred_reactions))
    return (prot_rxns, pred_reactions)

def categorize_prots(annot_struct_dict,             
                     pgdb_kb,
                     org_taxon,
                     nog2rxn_conn,
                     taxon2tuple,
                     max_rxns = 100,
                     enclosing_rank = "order"):
    equal_prots = []
    fp_prots = []
    fn_prots = []
    fn_fp_prots = []

    for prot in annot_struct_dict.keys():
        prot_rxns, pred_rxns = pp_annot(prot,
                                        annot_struct_dict,
                                        pgdb_kb,
                                        org_taxon,
                                        nog2rxn_conn,
                                        taxon2tuple,
                                        verbose_p = False,
                                        enclosing_rank = enclosing_rank)
        fp_rxns = set(pred_rxns) - set(prot_rxns)
        fn_rxns = set(prot_rxns) - set(pred_rxns)
        if set(pred_rxns) == set(prot_rxns):
            equal_prots.append(prot)
        elif len(fp_rxns) > 0 and len(fn_rxns) > 0:
            fn_fp_prots.append(prot)
        elif len(fp_rxns) > 0:
            fp_prots.append(prot)
        elif len(fn_rxns) > 0:
            fn_prots.append(prot)

    return (equal_prots, fn_fp_prots, fp_prots, fn_prots)
    

                
## This pre-loads the reference files for Reactionary & MetaCyc:
def load_env(metacyc_dir, ref_db_path):
    
    load_pgdb(metacyc_dir)
    #eggnog2rxns = load_eggnog_rxn_mapping_file(ref_db_path)
    orphan_file = os.path.dirname(__file__) + '/dbs/effective-metacyc-orphan-rxns_2020-07-21'
    orphan_dict = load_metacyc_effective_orphan_reactions(orphan_file)
    metaKB = get_kb('META')

    ## set up the ref DB object:
    conn = sqlite3.connect(ref_db_path + '/reactionary.db')
    conn.row_factory = sqlite3.Row
    
    metacyc_predictable_rxns = get_pgdb_testable_reactions(get_kb('META'), orphan_dict, restrict_xport_p=False)
    return envData(nog2rxn_conn = conn,
                   orphan_dict  = orphan_dict,
                   metacyc_predictable_rxns = metacyc_predictable_rxns)
                   

pgdbEnvData = namedtuple('pgdbEnvData',
                         ['pgdb_testable_reactions',
                          'annot_ogs',
                          'annot_go_terms',
                          'taxon2tuple',
                          'annot_dict'])

## This loads in the reference data for a given PGDB,
## so that it doesn't need to be recomputed after many runs.
def load_pgdb_env(pgdb_dir, org_id, annot_file, orphan_dict, nog2rxn_conn):
    load_pgdb(pgdb_dir)
    pgdb_kb = get_kb(org_id)
    annot_ogs, annot_go_terms = load_eggnog_annotation(annot_file, nog2rxn_conn, annot_mode='most_specific')
    annot_dict = load_annot_file(annot_file)
    taxon2tuple = fetch_taxa_of_annotation(annot_file)
    return pgdbEnvData(pgdb_testable_reactions = get_pgdb_testable_reactions(pgdb_kb, orphan_dict, restrict_xport_p=False),
                       annot_ogs = annot_ogs,
                       annot_go_terms = annot_go_terms,
                       taxon2tuple = taxon2tuple,
                       annot_dict = annot_dict)

### Print PGDB report, comparing Reactionary pathway predictions to PGDB pathways for a select set of pathway classes:

def get_warpath_pwys(taxon_id,
                     annot_path,
                     conn,
                     enclosing_rank):

    output_dir = '/tmp'
    ncbi_taxon_tuple = fetch_taxon_info([taxon_id])[taxon_id]
    taxon2tuple = fetch_taxa_of_annotation(annot_path)
    rxn2annot = augment_eggnog_annotation(annot_path,
                                          taxon2tuple,
                                          ncbi_taxon_tuple,
                                          conn,
                                          output_dir,
                                          max_rxns = 10,
                                          enclosing_rank = enclosing_rank)
    annotated_eggnog_file = output_dir + '/' + \
                            os.path.basename(annot_path)+'.reactionary'
    pwy_pred_results, _ = predict_pathways(annotated_eggnog_file,
                                           ncbi_taxon_tuple,
                                           output_dir)
    return pwy_pred_results, rxn2annot

def warpath_vs_pgdb_roc(taxon_id, predicted_pwys, pgdb, metaKB):
    for threshold in range(0,105,5):
        f1, precision, recall, \
            tp, fp, fn = warpath_vs_pgdb_stats(taxon_id,
                                               predicted_pwys,
                                               threshold/100,
                                               pgdb,
                                               metaKB)
        print(f'{f1:.2f}\t{precision:.2f}\t{recall:.2f}\t{tp}\t{fp}\t{fn}')
              

def eval_pwy_pred_p(taxon_id, pwy_pred, threshold):
    ncbi = NCBITaxa('/home/taltman/data/taxa.sqlite')
    tax_domain_p = len(set([str(tax_id) for tax_id in ncbi.get_lineage(taxon_id)]) & set(pwy_pred[3])) > 0
    pwy_p = tax_domain_p and pwy_pred[2] >= threshold
    if pwy_pred[6] != None:
        pwy_p = pwy_p and pwy_pred[6]
    if pwy_pred[8] != None:
        pwy_p = pwy_p and pwy_pred[8]
    
    return pwy_p
    
def warpath_vs_pgdb_stats(taxon_id, predicted_pwys, threshold, pgdb, metaKB):
    pwy_class = get_frame(metaKB, 'Pathways')
    super_pwy_class = get_frame(metaKB, 'Super-Pathways')
    predictable_pwys = [ pwy.frame_id
                         for pwy in get_frame_all_children(pwy_class, frame_types='instance')
                         if super_pwy_class not in pwy.get_frame_parents() ]
    pwy_class = get_frame(pgdb, 'Pathways')
    super_pwy_class = get_frame(pgdb, 'Super-Pathways')
    ecoli_predictable_pwys = [ pwy.frame_id
                               for pwy in get_frame_all_children(pwy_class, frame_types='instance')
                               if super_pwy_class not in pwy.get_frame_parents() ]

    predicted_pwy_ids = [ pred[0] for pred in predicted_pwys if eval_pwy_pred_p(taxon_id,
                                                                                pred,
                                                                                threshold) ]

    true_positives  = set(ecoli_predictable_pwys) & set(predicted_pwy_ids)
    false_positives = set(predicted_pwy_ids) - set(ecoli_predictable_pwys)
    false_negatives = set(ecoli_predictable_pwys) - set(predicted_pwy_ids)
    precision = len(true_positives)/len(predicted_pwy_ids)
    recall    = len(true_positives)/len(ecoli_predictable_pwys)
    f1_score = 2.0*precision*recall/(precision+recall)
    return (f1_score,
            precision,
            recall,
            len(true_positives),
            len(false_positives),
            len(false_negatives))


def warpath_vs_pgdb_pwys_report(env_tuple,
                                pgdb_dir,
                                org_id,
                                annot_path,
                                rxn_taxon_id,
                                pgdb_taxon_id,
                                pwy_class_list):
    metaKB = get_kb('META')
    
    pgdb_env_tuple = load_pgdb_env(pgdb_dir,
				   org_id,
				   annot_path,
				   env_tuple.orphan_dict,
                                   env_tuple.nog2rxn_conn)
    pgdb_kb = get_kb(org_id)
    
    pgdb_val_list = pgdb_validate(pgdb_env_tuple.annot_ogs,
                                  rxn_taxon_id,
                                  env_tuple.nog2rxn_conn,
                                  pgdb_env_tuple.taxon2tuple,
                                  env_tuple.metacyc_predictable_rxns,
                                  pgdb_env_tuple.pgdb_testable_reactions,
                                  annot_struct_dict = pgdb_env_tuple.annot_dict,
                                  tax_restrict=True,
                                  per_annot_p=True)
    
    # pgdb_taxon_frame = coerce_taxonid_to_metacyc_taxon_frame(pgdb_taxon_id,
    #                                                          metaKB,
    #                                                          Entrez.email)

    ncbi_taxon_tuple = fetch_taxon_info([pgdb_taxon_id])[pgdb_taxon_id]
    
    pwys = predict_metacyc_pathways(pgdb_val_list[0], ncbi_taxon_tuple)

    pwy_classes = get_frames(metaKB, pwy_class_list)
    
    pwys_dict = { pwy_pred[0]: pwy_pred for pwy_pred in pwys}
    
    print('\n### Pathway Prediction Comparison: ###\n')
    
    for pwy_class in pwy_class_list:
        pgdb_class = get_frame(pgdb_kb, pwy_class)
        meta_class = get_frame(metaKB,  pwy_class)
        if meta_class.class_p():
            pgdb_pwys_in_class = get_frame_all_children(pgdb_class,
                                                    frame_types='instance')
            warpath_pwys_in_class = [ pwy for pwy in get_frame_all_children(meta_class, frame_types='instance') if pwy.frame_id in pwys_dict ]
        else:
            pgdb_pwys_in_class = [ pgdb_class ]
            warpath_pwys_in_class = [ meta_class ] if meta_class.frame_id in pwys_dict else []
        print("[" + meta_class.frame_id + "]", meta_class.get_slot_values('COMMON-NAME')[0] + ':')
        print('\tPGDB pathways:')
        for pgdb_pwy in pgdb_pwys_in_class:
            if pgdb_pwy != None:
                print('\t\t[' + pgdb_pwy.frame_id + '] ' + pgdb_pwy.get_slot_values('COMMON-NAME')[0])
        ##print('\t' + str(pgdb_pwys_in_class) )
        print('\tWarPath predicted pathways:')
        for warpath_pwy in warpath_pwys_in_class:
            print('\t\t[' + warpath_pwy.frame_id + '] ' + warpath_pwy.get_slot_values('COMMON-NAME')[0] + ':')
            print('\t\t\tWeighted reaction norm: ' + str(pwys_dict[warpath_pwy.frame_id][2]))
            print('\t\t\tTaxonomic domain(s): ' + str(pwys_dict[warpath_pwy.frame_id][3]))
        print('')
    
    return [pgdb_env_tuple,
            pgdb_val_list,
            pwys]


def pwy_comp_report(pwy,
                    pgdbKB,
                    predicted_rxns):
    key_rxns = pwy.get_slot_values('KEY-REACTIONS')
    key_p = ''
    print('[' + pwy.frame_id + ']', pwy.get_slot_values('COMMON-NAME')[0], sep='\t')
    print('', 'ID', 'Key Rxn?', 'PGDB', 'Reactionary', sep = '\t')
    for rxn in pwy.get_slot_values('REACTION-LIST'):
        print('',
              rxn.frame_id,
              rxn in key_rxns,
              get_frame(pgdbKB, rxn.frame_id) != None,
              rxn.frame_id in predicted_rxns,
              sep = '\t')

#### Pwy Pred Validation

## Run this first:
## rxn2annot = augment_eggnog_annotation(annot_file, taxon2tuple, ncbi_taxon_tuple, metacyc_env_tuple.nog2rxn_conn, '/tmp', enclosing_rank='genus')

def run_pwy_pred_validation(orgKB, ncbi_taxon_tuple, rxn2annot):
    ecoli_pwys = [ pwy.frame_id for pwy in get_frame_all_children(get_frame(orgKB,"Pathways"),frame_types="instance") ]
    threshold_pwys = {}
    pwy_preds = predict_metacyc_pathways(list(rxn2annot.keys()), ncbi_taxon_tuple)
    for threshold in range(00,101,5):
        pred_pwys= [ pwy_data[0] for pwy_data in pwy_preds if predict_pathways(pwy_data,threshold/100) ]
        tp = set(ecoli_pwys) & set(pred_pwys)
        tn = set(ecoli_pwys) - set(pred_pwys)
        fp = set(pred_pwys) - set(ecoli_pwys)
        precision = len(tp)/len(set(pred_pwys))
        recall = len(tp)/len(set(ecoli_pwys))
        f1_score = (2.0*precision*recall)/(precision+recall)
        print(threshold,
              f1_score,
              precision,
              recall)
              

    
### When run as a script:
if __name__ == "__main__":
    
    ### Command-line arguments:
    
    metacyc2go_file         = sys.argv[1]
    annot_file              = sys.argv[2]
    ecocyc_dir              = sys.argv[3]
    go2metacyc_inhouse_file = sys.argv[4]
    metacyc_dir             = sys.argv[5]
    nog2rxn_file            = sys.argv[6]
    orphan_file             = sys.argv[7]
    known_rxn_file          = sys.argv[8]
    tax_id                  = sys.argv[9]

    # load_ecocyc_metacyc(ecocyc_dir,
    #                     metacyc_dir)
    load_pgdb(metacyc_dir)

    eggnog2rxns = load_eggnog_rxn_mapping_file(nog2rxn_file)
    orphan_dict = load_metacyc_effective_orphan_reactions(orphan_file)
    ## vvvv fix this
    annot_ogs, annot_go_terms = load_eggnog_annotation(annot_file,eggnog2rxns, annot_mode='most_specific')
    known_rxns  = load_known_rxn_file(known_rxn_file)

    # test_uniprot_eggnog([],
    #                     annot_ogs,
    #                     'TAX-511145',
    #                     eggnog2rxns, 
    #                     orphan_dict,
    #                     orgKB=get_kb('ECOLI'))

    test_uniprot_eggnog(known_rxns,
                         annot_ogs,
                        tax_id, # 'TAX-511145'
                        eggnog2rxns, 
                        orphan_dict)
    
