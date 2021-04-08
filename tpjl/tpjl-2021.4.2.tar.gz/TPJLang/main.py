import json
from zipfile import ZipFile

"""
    TPJL (TechGeeks Portable JSON Language) is a free & OpenSource Portable version of JSON.
    You can send a .tpjl file to anyone and he can open it with the read() function and can write with the write() function!
    Please Support us by Contributing by creating a pull request on GitHub.
                                                                                                                            Thanks,
                                                                                                                            Rajdeep Malakar,
                                                                                                                            Chief Executive Director,
                                                                                                                            TechGeeks <https://tgeeks.cf>
"""

def write(filename, JSON):
    """
        Write a .tpjl file with a easy syntax : read("Filename_without_Extension", JSONVariable)
    """
    JSON = json.dumps(JSON)
    with ZipFile(f'{filename}.tpjl', 'w') as tpjl:
        tpjl.writestr('MANIFEST.json', JSON)

def read(filename):
    """
        Read a .tpjl file with a easy syntax : read("Filename_without_Extension")
    """
    with ZipFile(f'{filename}.tpjl', 'r') as tpjl:
        json_data_read = tpjl.read('MANIFEST.json')
        output = json.loads(json_data_read)
        return output

zero = read("config")
zero = zero["0"]
zero = zero["_name"]
print(zero)