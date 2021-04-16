import os

from enrichwrap import enrich, add_mapping


def get_variables_for_execute(sas_data, ID_variables, skip_variables=False):
    retval = []
    if skip_variables:
        return retval

    for key in sas_data.keys():
        isnum = True
        inner = ['                  in_out ']
        val = sas_data[key]
        if isinstance(val, float) or isinstance(val, int):
            inner.append('double ')
        elif isinstance(val, str):
            inner.append('varchar ')
            isnum = False
        else:
            # Tackle else other types
            inner.append('varchar ')
            print('what to print')
        inner.append(key)
        inner.append(',')
        retval.append(''.join(inner))
        if isnum:
            strval = '{"name": "' + key + '", "dataType": "decimal", "direction": "output"},'
        else:
            strval = '{"name": "' + key + '", "dataType": "string", "direction": "output"},'
        ID_variables.append(strval)

    return retval

def is_numeric(val):
    if isinstance(val, float) or isinstance(val, int):
        return True
    return False

def get_inner_python_output_line(sas_data, skip_variables=False):
    retval = []
    if len(sas_data.keys()) == 0:
        return ''.join(retval)

    # Bail out if there are too many keys, as it will blow out the 32767 character limit for ID DS2
    if len(sas_data.keys()) > 50 or skip_variables:
        retval.append('             rc = py.appendSrcLine(\'   "Output: success_rc,sas_data_json')
    else:
        for key in sas_data.keys():
            if len(retval) == 0:
                retval.append('             rc = py.appendSrcLine(\'   "Output: success_rc,sas_data_json,')
            else:
                retval.append(',')
            retval.append(key)

    retval.append('" \');')
    return ''.join(retval)


def get_assignment_from_sasdata(sas_data, skip_variables=False):
    # Bail out if there are too many keys, as it will blow out the 32767 character limit for ID DS2
    if skip_variables or len(sas_data.keys()) == 0 or len(sas_data.keys()) > 50:
        return ''

    retval = ['             rc = py.appendSrcLine(\'   if len(vendor_response.keys()) > 0:\');']
    for key in sas_data.keys():
        val = sas_data[key]
        inner = ['             rc = py.appendSrcLine(\'      ']
        inner.append(key)
        inner.append(' = ')
        inner.append('sas_data.get("')
        inner.append(key)
        inner.append('", ')
        if is_numeric(val):
            inner.append('0')
        else:
            inner.append('""')
        inner.append(')\');')
        retval.append(''.join(inner))

    return retval

def get_predefined_enrichment():
    return ['biocatch', 'giact', 'socure', 'payfoneverify', 'payfonetrust', 'bokugpir', 'bokumaa', 'datavisor',
            'giact', 'iovation']

def get_mappings_and_call_enrich(tool, mapping_in):
    retval = ''
    if tool in get_predefined_enrichment():
        str1 = '             rc = py.appendSrcLine(\'   mappings = enrichwrap.get_' + tool + '_mappings()\');'
        str2 = '             rc = py.appendSrcLine(\'   val = enrichwrap.enrich("' + tool + '", vendor_required_data, targets, mappings)\');'
        retval = '\n'.join([str1, str2])
    elif mapping_in is not None:
        inner =     ['             rc = py.appendSrcLine(\'   if mapping_in is not None:\');']
        inner.append('             rc = py.appendSrcLine(\'      mappings = enrichwrap.add_mapping_in_str(mapping_in, mapping_out, custom_target, False)\');')
        inner.append('             rc = py.appendSrcLine(\'   else:\');')
        inner.append('             rc = py.appendSrcLine(\'      mappings = None\');')
        inner.append('             rc = py.appendSrcLine(\'   val = enrichwrap.enrich(custom_target, vendor_required_data, targets, mappings)\');')
        retval = '\n'.join(inner)
    else:
        str1 = '             rc = py.appendSrcLine(\'   mappings = None\');'
        str2 = '             rc = py.appendSrcLine(\'   val = enrichwrap.enrich(None, vendor_required_data, targets, mappings)\');'
        retval = '\n'.join([str1, str2])

    return retval

