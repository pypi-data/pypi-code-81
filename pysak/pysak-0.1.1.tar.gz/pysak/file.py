from .path import *

import json


# dict存入本地json文件
def dict2jsonFile(data={"a": 1, "b": 2, "c": 3}, fileName="data.json", RelativePath="\\"):
    """
    dict转json文件
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
        # json.dump(json_str, json_file)

    return True


# json文件内容转dict
def jsonFile2dict(fileName="data.json", RelativePath="\\"):
    """

    @param fileName:
    @param RelativePath:
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

    filePath = f"{PATH}\\{fileName}"

    # 判断文件是否存在
    if not isPathExists(filePath):
        print(f"文件不存在：{filePath}")
        return False

    # 读取json文件，并转换为dict
    with open(filePath, 'r') as json_file:
        new_dict = json.load(json_file)

    # 字符串转dict
    # new_dict = json.loads(json_str)

    return new_dict


# 将字符串存入本地文件
def str2file(content="hello world!", fileName="data.txt", RelativePath="\\"):
    # 获取项目根目录
    ROOT_PATH = getRootPath()

    if ROOT_PATH == False:
        return False

    if RelativePath != "":
        PATH = f"{ROOT_PATH}{RelativePath}"
    else:
        PATH = ROOT_PATH
    mkdir(PATH)

    with open(f"{PATH}\\{fileName}", 'w') as file:
        file.write(content)

    return True
