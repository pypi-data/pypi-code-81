'''
FFmpeg I/O package




ffmpegio.stream.open()
ffmpegio.stream.read()
ffmpegio.stream.write()

underlying 
'''

#!/usr/bin/python
# -*- coding: utf-8 -*-

# from . import ffmpeg

# import numpy as np
# import json
# import shutil
# import logging
# import sys
# import os
# import re
# import subprocess as sp
# from . import caps


def get_format_info(inputFileName):
    """get media container info of the media file

    inputFileName (str): media file path
    """
    return ffmpeg.probe(inputFileName).get("format", dict())
