import json
import os
import xml.dom.minidom

mapping_common_to_SAS = {}


def get_mappings_in_out(
        in_enrichname='biocatch_getscore', in_file_name='biocatch_getscore_payload.xml', in_subtype='getScore',
        out_enrichname='biocatch_out', out_file_name='biocatch_to_sas.xml', out_mapperId='biocatchRespToOde',
        basedir=None):

    if basedir is None:
        basedir = os.path.dirname(__file__) + os.path.sep + 'xml' + os.path.sep

    if in_subtype not in get_mapping(in_file_name, basedir):
        print('stop here!')
    mapping_in = get_mapping(in_file_name, basedir)[in_subtype]

    if out_mapperId not in read_to_sas_mappings(out_file_name):
        print('stop there')
    mapping_out = read_to_sas_mappings(out_file_name)[out_mapperId]

    return {in_enrichname: mapping_in, out_enrichname: mapping_out}


def get_subtype(is_common_mapping, elem):
    sub_type = 'payload'
    if not is_common_mapping:
        attr = ''
        node_i_am_on = elem
        while node_i_am_on.parentNode != '' and attr != 'message':
            attr = node_i_am_on.parentNode.tagName
            node_i_am_on = node_i_am_on.parentNode
        sub_type = node_i_am_on.getAttribute('subType')
    return sub_type


def get_mapper_id(is_common_mapping, elem):
    sub_type = ''
    if not is_common_mapping:
        attr = ''
        node_i_am_on = elem
        while node_i_am_on.parentNode != '' and attr != 'message':
            attr = node_i_am_on.parentNode.tagName
            node_i_am_on = node_i_am_on.parentNode
        sub_type = node_i_am_on.getAttribute('mapperId')
    return sub_type


def read_to_sas_mappings(infile, basedir=None):
    if basedir is None:
        basedir = os.path.dirname(__file__) + os.path.sep + 'xml' + os.path.sep

    source_to_target = {}
    dom_tree = xml.dom.minidom.parse(basedir + os.path.sep + infile)
    source_fields = dom_tree.documentElement.getElementsByTagName('srcField')
    previous_check_for_array0 = ''
    previous_target = ''
    for elem in source_fields:
        mapper_id = get_mapper_id(False, elem)
        if mapper_id not in source_to_target.keys():
            source_to_target[mapper_id] = {}

        source_field = elem.getAttribute('name')
        target_field = elem.parentNode.getAttribute('name')
        if target_field[0:1] == '/':
            target_field = target_field[1:]

        source_to_target[mapper_id][target_field] = source_field

        if source_field.find('[') > 0 and source_field.find(']') > 0:
            source_up_to_bracket = source_field[0: source_field.find('[')]
            previous_is_missing_bracket = previous_check_for_array0.find('[') < 0
            has_prev_str = source_field.find(previous_check_for_array0) >= 0
            zeroth_element = has_prev_str and source_field[source_field.find(previous_check_for_array0) + len(previous_check_for_array0)] == '['
            if previous_is_missing_bracket:
                if has_prev_str and zeroth_element:
                    source_to_target[mapper_id][previous_target] = previous_check_for_array0 + '[0]'
                elif previous_check_for_array0.startswith(source_up_to_bracket):
                    if previous_check_for_array0[previous_check_for_array0.rindex('/')+1] == source_field[source_field.rindex('/')+1]:
                        endbit = previous_check_for_array0[len(source_up_to_bracket):]
                        newval = source_up_to_bracket + '[0]' + endbit
                        source_to_target[mapper_id][previous_target] = newval

        previous_check_for_array0 = source_field
        previous_target = target_field

    return source_to_target


def read_default_mappings(xmldir, infile, isCommonMapping):
    global mapping_common_to_SAS

    if xmldir is None:
        xmldir = os.path.dirname(__file__) + os.path.sep + 'xml' + os.path.sep

    source_to_target = {}
    dom_tree = xml.dom.minidom.parse(xmldir + os.path.sep + infile)
    source_fields = dom_tree.documentElement.getElementsByTagName('srcField')
    for elem in source_fields:
        # Get subType for context I am in
        sub_type = get_subtype(isCommonMapping, elem)
        if sub_type not in source_to_target.keys():
            source_to_target[sub_type] = {}

        source_field = elem.getAttribute('name')
        if source_field[0:1] == '/':
            source_field = source_field[1:]
        target_field = elem.parentNode.getAttribute('name')
        if target_field[0:1] == '/':
            target_field = target_field[1:]
        if not isCommonMapping:
            if source_field in mapping_common_to_SAS.keys():
                source_field = mapping_common_to_SAS.get(source_field)
            else:
                if source_field.find('/') > 0:
                    source_field = source_field[source_field.rindex('/') + 1:]
                    if source_field in mapping_common_to_SAS.keys():
                        source_field = mapping_common_to_SAS.get(source_field)

        if isCommonMapping:
            source_to_target[sub_type][source_field] = target_field
        else:
            source_to_target[sub_type][target_field] = source_field

    return source_to_target


