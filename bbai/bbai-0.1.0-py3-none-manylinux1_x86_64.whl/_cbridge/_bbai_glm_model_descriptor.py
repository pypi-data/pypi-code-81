from ._bbai_handle import bbai_handle
from ._bbai_model_descriptor import BbaiModelDescriptor

class BbaiGlmModelDescriptor(BbaiModelDescriptor):
    def __self__(self, ptr):
        BbaiModelDescriptor.__init__(self, ptr)
