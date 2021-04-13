def pyarrow(version = "3.0.0"):

    from packaging.version import parse
    from importlib import import_module

    from ._command import command

    try:
        from pyarrow import __version__ as INFO
        if parse(INFO) < parse(version):
            command("pip install --upgrade pyarrow")
    except:
        command("pip install --upgrade pyarrow")
        from pyarrow import __version__ as INFO

    print(F"{'pyarrow'.rjust(50)} : {INFO}")

    return import_module("pyarrow")
