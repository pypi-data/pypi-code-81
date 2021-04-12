# modify from https://github.com/thuml/Transfer-Learning-Library
import torch
import torch.nn as nn


class EntropyMinimumLoss(nn.Module):
    r"""Entropy of N predictions :math:`(p_1, p_2, ..., p_N)`.
    The definition is:

    .. math::
        d(p_1, p_2, ..., p_N) = -\dfrac{1}{K} \sum_{k=1}^K \log \left( \dfrac{1}{N} \sum_{i=1}^N p_{ik} \right)

    where K is number of classes.

    Parameters:
        - **pred** (tensor): Classifier predictions. Expected to contain raw, normalized scores for each class
    """

    def __init__(self):
        super().__init__()

    def forward(self, pred: torch.Tensor) -> torch.Tensor:

        return -torch.mean(torch.log(torch.mean(pred, 0) + 1e-6))


class ClassifierDiscrepancyLoss(nn.Module):
    r"""The `Classifier Discrepancy` in `Maximum Classiﬁer Discrepancy for Unsupervised Domain Adaptation <https://arxiv.org/abs/1712.02560>`_.
    The classfier discrepancy between predictions :math:`p_1` and :math:`p_2` can be described as:

    .. math::
        d(p_1, p_2) = \dfrac{1}{K} \sum_{k=1}^K | p_{1k} - p_{2k} |,

    where K is number of classes.

    Parameters:
        - **pred1** (tensor): Classifier predictions :math:`p_1`. Expected to contain raw, normalized scores for each class
        - **pred2** (tensor): Classifier predictions :math:`p_2`
    """

    def __init__(self):
        super().__init__()

    def forward(self, pred1: torch.Tensor, pred2: torch.Tensor) -> torch.Tensor:

        return torch.mean(torch.abs(pred1 - pred2))
