from __future__ import print_function
from builtins import str
import gzip, time, pickle, shutil
from collections import defaultdict, namedtuple
import urllib.parse
import urllib.request
import requests
from contextlib import closing
from Bio import Entrez, SwissProt
from camelot_frs.pgdb_loader import load_pgdb
from camelot_frs.camelot_frs import KB, get_kb, get_frame, get_frame_all_children
from camelot_frs.pgdb_api    import potential_generic_reaction_p, get_generic_reaction_all_subs, sub_reactions_of_reaction, uniprot_links_of_reaction, monomers_of_complex, get_dblinks

'''
gen_mapping_file.py: Generate new reference files for Reactionary

This code should only need to be run once per MetaCyc release by the maintainer, and never by end-users.

Steps:
1. Obtain the latest versions of the flat-files for MetaCyc, EcoCyc, and BsubCyc
2. Update Reactionary and/or Camelot to make sure it can still work with the PGDBs without any bugs.
3. Run: load_pgdb('/path/to/metacyc/data')
4. Run create_uniprot2rxn_file
5. Run map_eggnog_rxn_mapping
6. Run print_eggnog_rxn_mapping to save results to file.
7. Run analyze_metacyc_rxns to see if effective orphan enzymes have changed.
'''

## Email address for Entrez:
Entrez.email = 'reactionary.entrez@altmananalytics.com'


#metaKB = get_kb('META')

## We want to have these mapping files self-document how they came upon the linkages, to assist with debugging.
## Instead of mapping between a UniProt accession and a reaction, there will be some keywords included, examples:
## ['RXN-12345', 'ENZRXN-1', 'direct']
## ['RXN-54321', 'ENZRXN-1', 'sub-reaction of RXN-12345']
## ['RXN-00001', 'ENZRXN-2', 'generic-reaction of RXN-99']

def create_uniprot2rxn_file(metacyc2rhea, rhea2swissprot, specific_rxn_p=True):
    uniprot2rxn = defaultdict(list)
    metaKB = get_kb('META')
    i = 0
    all_maps = []

    ## TODO: filter out sub-reactions, they are processed by the helper function.
    for enzrxn in get_frame_all_children(get_frame(metaKB, 'Enzymatic-Reactions'), frame_types = 'instance'):
        i += 1
        if (i % 100) == 0:
            print("Processed " + str(i) + " enzymatic reactions.")
        print( enzrxn.frame_id)
        for accession, rxn_relation in create_uniprot_rxn_map(enzrxn, metacyc2rhea, rhea2swissprot, specific_rxn_p=specific_rxn_p):
            uniprot2rxn[accession].append(rxn_relation)
    return uniprot2rxn

def get_metacyc_uniprot_accs(metaKB):
    accs = []
    bad_prots = [get_frame(metaKB, 'CPLX0-231'),
                 get_frame(metaKB, 'ABC-23-CPLX'),
                 get_frame(metaKB, 'ACETOLACTSYNII-CPLX')]
    print('Bad proteins in MetaCyc 24.0, check to see if issue fixed!', bad_prots)
    for enzrxn in get_frame_all_children(get_frame(metaKB, 'Enzymatic-Reactions'), frame_types = 'instance'):
        direct_enz = enzrxn.get_slot_values('ENZYME')[0]
        if direct_enz not in bad_prots:
            for accession in [ get_dblinks(monomer, 'UNIPROT') for monomer in monomers_of_complex(direct_enz)]:
                if accession:
                    accs.append(accession[0])
    return list(set(accs))

    
