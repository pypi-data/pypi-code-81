from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from camelot_frs.pgdb_loader import load_pgdb
from camelot_frs.camelot_frs import get_kb, get_frame, get_frames, frame_subsumes_or_equal_p
import reactionary.reactionary_lib
from reactionary.reactionary_lib import load_eggnog_rxn_mapping_file, find_og_in_annot_line, map_filter_taxon2domain, eggnog_annot2rxns, parse_annot_line
from reactionary.warpath import predict_metacyc_pathways
from ete3 import NCBITaxa
from Bio import Entrez
from collections import defaultdict
from pathlib import Path
import sys, gzip, os, urllib.request, subprocess, textwrap

eggnog_mapper_OG_field = 18
rxn_field              = 22

## Reaction annotation data file path:
#ref_db_old_url = "https://ndownloader.figshare.com/files/25440413?private_link=9f94fa9056cdbb4f0b83"


def fetch_ref_db(download_url, local_db_path):

    ## First, fetch the compressed SQL database:
    print("Fetching the compressed database...", file=sys.stderr)
    local_filename, headers = urllib.request.urlretrieve(download_url)    
    print("... done!", file=sys.stderr)
    
    ## Then, attempt to decompress the SQL and rebuild the SQLite3 DB:
    print("Decompressing and rebuilding the compressed database...", file=sys.stderr)
    output = subprocess.check_output('gunzip < ' + local_filename + ' | sqlite3 ' + local_db_path, shell=True)
    print("... done!", file=sys.stderr)


def add_refs2ref_db(new_refs_path,
                    nog2rxn_conn):
    new_refs = []
    cursor = nog2rxn_conn.cursor()
    with open(new_refs_path) as refs_fh:
        for line in refs_fh:
            entry = line.strip().split("\t")
            cursor.execute("INSERT INTO nog2rxn VALUES (?, '', '', ?, '', 'USER', '', '')", entry)
    nog2rxn_conn.commit()

def augment_eggnog_annotation(eggnog_annot_file,
                              annot_taxon2tuple,
                              ncbi_taxon,
                              nog2rxn_conn,
                              output_dir,
                              max_rxns=10,
                              enclosing_rank='superkingdom'):
    
    line_num = 0
    rxn2annot = defaultdict(list)
    max_rxn_prot_annots = []
    #eggnog2rxns  = load_eggnog_rxn_mapping_file(nog2rxn_file)

    ## Print augmented EggNOG-Mapper output file:
    with open(output_dir + '/' + os.path.basename(eggnog_annot_file) + '.reactionary', "w") as aug_annot_fh:
        with open(eggnog_annot_file) as annot_fh:
            for line in annot_fh:
                line_num += 1
                reactions = []
                ##print "Line: " + str(line_num)
                if line.startswith('#query_name'):
                    print(line.strip() + '\tMetaCyc_Reaction', file=aug_annot_fh)
                elif line.startswith('#'):
                    print(line.strip(), file=aug_annot_fh)
                else:
                    fields   = line.strip().split('\t')
                    curr_annot = parse_annot_line(line)
                    (reaction_tuples,
                     mapped_rank,
                     mapped_taxon,
                     prot_id,
                     og              ) = eggnog_annot2rxns(curr_annot,
                                                           ncbi_taxon,
                                                           nog2rxn_conn,
                                                           annot_taxon2tuple,
                                                           enclosing_rank = enclosing_rank)
                    rxn_list = list(set([ rxn_tuple[3] for rxn_tuple in reaction_tuples ]))
                    if len(reaction_tuples) <= max_rxns:
                        for rxn in rxn_list:
                            rxn2annot[rxn].append([reaction_tuples, mapped_rank, mapped_taxon, prot_id, og])
                        fields.append(",".join(rxn_list))
                        print("\t".join(fields), file=aug_annot_fh)
                    else:
                        max_rxn_prot_annots.append([reaction_tuples,
                                                    mapped_rank,
                                                    mapped_taxon,
                                                    prot_id,
                                                    og])
    
    ## Print reaction report:
    print_reaction_report(output_dir, rxn2annot)
    
    ## Print annotations which have exceeded the max number of reactions predicted:
    print_multi_reaction_protein_report(output_dir, max_rxn_prot_annots)
    
    return rxn2annot


def print_reaction_report(output_dir, rxn2annot):
    with open(output_dir + "/reactions.txt", "w") as rxn_fh:
        print("# Reaction frame ID", file=rxn_fh)
        print('\t'.join(["# ",
                         "Protein ID",
                         "Link Type",
                         "NOG",
                         "Rank",
                         "Taxon ID"]),
                        file=rxn_fh)
        for rxn in rxn2annot:
            print(rxn, file=rxn_fh)
            for (reaction_tuples, mapped_rank, mapped_taxon, prot_id, og) in rxn2annot[rxn]:
                print("\t".join(["",
                                 prot_id,
                                 [ rxn_tuple[5] for rxn_tuple in reaction_tuples if rxn_tuple[3] == rxn ][0],
                                 og,
                                 mapped_rank,
                                 mapped_taxon.tax_id]),
                      file=rxn_fh)

                
