def bokeh(version = "2.3.1"):

    from packaging.version import parse
    from importlib import import_module

    from ._command import command

    try:
        from bokeh import __version__ as INFO
        if parse(INFO) < parse(version):
            command("pip install --upgrade bokeh")
    except:
        command("pip install --upgrade bokeh")
        from bokeh import __version__ as INFO

    print(F"{'bokeh'.rjust(50)} : {INFO}")

    return import_module("bokeh")
