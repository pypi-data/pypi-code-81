from enrichwrap import add_outstr


def get_sas_outval(valToFind, enrichtarget, enrichment_returned_data_dict):
    marchinglist = []
    data_level = {}
    for a_string in valToFind.split('/'):
        if a_string != '':
            marchinglist.append(a_string)
    if marchinglist[0] not in enrichment_returned_data_dict.get(enrichtarget).keys() and \
            'data' in enrichment_returned_data_dict.get(enrichtarget).keys():
        # Go down into Data subkey
        data_level = enrichment_returned_data_dict.get(enrichtarget).get('data')
        if type(data_level) is list and len(data_level) == 1:
            data_level = data_level[0]
        if marchinglist[0] not in data_level.keys() and 'results' in data_level.keys():
            data_level = data_level.get('results')
        for this_item in marchinglist:
            if this_item.find('[') > 0 and this_item.find(']') > 0:
                main_part = this_item[0:this_item.find('[')]
                list_index = int(this_item[this_item.find('[')+1:this_item.rfind(']')])
                if type(data_level) is dict and main_part in data_level.keys() and type(data_level.get(main_part)) is list and len(data_level.get(main_part)) > list_index and this_item != marchinglist[len(marchinglist)-1]:
                    data_level = data_level.get(main_part)[list_index]
                    continue

                if type(data_level) is list and this_item == marchinglist[len(marchinglist)-1]:
                    if list_index+1 < len(data_level):
                        return data_level[list_index]
                    else:
                        raise Exception('not found')

                if main_part in data_level.keys():
                    data_list = data_level.get(main_part)
                    if len(data_list) > list_index:
                        return data_list[list_index]
                    else:
                        raise Exception('not found')
                else:
                    raise Exception('not found')
            if type(data_level) is list and this_item == marchinglist[len(marchinglist)-1]:
                return data_level
            if this_item not in data_level.keys():
                # for the case of bokumaa, the data can come back without the hierarchy the xml has
                if marchinglist[len(marchinglist)-1] in data_level.keys():
                    return data_level.get(marchinglist[len(marchinglist)-1])
                raise Exception('not found')
            data_level = data_level.get(this_item)
    return data_level


def convert_to_sas(enrichment_returned_data_dict, mappings):
    out_dictionary = {}
    for enrich in enrichment_returned_data_dict.keys():
        if (enrich+'_out') in mappings.keys():
            sas_mappings = mappings.get(enrich + "_out").copy()
            add_outstr('-------------------------------------------------------------------')
            add_outstr('For enrichment %s' % enrich)
            add_outstr('sas_mappings: %s' % sas_mappings)
            add_outstr('enriched_data %s' % enrichment_returned_data_dict.get(enrich))
            print(enrichment_returned_data_dict.get(enrich))
            for out_sas_key in sas_mappings.keys():
                try:
                    val2 = get_sas_outval(sas_mappings.get(out_sas_key), enrich, enrichment_returned_data_dict)
                    if isinstance(val2, bool):
                        val2 = int(val2 is True)
                    out_dictionary[out_sas_key] = val2
                except:
                    handleOrIgnoreError(out_sas_key, False)

    return out_dictionary


def handleOrIgnoreError(out_sas_key, handle=True):
    if handle:
        add_outstr('value not found for %s' % out_sas_key)
