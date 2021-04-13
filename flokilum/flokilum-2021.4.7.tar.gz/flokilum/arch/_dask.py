def dask(version = "2021.4.0"):

    from packaging.version import parse
    from importlib import import_module

    from ._command import command

    try:
        from dask import __version__ as INFO
        if parse(INFO) < parse(version):
            command("pip install --upgrade dask[complete]")
    except:
        command("pip install --upgrade dask[complete]")
        from dask import __version__ as INFO

    print(F"{'dask'.rjust(50)} : {INFO}")

    from dask.distributed import Client, LocalCluster
    cluster = LocalCluster()
    client  = Client(cluster)

    return client, import_module("dask.array"), import_module("dask.dataframe"), import_module("dask.bag")
