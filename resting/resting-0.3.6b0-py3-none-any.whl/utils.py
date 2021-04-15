

class DeferredService:

    _service = None

    def _init(self):
        raise NotImplemented("Override this method in your deferred object")

    def __getattr__(self, item):
        if not self._service:
            self._init()

        if item in ['_service', '_init']:
            return super(DeferredService, self).__getattr__(self, item)
        else:
            return getattr(self._service, item)

    def __setattr__(self, key, value):

        if key in ['_service', '_init']:
            self.__dict__[key] = value
        else:
            if not self._service:
                self._init()
            setattr(self._service, key, value)

    def __delattr__(self, item):
        if item == "_service":
            raise AttributeError("You can not delete _service attr")
