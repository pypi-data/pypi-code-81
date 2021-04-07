from .path import *

import json


def dict2jsonfile(data: dict, fileName="data.json", path=getRootPath()):
    if fileName == "" or path == "":
        return False

    json_str = json.dumps(data, indent=4)
    with open(f"{path}\\{fileName}", 'w') as json_file:
        json_file.write(json_str)

    return True
