def construct_dict_from_dotkv(dict = {}, fields = [], value = None):
    if len(fields) <= 1:
        dict[fields[0]] = value
    else:
        dict[fields[0]] = construct_dict_from_dotkv(
            dict[fields[0]] if fields[0] in dict else {}, fields[1:], value)
        
    return dict

def construct_dotkv_from_dict(source = {}, key = '', temp_result = {}):
    for k, v in source.items():
        if type(v) == dict:
            temp_result = construct_dotkv_from_dict(v,key + '.' +k if key != '' else k, temp_result)
        else:
            temp_result[key + '.' + k if key != '' else k] = v
    
    return temp_result   

def merge_dict(dict1, dict2):
    dotkv1 = construct_dotkv_from_dict(source = dict1, key = '', temp_result = {})
    dotkv2 = construct_dotkv_from_dict(source = dict2, key = '', temp_result = {})
    set1 = set(dotkv1)
    set2 = set(dotkv2)
    
    union = set1 | set2
    
    union_dict = {} 
    for key in union:
        union_dict = construct_dict_from_dotkv(
            union_dict, key.split('.'), dotkv2[key] if key in set2 else dotkv1[key])
    
    return union_dict
    
