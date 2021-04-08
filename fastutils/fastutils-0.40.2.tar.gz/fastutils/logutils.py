import os
from logging.config import dictConfig

from . import dictutils


def get_console_handler(formatter="default", loglevel="DEBUG"):
    return {
        "level": loglevel,
        "class": "logging.StreamHandler",
        "formatter": formatter,
    }

def get_file_handler(filename, formatter="default", loglevel="DEBUG" ):
    if os.name == "nt":
        return {
            "level": loglevel,
            "class": "logging.FileHandler",
            "filename": filename,
            "formatter": formatter,
        }
    else:
        return  {
            "level": loglevel,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": filename,
            "when": "midnight",
            "interval": 1,
            "backupCount": 30,
            "formatter": formatter,
        }

def get_simple_config(logfile=None, loglevel=None, logfmt=None, logging=None, **kwargs):
    """
        {
            "logfile": "LOG FILE PATH",
            "loglevel": "DEBUG/INFO/...",
            "logfmt": "default/json",
            "logging": {
                ...
            }
        }
    """
    config = logging or {}
    logfile = logfile or config.get("logfile", "app.log")
    loglevel = loglevel or config.get("loglevel", "INFO")
    logfmt = logfmt or config.get("logfmt", "default")
    # make sure log folder exists...
    logfolder = os.path.abspath(os.path.dirname(logfile))
    if not os.path.exists(logfolder):
        os.makedirs(logfolder, exist_ok=True)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "{asctime} {levelname} {pathname} {lineno} {module} {funcName} {process} {thread} {message}",
                "style": "{"
            },
            "message_only": {
                "format": "{message}",
                "style": "{",
            },
            "json": {
                "class": "jsonformatter.JsonFormatter",
                "format": {
                    "asctime": "asctime",
                    "levelname": "levelname",
                    "pathname": "pathname",
                    "lineno": "lineno",
                    "module": "module",
                    "funcName": "funcName",
                    "process": "process",
                    "thread": "thread",
                    "message": "message",
                },
            },
        },
        "handlers": {
            "default_console": get_console_handler("default", "DEBUG"),
            "default_file": get_file_handler(logfile, "default", "DEBUG"),
            "json_console": get_console_handler("json", "DEBUG"),
            "json_file": get_file_handler(logfile, "json", "DEBUG"),
            "message_only_console": get_console_handler("message_only", "DEBUG"),
            "message_only_file": get_file_handler(logfile, "message_only", "DEBUG"),
        },
        "loggers": {
        },
        "root": {
            "handlers": [logfmt+"_file", logfmt+"_console"],
            "level": loglevel,
            "propagate": True,
        }
    }
    dictutils.deep_merge(logging_config, config)
    dictutils.deep_merge(logging_config, kwargs)
    return logging_config

def setup(*args, **kwargs):
    config = get_simple_config(*args, **kwargs)
    dictConfig(config)