def print_multi_reaction_protein_report(output_dir, max_rxn_prot_annots):
    if len(max_rxn_prot_annots) > 0:
        with open (output_dir + "/multi-reaction-proteins.txt", "w") as multi_rxn_fh:
            print('\t'.join(["# Protein ID",
                             "NOG",
                             "Rank",
                             "Taxon ID",
                             "Reactions"]),
                  file=multi_rxn_fh)
            for (reaction_tuples, mapped_rank, mapped_taxon, prot_id, og) in max_rxn_prot_annots:
                print('\t'.join([prot_id,
                                 og,
                                 mapped_rank,
                                 mapped_taxon.tax_id,
                                 ';'.join([rxn_tuple[3] for rxn_tuple in reaction_tuples])]),
                      file=multi_rxn_fh)
    


def predict_pathways(eggnog_rxn_annot_file, ncbi_taxon_tuple, output_dir):

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
    pwy_predictions = predict_metacyc_pathways(list(rxn_ids.keys()),
                                               ncbi_taxon_tuple)
    
    ## Print pathway predictions:
    #output_dir = os.path.dirname(os.path.abspath(eggnog_rxn_annot_file))
    report_file = output_dir + '/pathways.txt'
    with open(report_file, 'w') as pwy_fh:
        print('\t'.join(["# Pathway Frame ID",
                         "Pathway Name",
                         "Enzyme-Info-Content-Norm",
                         "Taxonomic Domain(s)",
                         "Present Reaction(s)",
                         "Missing Reaction(s)",
                         "All Key Reactions Present?",
                         "Key Reactions",
                         "Key Non Reactions Satisfied?",
                         "Key Non Reactions"]),
              file=pwy_fh)
        for pred in pwy_predictions:
            print('\t'.join([pred[0],
                             pred[1],
                             str("%0.3f" % pred[2]), 
                             ';'.join(pred[3]),
                             ';'.join(pred[4]),
                             ';'.join(pred[5]),
                             str(pred[6]),
                             ';'.join(pred[7]),
                             str(pred[8]),
                             ';'.join(pred[9])]),
                  file=pwy_fh)

    return (pwy_predictions, report_file)

def gen_metacyc_link(metacyc_frame):
    return 'https://metacyc.org/META/NEW-IMAGE?object=' + metacyc_frame

def gen_ncbi_tax_link(taxon_id):
    return 'https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Info&id=' + \
        str(taxon_id) + \
        '&lvl=3&lin=f&keep=1&srchmode=1&unlock'

def gen_eggnog_link(nog):
    return 'http://eggnogdb.embl.de/#/app/results?target_nogs=' + nog.split('@')[0]


def gen_sphinx_hyperlink(link, text):
    return '`' + text + ' <' + link + '>`_'

