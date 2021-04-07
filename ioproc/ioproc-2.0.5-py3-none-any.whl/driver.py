#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pathlib as pt

import click

from ioproc.config import configProvider
from ioproc.defaults import *
from ioproc.logger import mainlogger as log
from ioproc.datamanager import DataManager
from ioproc.actionmanager import getActionManager
from ioproc.tools import freeze, setupFolderStructure


__author__ = ["Benjamin Fuchs", "Judith Vesper", "Felix Nitsch"]
__copyright__ = "Copyright 2020, German Aerospace Center (DLR)"
__credits__ = ["Niklas Wulff", "Hedda Gardian", "Gabriel Pivaro", "Kai von Krbek"]

__license__ = "MIT"
__version__ = "1.0.2"
__maintainer__ = "Felix Nitsch"
__email__ = "ioProc@dlr.de"
__status__ = "Production"


IOPROCINSTALLROOT = pt.Path(__file__).resolve().parent
SCHEMAPATH = pt.Path(IOPROCINSTALLROOT, "schema")
HOME = pt.Path.home()

defaultConfigContent = defaultConfigContent.format(IOPROCINSTALLROOT.as_posix())


@click.command()
@click.option('--setupworkflow', is_flag=True, help='generate default setupworkflow setup')
@click.option('--userconfig', '-c', default=None, help='path to user.yaml')
@click.option('--setupfolders', is_flag=True, help='generate default folder structure')
@click.option('--workflowname', default='workflow1', help='name of your workflow' )
def ioproc(setupworkflow, userconfig, setupfolders, workflowname):
    _main(setupworkflow, userconfig, setupfolders, workflowname)


def _main(setupworkflow=False, userconfig=None, setupfolders=False, workflowname='workflow1'):
    """
    Main driver which triggers the setup of the required folder structure, if needed.
    It also sets the user config path and the workflow structure, if they are not set up already.
    If the workflow is already set up, the action manager and the data manager are initialized.
    Next and according to the provided user configuration, the workflow with its actions
    is executed, which can also be started from a checkpoint to resume a previously started run.
    If loading from a checkpoint is enabled, it is ensured that the given tag is existent in the directory,
    otherwise an Exception is raised.
    """
    if setupfolders:
        setupFolderStructure(workflowname)
        return

    userConfigPath = pt.Path(pt.Path.cwd(), 'user.yaml')

    if userconfig is not None:
        userConfigPath = pt.Path(userconfig)

    if setupworkflow and not userConfigPath.exists():
        if not userConfigPath.parent.exists():
            raise IOError(f"Path to user config not found: {userConfigPath.as_posix()}")

        with userConfigPath.open('w') as opf:
            opf.write(defaultUserContent)

        workflowStartScript = userConfigPath / 'run.py'
        if not workflowStartScript.exists():
            with workflowStartScript.open('w') as opf:
                opf.write(defaultRunPyFile)

    configProvider.setPathes(
                             userConfigPath=userConfigPath,
                             )
    config = configProvider.get()

    if not setupworkflow:
        actionMgr = getActionManager()
        assert len(actionMgr) > 0, "ActionManager is not defined. Ensure 'actionFolder' path in 'user.yaml' is set correctly."
        dmgr = DataManager(config['user'])

        log.info('starting workflow')

        log.debug('commencing action calling')

        FROMCHECKPOINT = config['user']['fromCheckPoint'] != 'start'

        if FROMCHECKPOINT:
            given_tag = config['user']['fromCheckPoint']
            if not pt.Path('./Cache_{}.h5f'.format(given_tag)).is_file():
               message = 'cannot find cache file with given tag name `{}`'.format(given_tag)
               log.exception(message)
               raise Exception(message)

        for iActionInfo in config['user']['workflow']:
            iActionInfo = iActionInfo[list(iActionInfo.keys())[0]]
            if FROMCHECKPOINT and 'tag' in iActionInfo and iActionInfo['tag'] != config['user']['fromCheckPoint']:
                continue
            elif FROMCHECKPOINT and 'tag' in iActionInfo and iActionInfo['tag'] == config['user']['fromCheckPoint']:
                FROMCHECKPOINT = False
                dmgr.fromCache(config['user']['fromCheckPoint'], iActionInfo)
                log.info('reading from cache for tag "{}"'.format(config['user']['fromCheckPoint']))
                continue
            elif FROMCHECKPOINT:
                continue

            log.debug('executing action "'+iActionInfo['call']+'"')
            dmgr.entersAction(iActionInfo)
            try:
                actionMgr[iActionInfo['project']][iActionInfo['call']](dmgr, config, freeze(iActionInfo))
            except Exception as e:
                log.exception('Fatal error during execution of action "'+iActionInfo['call']+'":\nData manager log:\n'+dmgr.report())
                raise e
            dmgr.leavesAction()


if __name__ == '__main__':
    ioproc()
