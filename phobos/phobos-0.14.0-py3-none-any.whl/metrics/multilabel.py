import numpy as np


def emr(predicted, target, **kwargs):
    return np.all(target == predicted, axis=1).mean()


def hamming(predicted, target, **kwargs):
    tmp = 0
    for i in range(target.shape[0]):
        tmp += np.size(target[i] == predicted[i]) - np.count_nonzero(target[i] == predicted[i])
    return tmp / (target.shape[0] * target.shape[1])
