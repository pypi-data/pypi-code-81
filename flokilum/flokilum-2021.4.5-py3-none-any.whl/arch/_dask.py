def dask():

    from packaging.version import parse
    from importlib import import_module

    from .._install_min import install_min

    install_min(package="dask", pip_name="dask[complete]", version="2021.4.0")

    # print(F"{'dask'.rjust(50)} : {INFO}")

    from dask.distributed import Client, LocalCluster
    cluster = LocalCluster()
    client  = Client(cluster)

    return client, import_module("dask.array"), import_module("dask.dataframe"), import_module("dask.bag")
