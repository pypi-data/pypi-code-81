import numpy as np
import math


def fast_hist(predicted, target, num_classes):
    k = (predicted >= 0) & (target < num_classes)
    return np.bincount(num_classes * predicted[k].astype(np.uint8) + target[k],
                       minlength=num_classes**2).reshape(num_classes, num_classes)


def cal_kappa(hist):
    if hist.sum() == 0:
        po = 0
        pe = 1
        kappa = 0
    else:
        po = np.diag(hist).sum() / hist.sum()
        pe = np.matmul(hist.sum(1), hist.sum(0).T) / hist.sum() ** 2
        if pe == 1:
            kappa = 0
        else:
            kappa = (po - pe) / (1 - pe)
    return kappa


def mIoU_and_SeK(predicted, target, num_classes):
    hist = fast_hist(predicted.flatten(), target.flatten(), num_classes)
    hist_fg = hist[1:, 1:]
    c2hist = np.zeros((2, 2))
    c2hist[0][0] = hist[0][0]
    c2hist[0][1] = hist.sum(1)[0] - hist[0][0]
    c2hist[1][0] = hist.sum(0)[0] - hist[0][0]
    c2hist[1][1] = hist_fg.sum()
    hist_n0 = hist.copy()
    hist_n0[0][0] = 0
    kappa_n0 = cal_kappa(hist_n0)
    iu = np.diag(c2hist) / (c2hist.sum(1) + c2hist.sum(0) - np.diag(c2hist))
    IoU_fg = iu[1]
    IoU_mean = (iu[0] + iu[1]) / 2
    Sek = (kappa_n0 * math.exp(IoU_fg)) / math.e

    return IoU_mean, Sek


def mIoU(predicted, target, num_classes):
    return mIoU_and_SeK(predicted, target, num_classes)[0]


def SeK(predicted, target, num_classes):
    return mIoU_and_SeK(predicted, target, num_classes)[1]