def get_check_if_keys_is_populated(tool):
    if tool in get_predefined_enrichment():
        str1 = '             rc = py.appendSrcLine(\'   if "' + tool + '" in vendor_response.keys():\');'
        str2 = '             rc = py.appendSrcLine(\'      success_rc = vendor_response["' + tool + '"]["result"]\');'
    else:
        str1 = '             rc = py.appendSrcLine(\'   if len(vendor_response.keys()) == 0:\');'
        str2 = '             rc = py.appendSrcLine(\'      success_rc = "undetermined"\');'

    return '\n'.join([str1, str2])

def get_return_line(sas_data, skip_variables=False):
    # Bail out if there are too many keys, as it will blow out the 32767 character limit for ID DS2
    if skip_variables or len(sas_data.keys()) > 50:
        return '             rc = py.appendSrcLine(\'   return success_rc,sas_data_json\');'

    retval = ['             rc = py.appendSrcLine(\'   return success_rc,sas_data_json,']
    inner = []
    for key in sas_data.keys():
        if len(inner) > 0:
            inner.append(',')
        inner.append(key)
    retval.append(''.join(inner))
    retval.append('\');')
    return ''.join(retval)

def get_py_str(key, matching_val):
    inner = ['       ']
    inner.append(key)
    inner.append(' = py.get')
    if is_numeric(matching_val):
        inner.append('Double')
    else:
        inner.append('String')
    inner.append('(\'')
    inner.append(key)
    inner.append('\');')
    return ''.join(inner)

def get_space_num(sas_data):
    maxstrlen = 0
    for key in sas_data.keys():
        thislen = len(get_py_str(key, sas_data[key]))
        maxstrlen = max(thislen, maxstrlen)
    maxstrlen += 10
    return maxstrlen

def get_end_variables(sas_data, skip_variables=False):
    retval = []
    maxstrlen = get_space_num(sas_data)

    # Bail out if there are too many keys, as it will blow out the 32767 character limit for ID DS2
    if not skip_variables and len(sas_data.keys()) <= 50:
        for key in sas_data.keys():
            str1 = get_py_str(key, sas_data[key])
            spacenum = maxstrlen - len(str1)
            inner = [str1]
            for _ in range(spacenum):
                inner.append(' ')

            inner.append('if rc then return;')
            retval.append(''.join(inner))

    str2 = '       success_rc = py.getString(\'success_rc\');'
    str_outcome = [str2]
    spacenum = maxstrlen - len(str2)
    for _ in range(spacenum):
        str_outcome.append(' ')
    str_outcome.append('if rc then return;')
    retval.append(''.join(str_outcome))

    str3 = '       sas_data_json = py.getString(\'sas_data_json\');'
    str_sas_data_json = [str3]
    spacenum = maxstrlen - len(str3)
    for _ in range(spacenum):
        str_sas_data_json.append(' ')
    str_sas_data_json.append('if rc then return;')
    retval.append(''.join(str_sas_data_json))

    return retval

def gen_ds2_structure_basic(tool, mappings, skip_variables=False):
    return gen_ds2_structure(tool, mappings, None, None, None, None, None, skip_variables, False)

