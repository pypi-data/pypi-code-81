from .path import *

import json


def dict2jsonfile(data={"a": 1, "b": 2, "c": 3}, fileName="data.json", RelativePath="test\\data"):
    """
    @param data: dict字典类型数据
    @param fileName: 生成的文件名
    @param RelativePath: 生成文件的相对路径
    @return:
    """
    # 获取项目根目录
    ROOT_PATH = getRootPath()

    if ROOT_PATH == False:
        return False

    if RelativePath != "":
        PATH = f"{ROOT_PATH}{RelativePath}"
    else:
        PATH = ROOT_PATH
    mkdir(PATH)

    json_str = json.dumps(data, indent=4)

    with open(f"{PATH}\\{fileName}", 'w') as json_file:
        json_file.write(json_str)

    return True
