# Copyright (c) Gorilla-Lab. All rights reserved.
import torch

def guassian_kernel(source, target, kernel_mul=2.0, kernel_num=5, fix_sigma=None):
    n_samples = int(source.size()[0]) + int(target.size()[0])
    total = torch.cat([source, target], dim = 0)
    total0 = total.unsqueeze(0).expand(int(total.size(0)), int(total.size(0)), int(total.size(1)))
    total1 = total.unsqueeze(1).expand(int(total.size(0)), int(total.size(0)), int(total.size(1)))
    L2_distance = ((total0 - total1) ** 2).sum(2)
    if fix_sigma:
        bandwidth = fix_sigma
    else:
        bandwidth = torch.sum(L2_distance.data) / (n_samples ** 2 - n_samples)
    bandwidth /= kernel_mul ** (kernel_num // 2)
    bandwidth_list = [bandwidth * (kernel_mul ** i) for i in range(kernel_num)]
    kernel_val = [torch.exp(-L2_distance / bandwidth_temp) for bandwidth_temp in bandwidth_list]
    # return sum(kernel_val) / len(kernel_val)
    return sum(kernel_val)

def mixup_criterion(criterion, pred, y_a, y_b, lamda):
    r"""
    Criterion for method using mixup trick. Because the mixed label has two
    non-zero elements, so the formula of loss also contain two items.
    """
    return lamda * criterion(pred, y_a) + (1 - lamda) * criterion(pred, y_b)
