import traceback
import pandas as pd
import numpy as np

def read_convert(input_str: str) -> list:
    """This function reads the string format and then converts it to a dictionary of lists"""
    dict_list = []
    try:
        inputs = input_str.split("__::__")
        for lines in inputs:
            line_dict = {}
            line = lines.split("__$$__")
            for l in line:
                dict_value = l.split("__=__")
                key = dict_value[0]
                if len(dict_value) == 1:
                    value = ""
                else:
                    value = dict_value[1]
                if key != "":
                    line_dict[key] = value
            dict_list.append(line_dict)
    except Exception as e:
        print(traceback.format_exc(), flush=True)
    return dict_list


def write_convert(input_list: list) -> str:
    """This function reads convert the list of dictionaries(Tabular format) to a string format"""
    output_str = ""
    try:
        for dicts in input_list:
            for key, value in dicts.items():
                output_str = output_str + key + "__=__" + value
                output_str = output_str + "__$$__"
            output_str = output_str[:len(output_str) - 6]
            output_str = output_str + "__::__"
        output_str = output_str[:len(output_str) - 6]
    except Exception as e:
        print(traceback.format_exc(), flush=True)
    return output_str


def string_to_df(input_str: str, rename_cols: dict = {}, drop_dupes = False) -> pd.DataFrame():
    """This function converts the string format to a DataFrame"""
    final_dataframe = pd.DataFrame()
    try:
        for index, data_list in enumerate(input_str.split('__::__')):
            if str(data_list) == '':
                continue
            for each_data in data_list.split('__$$__'):
                if each_data == '':
                    continue
                if '__=__' in each_data:
                    final_dataframe.at[index, str(each_data.split('__=__')[0])] = str(each_data.split('__=__')[1])
        if len(rename_cols) != 0:
            try:
                final_dataframe = final_dataframe.rename(rename_cols, axis=1)
            except Exception as e:
                print(traceback.format_exc(), flush=True)
        if drop_dupes:
            final_dataframe = final_dataframe.drop_duplicates()
        final_dataframe = final_dataframe.replace(np.nan, '', regex=True)
    except Exception as e:
        print(traceback.format_exc(), flush=True)
    return final_dataframe
    

def df_to_string(input_df: pd.DataFrame(), rename_cols: dict = {}, drop_dupes = False) -> str:
    """This function converts a DataFrame to the string format"""
    final_string = ''
    try:
        input_df = input_df.replace(np.nan, '', regex=True)
        if len(rename_cols) != 0:
            try:
                input_df = input_df.rename(rename_cols, axis=1)
            except Exception as e:
                print(traceback.format_exc(), flush=True)
        if drop_dupes:
            input_df = input_df.drop_duplicates()
        for data_dict in input_df.to_dict('r'):
            for key in data_dict.keys():
                final_string += str(key) + '__=__' + str(data_dict[key]) + '__$$__'
            final_string += '__::__'
    except Exception as e:
        print(traceback.format_exc(), flush=True)
    return final_string