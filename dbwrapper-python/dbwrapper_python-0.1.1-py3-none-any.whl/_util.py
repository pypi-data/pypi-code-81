
import time
import re
NUMBER_REGEX = re.compile(r"^\d+\.?\d*$")

def sql(obj, **kwargs):
    if hasattr(obj, "__sql__"):
        return type(obj).__sql__(obj, **kwargs)
    elif isinstance(obj, (list, set)):
        return "(%s)" % (",".join(sql(x) for x in obj))
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

def execute(logger, c, sql_str: str, params=[]):
    pre = time.time()
    try:
        cursor = c.cursor()
        cursor.execute(sql_str, params)
    except Exception as e:
        logger.exception("EXEC-EX: %s\n%s", sql_str, e)
        cursor.close()
        raise
    post = time.time()
    if logger is not None:
        logger.info("EXEC: %s Took %.3fms Rows=%d", sql_str, (post - pre) * 1000, cursor.rowcount)
    return cursor

def executemany(logger, c, sql_str: str, params=[]):
    pre = time.time()
    try:
        cursor = c.cursor()
        cursor.executemany(sql_str, params)
    except Exception as e:
        logger.exception("EXECMANY-EX: %s\n%s", sql_str, e)
        cursor.close()
        raise
    post = time.time()
    if logger is not None:
        logger.info("EXECMANY: %s Took %.3fms Rows=%d", sql_str, (post - pre) * 1000, cursor.rowcount)
    return cursor

class cached_property(object):
    def __init__(self, func, name=None):
        self.func = func
        self.name = name if name is not None else func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, obj, cls):
        if obj is None:
            return self

        if self.name not in obj.__dict__:
            obj.__dict__[self.name] = self.func(obj)
        
        return obj.__dict__[self.name]

    def __set__(self, obj, val):
        raise AttributeError("Cannot set property %s" % self.name)

    def __delete__(self, obj):
        if self.name in obj.__dict__:
            del obj.__dict__[self.name]

def skip_empty_join(sep, *vals):
    lst = [str(x) for x in vals if x is not None and x != ""]

    return sep.join(lst)

def skip_empty_format(fmt, value, onempty=""):
    if value is None:
        return onempty
    else:
        return fmt % value

def Navigator(obj, nav_name, schema_fn, getter_fn, name_fn=str):
    d = {}
    
    l = 0
    for name in schema_fn():
        d[name_fn(name)] = property((lambda name: lambda self: getter_fn(name))(name))
        l += 1

    d["__contains__"] = lambda self, x: x in schema_fn()
    d["__len__"] = lambda self: l

    return type(nav_name, (object,), d)()

def computeIfAbsent(d, key, fn):
    if key not in d:
        d[key] = fn(key)
    
    return d[key]

class Literal:
    def __init__(self, sql):
        self.sql = sql

    def __str__(self):
        return "Literal[%s]" % self.sql

    def __sql__(self, **kwargs):
        return self.sql

def Function(text):
    class func:
        def __init__(self, *args, alias=None):
            self.args = args or []
            self.alias = alias
        
        def __str__(self):
            return self.__sql__()
        
        def __sql__(self, usage=None):
            if usage == "column-like" and self.alias is not None:
                return self.alias
            else:
                return "%s(%s)%s" % (
                    text,
                    ",".join(sql(x) for x in self.args),
                    (" AS %s" % self.alias) if self.alias else ""
                )
            
        def with_alias(self, alias):
            return func(*self.args, alias=alias)

    return func
