from __future__ import print_function
from Bio import Entrez
from ete3 import NCBITaxa
from camelot_frs.camelot_frs import get_kb, get_frame, get_frames, get_frame_all_parents, get_frame_all_children, frame_parent_of_frame_p, frame_subsumes_or_equal_p
from camelot_frs.pgdb_loader import load_pgdb
from camelot_frs.pgdb_api import uniprot_links_of_reaction, potential_generic_reaction_p, get_generic_reaction_all_subs, sub_reactions_of_reaction, enzymes_of_reaction, potential_pathway_hole_p

from collections import defaultdict, namedtuple
from random import shuffle
import sys, gzip, sqlite3

### Local definitions:

## Named tuples for clearer data-structure accessors:

Taxon = namedtuple('Taxon', ['tax_id', 'scientific_name', 'parent_tax_id', 'rank', 'lineage'])
Annot = namedtuple('Annot', ['prot_id', 'description', 'ecs', 'eggnog_ids'])

eggnog_mapper_ogg_field = 18

## This needs to be set by the code which imports this module:
taxon_db_path = ''

### Code for fetching NCBI Taxonomy taxon information:

## We need to use BioPython to take all of the EggNOG OG taxa, and
## fetch the "lineage" information along with ranks, to allow filtering:
# def fetch_taxon_info(tax_ids):
#     taxon2tuple = {}
    
#     epost_keys = Entrez.read(Entrez.epost('taxonomy', id=','.join(tax_ids)))
#     fetch_handle = Entrez.efetch(db='taxonomy',
#                                  webenv=epost_keys['WebEnv'],
#                                  query_key=epost_keys['QueryKey'],
#                                  retmode="xml")
#     taxa = Entrez.read(fetch_handle)
#     for taxon in taxa:
#         taxon_id = taxon['TaxId']
#         if 'LineageEx' in taxon:
#             curr_taxon = Taxon(tax_id = taxon_id,
#                                scientific_name = taxon['ScientificName'],
#                                parent_tax_id = taxon['ParentTaxId'],
#                                rank = taxon['Rank'],
#                                lineage = taxon['LineageEx'])
#         else:
#             curr_taxon = Taxon(tax_id = taxon['TaxId'],
#                                scientific_name = taxon['ScientificName'],
#                                parent_tax_id = taxon['ParentTaxId'],
#                                rank = taxon['Rank'],
#                                lineage = [])
#         taxon2tuple[taxon_id] = curr_taxon
    
#     return taxon2tuple

## using ete3, we report the data in the same format as Entrez returns:
def fetch_taxon_info(tax_ids):
    ncbi = NCBITaxa(taxon_db_path)
    taxon2tuple = {}
    for tax_id in tax_ids:                                        
        ## Remove the 'root' node from the beginning, and the tax_id from the end (redundant):
        curr_lineage = ncbi.get_lineage(tax_id)[1:-1]
        if curr_lineage:
            lineage_list = [ {'TaxId': str(lineage_taxon_id),
                              'ScientificName': ncbi.translate_to_names([lineage_taxon_id])[0],
                              'Rank': ncbi.get_rank([lineage_taxon_id])[lineage_taxon_id] }
                             for lineage_taxon_id in curr_lineage ]
            parent_id = str(curr_lineage[-1])
        else:
            lineage_list = []
            parent_id = '1'
        curr_rank = ncbi.get_rank([tax_id])
        curr_taxon = Taxon(tax_id = tax_id,
                           scientific_name = ncbi.translate_to_names([int(tax_id)])[0],
                           parent_tax_id = parent_id,
                           rank = curr_rank[int(tax_id)] if len(curr_rank) > 1 else 'no rank',
                           lineage = lineage_list)
        taxon2tuple[tax_id] = curr_taxon

    return taxon2tuple

## Helper predicate function
def ncbi_taxon_p(taxon_id):
    ncbi = NCBITaxa(taxon_db_path)
    return len(ncbi.get_rank([taxon_id])) > 0


