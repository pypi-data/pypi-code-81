#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import argparse
import logging
import logging.handlers
#############################################
# File Name: maind.py
# Author: stosc
# Mail: stosc@sidaxin.com
# Created Time:  2020-2-8 19:17:34
#############################################
import os
import sys
import time

import _thread


try:
    from data2es.myDaemon import Daemon
    from data2es.main import *
    from data2es import __daemonName__, __serverName__, __version__
except ModuleNotFoundError:
    from myDaemon import Daemon
    from main import *
    from __init__ import __daemonName__, __serverName__, __version__

import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)


def setFileLog(filename):
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class D2esServiceDaemon(Daemon):
    def run(self, args):
        print('#(dt) Daemon started with pid %s \n' % (os.getpid()))
        runData2es(args[1], self.splitLogFile)

    def stop(self):
        super(D2esServiceDaemon, self).stop()

    def statue(self):
        return super(D2esServiceDaemon, self).getStatueCode()


ug = ''' %s {%s} 

positional arguments:
  {start|stop|restart|kill}
                        This control command can be used with start or stop or
                        restart or kill. Used to control the running of
                        data2esd daemons

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIGFILE_PATH, --config CONFIGFILE_PATH
                        Specify configuration file path.
  -l LOG_FILE_PATH, --logfile LOG_FILE_PATH
                        Specify log file path.
  -v, --version         show program's version number and exit
'''


def run():
    PIDFILE = '/tmp/%s.pid' % __daemonName__
    LOG = '/tmp/%s.log' % __daemonName__
    ERR = '/tmp/%s.err.log' % __daemonName__
    CONFFILE = None
    rc = 'start|stop|restart|kill|statue'
    parser = argparse.ArgumentParser(
        prog='%s' % __daemonName__, usage=ug % (__daemonName__, rc))
    parser.add_argument("-c", "--config", help="Specify configuration file path.", metavar='CONFIGFILE_PATH',
                        required=False)
    parser.add_argument("-l", "--logfile", help="Specify log file path.", metavar='LOG_FILE_PATH',
                        required=False)
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + __version__)
    # 添加参数解析
    parser.add_argument("runControl", metavar='{%s}' % rc, nargs='+', choices=rc.split('|'),
                        help="This control command can be used with %s. Used to control the running of data2esd daemons" % (
                            rc.replace('|', ' or ')))
    # 开始解析
    args = parser.parse_args()
    runCmd = args.runControl[0]

    if args.logfile != None:
        with open(args.logfile, 'w'):  # OSError if file exists or is invalid
            pass
        if os.path.isfile(args.logfile):
            LOG = args.logfile
    rca = rc.split('|')
    daemon = D2esServiceDaemon(pidfile=PIDFILE, stdout=LOG, stderr=LOG)
    setFileLog(LOG)
    if runCmd == rca[0]:
        CONFFILE = args.config
        if CONFFILE == None:
            logger.error(
                'when start must specify configuration file path use -c/--config.')
            sys.exit(-1)
        else:
            if os.path.exists(CONFFILE):
                if os.path.exists(LOG):
                    logger.info('The log file is %s' % os.path.abspath(LOG))
                    logger.info('The config file is %s' %
                                os.path.abspath(CONFFILE))
                    daemon.start(['-c', CONFFILE, '-l', LOG])
                else:
                    logger.info('The log file %s is not exists' %
                                os.path.abspath(LOG))
            else:
                logger.info('The config file %s is not exists' %
                            os.path.abspath(CONFFILE))
    elif runCmd == rca[1]:
        daemon.stop()
    elif runCmd == rca[2]:
        daemon.restart()
    elif runCmd == rca[3]:
        daemon.kill()
    elif runCmd == rca[4]:
        statueCode = daemon.statue()
        if statueCode == -1:
            print('data2es is not run.')
        else:
            print(statueCode)


if __name__ == '__main__':
    run()
