#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import pathlib as pt

from ioproc.driver import _main


__author__ = ["Benjamin Fuchs"]
__copyright__ = "Copyright 2020, German Aerospace Center (DLR)"
__credits__ = ["Felix Nitsch", "Judith Vesper", "Niklas Wulff", "Hedda Gardian", "Gabriel Pivaro", "Kai von Krbek"]

__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Felix Nitsch"
__email__ = "ioProc@dlr.de"
__status__ = "Production"


envPath = pt.Path()

pathvar = os.environ['PATH']
elem = pathvar.split(';')

for ielem in elem:
    if 'Scripts' in ielem:
        envPath = pt.Path(ielem).parent
        break


def create_folders(workflowName='yourTestWorkflow'):
    '''
    Creates the required folder structure.
    '''
    _main(setupworkflow=False, userconfig=None, setupfolders=True, workflowname=workflowName)

def create_workflow(workflowName='yourTestWorkflow'):
    '''
    Creates a new workflow in the current work directory.
    '''
    # REMINDER: currently not used. Could be interfaced in the future.
    _main(setupworkflow=True, userconfig=None, setupfolders=False, workflowname=workflowName)

def start(userconfig=None):
    '''
    Executes the workflow manager.
    '''
    _main(setupworkflow=False, userconfig=userconfig, setupfolders=False, workflowname=None)
