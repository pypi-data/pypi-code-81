def install_min(package, pip_name, version):

    from packaging.version import parse
    from importlib import import_module

    from ._command import command

    try:
        package_module = import_module(package)
        package_version = getattr(package_module, "__version__")
        if parse(package_version) < parse(version):
            command(F"pip install --upgrade {pip_name}")
    except:
        command(F"pip install --upgrade {pip_name}")
        package_module = import_module(package)
        package_version = getattr(package_module, "__version__")

    print(F"{package.rjust(50)} : {package_version}")
