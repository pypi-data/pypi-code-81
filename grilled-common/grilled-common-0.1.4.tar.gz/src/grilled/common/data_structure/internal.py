def __turn_two_demension_dict_into_one_demension_combination(
    two_demension_dict: dict
) -> dict:
    res = {}
    for node_1, _dict in two_demension_dict.items():
        for node_2, value in _dict.items():
            if ((node_1, node_2) in res) or ((node_2, node_1) in res):
                continue
            res[node_1, node_2] = value
    return res

def __turn_two_demension_dict_into_one_demension_permutation(
    two_demension_dict: dict
) -> dict:
    res = {}
    for node_1, _dict in two_demension_dict.items():
        for node_2, value in _dict.items():
            if ((node_1, node_2) in res):
                continue
            res[node_1, node_2] = value
    return res

def __delete_repeat_key(one_demension_dict: dict
) -> dict:
    key_to_delete = []
    for node1, node2 in one_demension_dict:
        if node1 == node2:
            key_to_delete.append((node1, node2))
    for key in key_to_delete:
        del one_demension_dict[key]

def turn_two_demension_dict_into_one_demension(
    two_demension_dict: dict, 
    method: str="permutation",
    repeat: bool=False
) -> dict:
    """
    将二维字典转成一维字典，例：
    {"x": {"y": 10}}  =>  {("x", "y"): 10}
    two_demension_dict - 二维字典
    method - 选择以“组合”或“排列”的方式合并
    repeat - 相同的顶点是否允许组合
    """
    if method == "permutation":
        res = __turn_two_demension_dict_into_one_demension_permutation(two_demension_dict)
    elif method == "combination":
        res = __turn_two_demension_dict_into_one_demension_combination(two_demension_dict)
    else:
        raise Exception(f"Unsupportable param \"method\" {method}.")
    if not repeat:
        __delete_repeat_key(res)
    return res

def __check_vector_length(*args: list
) -> bool:
    """
    检查多个列表的长度是否一致
    """
    length_list = []
    for vector in args:
        length_list.append(len(vector))
    return length_list[0] == (sum(length_list) // len(length_list))

def v_greater_than(vector_1: list, vector_2: list
) -> list:
    """
    比较向量1是否大于向量2，即比较向量1的对应元素是否大于向量2，
    如果大于则为True，否则为False
    将所有比较结果打包在一个列表中作为返回值
    vector_1 - 向量1 
    vector_2 - 向量2
    """
    if __check_vector_length(vector_1, vector_2):
        res_bool_list = []
        for element_1, element_2 in zip(vector_1, vector_2):
            if element_1 >= element_2:
                res_bool_list.append(True)
            else:
                res_bool_list.append(False)
        return res_bool_list
    else:
        raise Exception("Length is not equal between vector_1 and vector_2.")
