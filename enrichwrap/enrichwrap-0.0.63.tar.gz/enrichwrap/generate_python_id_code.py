import os

from enrichwrap import enrich, add_mapping

dotted_sep = '   # ............................................................................................................'
dashed_sep = '   # ------------------------------------------------------------------------------------------------------------'

def get_return_line(extra, sas_data):
    val = ['   return ']
    if extra is not None:
        val.append(extra)
    for key in sas_data.keys():
        if len(val) > 0:
            val.append(',')
        val.append(key)
    return ''.join(val)


def get_output_line(extra, sas_data):
    val = ["   'Output:"]
    if extra is not None:
        val.append(extra)
    for key in sas_data.keys():
        if len(val) > 0:
            val.append(',')
        val.append(key)
    val.append("'")
    return ''.join(val)


def get_starter_body(tool, http_url=None, http_port=None, vendor_required_data_in=None, targets_in=None, mappings_in=None, mappings_out=None):

    vendor_required_data = None
    if vendor_required_data_in is not None:
        vendor_required_data = vendor_required_data_in

    content = ["", dashed_sep,
               "# TODO: Either import the decision 'variables-biocatch' or complete the subsequent TODO items",
               dashed_sep, "", dotted_sep, "   #    Specify the data to use for the enrichment", dotted_sep]

    if vendor_required_data is not None:
        content.append("   vendor_required_data = '" + vendor_required_data_in + "'")
    else:
        content.append("   data = []")
        content.append("   data.append('{\"_1_app_account_balance\": 23696')")
        content.append("   data.append(' \"_1_app_account_holder_fullnm\": \"Kennith\"')")
        content.append("   data.append(' \"_1_app_account_num\": \"19204353938236134\"}')")
        content.append("   vendor_required_data = ','.join(data)")
    content.append("")

    content.append(dotted_sep)
    content.append("   #    Specify the target machine on which the third party enrichment services are running")
    content.append(dotted_sep)
    if http_url is not None:
        content.append("   targets = enrichwrap.set_default_targets('" + http_url + "', '" + http_port + "')")
    else:
        content.append("   targets = enrichwrap.set_default_targets('10.44.16.24', '8200')")

    if targets_in is not None:
        content.append("   targets = enrichwrap.add_or_update_target('" + tool + "',")
        content.append("             " + str(targets_in[tool]) + ")")
    content.append("")

    content.append(dotted_sep)
    content.append("   #     Use the default (provided) mappings")
    content.append("   #        - from vendor_required_data to the third party enrichment")
    content.append("   #        - from the third party enrichment to the variables that we can export from this node")
    content.append(dotted_sep)
    if mappings_in is not None and mappings_out is not None:
        content.append("   to_map = " + str(mappings_in))
        content.append("   from_map = " + str(mappings_out))
        content.append("   mappings = enrichwrap.add_mapping(to_map, from_map, '" + tool + "', False)")
    else:
        content.append("   mappings = None")
    content.append("")

    content.append("   val = enrichwrap.enrich('" + tool + "', vendor_required_data, targets, mappings)")
    content.append("   sas_data = val['sas_data']")
    content.append("   vendor_response = val['vendor_response']")
    content.append("")
    content.append(dotted_sep)
    content.append("   # TODO: Go to the Variables tab, and ensure that sas_data_json and success_or_failure_rc are set to Character")
    content.append(dotted_sep)
    content.append("   sas_data_json = str(sas_data)")
    content.append("")
    content.append("   # Comes back as success or failure")
    content.append("   success_or_failure_rc = vendor_response['" + tool + "']['result']")
    return '\n'.join(content)

def get_variables(sas_data):
    content = []
    bools = []
    ints = []
    strings = []
    # Find the booleans
    for key in sas_data.keys():
        val = sas_data[key]
        if isinstance(val, bool):
            bools.append("   " + key + " = (sas_data.get('" + key + "', False) is True)")

    # Find the integers
    for key in sas_data.keys():
        val = sas_data[key]
        if isinstance(val, bool) == False and isinstance(val, int):
            ints.append("   " + key + " = sas_data.get('" + key + "', 0)")

    # Find the strings
    for key in sas_data.keys():
        val = sas_data[key]
        if isinstance(val, str):
            strings.append("   " + key + " = sas_data.get('" + key + "', '')")

    if len(bools) > 0:
        content.append(dotted_sep)
        content.append('   # TODO: Go to the Variables tab, and ensure the following are mapping to Boolean')
        content.append(dotted_sep)
        content.append('   # Booleans')
        content.append('\n'.join(bools))
        content.append('')

    if len(ints) > 0:
        content.append(dotted_sep)
        content.append('   # TODO: Go to the Variables tab, and ensure the following are mapping to Integer')
        content.append(dotted_sep)
        content.append('\n'.join(ints))
        content.append('')

    if len(strings) > 0:
        content.append(dotted_sep)
        content.append('   # TODO: Go to the Variables tab, and ensure the following are mapping to Strings')
        content.append(dotted_sep)
        content.append('\n'.join(strings))
        content.append('')

    return '\n'.join(content)


def gen_python_structure(tool, mappings, vendor_required_data=None, targets=None, mappings_in=None, mappings_out=None, write_to=None):
    if write_to is not None and os.path.isdir(write_to):
        IDFiles = write_to + os.path.sep
    else:
        starting_dir = os.path.dirname(__file__)
        IDFiles = starting_dir + os.path.sep + '..' + os.path.sep + 'ID_modules' + os.path.sep + 'python' + os.path.sep

    print('Content for structure will go here [%s]' % IDFiles)
    #list_samples = glob.glob(IDFiles + '*.*')

    bench = None
    filename = IDFiles + 'bench_' + tool + '.txt'
    if os.path.isfile(filename):
        bench_file = open(filename, 'r')
        bench = bench_file.read()
        bench_file.close()

    if mappings is not None:
        outgoing_data = enrich(tool, vendor_required_data, targets, mappings)
    else:
        created_mappings = add_mapping(mappings_in, mappings_out, tool, False)
        outgoing_data = enrich(tool, vendor_required_data, targets, created_mappings)

    sas_data = outgoing_data['sas_data']
    extra = 'success_or_failure_rc,sas_data_json'

    id_content = ["import enrichwrap",
                  '',
                  "''' List all output parameters as comma-separated values in the \"Output:\" docString. Do not specify \"None\" if there is no output parameter. '''",
                  "def execute ():",
                  get_output_line(extra, sas_data),
                  get_starter_body(tool, "10.44.16.24", "8200", vendor_required_data, targets, mappings_in, mappings_out),
                  '',
                  get_variables(sas_data),
                  get_return_line(extra, sas_data),
                  '']

    if bench is None:
        bench = open(filename, 'w')
        strcontent = '\n'.join(id_content)
        bench.write(strcontent)
        bench.close()
    elif bench != id_content:
        compare_file = open(IDFiles + 'compare_' + tool + '.txt', 'w')
        strcontent = '\n'.join(id_content)
        compare_file.write(strcontent)
        compare_file.close()

    return bench, '\n'.join(id_content)


