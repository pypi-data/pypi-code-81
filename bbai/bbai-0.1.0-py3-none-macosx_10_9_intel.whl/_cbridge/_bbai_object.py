from ._bbai_handle import bbai_handle

class BbaiObject(object):
    def __init__(self, ptr):
        self._pointer = ptr

    @property
    def pointer(self):
        return self._pointer

    def __del__(self):
        bbai_handle.bbai_destroy(self._pointer)