## ToDo: figure out best way to serialize: JSON?
def print_taxon_file(taxon2lineage):
    pass


### Annotation file loading:
def load_annot_file(annot_file):
    annot_dict = {}
    with open(annot_file,'r') as annot_fh:
        for line in annot_fh:
            curr_annot = parse_annot_line(line)
            if curr_annot:
                annot_dict[curr_annot.prot_id] = curr_annot
    return annot_dict


def parse_annot_line (line):
    if not line.startswith('#'):
        fields = line.split("\t")
        fields[len(fields)-1] = fields[len(fields)-1].rstrip('\r\n')
        if fields[0].startswith('gnl'):
            prot_id = fields[0].split('|')[2]
        else:
            prot_id = fields[0]
        ecs = fields[7].split(',')
        eggnog_ids = fields[18].split(',')
        curr_annot = Annot(prot_id = prot_id,
                           description = fields[21],
                           ecs = ecs,
                           eggnog_ids = eggnog_ids)
        return curr_annot


### EggNOG mapping file:

RxnMap = namedtuple('RxnMap', ['OG',
                               'tax_id',
                               'uniprot_acc',
                               'rxn',
                               'enzrxn',
                               'relation',
                               'related_rxn',
                               'rhea_id'],
                    defaults=[None])
                            

def load_eggnog_rxn_mapping_file(mapping_file):
    
    eggnog2rxns = defaultdict(list)
    #eggnog2map  = defaultdict(list)
    #rxn2map     = defaultdict(list)
    #og2taxid    = {}
    
    with gzip.open(mapping_file,'rt') as nog2rxn_fh:
        for line in nog2rxn_fh:
            fields = line.strip().split('\t')
            if len(fields) == 6:
                curr_rxn_map = RxnMap._make(fields + [None])
            else:
                curr_rxn_map = RxnMap._make(fields)
                
            eggnog2rxns[fields[0]].append(curr_rxn_map)
            # eggnog2map[fields[0]].append(fields)
            # og2taxid[fields[0]] = fields[1]
            # if fields[5] == 'direct':
            #     eggnog2rxns[fields[0]].add(fields[3])
            #     rxn2map[fields[3]].append(fields)
            # else:
            #     eggnog2rxns[fields[0]].add(fields[6])
            #     rxn2map[fields[6]].append(fields)
    
    return eggnog2rxns


        
## Load MetaCyc effective orphan reactions:
def load_metacyc_effective_orphan_reactions(orphan_file):
    metacyc_orphan_rxns = defaultdict(int)
    with open(orphan_file) as orphan_fh:
        for line in orphan_fh:
            metacyc_orphan_rxns[line.strip()]
    return metacyc_orphan_rxns

### Load in EggNOG annotation of proteins:

## Print warnings about unrecognized taxon IDs from annotation file:
def fetch_taxa_of_annotation(annot_file):
    tax_ids = []
    present_tax_ids = []
    with open(annot_file) as annot_fh:
        for line in annot_fh:
            if not line.startswith('#'):
                fields = line.strip().split('\t')
                ogs = fields[18].split(',')
                tax_ids.extend([ og.split('@')[1] for og in ogs ])
    for tax_id in set(tax_ids):
        if not ncbi_taxon_p(tax_id):
            print('Warning: Unable to find the following annotation file taxon ID in local NCBI Taxonomy DB (will be skippped): ' + str(tax_id), file = sys.stderr)
        else:
            present_tax_ids.append(tax_id)
            #    tax_ids = list(set(tax_ids))
    return fetch_taxon_info(present_tax_ids)


