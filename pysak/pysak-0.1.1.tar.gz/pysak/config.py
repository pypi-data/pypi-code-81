import configparser
from pysak.path import *


def getConfig(configPath="config\\main.ini", section=""):
    """
        读取指定的ini配置文件

    :param configPath: 配置文件相对路径 如：config\\main.ini
    :param section: 配置文件下的section
    :return:
    """
    config = configparser.ConfigParser()
    config.read_file(open(f"{getRootPath()}{configPath}", encoding='UTF-8'))

    # 获取conf中的section
    sections = config.sections()

    configs = {}

    for index in range(len(sections)):
        configs[sections[index]] = {}

    for index in range(len(configs)):
        sectionName = sections[index]

        # 当前section的所有option
        options = config.options(sectionName)
        for index in range(len(options)):
            # configs[sectionName][options[index]] = {}
            configs[sectionName][options[index]] = str(config.get(sectionName, options[index]))

    # 获取version的值 方法1
    # version = str(config.get(sections[0], paramList[0]))
    # 获取version的值 方法2
    # version = str(config.get("EditionInfo", "version"))
    return configs


def editConfig(section="", option="", value="", configPath="config\\main.ini"):
    """
        修改section下option的值为value
    :param section: 配置文件section
    :param option: section下的option
    :param value: 需要修改成什么值
    :param configPath: 配置文件相对路径 如：config\\main.ini
    :return:
    """
    config = configparser.ConfigParser()
    config.read_file(open(f"{getRootPath()}{configPath}", encoding='UTF-8'))

    # 获取conf中的section
    sections = config.sections()

    # 修改section下option的值为value
    config.set(section, option, str(value))
    config.write(open(configPath, "w"))
