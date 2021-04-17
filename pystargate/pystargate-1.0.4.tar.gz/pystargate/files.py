#!/usr/bin/env python
# -*- coding:utf-8
from .libs import common,extend
_common=common
_extend=extend.Extend()

def BatchFindFiles(dir):
    return _common.FindFiles(dir)

def OpenFiles(files_name):
    _common.OpenFiles(files_name)

def BatchFindOpenFiles(files_dir):
    _extend.FindOpenFiles(files_dir)

def CopyFiles(src,dst):
    return _common.CopyFiles(src,dst)

def BatchCopyFiles(src,dst,t=0):
    return _common.BatchCopyFiles(src,dst,t)

def MoveFiles(src,dst):
    return _common.MoveFiles(src,dst)

def BatchMoveFiles(src,dst,t=0):
    return _common.BatchMoveFiles(src,dst,t)