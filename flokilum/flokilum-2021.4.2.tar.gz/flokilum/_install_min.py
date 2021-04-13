def install_min(package, pip_name, version):

    from packaging.version import parse
    from importlib import import_module

    from ._command import command

    try:
        from package import __version__ as INFO
        if parse(INFO) < parse(version):
            command("pip install --upgrade {pip_name}")
    except:
        command("pip install --upgrade {pip_name}")
        from package import __version__ as INFO
