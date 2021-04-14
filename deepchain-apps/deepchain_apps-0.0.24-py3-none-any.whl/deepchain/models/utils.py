"""
Basic tools to build and evaluate a model
"""
from typing import Callable, List, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import torch
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score
from torch.utils.data import DataLoader, TensorDataset


def dataloader_from_numpy(
    X: np.ndarray, y: np.array, batch_size: int = None
) -> DataLoader:
    """
    function that build a torch dataset
    """
    tensor_set = TensorDataset(torch.tensor(X).float(), torch.tensor(y).float())
    loader = DataLoader(tensor_set, batch_size=batch_size)
    return loader


def model_evaluation_accuracy(
    dataloader: DataLoader, model: Callable
) -> Tuple[np.array, np.array]:
    """
    Make prediction for test data
    Args:
        dataloader: a torch dataloader containing dataset to be evaluated
        model : a callable trained model with a predict method
    """
    prediction, truth = [], []
    for X, y in dataloader:
        y_hat = model.predict(X)
        prediction += y_hat.detach().numpy().flatten().tolist()
        truth += y.detach().numpy().flatten().tolist()

    prediction, truth = np.array(prediction), np.array(truth)

    acc_score = accuracy_score(truth, (prediction > 0.5).astype(int))
    auc = roc_auc_score(truth, prediction)
    print(f" Test :  accuracy score : {acc_score:0.2f} - AUC score : {auc:0.2f}  ")

    return prediction, truth


def confusion_matrix_plot(
    y_true: Union[list, np.array], y_pred: Union[list, np.array], class_: List
):
    """
    Plot a confusion matrix based on
    """
    conf_arr = confusion_matrix(y_true, y_pred)
    norm_conf = []
    for i in conf_arr:
        a = 0
        tmp_arr = []
        a = sum(i, 0)
        for j in i:
            tmp_arr.append(float(j) / float(a))
        norm_conf.append(tmp_arr)

    fig = plt.figure(figsize=(10, 7))
    plt.clf()
    ax = fig.add_subplot(111)
    ax.set_title("Confusion Matrix")

    res = ax.imshow(np.array(norm_conf), cmap=plt.cm.Blues, interpolation="nearest")

    width, height = conf_arr.shape

    for x in range(width):
        for y in range(height):
            ax.annotate(
                str(conf_arr[x][y]),
                xy=(y, x),
                horizontalalignment="center",
                verticalalignment="center",
                size=25,
            )
    cb = fig.colorbar(res)
    alphabet = class_

    plt.xticks(range(width), alphabet[:width])
    plt.yticks(range(height), alphabet[:height])
    plt.savefig("confusion_matrix.png", format="png")
    plt.show()
    return
