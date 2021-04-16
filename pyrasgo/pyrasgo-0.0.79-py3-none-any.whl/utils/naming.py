from datetime import datetime
import hashlib
from more_itertools import lstrip
import pandas as pd
import uuid

def make_timestamp():
    now = datetime.now()
    return now.strftime("%Y_%m_%d_%H_%M")

def random_table_name():
    identifier = str(uuid.uuid4())
    table_name = ''.join(list(lstrip(hashlib.md5(identifier.encode('utf-8')).hexdigest(),
                            lambda x: x.isnumeric()))).upper()
    return table_name

def _snowflakify_data_type(dtype: str):
    if dtype.lower() in ["object", "text"]:
        return "string"
    else:
        return dtype.lower()

def _snowflakify_list(list_in):
    """
    param list_in: list
    return list_out: list
    Changes a list of columns to Snowflake compliant names
    """
    return [_snowflakify_name(n) for n in list_in]

def _snowflakify_name(name):
    """
    param name: string
    return: string
    Converts a string to a snowflake compliant value
    Removes double quotes, replaces dashes/dots/spaces with underscores, casts to upper case
    """
    return name.replace(" ", "_").replace("-", "_").replace('"', '').replace(".","_").upper()