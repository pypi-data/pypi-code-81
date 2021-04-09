import Pyro5.api


def createProxy(host: str = 'localhost', port: int = 23000, _objectId: str = 'TimeTagger'):
    """Returns Proxy object to the remote Time Tagger RPC

    Args:
        host (str, optional): Server hostname or IP address. Defaults to 'localhost'.
        port (int, optional): Server port. Defaults to 23000.
        _objectId (str, optional): Pyro Object ID. Defaults to 'TimeTagger'.

    Returns:
        Pyro5.api.Proxy: Proxy object to the Time Tagger Library.
    """
    uri = f"PYRO:{_objectId}@{host}:{port}"
    return Pyro5.api.Proxy(uri)