## There are a couple of ways that we can pick an annotation:
## 1. Use the "bestOG"
## 2. Pick the most specific OG(s)
## 3. Pick the most specific OG(s) subject to a taxonomic constraint
##    (i.e., don't use an archaeal OG if the target genome is a gammaproteobacterium)
def load_eggnog_annotation(annot_file, nog2rxn_conn, annot_mode='most_specific'):
    num_annots = 0
    annot_go_terms  = defaultdict(int)
    annot_ogs       = defaultdict(int)
    annot_taxon2tuple = fetch_taxa_of_annotation(annot_file)
    
    with open(annot_file) as annot_fh:
        for line in annot_fh:
            if not line.startswith('#'):
                fields   = line.strip().split('\t')
                for go_term in fields[6].split(','):
                    annot_go_terms[go_term.strip()]
                best_og = find_og_in_annot_line(fields[18],"", nog2rxn_conn, annot_taxon2tuple, annot_mode=annot_mode)
                if best_og != "":
                    annot_ogs[best_og]
    return annot_ogs, annot_go_terms


def find_og_in_annot_struct(annot_struct,
                            nog2rxn_conn,
                            annot_taxon2tuple,
                            annot_mode='most_specific'):
    return find_og_in_annot_line(','.join(annot_struct.eggnog_ids),
                                 '',
                                 nog2rxn_conn,
                                 annot_taxon2tuple,
                                 annot_mode='most_specific')


def find_og_in_annot_line(ogs_field, best_og_field, nog2rxn_conn, annot_taxon2tuple, annot_mode='most_specific'):
    if annot_mode == 'most_specific':
        return select_most_specific_annotation(ogs_field.split(','), nog2rxn_conn, annot_taxon2tuple)[0]
    elif annot_mode == 'most_specific_v2':
        return select_most_specific_annotation_v2(ogs_field.split(','),
                                                  best_og_field.split('|')[0],
                                                  nog2rxn_conn)
    elif annot_mode == 'all':
        return load_all_annotations(ogs_field.split(','))
    elif annot_mode == 'best':
        return 'ENOG41'+ best_og_field.split('|')[0]

def ogs_in_db(conn, OG):
    cursor = conn.cursor()
    cursor.execute('select * from nog2rxn where OG = ?', (OG,))
    return cursor.fetchall()

## Returns the most specific OG which has a Reactionary annotation
## No taxonomic filtering takes place here, though it possibly
## would be a good point at which to do so.
def select_most_specific_annotation(raw_ogs, nog2rxn_conn, annot_taxon2tuple):
    most_specific_og = ""
    most_specific_og_taxon = ""
    most_specific_og_dist = 0
    for og in raw_ogs:
        ##og_id = og.split('@')[0]
        og_taxon = og.split('@')[1]
        if ncbi_taxon_p(og_taxon) and len(ogs_in_db(nog2rxn_conn, og)) > 0:
            if og_taxon in annot_taxon2tuple:
                og_dist  = len(annot_taxon2tuple[og_taxon].lineage)
            else:
                og_dist = 0
            if og_dist > most_specific_og_dist:
                most_specific_og_dist = og_dist
                most_specific_og = og
                most_specific_og_taxon = og_taxon
    return [most_specific_og, most_specific_og_taxon]

def ncbi_taxon_subsumes_or_equal_p(parent, child):
    if parent.tax_id == child.tax_id:
        return True
    else:
        parent_taxon = [ taxon for taxon in child.lineage if taxon['TaxId'] == parent.tax_id ]
        return len(parent_taxon) > 0

    
def ncbi_taxon_id_in_lineage_p(taxon_ids, ncbi_taxon):
    found = False
    for taxon_id in taxon_ids:
        for taxon in ncbi_taxon.lineage:
            if taxon['TaxId'] == taxon_id:
                found = True
    return found
    