def gen_ds2_structure(tool, mappings, vendor_required_data=None, targets=None, mappings_in=None, mappings_out=None, write_to=None, skip_variables=False, custom=False):
    if write_to is not None and os.path.isdir(write_to):
        IDFiles = write_to + os.path.sep
    else:
        starting_dir = os.path.dirname(__file__)
        IDFiles = starting_dir + os.path.sep + '..' + os.path.sep + 'ID_modules' + os.path.sep + 'ds2' + os.path.sep

    print('Content for structure will go here [%s]' % IDFiles)
    #list_samples = glob.glob(IDFiles + '*.*')

    bench = None
    filename = IDFiles + 'bench_' + tool + '.txt'
    if os.path.isfile(filename):
        bench_file = open(filename, 'r')
        bench = bench_file.read()
        bench_file.close()

    if mappings is not None:
        outgoing_data = enrich(tool, vendor_required_data, None, mappings)
    else:
        created_mappings = add_mapping(mappings_in, mappings_out, tool, False)
        outgoing_data = enrich(tool, vendor_required_data, targets, created_mappings)

    sas_data = outgoing_data['sas_data']

    id_content = ['package "${PACKAGE_NAME}" /inline;',
                  '   dcl package pymas py;',
                  '   dcl double revision;',
                  '   method execute(',
                  '                  varchar(32767) url,',
                  '                  varchar port,']
    if custom:
        id_content.append('                  varchar custom_target,')
        id_content.append('                  varchar(32767) vendor_data,')
        id_content.append('                  varchar(32767) custom_body,')
        id_content.append('                  varchar(32767) mapping_in,')
        id_content.append('                  varchar(32767) mapping_out,')

    id_content.append('                  varchar(32767) pycode,')
    id_content.append('                  in_out varchar success_rc,')
    id_content.append('                  in_out double rc,')

    ID_variables = ['{"name": "url", "dataType": "string", "direction": "input", "length": 32767},']
    ID_variables.append('{"name": "port", "dataType": "string", "direction": "input"},')
    ID_variables.append('{"name": "pycode", "dataType": "string", "direction": "input", "length": 32767},')
    ID_variables.append('{"name": "success_rc", "dataType": "string", "direction": "output"},')
    ID_variables.append('{"name": "rc", "dataType": "decimal", "direction": "output"},')

    id_content.extend(get_variables_for_execute(sas_data, ID_variables, skip_variables))

    ID_variables.append('{"name": "sas_data_json", "dataType": "string", "direction": "output", "length": 32767}')
    id_content.append('                  in_out varchar(32767) sas_data_json);',)
    id_content.append('')
    id_content.append('       if null(py) then do;')
    id_content.append('          py = _new_ pymas();')
    id_content.append('          rc = py.useModule(\'enrichshim\', 1);')
    id_content.append('          if rc then do;')
    id_content.append('             rc = py.appendSrcLine(\'import enrichwrap\');')
    id_content.append('             rc = py.appendSrcLine(\'import json\');')
    id_content.append('             rc = py.appendSrcLine(\'\');')
    id_content.append('             rc = py.appendSrcLine(\'def get_steps(s):\');')
    id_content.append('             rc = py.appendSrcLine(\'   "Output: r" \');')
    id_content.append('             rc = py.appendSrcLine(\'   r = enrichwrap.get_steps(s)\');')
    id_content.append('             rc = py.appendSrcLine(\'   return str(r)\');')
    id_content.append('             rc = py.appendSrcLine(\'\');')
    id_content.append('             rc = py.appendSrcLine(\'def enrich(vendor_required_data, target_url, target_port, custom_target=None, custom_body=None, mapping_in=None, mapping_out=None):\');')
    id_content.append(get_inner_python_output_line(sas_data, skip_variables))
    id_content.append('             rc = py.appendSrcLine(\'\');')
    id_content.append('             rc = py.appendSrcLine(\'   targets = None\');')
    id_content.append('             rc = py.appendSrcLine(\'   if target_url is not None:\');')
    id_content.append('             rc = py.appendSrcLine(\'      targets = enrichwrap.set_default_targets(target_url, target_port)\');')
    id_content.append('             rc = py.appendSrcLine(\'\');')
    id_content.append('             rc = py.appendSrcLine(\'   if custom_target is not None and custom_body is not None:\');')
    id_content.append('             rc = py.appendSrcLine(\'      targets = enrichwrap.add_target_with_map_str(custom_target, custom_body)\');')
    id_content.append('             rc = py.appendSrcLine(\'\');')

    if custom:
        id_content.append('             rc = py.appendSrcLine(\'   success_rc = "success"\');')
    else:
        id_content.append('             rc = py.appendSrcLine(\'   success_rc = None\');')

    id_content.append(get_mappings_and_call_enrich(tool, mappings_in))
    id_content.append('             rc = py.appendSrcLine(\'   sas_data = val["sas_data"]\');')
    id_content.append('             rc = py.appendSrcLine(\'   vendor_response = val["vendor_response"]\');')
    id_content.append(get_check_if_keys_is_populated(tool))
    id_content.extend(get_assignment_from_sasdata(sas_data, skip_variables))
    id_content.append('             rc = py.appendSrcLine(\'   sas_data_json = json.dumps(sas_data)\');')
    id_content.append(get_return_line(sas_data, skip_variables))
    id_content.append('             pycode = py.getSource();')
    id_content.append('             revision = py.publish(pycode, \'enrichshim\');')
    id_content.append('             if revision lt 1 then do;')
    id_content.append('                rc = -1;')
    id_content.append('                success_rc = \'problem in usemodule\';')
    id_content.append('                return;')
    id_content.append('             end; /* End of if revision lt 1 */')
    id_content.append('          end; /* End of if useModule failed */')
    id_content.append('')
    id_content.append('          rc = py.useMethod(\'enrich\');')
    id_content.append('          if rc then return;')
    id_content.append('       end; /* end of if null(py) */')
    id_content.append('')
    if custom:
        id_content.append('       py.setString(\'vendor_required_data\', vendor_data);')
        id_content.append('       py.setString(\'target_url\', url);')
        id_content.append('       py.setString(\'target_port\', port);')
        id_content.append('       py.setString(\'custom_target\', custom_target);')
        id_content.append('       py.setString(\'custom_body\', custom_body);')
        id_content.append('       py.setString(\'mapping_in\', mapping_in);')
        id_content.append('       py.setString(\'mapping_out\', mapping_out);')
    else:
        id_content.append('       py.setString(\'vendor_required_data\', \'{"UniqueId": 23456, "username": "John Q Public"}\');')
        id_content.append('       py.setString(\'target_url\', \'10.44.16.24\');')
        if tool not in get_predefined_enrichment():
            id_content.append('       py.setString(\'target_port\', \'8400\');')
        else:
            id_content.append('       py.setString(\'target_port\', \'8200\');')
            id_content.append('       py.setString(\'custom_target\', \'' + tool + '\');')
        if tool not in get_predefined_enrichment():
            id_content.append('       py.setString(\'custom_body\', \'{"url": "http://10.44.16.24:8400/custom_site/items", "mechanism": "GET", "params": {"name": "John", "age": 22}}\');')
            id_content.append('       py.setString(\'mapping_in\', \'{"UniqueId": "uniqueId", "username": "user_name"}\');')
            id_content.append('       py.setString(\'mapping_out\', \'{"_a_score": "score", "_a_confidence": "confidence", "_a_reference": "reference"}\');')

    id_content.append('       rc = py.execute();')
    id_content.extend(get_end_variables(sas_data, skip_variables))
    id_content.append('   end;')
    id_content.append('endpackage;')
    id_content.append('')

    if bench is None:
        bench_file = open(filename, 'w')
        bench = '\n'.join(id_content)
        bench_file.write(bench)
        bench_file.close()
    elif bench != id_content:
        compare_file = open(IDFiles + 'compare_' + tool + '.txt', 'w')
        strcontent = '\n'.join(id_content)
        compare_file.write(strcontent)
        compare_file.close()

    flat_contents = '\n'.join(id_content)
    flat_contents = flat_contents.replace('"', '\\"')
    flat_contents = flat_contents.replace('\n', '\\n')
    flat_full = ['{']
    flat_full.append('    "contentType": "DS2",')
    flat_full.append('    "staticContent": "' + flat_contents + '",')
    flat_full.append('    "nodeTypeSignatureTerms": [')
    for line in ID_variables:
        flat_full.append('        ' + line)
    flat_full.append('    ]')
    flat_full.append('}')

    flat_files = IDFiles + os.path.sep + 'flat' + os.path.sep
    flat_file = open(flat_files + 'flat_' + tool + '.txt', 'w')
    flat_file.write('\n'.join(flat_full))
    flat_file.close()

    return bench, '\n'.join(id_content), flat_contents


