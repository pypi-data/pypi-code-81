from .._cbridge._bbai_handle import bbai_handle
from .._cbridge._bbai_glm_model_descriptor import BbaiGlmModelDescriptor

import numpy as np

class LogisticRegression(object):
    def __init__(
            self,
            init0=None,
            fit_intercept=True,
            normalize=False,
            penalty='l2',
            active_classes = 'auto',
            C=None,
            tolerance=0.0001):
        hyperparameters = None
        if C:
            hyperparameters = np.array([1 / np.sqrt(2 * C)])
        self.params_ = {}
        self.set_params(
                init0 = init0,
                fit_intercept=fit_intercept,
                normalize=normalize,
                penalty=penalty,
                active_classes=active_classes,
                C=C,
                tolerance=tolerance
        )
        if tolerance <= 0:
            raise RuntimeError("invalid tolerance")

    def get_params(self, deep=True):
        """Get parameters for this estimator."""
        return self.params_

    def set_params(self, **parameters):
        """Set parameters for this estimator."""
        for parameter, value in parameters.items():
            self.params_[parameter] = value

    def fit(self, X, y):
        """Fit the logistic regression model."""
        self.classes_ = list(sorted(set(y)))
        self._loss_link = bbai_handle.bbai_model_loss_link_multinomial_logistic
        if self.params_['active_classes'] == 'm1' or len(self.classes_) == 2:
            self._loss_link = bbai_handle.bbai_model_loss_link_multinomial_logistic_m1
        model_descriptor = BbaiGlmModelDescriptor(
                bbai_handle.bbai_glm_make_model_descriptor(
                    self._loss_link,
                    bbai_handle.bbai_model_regularizer_l2
                )
        )
        model_descriptor.set_normalize_option(self.params_['normalize'])
        model_descriptor.set_fit_intercept_option(self.params_['fit_intercept'])
        C = self.params_['C']
        if C:
            hyperparameters = np.array([1 / np.sqrt(2 * C)])
            model_descriptor.set_hyperparameters(hyperparameters)
        model = model_descriptor.fit(X, y)
        self._set_model_coefficients(model, X.shape[1])

    def _set_model_coefficients(self, model, num_features):
        self._num_active_classes = len(self.classes_)
        if self._loss_link == bbai_handle.bbai_model_loss_link_multinomial_logistic_m1:
            self._num_active_classes -= 1
        weights = np.zeros(self._num_active_classes * num_features)
        model.get_weights(weights)
        self.coef_ = weights.reshape(self._num_active_classes, num_features)

        intercepts = np.zeros(self._num_active_classes)
        model.get_intercepts(intercepts)
        self.intercept_ = intercepts

        if self._num_active_classes == 1:
            # we invert so as to match the conventional way of representing weights
            self.coef_ = -self.coef_
            self.intercept_ = -self.intercept_

        self.hyperparameters_ = np.zeros(1)
        model.get_hyperparameters(self.hyperparameters_)

        penalty = self.params_['penalty']
        if penalty == 'l2':
            Cs = 0.5 / self.hyperparameters_ ** 2
            if len(Cs) == 1:
                self.C_ = Cs[0]
            else:
                self.C_ = Cs

    def predict(self, X):
        predict_proba = self.predict_proba(X)
        result = np.zeros(len(X))
        for i, predi in enumerate(predict_proba):
            result[i] = self.classes_[np.argmax(predi)]
        return result

    def predict_log_proba(self, X):
        return np.log(self.predict_proba(X))

    def predict_proba(self, X):
        if len(X.shape) != 2 or X.shape[1] != self.coef_.shape[1]:
            raise RuntimeError("invalid X")
        if self._num_active_classes == 1:
            return self._predict_proba_binomial(X)
        return self._predict_proba_multinomial(X)

    def _predict_proba_binomial(self, X):
        u = np.dot(X, self.coef_[0, :]) + self.intercept_[0]
        t = 1 / (1 + np.exp(-u))
        result = np.zeros((len(t), 2), dtype=np.double)
        result[:, 0] = 1 - t
        result[:, 1] = t
        return result

    def _predict_proba_multinomial(self, X):
        U = np.dot(X, self.coef_.T) + self.intercept_
        if self._num_active_classes < len(self.classes_):
            U = np.hstack((U, np.zeros((U.shape[0], 1))))
        for i, ui in enumerate(U):
            exp_ui = np.exp(ui)
            U[i, :] = exp_ui / np.sum(exp_ui)
        return U