#TODO: Add argument for taking hash table of mappings from uniprot IDs to rhea, EC_num, and Uniprot IDs...
def create_uniprot_rxn_map(enzrxn, metacyc2rhea, rhea2swissprot, specific_rxn_p=True):
    relations = []
    direct_rxn = enzrxn.get_slot_values('REACTION')[0]
    direct_enz = enzrxn.get_slot_values('ENZYME')[0]
    rxns     = [[direct_rxn.frame_id,enzrxn.frame_id,'direct','']]

    if specific_rxn_p:
        if potential_generic_reaction_p(direct_rxn):
            for specific_rxn in get_generic_reaction_all_subs(direct_rxn):
                rxns.append([direct_rxn.frame_id,enzrxn.frame_id,'generic-specific',specific_rxn.frame_id])
    
    ## I really should filter out sub-reactions that are spontaneous or orphan'ed, but I'm punting for now,
    ## Since there shouldn't be any in theory (enzyme assigned to "composite" reaction could cover all components)
    for sub_rxn in sub_reactions_of_reaction(direct_rxn):
        rxns.append([direct_rxn.frame_id,enzrxn.frame_id,'composite-sub',sub_rxn.frame_id])
    
    ## The following logic takes the links from the direct reaction, 
    ## and shares them with all of its' "instance reactions":

    ### Some Rhea reporting:
    #for accession in [ get_dblinks(monomer, 'UNIPROT') for monomer in monomers_of_complex(direct_enz)]:
    #     print("Test:", accession)
    #     for (rhea_id, ec_num) in uniprot2rhea[accession[0]]:
    #         print("  Rhea: ", rhea_id, ec_num)
    #         for swissprot_acc in rhea2swissprot[rhea_id]:
    #             print("    SwissProt:", swissprot_acc)
    # print("  MetaCyc:", direct_rxn.frame_id, direct_rxn.get_slot_values('EC-NUMBER'))

    ## First, we add links to UniProt via Rhea:
    #if direct_rxn in metacyc2rhea:
    for rhea_id in metacyc2rhea[direct_rxn.frame_id]:
        for sprot in rhea2swissprot[rhea_id]:
            for rxn_relation in rxns:
                relations.append([sprot, rxn_relation + [rhea_id]])
                
    ## If we cannot map to UniProt via Rhea, we fall back to trying with
    try:
        ## 
        for accession in [ get_dblinks(monomer, 'UNIPROT') for monomer in monomers_of_complex(direct_enz)]:
            for rxn_relation in rxns:
                if accession:
                    relations.append([accession[0], rxn_relation + [None]])
                #uniprot2rxn[accession].append(rxn_relation)
        
        ## Here I should do a separate loop, where we go over UniProt
        ## accessions linked indirectly via Rhea reactions.
        ## Add another column at end to clarify the "original" uniprot ID, and the Rhea ID
    except:
        print("Unable to find uniprot links for reaction " + direct_rxn.frame_id)
    
    return relations

# def print_uniprot2rxn(install_path, uniprot2rxn_dict):
#     with open(install_path + '/dbs/uniprot2rxn.txt', "w") as out:
#         for acc in uniprot2rxn_dict.keys():
#             for 
#             print >>out, "\t".join([acc] + uniprot2rxn

def analyze_uniprot2rxn(metaKB, uniprot2rxn):
    enzrxns = get_frame_all_children(get_frame(metaKB,'Enzymatic-Reactions'), frame_types='instance')
    num_rxns_w_enz = len(set([enzrxn.get_slot_values('REACTION')[0] for enzrxn in enzrxns]))
    num_uniprot2rxn_rxns = len(set([relation[0] for relation_list in list(uniprot2rxn.values()) for relation in relation_list ]))
    print("Number of MetaCyc Reactions with enzymes: " + str(num_rxns_w_enz))
    print("Number of MetaCyc Reactions in uniprot2rxn: " + str(num_uniprot2rxn_rxns))

## If everything looks good using analyze_uniprot2rxn above, go ahead and "backup" the
## uniprot2rxn datastructure, as it takes over an hour to prepare.
def pickle_uniprot2rxn(uniprot2rxn,filename):
    with open(filename,'wb') as output_fh:
        pickle.dump(uniprot2rxn, output_fh, protocol=pickle.HIGHEST_PROTOCOL)

#### UniProt Queries ####

'''
We need to perform some programmatic queries of UniProt to perform the following mappings:

1. Get all UniProt accessions from proteins which catalyze reactions in MetaCyc
2. Fetch structured data for these entries from UniProt using API
3. For all entries with Rhea accessions, perform queries to pull in these additional proteins.
4. Upload total set of accessions, and download FASTA file for all accessions:

'''

