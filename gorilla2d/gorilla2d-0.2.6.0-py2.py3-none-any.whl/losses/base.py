# Copyright (c) Gorilla-Lab. All rights reserved.
import torch.nn as nn

def _assert_no_grad(variable):
    assert not variable.requires_grad, \
        "nn criterions don't compute the gradient w.r.t. targets - please " \
        "mark these variables as volatile or not requiring gradients"

class _Loss(nn.Module):
    def __init__(self, size_average=True):
        super().__init__()
        self.size_average = size_average


class _WeightedLoss(_Loss):
    def __init__(self, weight=None, size_average=True):
        super().__init__(size_average)
        self.register_buffer('weight', weight)
