#!/usr/bin/env python

# LIBS
from datetime import datetime
import traceback

# LOGGING
import logging

# CREATE TOP LOG LEVEL
log = logging.getLogger("uvicorn.error")

def Info(message):
    log.info(message)

def Debug(message):
    log.debug(message)

def Warning(message):
    log.warning(message)

def Error(sector, e, traceback=True):
    _trace = None
    message = ""
    if traceback:
        _trace = traceback.format_exc()
        message = f"\n {sector if sector else ''}: {_trace if _trace else ''} \n"
    log.error(f"{message} Message: {e if e else ''}")

def Critical(sector, e):
    _trace = traceback.format_exc()
    log.critical(f"{sector} \n {_trace} \n {e}")