def generate_ReST_report(output_dir, rxn2annot, pwy_pred_results):

    ncbi = NCBITaxa(reactionary.reactionary_lib.taxon_db_path)
    Path(output_dir + '/report-src').mkdir(parents=True, exist_ok=True)
    
    report_file = output_dir + '/report-src/index.rst'
    
    with open(report_file, 'w') as report_fh:

        ## Print the header:
        print(textwrap.dedent("""\
        Reactionary Report
        ==================
        
        This is a report generated by Reactionary (https://bitbucket.org/tomeraltman/reactionary/).
        
        .. contents:: Table of Contents
           :backlinks: entry

        Reactions
        ---------
        """),
              file = report_fh)

        ## Generate Reaction Table:
        
        print(".. csv-table:: Predicted Reactions", file = report_fh)
        print('   :header: "Reaction ID", "Protein ID", "Link Type", "NOG", "Rank", "Taxon ID", "Taxon Name"',
              file = report_fh)
        print('   :delim: |\n', file = report_fh)
        for rxn in rxn2annot:
            rxn_link = gen_sphinx_hyperlink(gen_metacyc_link(rxn), rxn)
            for (reaction_tuples, mapped_rank, mapped_taxon, prot_id, og) in rxn2annot[rxn]:
                taxon_link = gen_sphinx_hyperlink(gen_ncbi_tax_link(mapped_taxon.tax_id), mapped_taxon.tax_id)
                
                print("   " + "|".join([ rxn_link,
                                         prot_id,
                                         [ rxn_tuple[5] for rxn_tuple in reaction_tuples if rxn_tuple[3] == rxn ][0],
                                         gen_sphinx_hyperlink(gen_eggnog_link(og),og),
                                         mapped_rank,
                                         taxon_link,
                                         mapped_taxon.scientific_name]),
                      file=report_fh)
        print("", file = report_fh)

        
        ## Print Pathways section:
        print(textwrap.dedent("""\
        Pathways
        --------
        """),
              file = report_fh)
        
        ## Generate Pathway Table:

        print('.. csv-table:: Predicted Pathways', file = report_fh)
        print('   :header: ' + ', '.join(['"Pathway Frame ID"',
                                          '"Pathway Name"',
                                          '"Enzyme-Info-Content-Norm"',
                                          '"Taxonomic Domain(s)"',
                                          '"Present Reaction(s)"',
                                          '"Missing Reaction(s)"',
                                          '"All Key Reactions Present?"',
                                          '"Key Reactions"',
                                          '"Key Non Reactions Satisfied?"',
                                          '"Key Non Reactions"']),
              file = report_fh)
        print('   :delim: |\n', file = report_fh)
        for pred in pwy_pred_results:
            pwy_link = gen_sphinx_hyperlink(gen_metacyc_link(pred[0]), pred[0])
            taxonomic_domain_list = []
            for tax_id, name in ncbi.get_taxid_translator(pred[3]).items():
                rank = ncbi.get_rank([tax_id])[tax_id]
                taxonomic_domain_list.append(gen_sphinx_hyperlink(gen_ncbi_tax_link(tax_id),
                                                                  name + ' (' + rank + ')'))
                present_rxns = '; '.join([gen_sphinx_hyperlink(gen_metacyc_link(rxn),rxn)
                                          for rxn in pred[4] ])
                missing_rxns = '; '.join([gen_sphinx_hyperlink(gen_metacyc_link(rxn),rxn)
                                          for rxn in pred[5] ])
                key_rxns     = '; '.join([gen_sphinx_hyperlink(gen_metacyc_link(rxn),rxn)
                                          for rxn in pred[7] ])
                key_non_rxns = []
                if len(pred[9]) > 0:
                    key_non_rxns = '; '.join([pred[9][0]] + \
                                             [gen_sphinx_hyperlink(gen_metacyc_link(rxn),rxn)
                                              for rxn in pred[9][1:] ])
            print("   " + "|".join([ pwy_link,
                                     pred[1],
                                     str("%0.3f" % pred[2]), 
                                     '; '.join(taxonomic_domain_list),
                                     present_rxns,
                                     missing_rxns,
                                     str(pred[6]),
                                     key_rxns,
                                     str(pred[8]),
                                     key_non_rxns if len(key_non_rxns) > 0 else '\ ']),
                  file=report_fh)
        print("", file = report_fh)


    ## Run Sphinx to generate the report:
    sphinx_conf_file = os.path.dirname(__file__)
    output = subprocess.check_output(' '.join(['sphinx-build',
                                               '-b',
                                               'html',
                                               '-c',
                                               sphinx_conf_file,
                                               output_dir + '/report-src',
                                               output_dir]),
                                     shell=True)
        
              
            
### Deprecated

def coerce_taxonid_to_metacyc_taxon_frame(taxon_id_str,
                                          metaKB,
                                          email_address):
    
    Entrez.email = email_address
    
    ## Try to find taxon in MetaCyc; if successful, return the frame:
    ## "didn't find ID in MetaCyc, searching NCBI..."
    metacyc_taxon_frame = get_frame(metaKB,
                                    'TAX-' + taxon_id_str)
    
    if metacyc_taxon_frame != None:
        return metacyc_taxon_frame
    else:
        print("Didn't find given NCBI Taxonomy DB ID in MetaCyc, attempting to coerce using NCBI Entrez...", file=sys.stderr)
        
        ## If not, try to fetch the ID from NCBI Entrez:        
        try:
            handle = Entrez.efetch(db="taxonomy",
                                   id=taxon_id_str)
        
        ## Throw if not found:
        except:
            raise ValueError("NCBI Entrez did not recognize the given Taxon ID: '" + taxon_id_str + "'", taxon_id_str)
        
        ## Parse the XML:
        taxon_record = Entrez.read(handle)
        handle.close()
    
        ## Going to assume that list of hashes in XML is in the same order as the lineage,
        ## and thus will walk backwards until we find a hit:
        taxon_record[0]['LineageEx'].reverse()
        lineage = taxon_record[0]['LineageEx']
        for taxon_dict in lineage:
            metacyc_taxon_frame = get_frame(metaKB,
                                            'TAX-' + taxon_dict['TaxId'])
            if metacyc_taxon_frame != None:
                print("Reactionary: Coerced provided NCBI Taxonomy DB ID from '" + taxon_id_str + "' to '" + taxon_dict['TaxId'] + "' (" + taxon_dict['ScientificName'] + ", rank: '" + taxon_dict['Rank'] + "')", file=sys.stderr)
                break
    
    return metacyc_taxon_frame
        


    

    

### When run as a script:
#if __name__ == "__main__":
