from importlib import import_module


def get_func_from_str(func_str):
    m, f = func_str.rsplit('.', 1)
    mod = import_module(m)
    func = getattr(mod, f)
    return func
