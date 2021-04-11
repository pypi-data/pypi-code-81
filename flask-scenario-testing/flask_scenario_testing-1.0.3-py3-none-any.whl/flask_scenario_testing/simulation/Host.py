class Host(object):
    def __init__(self, hostname: str, port: str):
        self.hostname = hostname
        self.port = port

    def url(self, path=None):
        base = 'http://{}:{}'.format(self.hostname, self.port)

        if not path:
            return base

        return '{}/{}'.format(base, path)