def map_filter_taxon2domain(org_taxon):
    bacteria = Taxon(tax_id='2',
                     scientific_name='Bacteria',
                     parent_tax_id='131567',
                     rank='superkingdom',
                     lineage=[{'TaxId': '131567',
                               'ScientificName': 'cellular organisms',
                               'Rank': 'no rank'}])
    archaea = Taxon(tax_id='2157',
                    scientific_name='Archaea',
                    parent_tax_id='131567',
                    rank='superkingdom',
                    lineage=[{'TaxId': '131567',
                              'ScientificName': 'cellular organisms',
                              'Rank': 'no rank'}])
    eukaryota = Taxon(tax_id='2759',
                      scientific_name='Eukaryota',
                      parent_tax_id='131567',
                      rank='superkingdom',
                      lineage=[{'TaxId': '131567',
                                'ScientificName': 'cellular organisms',
                                'Rank': 'no rank'}])
    if ncbi_taxon_subsumes_or_equal_p(archaea, org_taxon):
        return archaea
    if ncbi_taxon_subsumes_or_equal_p(bacteria, org_taxon):
        return bacteria
    if ncbi_taxon_subsumes_or_equal_p(eukaryota, org_taxon):
        return eukaryota

    
def map_rank(rank, org_taxon, annot_taxon2tuple):
    
    rank_order = ['superkingdom',
                  'phylum',
                  'class',
                  'order',
                  'family',
                  'genus' ]
    
    
    ## First, try to map the rank to something more specific:
    given_rank_idx = rank_order.index(rank)
    for rank_idx in range(given_rank_idx, len(rank_order)):
        curr_rank = rank_order[rank_idx]
        target_tax_id = [taxon['TaxId'] for taxon in org_taxon.lineage
                         if taxon['Rank'] == curr_rank ][0]
        if target_tax_id in annot_taxon2tuple:
            return (curr_rank, annot_taxon2tuple[target_tax_id])
    
    ## Second, try to map the rank to something subsuming:
    given_rank_idx = rank_order.index(rank)
    for rank_idx in range(given_rank_idx, 0, -1):
        curr_rank = rank_order[rank_idx]
        target_tax_id = [taxon['TaxId'] for taxon in org_taxon.lineage
                         if taxon['Rank'] == curr_rank ][0]
        if target_tax_id in annot_taxon2tuple:
            return (curr_rank, annot_taxon2tuple[target_tax_id])
        

    
## Reaction Prediction

def mapOG2rxn_tuples(og, nog2rxn_conn, taxon2tuple, org_taxon, tax_restrict=True):
    reactions = []
    og_tax_id = og.split('@')[1]
    if tax_restrict and \
       og_tax_id in taxon2tuple and \
       ncbi_taxon_subsumes_or_equal_p(org_taxon, taxon2tuple[og_tax_id]):
        reactions = ogs_in_db(nog2rxn_conn, og)
    
    return reactions


'''
There are many ways to map from a list of OGs to one or more reactions.

This function takes a policy argument, and then applies it to the raw data.

* instance_rxns_p:
  boolean, indicates whether to return instance reactions as return values 
  if their subsuming generic reaction is also in the return set.

* max_rxns:
  Integer, max number of reactions to return. If an OG is so generic that it would pull in more than max_rxns number of reactions, then it is deemed uninformative and nothing is pulled in.
'''

def eggnog_annot2rxns(annot_struct,
                      org_taxon,
                      nog2rxn_conn,
                      annot_taxon2tuple,
                      instance_rxns_p=False,
                      enclosing_rank='superkingdom'):
    
    og = find_og_in_annot_struct(annot_struct,
                                 nog2rxn_conn,
                                 annot_taxon2tuple,
                                 annot_mode='most_specific')
    if not og:
        return [], '', 'no OG found with associated reactions', '', ''

    
    #filter_taxon = map_filter_taxon2domain(org_taxon)

    mapped_rank, mapped_taxon = map_rank(enclosing_rank,
                                         org_taxon,
                                         annot_taxon2tuple)
    #if mapped_rank != enclosing_rank:
    #    print("Warning: Reactionary taxonomic rank adjusted to: " + mapped_rank, file=sys.stderr)
        
    # filter_taxon_id = [taxon['TaxId'] for taxon in org_taxon.lineage
    #                    if taxon['Rank'] == enclosing_rank ][0]
    #
    #filter_taxon = annot_taxon2tuple[ mapped_tax_id ]
    
    reaction_tuples = mapOG2rxn_tuples(og,
                                       nog2rxn_conn,
                                       annot_taxon2tuple,                          
                                       mapped_taxon,
                                       tax_restrict=True)
    
    ## Remove instance reactions when subsuming generic reaction is present:
    ## No-op for now, premature optimization
    
    return (reaction_tuples,
            mapped_rank,
            mapped_taxon,
            annot_struct.prot_id,
            og)
                
    




