def pyarrow():

    from packaging.version import parse
    from importlib import import_module

    from .._install_min import install_min

    install_min(package="pyarrow", pip_name="pyarrow", version="3.0.0")

    # print(F"{'pyarrow'.rjust(50)} : {INFO}")

    ## dont need to load this
    # return import_module("pyarrow")
