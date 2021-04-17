from ._bbai_handle import bbai_handle
from ._bbai_object import BbaiObject
from ._bbai_model import BbaiModel

import numpy as np
from cffi import FFI

ffi = FFI()

class BbaiModelDescriptor(BbaiObject):
    def __self__(self, ptr):
        BbaiObject.__init__(self, ptr)

    def set_normalize_option(self, normalize):
        bbai_handle.bbai_model_set_normalize_option(self.pointer, int(normalize))

    def set_fit_intercept_option(self, fit_intercept):
        bbai_handle.bbai_model_set_fit_intercept_option(self.pointer, int(fit_intercept))

    def set_hyperparameters(self, hyperparameters):
        num_hyperparameters = hyperparameters.shape[0]
        hyperparameters = np.array(hyperparameters, dtype=np.double)
        bbai_handle.bbai_model_set_hyperparameters(
                self.pointer,
                num_hyperparameters,
                ffi.cast("double *", hyperparameters.ctypes.data)
        )

    def fit(self, X, y):
        n, p = X.shape
        X = np.array(X, dtype=np.double, order='F')
        y = np.array(y, dtype=np.double)
        return BbaiModel(bbai_handle.bbai_model_fit(
                self.pointer,
                n, p,
                ffi.cast("double *", X.ctypes.data),
                ffi.cast("double *", y.ctypes.data)
        ))