def get_mapping (which_file, xmldir=None, include_sas=False):
    global mapping_common_to_SAS

    if len(mapping_common_to_SAS.keys()) == 0:
        mapping_common_to_SAS = read_default_mappings(xmldir, 'common_to_sas.xml', True)

    return read_default_mappings(xmldir, which_file, include_sas)


def get_payfoneverify_mappings():
    return get_mappings_in_out('payfoneverify', 'payfone_payload.xml', 'verify',
                               'payfoneverify_out', 'payfone_to_sas.xml', 'payfoneverifyRespToOde')


def get_payfonetrust_mappings():
    return get_mappings_in_out('payfonetrust', 'payfone_payload.xml', 'trust',
                               'payfonetrust_out', 'payfone_to_sas.xml', 'payfonetrustRespToOde')


def get_bokugpir_mappings():
    return get_mappings_in_out('bokugpir', 'boku_gpir_payload.xml', 'getPhoneIdentificationResult',
                               'bokugpir_out', 'boku_gpir_to_sas.xml', 'bokugpirRespToOde')


def get_bokumaa_mappings():
    return get_mappings_in_out('bokumaa', 'boku_maa_payload.xml', 'matchAndAttributes',
                               'bokumaa_out', 'boku_maa_to_sas.xml', 'bokumaaRespToOde')


def get_socure_mappings():
    return get_mappings_in_out('socure', 'socure_payload.xml', 'payload',
                               'socure_out', 'socure_to_sas.xml', 'socureRespToOde')


def get_datavisor_mappings():
    return get_mappings_in_out('datavisor', 'datavisor_payload.xml', 'payload',
                               'datavisor_out', 'datavisor_to_sas.xml', 'datavisorRespToOde')


def get_giact_mappings():
    return get_mappings_in_out('giact', 'giact_payload.xml', 'payload',
                               'giact_out', 'giact_to_sas.xml', 'giactRespToOde')


def get_iovation_mappings():
    return get_mappings_in_out('iovation', 'iovation_payload.xml', 'payload',
                               'iovation_out', 'iovation_to_sas.xml', 'iovationRespToOde')


def get_biocatch_mappings():
    return get_mappings_in_out('biocatch', 'biocatch_getscore_payload.xml', 'getScore',
                               'biocatch_out', 'biocatch_to_sas.xml', 'biocatchRespToOde')


def get_mapping_choices():
    all = get_all_mappings()
    vals = ''
    for key in all.keys():
        if str(key).endswith('_out'):
            continue
        if len(vals) > 0:
            vals += ', '
        vals += key
    return vals


def add_mapping_in_str(str_map_to, str_map_from, enrichment_name, include_default=True):
    map_to_enrichment = json.loads(str_map_to)
    map_from_enrichment = json.loads(str_map_from)
    return add_mapping(map_to_enrichment, map_from_enrichment, enrichment_name, include_default)

# to_map = {'UniqueId': 'uniqueId', 'username': 'user_name'}
# from_map = {'score': '_a_score', 'confidence': '_a_confidence', 'reference': '_a_referenceId'}
# mapping = add_mapping(to_map, from_map, 'custom', False)
def add_mapping(map_to_enrichment, map_from_enrichment, enrichment_name, include_default=True):
    retmap = {}
    if include_default:
        retmap = get_all_mappings()

    retmap[enrichment_name] = map_to_enrichment
    retmap[enrichment_name + '_out'] = map_from_enrichment

    return retmap


def get_all_mappings():
    global mapping_common_to_SAS

    mapping_payfone_verify = get_payfoneverify_mappings()
    mapping_payfone_trust = get_payfonetrust_mappings()
    mapping_boku_gpir = get_bokugpir_mappings()
    mapping_boku_maa = get_bokumaa_mappings()
    mapping_socure = get_socure_mappings()
    mapping_datavisor = get_datavisor_mappings()
    mapping_giact = get_giact_mappings()
    mapping_iovation = get_iovation_mappings()
    mapping_biocatch = get_biocatch_mappings()

    retmap = {}
    retmap.update(mapping_payfone_verify)
    retmap.update(mapping_payfone_trust)
    retmap.update(mapping_boku_gpir)
    retmap.update(mapping_boku_maa)
    retmap.update(mapping_socure)
    retmap.update(mapping_datavisor)
    retmap.update(mapping_giact)
    retmap.update(mapping_iovation)
    retmap.update(mapping_biocatch)
    return retmap


if __name__ == '__main__':
    print(get_mapping_choices())
