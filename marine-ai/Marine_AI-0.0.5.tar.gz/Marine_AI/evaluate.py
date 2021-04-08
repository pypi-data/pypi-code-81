import numpy as np


def rmse(y_true, y_preds):
    total = 0
    length = len(y_true)
    for i in range(len(y_true)):
        total = total + (y_true[i] - y_preds[i]) ** 2
    rmse =np.sqrt((1 / length) * total)
    return rmse

def cor(y_ture, y_preds):
    length = len(y_preds)
    A, B, C = 0, 0, 0
    y_tm = np.mean(y_ture)
    y_pm = np.mean(y_preds)
    for i in range(length):
        A = A + (y_ture[i] - y_tm) * (y_preds[i] - y_pm)
        B = B + (y_ture[i] - y_tm) ** 2
        C = C + (y_preds[i] - y_pm) ** 2
    cor = A / np.sqrt(B * C)
    return cor