## Call like:
## uniprot2rxn = create_uniprot2rxn_file(specific_rxn_p=False)
## fetch_uniprot_data(list(uniprot2rxn.keys()), 'foo@example.com')
## Took ~7 tries before it succeeded, be patient...

def fetch_uniprot_data(accs, email_address):
    with open("metacyc_uniprot_ids.txt","w") as uni_acc_fh:
        for acc in accs:
            print(acc, file=uni_acc_fh)
    
    url = "https://www.uniprot.org/uploadlists/"
    headers = {
        'User-Agent': 'Reactionary 0.1',
        'From': email_address
    }
    
    params = { 'from': 'ACC+ID',
               'to': 'ACC',
               'format': 'txt'
    }
    
    files = {'file': open('metacyc_uniprot_ids.txt')}
    
    request = requests.post(url,
                            files=files,
                            data = params,
                            headers=headers)
    
    with open('metacyc_uniprot_data.txt','w') as uni_data_fh:
        print(request.text[:-1], file=uni_data_fh)
    
    uniprot_records = []
    with open('metacyc_uniprot_data.txt') as uni_data_fh:
        for record in SwissProt.parse(uni_data_fh):
            uniprot_records.append(record)
    
    return uniprot_records

def get_record_rhea_ids(record):
    acc = record.accessions[0]
    rhea_list = []
    for comment in record.comments:            
        if comment.startswith('CATALYTIC') and 'Rhea:RHEA' in comment:
            rhea_id = comment.split(';')[1].split(',')[0].strip().split(':')[2]
            # ec_num = None
            # if "EC=" in comment:
            #     for comment_part in comment.split(';'):
            #         if "EC=" in comment_part:
            #             ec_num = comment_part.strip().strip('EC=')
            # rhea_list.append((rhea_id, ec_num))
            rhea_list.append(rhea_id)
    return rhea_list

def make_uniprot2rhea_dict(uniprot_dat_file):
    uniprot2rhea = defaultdict(list)
    rhea2uniprot = defaultdict(list)
    with open(uniprot_dat_file) as uniprot_fh:        
        for record in SwissProt.parse(uniprot_fh):
            acc = record.accessions[0]
            rhea_ids = get_record_rhea_ids(record)
            uniprot2rhea[acc] = rhea_ids
            for rhea_id in rhea_ids:
                rhea2uniprot[rhea_id].append(acc)
    return uniprot2rhea, rhea2uniprot
                

def query_uniprot_by_rhea(rhea_id, email_address):
    headers = {
        'User-Agent': 'Reactionary 0.1',
        'From': email_address
    }
    
    rhea_query_url = 'https://www.uniprot.org/uniprot/?query=annotation:(type:"catalytic activity" rhea:' + rhea_id + ')&format=txt'
    rhea_raw_prots = requests.get(rhea_query_url, headers=headers)
    
    with open("temp_rhea.txt","w") as rhea_data_fh:
        print(rhea_raw_prots.text[:-1], file=rhea_data_fh)
    
    rhea_records = []    
    with open('temp_rhea.txt') as rhea_data_fh:
        for record in SwissProt.parse(rhea_data_fh):
            rhea_records.append(record)
    return rhea_records


def download_curr_swissprot():
    url = 'ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz'
    
    with closing(urllib.request.urlopen(url)) as handle:
        with open('/tmp/uniprot_sprot.dat.gz', "wb") as sprot_fh:
            shutil.copyfileobj(handle, sprot_fh)

# def make_rhea2uniprot_dict(uniprot2rhea_dict, email_address):
#     rhea2uniprot = defaultdict(list)
#     for acc in list(uniprot2rhea_dict.keys())[0:5]:
#         print(acc)
#         for (rhea_id, _) in uniprot2rhea_dict[acc]:
#             rhea_records = query_uniprot_by_rhea(rhea_id, email_address)
#             for rhea_record in rhea_records:
#                 rhea2uniprot[rhea_id].append(rhea_record.accessions[0])
#     return rhea2uniprot

