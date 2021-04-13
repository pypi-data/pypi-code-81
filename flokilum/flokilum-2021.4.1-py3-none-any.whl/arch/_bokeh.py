def bokeh():

    from packaging.version import parse
    from importlib import import_module

    from ../_install_min import install_min

    install_min(package="bokeh", pip_name="bokeh", version="2.3.1")

    print(F"{'bokeh'.rjust(50)} : {INFO}")

    ## do not need to load this directly
    # return import_module("bokeh")
