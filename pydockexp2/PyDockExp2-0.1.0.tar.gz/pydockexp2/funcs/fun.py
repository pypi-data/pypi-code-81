import numpy as np 
import matplotlib.pyplot as plt


class Function:

    @staticmethod
    def sigmoid(x: np.array, k: np.float64) -> np.array:
        """ Compute the logistic sigmoid function over x with parameter k """
        return 1 / (1 + np.exp((-1) * x * k))

    @staticmethod
    def linear(x: np.array, a: np.array, b: np.array) -> np.array:
        """ Compute the linear function over x with parameter a and b """
        try:
            X     = np.append(x, np.ones(x.shape[0]).reshape(-1, 1), axis=1)
            Theta = np.append(a, b, axis=0)
            return np.matmul(X, Theta)
        except ValueError:
            return