def load_swissprot(swissprot_file):
    
    with open(swissprot_file) as sprot_fh:
        records = [ record for record in SwissProt.parse(sprot_fh)]
    return records

def map_metacyc2uniprot(rhea2metacyc_file, rhea2uniprot_sprot):
    metacyc_rhea_ids = defaultdict(int)
    uniprot_ids = defaultdict(int)
    metacyc2rhea = defaultdict(set)
    rhea2swissprot = defaultdict(set)
    
    line_num = 0
    with open(rhea2metacyc_file) as rhea2meta_fh:
        for line in rhea2meta_fh:
            line_num += 1
            if line_num > 1:
                fields = line.strip().split('\t')
                metacyc_rhea_ids[fields[0]]
                metacyc_rhea_ids[fields[2]]
                metacyc2rhea[fields[3]].add(fields[0])
                metacyc2rhea[fields[3]].add(fields[2])
    
    line_num = 0
    with open(rhea2uniprot_sprot) as rhea2sprot_fh:
        for line in rhea2sprot_fh:
            line_num += 1
            if line_num > 1:
                fields = line.strip().split('\t')
                rhea2swissprot[fields[0]].add(fields[3])
                rhea2swissprot[fields[2]].add(fields[3])
                if fields[0] in metacyc_rhea_ids or fields[2] in metacyc_rhea_ids:
                    uniprot_ids[fields[3]]
    
    return list(uniprot_ids.keys()), metacyc2rhea, rhea2swissprot


def print_uniprot_record_as_fasta(fasta_fh, record):
    acc = record.accessions[0]
    print('>'+acc, file=fasta_fh)
    print(record.sequence, file=fasta_fh)

def filter_sprot_by_acc(accs,
                        swissprot_file,
                        fasta_filename):
    sprot_accs = []
    accs_dict = { acc:1 for acc in accs }
    with open(swissprot_file) as sprot_fh:
        with open(fasta_filename,"w") as fasta_fh:
            records = SwissProt.parse(sprot_fh)
            for record in records:
                acc = record.accessions[0]
                if acc in accs_dict:
                    sprot_accs.append(acc)
                    print_uniprot_record_as_fasta(fasta_fh,
                                                  record)
    return list(set(accs)-set(sprot_accs))

## We need a way to easily fetch TrEMBL sequences from MetaCyc:
def generate_uniprot_fasta(swissprot_file,
                           fasta_filename,
                           uniprot2rhea,
                           metaKB):
    rhea2metacyc_uniprot = defaultdict(list)
    for (acc, rhea_list) in uniprot2rhea.items():
        for (rhea_id, ec_num) in rhea_list:
            rhea2metacyc_uniprot[rhea_id].append(acc)
    rhea2swissprot = defaultdict(list)
    uniprot_ids = get_metacyc_uniprot_accs(metaKB)
    sprot_accs = defaultdict(int)
    metacyc_accs_not_sprot = []
    with open(swissprot_file) as sprot_fh:
        with open(fasta_filename,"w") as fasta_fh:
            records = SwissProt.parse(sprot_fh)
            for record in records:
                acc = record.accessions[0]
                sprot_accs[acc]
                rhea_match_p = False
                for (rhea_id, ec_num) in get_record_rhea_ids(record):
                    if rhea_id in rhea2metacyc_uniprot:
                        ## We only collect rhea mappings relevant to MetaCyc:
                        rhea2swissprot[rhea_id].append(acc)
                        rhea_match_p = True
                if acc in uniprot_ids:
                    print_uniprot_record_as_fasta(fasta_fh,
                                                  record)
                else:
                    if rhea_match_p:                        
                        print_uniprot_record_as_fasta(fasta_fh,
                                                      record)
    non_sprot_accs = [ acc for acc in uniprot_ids if acc not in sprot_accs]
    return rhea2swissprot, non_sprot_accs

