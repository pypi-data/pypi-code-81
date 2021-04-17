from ._cbridge._bbai_handle import bbai_handle
from ._cbridge._bbai_glm_model_descriptor import BbaiGlmModelDescriptor

class LogisticRegression(object):
    def __init__(self):
        pass

    def fit(self, X, y):
        ptr = bbai_handle.bbai_glm_make_model_descriptor(
                    bbai_handle.bbai_model_loss_link_logistic,
                    bbai_handle.bbai_model_regularizer_l2)
        return BbaiGlmModelDescriptor(ptr)
