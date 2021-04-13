# Copyright (c) Gorilla-Lab. All rights reserved.
import torch
import torch.nn as nn
from torch.autograd import Function

from .base import _WeightedLoss
from .utils import guassian_kernel


class MMDDomain(_WeightedLoss):
    # TODO: need to check its correctness

    def __init__(self, weight=None, size_average=True, kernel_mul=2.0, kernel_num=5, fix_sigma=None, mode="Linear"):
        super(MMDDomain, self).__init__(weight, size_average)
        self.kernel_mul = kernel_mul
        self.kernel_num = kernel_num
        self.fix_sigma = fix_sigma
        self.mode = mode

    def forward(self, input_s, input_t):
        batch_size = int(input_s.size()[0])
        kernels = guassian_kernel(input_s, input_t, kernel_mul=self.kernel_mul, kernel_num=self.kernel_num, fix_sigma=self.fix_sigma)
        if self.mode == "Full":
            loss1 = 0
            for s1 in range(batch_size):
                for s2 in range(s1 + 1, batch_size):
                    t1, t2 = s1 + batch_size, s2 + batch_size
                    loss1 += kernels[s1, s2] + kernels[t1, t2]
            loss1 = loss1 / float(batch_size * (batch_size - 1) / 2)

            loss2 = 0
            for s1 in range(batch_size):
                for s2 in range(batch_size):
                    t1, t2 = s1 + batch_size, s2 + batch_size
                    loss2 -= kernels[s1, t2] + kernels[s2, t1]
            loss2 = loss2 / float(batch_size * batch_size)
            return loss1 + loss2

        elif self.mode == "Linear":
            loss = 0
            for i in range(batch_size):
                s1, s2 = i, (i + 1) % batch_size
                t1, t2 = s1 + batch_size, s2 + batch_size
                loss += kernels[s1, s2] + kernels[t1, t2]
                loss -= kernels[s1, t2] + kernels[s2, t1]
            return loss / float(batch_size)


class CenterlossFunction(Function):
    # TODO: need to check its correctness

    @staticmethod
    def forward(ctx, feature, label, centers):
        ctx.save_for_backward(feature, label, centers)
        centers_pred = centers.index_select(0, label.long())
        return (feature - centers_pred).pow(2).sum(1).sum(0) / 2.0

    @staticmethod
    def backward(ctx, grad_output):
        feature, label, centers = ctx.saved_variables
        grad_feature = feature - centers.index_select(0, label.long())  # Eq. 3

        # init every iteration
        counts = torch.ones(centers.size(0))
        grad_centers = torch.zeros(centers.size())
        if feature.is_cuda:
            counts = counts.cuda()
            grad_centers = grad_centers.cuda()

        # Eq. 4 || need optimization !! To be vectorized, but how?
        for i in range(feature.size(0)):
            j = int(label[i].data[0])
            counts[j] += 1
            grad_centers[j] += (centers.data[j] - feature.data[i])
        grad_centers = grad_centers / counts.view(-1, 1)

        return grad_feature * grad_output, None, grad_centers


class CenterLoss(nn.Module):
    # TODO: need to check its correctness

    def __init__(self, num_classes, feat_dim):
        super(CenterLoss, self).__init__()
        self.num_classes = num_classes
        self.feat_dim = feat_dim
        self.centers = nn.Parameter(torch.randn(num_classes, feat_dim))
        self.centerlossfunction = CenterlossFunction.apply

    def forward(self, y, feat):
        # To squeeze the Tensor
        batch_size = feat.size(0)
        feat = feat.view(batch_size, 1, 1, -1).squeeze()
        # To check the dim of centers and features
        if feat.size(1) != self.feat_dim:
            raise ValueError("Center's dim: {0} should be equal to input feature's dim: {1}".format(self.feat_dim,feat.size(1)))
        return self.centerlossfunction(feat, y, self.centers)
