from ._bbai_handle import bbai_handle
from ._bbai_object import BbaiObject

import numpy as np
from cffi import FFI

ffi = FFI()

class BbaiModel(BbaiObject):
    def __self__(self, ptr):
        BbaiObject.__init__(self, ptr)

    def get_weights(self, weights):
        assert len(weights.shape) == 1
        assert weights.dtype == np.float64
        num_weights = weights.shape[0]
        bbai_handle.bbai_model_get_weights(
                self.pointer,
                num_weights,
                ffi.cast("double *", weights.ctypes.data)
        )

    def get_hyperparameters(self, hyperparameters):
        assert len(hyperparameters.shape) == 1
        assert hyperparameters.dtype == np.float64
        num_hyperparameters = hyperparameters.shape[0]
        bbai_handle.bbai_model_get_hyperparameters(
                self.pointer,
                num_hyperparameters,
                ffi.cast("double *", hyperparameters.ctypes.data)
        )

    def get_intercepts(self, intercepts):
        assert len(intercepts.shape) == 1
        assert intercepts.dtype == np.float64
        num_intercepts = intercepts.shape[0]
        bbai_handle.bbai_model_get_intercepts(
                self.pointer,
                num_intercepts,
                ffi.cast("double *", intercepts.ctypes.data)
        )