## Finally, we have to fetch the TrEMBL sequences, and print them out:
## Like the above step fetching the MetaCyc entries, this is prone to failure due to the UniProt web service being down. Will fail with message like: "Failed to find ID in first line." Manually inspect the 'metacyc_uniprot_data.txt' file to see full error message from UniProt.

def print_non_sprot_records(non_sprot_accs, fasta_file, email_address):
    non_sprot_records = fetch_uniprot_data(non_sprot_accs,
                                           email_address)
    with open(fasta_file, 'w') as out_fh:
        for record in non_sprot_records:
            print_uniprot_record_as_fasta(out_fh, record)

'''
TODO:
- Create script to merge the two FASTA files, instead of doing so manually.
'''
            
#### Process EggNOG output: 

def map_eggnog_rxn_mapping(annot_path, uniprot2rxn):
    #uniprot2rxn = create_uniprot2rxn_file()
    eggnog_rxn_mapping = []
    eggnog_uniprot_mapping = [] 
    uniprot_acs_w_eggnog_annot = defaultdict(int)
    metacyc_uniprots_w_annot  = defaultdict(int)
    metacyc_uniprots_w_eggnog = defaultdict(int)
    line_num = 0
    num_mappings = 0
    
    ### Add mappings coming from manually running emapper over UniProt proteins without EggNOG entries:
    
    with open(annot_path) as annot_fh: ##install_path + '/dbs/uniprot-metacyc-all/annot.emapper.annotations') as annot_fh:
        for line in annot_fh:
            if not line.startswith('#'):
                line_num += 1
                if (line_num % 100000) == 0:
                    print("Processed " + str(line_num) + " EggNOG annotations.")            
                fields = line.strip().split('\t')
                uniprot_ac = fields[0] #.split('|')[1]
                eggnog_ids = fields[18].split(',')
                if uniprot_ac in uniprot2rxn:
                    metacyc_uniprots_w_annot[uniprot_ac]
                if len(eggnog_ids) > 0:
                    uniprot_acs_w_eggnog_annot[uniprot_ac]
                    for raw_eggnog_id in eggnog_ids:
                        if len(raw_eggnog_id) > 0:
                            og_parts = raw_eggnog_id.split('@')
                            eggnog_id = og_parts[0]
                            taxon_id  = og_parts[1]
                        if uniprot_ac in uniprot2rxn:
                            metacyc_uniprots_w_eggnog[uniprot_ac]
                            for rxn_relation in uniprot2rxn[uniprot_ac]:
                                eggnog_rxn_mapping.append([raw_eggnog_id, taxon_id, uniprot_ac] + rxn_relation)
                                num_mappings += 1
                                if (num_mappings % 100000) == 0:
                                    print("  Added " + str(num_mappings) + " EggNOG-MetaCyc mappings.")
                        else:
                            eggnog_uniprot_mapping.append([raw_eggnog_id, taxon_id, uniprot_ac])
    
    ## Print some stats on the mapping work:
    print("Mapping Stats:")
    print("Number of UniProt accession numbers harvested from MetaCyc: ", len(list(uniprot2rxn.keys())))
    print("Number of MetaCyc UniProt accession numbers in annot file: ", len(metacyc_uniprots_w_annot))
    print("Number of MetaCyc UniProt accession numbers with EggNOG mapping(s): ", len(metacyc_uniprots_w_eggnog))
    print("Number of UniProt accessions with EggNOG annotation: ", len(list(uniprot_acs_w_eggnog_annot.keys())))
    print("Number of UniProt accessions without direct mapping: ", len(set([rxn for [rxn, _, _] in eggnog_uniprot_mapping])))
    
    return [eggnog_rxn_mapping, eggnog_uniprot_mapping, list(set(uniprot2rxn.keys()) - set(metacyc_uniprots_w_annot.keys()))]



def print_eggnog_rxn_mapping(eggnog_rxn_mapping,filename):
    with open(filename,'w') as output_fh:
        for entry in eggnog_rxn_mapping:
            str_entry = map(str, entry)
            print('\t'.join(list(str_entry)), file=output_fh)
    

