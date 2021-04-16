class ServerConfig:

    name: str
    host: str
    port: int

    def __init__(self, name: str, host: str, port: int):
        self.name = name
        self.host = host
        self.port = port
