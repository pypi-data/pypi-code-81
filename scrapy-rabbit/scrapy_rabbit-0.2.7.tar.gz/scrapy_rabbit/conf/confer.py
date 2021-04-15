# -*- coding: utf-8 -*-
# Author: Eamonn
# Email: china.eamonn@gmail.com
# Link: https://elanpy.com

import configparser
from fuclib import ezfuc
import os


class MyConfigParser(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


def get_config():
    current_path = os.path.abspath('../..')
    if 'conf' not in os.listdir(current_path):
        current_path = os.path.abspath('..')

    config_file_path = os.path.join(os.path.abspath(current_path + os.path.sep), 'conf', 'config.ini')
    conf = MyConfigParser()
    conf.read(config_file_path, encoding='utf-8')
    items = list()
    for section in conf.sections():
        items += conf.items(section)
    return ezfuc.dict_to_object(dict(items))


conf = get_config()