#### Obsolete / Deprecated:

def load_all_annotations(raw_ogs):
    og_taxlevel_dict = {}
    print(raw_ogs)
    for og in raw_ogs:
        og_id = og.split('@')[0]
        og_level = og.split('@')[1]
        if og_id.startswith('COG'):                    
            og_taxlevel_dict['NOG'] = og_id
        else:                    
            og_taxlevel_dict[og_level] = 'ENOG41' + og_id
    return list(og_taxlevel_dict.values())

## This is a hack, until we can do proper taxonomic queries:
    # og_taxlevel_dict = {}
    # for og in raw_ogs:
    #     og_id = og.split('@')[0]
    #     og_level = og.split('@')[1]
    #     if og_id.startswith('COG'):                    
    #         og_taxlevel_dict['NOG'] = og_id
    #     else:                    
    #         og_taxlevel_dict[og_level] = 'ENOG41' + og_id
    # ## If there's something more specific, pick that one
    # ##        otherwise, first pick pronog, then bactnog, and lastly use NOG.
    # if 'bactNOG' in og_taxlevel_dict.keys():
    #     return og_taxlevel_dict['bactNOG']
    # if 'NOG' in og_taxlevel_dict.keys():
    #     return og_taxlevel_dict['NOG']
    # for taxlevel in og_taxlevel_dict.keys():
    #     if taxlevel not in ['NOG','bactNOG','proNOG']:
    #         return og_taxlevel_dict[taxlevel]
    # if 'proNOG' in og_taxlevel_dict.keys():
    #     return og_taxlevel_dict['proNOG']
    # return None

def select_most_specific_annotation_v2(raw_ogs,best_og,eggnog2rxns):
    ## First, see if the 'best' hit is in our annotation set:
    if best_og in eggnog2rxns:
        return best_og
    
    ## Try to find a specific NOG that has a hit in our annotationset:
    for og in raw_ogs:
        og_id = og.split('@')[0]
        og_level = og.split('@')[1]
        if not og_id.startswith('COG') and og_level not in ['bactNOG', 'euNOG', 'arNOG'] and ('ENOG41'+og_id) in eggnog2rxns:
            return 'ENOG41'+og_id
    
    ## If no specific hits, try to find a kingdom-level hit:
    for og in raw_ogs:
        og_id = og.split('@')[0]
        og_level = og.split('@')[1]
        if not og_id.startswith('COG') and og_level in ['bactNOG', 'euNOG', 'arNOG'] and ('ENOG41'+og_id) in eggnog2rxns:
            return 'ENOG41'+og_id
    
    ## If all else fails, try to find a COG-level hit:
    for og in raw_ogs:
        og_id = og.split('@')[0]
        og_level = og.split('@')[1]
        if og_id.startswith('COG') and og_id in eggnog2rxns:
            return og_id
    
    ## If nothing has a hit in the eggnog2rxns hash, then just return the 'best' hit
    return best_og

## Report how many "hops" from taxon to root:
def tax_dist2root(metaKB, tax_id):
    tax_frame = get_frame(metaKB, "TAX-" + tax_id)
    if tax_frame:
        return len(get_frame_all_parents(tax_frame)) - 2
    else:
        return 0