# go_enzyme_instance_rxns = {}
# for rxn in go_enzyme_rxns.keys():
#     print rxn
#     instance_rxns = get_generic_reaction_all_subs(rxn)
#     if instance_rxns:
#         for inst_rxn in instance_rxns:
#             go_enzyme_instance_rxns[inst_rxn] = 1


## We use this function to print a working list of "effective orphans":
def analyze_metacyc_rxns(metaKB):
    
    all_rxns          = get_frame_all_children(get_frame(metaKB, 'Reactions'), frame_types='instance')
    direct_catalyzed_rxns    = [ rxn for rxn in all_rxns if 'ENZYMATIC-REACTION' in rxn.slots ]
    orphan_rxns       = [ rxn for rxn in all_rxns if rxn.get_slot_values('ORPHAN?') == [':YES-CONFIRMED'] ]
    spontaneous_rxns  = [ rxn for rxn in all_rxns if rxn.get_slot_values('SPONTANEOUS?') == ['T'] ]
    catalyzed_sub_rxns = defaultdict(int)
    catalyzed_instance_rxns = defaultdict(int)
    
    for rxn in direct_catalyzed_rxns:
        for sub_rxn in sub_reactions_of_reaction(rxn):
            catalyzed_sub_rxns[sub_rxn]
    
    for rxn in direct_catalyzed_rxns:
        print(rxn)
        for instance_rxn in get_generic_reaction_all_subs(rxn):
            catalyzed_instance_rxns[instance_rxn]
    
    uncertain_status = set(all_rxns) - set(direct_catalyzed_rxns) - set(orphan_rxns) - set(spontaneous_rxns) - set(catalyzed_sub_rxns.keys()) - set(catalyzed_instance_rxns.keys())
    
    return [all_rxns, direct_catalyzed_rxns, orphan_rxns, spontaneous_rxns, list(catalyzed_sub_rxns.keys()), list(catalyzed_instance_rxns.keys()), uncertain_status]



#### Code no longer used:

# enzymes = [enzrxn.get_slot_values('ENZYME')[0] for enzrxn in get_frame_all_children(get_frame(ecoliKB, 'Enzymatic-Reactions'), frame_types = 'instance')]
# go_enzymes = [enzyme for enzyme in enzymes if len(enzyme.get_slot_values('GO-TERMS')) > 0]


# metaKB = get_kb('META')
# go_enzyme_rxns = {}
# for enzrxn in get_frame_all_children(get_frame(metaKB, 'Enzymatic-Reactions'), frame_types = 'instance'):
#     print_enzrxn_go_rxn_relations(enzrxn)

def print_enzrxn_go_rxn_relations(enzrxn):
    enzyme     = enzrxn.get_slot_values('ENZYME')[0]
    direct_rxn = enzrxn.get_slot_values('REACTION')[0]
    enzymes    = [enzyme]
    rxns       = [direct_rxn]
    
    if protein_complex_p(enzyme):
        enzymes += monomers_of_complex(enzyme)
    
    if potential_generic_reaction_p(direct_rxn):
        rxns += get_generic_reaction_all_subs(direct_rxn)
        
    for monomer in enzymes:
        for rxn in rxns:
            for term in monomer.get_slot_values('GO-TERMS'):
                print('\t'.join([term.frame_id, rxn.frame_id]))


