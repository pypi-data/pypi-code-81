import logging
import os

outstr = ''
logout = False


def get_home():
    #    return str(pathlib.Path.home())
    return os.path.expanduser("~")


def setup_logging(logdir):
    if logout:
        if logdir is None:
            logdir = get_home()
        print('Logging to %s' % logdir)
        logging.basicConfig(filename=logdir + os.path.sep + 'enrichwrap.log', level=logging.DEBUG)


def get_outstr():
    global outstr
    return outstr


def add_outstr(newval):
    global outstr
    outstr += os.linesep + newval
    if logout:
        logging.info(newval)
    else:
        print(newval)


def set_logout(boolval):
    global logout
    logout = boolval


