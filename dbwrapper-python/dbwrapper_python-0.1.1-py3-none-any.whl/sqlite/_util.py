
import time
import re
import sqlite3
NUMBER_REGEX = re.compile(r"\d+\.?\d*")

def sql(obj, **kwargs):
    if hasattr(obj, "__sql__"):
        return type(obj).__sql__(obj, **kwargs)
    else:
        return escape_value(str(obj))

def escape_value(s):
    if s is None:
        return "NULL"
    elif type(s) in (int, float):
        return str(s)
    elif type(s) == str and (NUMBER_REGEX.match(s) or s.upper() == "NULL"):
        return s
    else:
        return "'" + str(s).replace("'", "''") + "'"

def execute(logger, c: sqlite3.Connection, sql_str: str, params=[])->sqlite3.Cursor:
    pre = time.time()
    try:
        cursor = c.execute(sql_str, params)
    except Exception as e:
        logger.exception("EXEC-EX: %s\n%s", sql_str, e)
        raise
    post = time.time()
    if logger is not None:
        logger.info("EXEC: %s Took %.3fms", sql_str, (post - pre) * 1000)
    return cursor

def executemany(logger, c: sqlite3.Connection, sql_str: str, params=[])->sqlite3.Cursor:
    pre = time.time()
    try:
        cursor = c.executemany(sql_str, params)
    except Exception as e:
        logger.exception("EXECMANY-EX: %s\n%s", sql_str, e)
        raise
    post = time.time()
    if logger is not None:
        logger.info("EXECMANY: %s Took %.3fms", sql_str, (post - pre) * 1000)
    return cursor

class cached_property(object):
    def __init__(self, func, name=None):
        self.func = func
        self.name = name if name is not None else func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, instance, class_):
        if instance is None:
            return self
        res = self.func(instance)
        setattr(instance, self.name, res)
        return res

def skip_empty_join(sep, *vals):
    lst = [str(x) for x in vals if x is not None and x != ""]

    return sep.join(lst)
