import json
import os
import sys
import traceback
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd

from swissarmykit.conf import *
from swissarmykit.data.BSoup import BItem
from swissarmykit.db.mongodb import BaseDocument


from swissarmykit.data.JsonData import JsonData
from swissarmykit.utils.command import Command
from swissarmykit.utils.numberutils import NumberUtils

from swissarmykit.utils.fileutils import FileUtils
from swissarmykit.utils.stringutils import StringUtils
from swissarmykit.utils.bytesutils import BytesUtils
from swissarmykit.office.excelutils import ExcelUtils
from swissarmykit.dataset.usa.USUtils import USUtils

class VideoUtils:

    def __init__(self):
        pass

    @staticmethod
    def get_meta_data(file, as_dict=False):
        if swissarmykit_conf.is_win():
            program = swissarmykit_conf.BIN_PATH + '/exiftool.exe'
        else:
            program = 'exiftool'

        commands = [program, file]
        meta =  Command.exec_output(commands)

        data = {}
        for m in meta.split('\n'):
            ms = m.split(':', 1)
            if len(ms) > 1:
                data[ms[0].strip()] = ms[1].strip()
                
        if as_dict:
            return data

        return meta, data


if __name__ == '__main__':
    file = "/Users/will/Downloads/Rick and Morty Season 4 UPDATED Complete 720p WEBRip x264/untitled folder/untitled folder/Rick and Morty S04E03 One Crew Over the Crewcoo's Morty.mkv"
    meta = VideoUtils.get_meta_data(file, as_dict=True)
    # meta = VideoUtils.get_meta_data(file)
    print(meta)
