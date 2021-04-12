from redis import ConnectionPool, StrictRedis


class ClientsConnection(StrictRedis):
    def __init__(self, **kwargs):
        super(ClientsConnection, self).__init__(**{**dict(
            connection_pool=ConnectionPool(host=kwargs.pop('host', 'localhost'), db=kwargs.pop('db', 0)),
            decode_responses=True), **kwargs}
        )


class ExecRedisClients(ClientsConnection):
    def __init__(self, clients_name, redis_config=None):
        self.__clients_name = clients_name
        self.__redis_config = redis_config or {clients_name: {}}
        super(ExecRedisClients, self).__init__(**self.__redis_config[self.__clients_name])

    def __clients_config(self, item):
        return self.__redis_config[item]