## This currently gets us 10619 out of 10866 UniProt proteins mapped to EggNOG
## The rest are oddball entries, like viral proteins. Punting for now.
def map_eggnog_rxn_mapping_original(install_path, uniprot2rxn):
    #uniprot2rxn = create_uniprot2rxn_file()
    eggnog_rxn_mapping = []
    uniprot_acs_w_eggnog_annot = defaultdict(int)
    uniprot_acs_w_eggnog_annot_from_tab = defaultdict(int)
    uniprot_acs_w_eggnog_annot_from_emapper = defaultdict(int)
    
    ### Add mappings coming from UniProt:
    with gzip.open(install_path + '/dbs/uniprot-metacyc-w-tax-info.tsv.gz','rt') as swissprot_eggnog:
        for line in swissprot_eggnog:
            if not line.startswith('Entry'):
                fields = line.strip().split('\t')
                ## This is necessary because some rows are "deleted" entries.
                if len(fields) > 6:
                    print(fields[0])
                    eggnog_ids = fields[6].split(';')
                    if len(eggnog_ids) > 1:
                        uniprot_acs_w_eggnog_annot[fields[0]]
                        uniprot_acs_w_eggnog_annot_from_tab[fields[0]]
                    for eggnog_id in eggnog_ids:
                        if len(eggnog_id) > 0:
                            for rxn_relation in uniprot2rxn[fields[0]]:
                                eggnog_rxn_mapping.append([eggnog_id, fields[0]] + rxn_relation)
    
    ### Add mappings coming from manually running emapper over UniProt proteins without EggNOG entries:
    
    ## Archaea:
    for domain in ['archaea', 'bacteria', 'eukaryota']:
        with open(install_path + '/dbs/uniprot-metacyc-no-eggnog-' + domain + '/annot.emapper.annotations') as annot_fh:
            for line in annot_fh:
                if not line.startswith('#'):
                    fields = line.strip().split('\t')
                    print(fields[0])
                    uniprot_ac = fields[0].split('|')[1]
                    eggnog_ids = fields[9].split(',')
                    if len(eggnog_ids) > 1:
                        uniprot_acs_w_eggnog_annot[uniprot_ac]
                        uniprot_acs_w_eggnog_annot_from_emapper[uniprot_ac]
                    for raw_eggnog_id in eggnog_ids:
                        if len(raw_eggnog_id) > 0:
                            og_parts = raw_eggnog_id.split('@')
                            if len(og_parts) > 1 and (og_parts[0].startswith('KOG') or og_parts[0].startswith('COG')):
                                eggnog_id = og_parts[0]
                            elif len(og_parts) > 1 and not og_parts[0].startswith('KOG'):
                                eggnog_id = 'ENOG41' + og_parts[0]
                            else:
                                eggnog_id = og_parts[0]
                            for rxn_relation in uniprot2rxn[uniprot_ac]:
                                eggnog_rxn_mapping.append([eggnog_id, uniprot_ac] + rxn_relation)
                        
    
    ## Print some stats on the mapping work:
    print("Mapping Stats:")
    print("Number of UniProt accession numbers harvested from MetaCyc: ", len(list(uniprot2rxn.keys())))
    print("Number of UniProt accessions with EggNOG annotation: ", len(list(uniprot_acs_w_eggnog_annot.keys())))
    print("   Number of UniProt accessions with EggNOG annotation from tab-delimited file: ", len(list(uniprot_acs_w_eggnog_annot_from_tab.keys())))
    print("   Number of UniProt accessions with EggNOG annotation from emapper output: ", len(list(uniprot_acs_w_eggnog_annot_from_emapper.keys())))
        
    return eggnog_rxn_mapping


## print out MetaCyc pwy report:
def print_metacyc_pwy_report(metaKB,output_file):
    pwys = get_frame_all_children(get_frame(metaKB, 'Pathways'), frame_types='instance')
    with open(output_file,'w') as output_fh:
        for pwy in pwys:
            if 'ENGINEERED?' not in pwy.slots:
                if 'KEY-NON-REACTIONS' in pwy.slots:
                    key_non_reactions = pwy.get_slot_values('KEY-NON-REACTIONS')[0].strip('()').split(' ')
                else:
                    key_non_reactions = ''
                print('|'.join((pwy.frame_id,
                                pwy.get_slot_values('COMMON-NAME')[0],
                                ','.join([taxon.frame_id for taxon in pwy.get_slot_values('TAXONOMIC-RANGE')]),
                                ','.join([rxn.frame_id for rxn in pwy.get_slot_values('REACTION-LIST')]),
                                ','.join([rxn.frame_id for rxn in pwy.get_slot_values('KEY-REACTIONS')]),
                                ','.join(key_non_reactions)
                )),
                      file=output_fh)
