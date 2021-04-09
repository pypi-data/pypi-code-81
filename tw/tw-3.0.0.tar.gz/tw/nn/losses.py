# Copyright 2021 The KaiJIN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
r"""Losses collections
"""

import itertools
import math
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F

# for autograd
from torch.autograd.function import once_differentiable

try:
  from tw import _C
except ImportError:
  _C = None

#!<-----------------------------------------------------------------------------
#!<  Content Loss
#!<-----------------------------------------------------------------------------


class ContentLoss(nn.Module):

  def __init__(self, f=2):
    super(ContentLoss, self).__init__()
    self.f = f

  def forward(self, im_batch1, im_batch2):
    r"""im_batch1, im_batch2 should be in N C H W, or N C S H W shape
    """
    assert im_batch1.shape == im_batch2.shape

    # find channel dimension
    dims = len(im_batch1.shape)
    assert dims in (4, 5)

    # get mean L2 loss
    if self.f == 2:
      content_loss = (im_batch1 - im_batch2).power(2).sum(dim=1).mean()
    elif self.f == 1:
      content_loss = (im_batch1 - im_batch2).abs().sum(dim=1).mean()
    return content_loss


#!<-----------------------------------------------------------------------------
#!<  Angle Loss
#!<-----------------------------------------------------------------------------


class AngleLoss(nn.Module):
  def __init__(self, gamma=0):
    super(AngleLoss, self).__init__()
    self.gamma = gamma
    self.it = 0
    self.LambdaMin = 5.0
    self.LambdaMax = 1500.0
    self.lamb = 1500.0

  def forward(self, input, target):
    self.it += 1
    cos_theta, phi_theta = input
    target = target.view(-1, 1)  # size=(B,1)

    index = cos_theta.data * 0.0  # size=(B,Classnum)
    index.scatter_(1, target.data.view(-1, 1), 1)
    index = index.bool()
    index = torch.autograd.Variable(index)

    self.lamb = max(self.LambdaMin, self.LambdaMax/(1+0.1*self.it))
    output = cos_theta * 1.0  # size=(B,Classnum)
    output[index] -= cos_theta[index]*(1.0+0)/(1+self.lamb)
    output[index] += phi_theta[index]*(1.0+0)/(1+self.lamb)

    logpt = F.log_softmax(output)
    logpt = logpt.gather(1, target)
    logpt = logpt.view(-1)
    pt = torch.autograd.Variable(logpt.data.exp())

    loss = -1 * (1-pt)**self.gamma * logpt
    loss = loss.mean()

    return loss


#!<-----------------------------------------------------------------------------
#!< KL Loss with standard deviation
#!<-----------------------------------------------------------------------------

class KLStandardGaussianLoss(nn.Module):
  r""" -KL[q(x)|N(0, I)] Loss
  """

  def __init__(self):
    super(KLStandardGaussianLoss, self).__init__()

  def forward(self, mean: torch.Tensor, var: torch.Tensor):
    mean = mean.squeeze()
    var = var.squeeze()
    assert len(mean.shape) == 2 and mean.shape == var.shape
    assert isinstance(mean, torch.Tensor) and isinstance(var, torch.Tensor)
    return (-0.5 * (1 + var.log() - mean.pow(2) - var)).sum(dim=1).mean()


#!<-----------------------------------------------------------------------------
#!< Log Ratio Metric Learning Loss
#!<-----------------------------------------------------------------------------


class LogRatioMetricLoss(nn.Module):
  r"""Paper [CVPR 2019]:
    Title: Deep metric learning beyond binary supervision
    Author: S.Kim, M. Seo, I. Laptev et al.
  """

  def __init__(self, device):
    super(LogRatioMetricLoss, self).__init__()
    self.device = device

  def forward(self, features, labels):
    r"""dense triplet sample + log ratio loss

    Args:
      features: [N, num_feature] [0 ~ 1]
      labels: [N, num_classes] [0, 1]

    Returns:
      losses:

    """
    bs, num_feature = features.shape
    labels = labels.float()

    _i = torch.randperm(bs).to(self.device)
    _j = torch.randperm(bs).to(self.device)

    f_ai = (features - features[_i]).pow(2).sum(dim=1)
    f_aj = (features - features[_j]).pow(2).sum(dim=1)
    y_ai = (labels - labels[_i]).pow(2).sum(dim=1)
    y_aj = (labels - labels[_j]).pow(2).sum(dim=1)

    # dense sample
    inds = y_ai > torch.tensor(0.0).to(self.device)
    inds &= y_ai < y_aj
    f_ai = f_ai[inds]
    f_aj = f_aj[inds]
    y_ai = y_ai[inds]
    y_aj = y_aj[inds]

    # dense sample again for features
    inds = f_ai > torch.tensor(0.0).to(self.device)
    inds &= f_aj > torch.tensor(0.0).to(self.device)
    f_ai = f_ai[inds]
    f_aj = f_aj[inds]
    y_ai = y_ai[inds]
    y_aj = y_aj[inds]

    # compute dist
    d_part_1 = f_ai.log() - y_ai.log()
    d_part_2 = f_aj.log() - y_aj.log()
    log_ratio_loss = (d_part_1 - d_part_2).pow(2)

    if f_ai.size(0) == 0:
      loss = 0.0
    else:
      loss = log_ratio_loss.sum() / f_ai.size(0)

    return loss


#!<-----------------------------------------------------------------------------
#!< Peak Signal to Noise Ratio
#!<-----------------------------------------------------------------------------

class PSNRLoss(nn.Module):
  r"""Peak Signal to Noise Ratio
    reference: https://github.com/huster-wgm/Pytorch-metrics/blob/master/metrics.py
  """

  def __init__(self):
    super(PSNRLoss, self).__init__()

  @staticmethod
  def binarize(y_data, threshold):
    r"""

    Args:
      y_data : [float] 4-d tensor in [batch_size, channels, img_rows, img_cols]
      threshold : [float] [0.0, 1.0]

    Returns:
      4-d binarized y_data

    """
    y_data[y_data < threshold] = 0.0
    y_data[y_data >= threshold] = 1.0
    return y_data

  @staticmethod
  def psnr(y_pred, y_true, dim=1, threshold=None):
    r"""

    Args:
      y_true : 4-d ndarray in [batch_size, channels, img_rows, img_cols]
      y_pred : 4-d ndarray in [batch_size, channels, img_rows, img_cols]
      threshold : [0.0, 1.0]

    Returns:
      PSNR, larger the better

    """
    if threshold:
      y_pred = PSNRLoss.binarize(y_pred, threshold)
    mse = torch.mean((y_pred - y_true) ** 2)
    return 10 * torch.log10(1 / mse)

  def forward(self, y_pred, y_true, dim=1, threshold=None):
    return PSNRLoss.psnr(y_pred, y_true, dim, threshold)


#!<-----------------------------------------------------------------------------
#!<
#!<-----------------------------------------------------------------------------

class PixelPositionAwareLoss(nn.Module):
  r"""Pixel Position Aware Loss:
    Titel: F3Net: Fusion, Feedback and Focus for Salient Object Detection
    Reference: https://github.com/weijun88/F3Net
  """

  def __init__(self, gamma=5, side=15, reduction=None):
    super(PixelPositionAwareLoss, self).__init__()
    self.gamma = gamma
    self.side = side
    self.reduction = reduction

  @staticmethod
  def pixel_position_aware_loss(pred, mask, gamma=5, side=15, reduction='mean'):
    weit = 1 + gamma * torch.abs(F.avg_pool2d(mask, kernel_size=int(side * 2 + 1), stride=1, padding=side) - mask)  # nopep8
    wbce = F.binary_cross_entropy_with_logits(pred, mask, reduce='none')
    wbce = (weit * wbce).sum(dim=(2, 3)) / weit.sum(dim=(2, 3))
    pred = torch.sigmoid(pred)
    inter = ((pred * mask) * weit).sum(dim=(2, 3))
    union = ((pred + mask) * weit).sum(dim=(2, 3))
    wiou = 1 - (inter + 1) / (union - inter + 1)

    if reduction == 'mean':
      return (wbce + wiou).mean()
    elif reduction == 'sum':
      return (wbce + wiou).sum()
    else:
      return (wbce + wiou)

  def forward(self, pred, mask):
    return PixelPositionAwareLoss.pixel_position_aware_loss(
        pred, mask,
        gamma=self.gamma,
        side=self.side,
        reduction=self.reduction)


#!<-----------------------------------------------------------------------------
#!< Reliab Loss
#!<-----------------------------------------------------------------------------


class ReliabLoss(nn.Module):
  r"""Leveraging Implicit Relative Labeling-Importance Information for Effective Multi-label Learning

    * Note: the version is modifed ReliabLoss
    1. the diagonal value of W is not set to zero.
    2. emp loss (due to negative loss, change to)
      emp_pos = max(f(y0) - f(y), 0), if y is positive label
      emp_neg = max(f(y) - f(y0), 0), if y is negative label
      r = |Yi| / |non Yi|
      emp_loss = emp_pos + r * emp_neg

  """

  def __init__(self, device, tao=0.2, alpha=0.5):
    super(ReliabLoss, self).__init__()
    self.tao = tao
    self.alpha = alpha
    self.device = device
    self.kl_loss = nn.KLDivLoss(reduction='batchmean')

  def forward(self, images, preds, labels):
    r"""

    Args:
      images: [N, C, H, W] the last layer of backbone conv
        NOTE: require input should normalized to [0, 1]
      preds: [N, C] classification prediction
      labels: [N, C] classification groundtruth

    Returns:
      loss_reliab: reliab loss

    """
    bs, nclass = labels.shape

    # * construct similarity matrix
    Xi = images.reshape(bs, 1, -1)
    Xj = images.reshape(1, bs, -1)
    W = torch.exp(-0.5 * (Xi - Xj).mean(dim=2).pow(2))  # .fill_diagonal_(0)
    # print_matrix(W)

    # * construct labeling-importance matrix
    D = W.sum(dim=1)
    D = torch.diag(D)
    # print_matrix(D)
    P = D.sqrt() * W * D.sqrt()
    # print_matrix(P)

    I = torch.ones(bs, 1).to(self.device)
    phi = torch.cat([I * self.tao, labels], dim=1)

    # * construct label propagation
    I = torch.eye(bs).to(self.device)
    F = ((1.0 - self.alpha) * (I - self.alpha * P)).inverse()
    F = torch.mm(F, phi)

    # print_matrix(phi)
    # print_matrix(F)

    # * estimate RLI degree
    U = F / F.sum(dim=1, keepdim=True)
    # print_matrix(U)

    # * compute normalized Z*
    preds = preds.exp() / preds.exp().sum(dim=1, keepdim=True)
    # print_matrix(preds)

    # * compute KL-div
    loss_reliab_dis = self.kl_loss((preds + 1e-5).log(), U)
    # print(loss_reliab_dis)

    # * compute emp loss
    r = labels.sum(dim=1, keepdim=True) / (nclass - labels.sum(dim=1, keepdim=True))  # nopep8
    preds_y0 = preds[..., 0].unsqueeze_(-1)
    preds_wo_y0 = preds[..., 1:]
    # print_matrix(preds_wo_y0 - preds_y0)

    # * compute rel and irrel
    emp_rel = torch.relu((preds_y0 - preds_wo_y0)[labels == 1]).mean()
    emp_irrel = torch.relu((r * (preds_wo_y0 - preds_y0))[labels == 0]).mean()
    loss_reliab_emp = (emp_rel + emp_irrel) * bs

    return loss_reliab_dis, loss_reliab_emp


#!<-----------------------------------------------------------------------------
#!< SSIM Loss
#!<-----------------------------------------------------------------------------

class StructuralSimilarityLoss(torch.nn.Module):

  def __init__(self, window_size=11, size_average=True):
    super(StructuralSimilarityLoss, self).__init__()
    self.window_size = window_size
    self.size_average = size_average
    self.channel = 1
    self.window = StructuralSimilarityLoss.create_window(window_size, self.channel)

  @staticmethod
  def gaussian(window_size, sigma):
    gauss = torch.Tensor([math.exp(-(x - window_size//2)**2/float(2*sigma**2)) for x in range(window_size)])  # nopep8
    return gauss/gauss.sum()

  @staticmethod
  def create_window(window_size, channel):
    _1D_window = StructuralSimilarityLoss.gaussian(window_size, 1.5).unsqueeze(1)
    _2D_window = _1D_window.mm(_1D_window.t()).float().unsqueeze(0).unsqueeze(0)
    window = torch.autograd.Variable(_2D_window.expand(channel, 1, window_size, window_size).contiguous())  # nopep8
    return window

  @staticmethod
  def ssim(img1, img2, window, window_size, channel, size_average=True):
    mu1 = F.conv2d(img1, window, padding=window_size//2, groups=channel)
    mu2 = F.conv2d(img2, window, padding=window_size//2, groups=channel)

    mu1_sq = mu1.pow(2)
    mu2_sq = mu2.pow(2)
    mu1_mu2 = mu1*mu2

    sigma1_sq = F.conv2d(img1*img1, window, padding=window_size//2, groups=channel) - mu1_sq  # nopep8
    sigma2_sq = F.conv2d(img2*img2, window, padding=window_size//2, groups=channel) - mu2_sq  # nopep8
    sigma12 = F.conv2d(img1*img2, window, padding=window_size // 2, groups=channel) - mu1_mu2  # nopep8

    C1 = 0.01**2
    C2 = 0.03**2

    ssim_map = ((2*mu1_mu2 + C1)*(2*sigma12 + C2)) / ((mu1_sq + mu2_sq + C1)*(sigma1_sq + sigma2_sq + C2))  # nopep8

    if size_average:
      return ssim_map.mean()
    else:
      return ssim_map.mean(1).mean(1).mean(1)

  @staticmethod
  def structural_similarity(img1, img2, window_size=11, size_average=True):
    (_, channel, _, _) = img1.size()
    window = StructuralSimilarityLoss.create_window(window_size, channel)

    if img1.is_cuda:
      window = window.cuda(img1.get_device())
    window = window.type_as(img1)

    return StructuralSimilarityLoss.ssim(img1, img2, window, window_size, channel, size_average)

  def forward(self, img1, img2):
    r"""

    Args:
      img1: [N, C, H, W]
      img2: [N, C, H, W]

    Returns:
      ssim loss:

    """

    (_, channel, _, _) = img1.size()

    if channel == self.channel and self.window.data.type() == img1.data.type():
      window = self.window
    else:
      window = StructuralSimilarityLoss.create_window(self.window_size, channel)

      if img1.is_cuda:
        window = window.cuda(img1.get_device())
      window = window.type_as(img1)

      self.window = window
      self.channel = channel

    return StructuralSimilarityLoss.ssim(img1, img2, window, self.window_size, channel, self.size_average)


#!<-----------------------------------------------------------------------------
#!< Smooth L1 Loss
#!<-----------------------------------------------------------------------------

class SmoothL1Loss(nn.Module):
  r"""very similar to the smooth_l1_loss from pytorch, but with the extra
    beta parameter.
  """

  def __init__(self, beta=1./9, reduction=None):
    super(SmoothL1Loss, self).__init__()
    self.beta = beta
    self.reduction = reduction

  def forward(self, inputs, targets):
    n = torch.abs(inputs - targets)
    cond = n < self.beta
    loss = torch.where(cond, 0.5 * n ** 2 / self.beta, n - 0.5 * self.beta)
    return loss


#!<-----------------------------------------------------------------------------
#!<
#!<-----------------------------------------------------------------------------


# TODO: Use JIT to replace CUDA implementation in the future.
class _SigmoidFocalLoss(torch.autograd.Function):

  @staticmethod
  def forward(ctx, logits, targets, gamma, alpha):
    ctx.save_for_backward(logits, targets)
    num_classes = logits.shape[1]
    ctx.num_classes = num_classes
    ctx.gamma = gamma
    ctx.alpha = alpha
    losses = _C.sigmoid_focalloss_forward(logits, targets, num_classes, gamma, alpha)
    return losses

  @staticmethod
  @once_differentiable
  def backward(ctx, d_loss):
    logits, targets = ctx.saved_tensors
    num_classes = ctx.num_classes
    gamma = ctx.gamma
    alpha = ctx.alpha
    d_loss = d_loss.contiguous()
    d_logits = _C.sigmoid_focalloss_backward(logits, targets, d_loss, num_classes, gamma, alpha)
    return d_logits, None, None, None, None


def sigmoid_focal_loss_cpu(logits, targets, gamma, alpha):
  num_classes = logits.shape[1]
  gamma = gamma[0]
  alpha = alpha[0]
  dtype = targets.dtype
  device = targets.device
  class_range = torch.arange(1, num_classes+1, dtype=dtype, device=device).unsqueeze(0)
  t = targets.unsqueeze(1)
  p = torch.sigmoid(logits)
  term1 = (1 - p) ** gamma * torch.log(p)
  term2 = p ** gamma * torch.log(1 - p)
  return -(t == class_range).float() * term1 * alpha - ((t != class_range) * (t >= 0)).float() * term2 * (1 - alpha)


class SigmoidFocalLoss(nn.Module):
  def __init__(self, gamma, alpha):
    super(SigmoidFocalLoss, self).__init__()
    self.gamma = gamma
    self.alpha = alpha

  def forward(self, input, target):
    if input.is_cuda:
      loss_func = _SigmoidFocalLoss.apply
    else:
      loss_func = sigmoid_focal_loss_cpu

    loss = loss_func(input.float(), target.int(), self.gamma, self.alpha)
    return loss.sum(dim=1)

  def __repr__(self):
    tmpstr = self.__class__.__name__ + "("
    tmpstr += "gamma=" + str(self.gamma)
    tmpstr += ", alpha=" + str(self.alpha)
    tmpstr += ")"
    return tmpstr


#!<-----------------------------------------------------------------------------
#!< OSDH Loss
#!<-----------------------------------------------------------------------------


class OrderSensitiveMetricLoss(nn.Module):
  r"""Order-Sensitive Deep Hashing for Multimorbidity Medical Image Retrieval.
  """

  def __init__(self, device, p=3, rho=5, alpha=0.5, ri_method='hamming'):
    super(OrderSensitiveMetricLoss, self).__init__()
    self.p = p
    self.rho = rho
    self.ri_method = ri_method
    self.alpha = alpha
    self.device = device

  def dist_hamming(self, x, y):
    r""" hamming distance between x and y.

    Where, dist = x * y^T

    Examples:
      1 1 0 0 1 1 1 1 0 0 0 0 0 1 1 0
      1 1 0 0 1 1 1 1 0 0 0 0 0 1 1 0
      0 0 2 0 1 0 2 0 0 0 0 0 0 1 1 0
      0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0
      1 1 1 0 4 1 3 1 0 0 0 1 0 1 1 0
      1 1 0 0 1 1 1 1 0 0 0 0 0 1 1 0
      1 1 2 0 3 1 4 1 0 0 0 0 0 2 2 0
      1 1 0 0 1 1 1 2 0 0 0 0 0 1 1 1
      0 0 0 0 0 0 0 0 2 0 0 0 1 0 0 1
      0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0
      0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0
      0 0 0 0 1 0 0 0 0 0 0 1 0 0 0 0
      0 0 0 0 0 0 0 0 1 0 0 0 1 0 0 1
      1 1 1 0 1 1 2 1 0 0 0 0 0 2 2 0

    Arguments:
      x: [N, num_classes]
      y: [M, num_classes]

    Returns:
      dist: [N, M]

    """
    return torch.mm(x, y.t()).float()

  def dist_importance_hamming(self, x, y, importance):
    r""" hamming importance between x, y

    where:
      \sum{m=0->13}(sum(ri_m, rj_m))/2, m in label * label > 0

    """
    x1 = torch.unsqueeze(x, dim=1)
    y1 = torch.unsqueeze(y, dim=0)
    x_imp = x1 * importance.unsqueeze(dim=1)
    y_imp = y1 * importance.unsqueeze(dim=0)
    dist = x_imp + y_imp
    dist[x1 * y1 == 0] = 0.0
    dist = dist.sum(dim=2) / 2.0
    return dist

  def dist_min_hamming(self, x, y, importance):
    r""" hamming importance with min area

    where:
      \sum{m=0->13}(min(ri_m, rj_m)), m in label * label > 0

    """
    x1 = torch.unsqueeze(x, dim=1)
    y1 = torch.unsqueeze(y, dim=0)
    x_imp = x1 * importance.unsqueeze(dim=1)
    y_imp = y1 * importance.unsqueeze(dim=0)
    dist = torch.min(x_imp, other=y_imp)
    dist[x1 * y1 == 0] = 0.0
    dist = dist.sum(dim=2)
    # print_matrix(dist)
    # print_matrix(self.dist_hamming(x, y))
    # print_matrix(self.dist_importance_hamming(x, y, importance))
    return dist

  def dist_similarity(self, x, y, num_hash_code):
    r"""cosine similarity distance between x and y.

    Examples:
      00.00 11.00 13.91 14.00 11.03
      11.00 00.00 10.90 11.00 08.04
      13.91 10.90 00.18 12.09 14.94
      14.00 11.00 12.09 00.00 14.96
      11.03 08.04 14.94 14.96 00.07

    Arguments:
      x: [N, num_classes]
      y: [M, num_classes]

    Returns:
      dist: [N, M]

    """
    return 0.5 * (num_hash_code - torch.mm(x, y.t()))

  def forward(self, hash_features, labels, preds=None):
    r"""compute order sensitive loss

    Docs:
    (1) Sample Routine:
      For each sample (idx), we first compute its hamming distance between others,
      then search for triplet (idx, i) and (idx, j) requires:
        $ hamming_dist(idx, i) > hamming_dist(idx, j)

      Note: maybe existing multiple (i) for multiple sample with same hamming dist
      For example:
        hamming(idx): 2, 1, 1, 0
        pairs: [idx, 2, 1], [idx, 2, 1], [idx, 2, 0]
               [idx, 1, 0], [idx, 1, 0]

    (2) Compute Loss:
      D(x, y) = 0.5 * (num_hash_code - dot<x, y>)
      Z(idx) = \sum{(2^ri - 2^rj)}
      L(idx) = (2^ri - 2^rj / Z(idx))max(0, D(bq, bi) - D(bq, bj) + rho)

    Arguments:
      hash_features: [N, hash_code] (0 ~ 1)
      labels: [N, num_classes] [0, 1]

    Returns:
      losses

    """
    # * compute similarity dist
    bs, num_hash = hash_features.shape

    with torch.no_grad():
      # * compute hamming dist, dist_gt should be [bs, bs] shape
      if self.ri_method == 'hamming':
        dist_gt = self.dist_hamming(labels, labels)
      elif self.ri_method == 'importance_hamming':
        dist_gt = self.dist_importance_hamming(labels, labels, preds)
      elif self.ri_method == 'min_hamming':
        dist_gt = self.dist_min_hamming(labels, labels, preds)
      else:
        raise NotImplementedError(self.ri_method)

      # * sample i, j in terms of q
      dist_gt = dist_gt.cpu()
      positions = []
      for idx in range(bs):
        dist_gt[idx, idx] = 0  # remove out self match
        r_val, r_ind = dist_gt[idx].sort(descending=True)

        unique_sets = r_val.unique()
        unique_size = len(unique_sets)
        position = []
        # print(unique_sets)
        if unique_size > 1:
          for i in range(unique_size - 1, -1, -1):
            ri_inds = r_ind[r_val == unique_sets[i]]
            for j in range(i - 1, -1, -1):
              rj_inds = r_ind[r_val == unique_sets[j]]
              for _i, _j in itertools.product(ri_inds, rj_inds):
                position.append([_i, _j])

        # * record current sample position and rij2
        positions.append(torch.tensor(position).to(self.device))

    #!< CUDA AREA
    # * dist sim between hash features
    dist_sim = self.dist_similarity(hash_features, hash_features, num_hash)
    dist_gt = dist_gt.to(self.device)
    dist_gt2 = 2 ** dist_gt

    # * compute loss
    losses = torch.zeros(1).to(self.device)
    counts = 0
    for idx, pos in enumerate(positions):

      # * number of sample, element of tuple
      n = pos.shape[0]

      # * skip empty
      if n == 0:
        continue

      # * index
      pos_i = pos[:, 0].long()
      pos_j = pos[:, 1].long()

      # * fetch similarity
      d_qi = dist_sim[idx][pos_i]
      d_qj = dist_sim[idx][pos_j]
      d_ri = dist_gt[idx][pos_i]
      d_rj = dist_gt[idx][pos_j]

      # * compute left term: 1/z * (2^ri - 2^rj)
      rij2 = dist_gt2[idx][pos_i] - dist_gt2[idx][pos_j]
      inv_z = 1.0 / rij2.sum()

      # * compute right term
      triplet_loss = torch.relu(d_qi - d_qj + self.rho)

      # * total
      loss = inv_z * rij2 * triplet_loss

      # * select parts
      if self.ri_method == 'hamming':
        loss = loss[(d_ri - d_rj) <= 2]
      elif self.ri_method == 'min_hamming':
        loss = loss[(d_ri - d_rj) > 0.7]

      losses += loss.sum()
      counts += loss.shape[0]

    if counts == 0:
      return losses
    return losses / counts


#!<-----------------------------------------------------------------------------
#!< Mutual Channel Loss
#!<-----------------------------------------------------------------------------

class MutualChannelLoss(nn.Module):
  r"""Paper:
    Title: The Devil is in the Channels: Mutual-Channel Loss for Fine-Grained Image Classification
    Author: Beijing University of Posts and Telecommunications
  """

  def __init__(self, device, cnum=20, reduction=None):
    super(MutualChannelLoss, self).__init__()
    from tw.nn.pooling import ChannelMaxPool

    self.cnum = cnum
    self.reduction = reduction
    self.ccmp = ChannelMaxPool(kernel_size=cnum, stride=cnum)
    self.gap = nn.AdaptiveAvgPool2d(output_size=(1, 1))
    self.device = device

  def forward(self, features, labels):
    r"""MC-Loss boost the backbone extractor ability.

    Arguments:
      features: [N, C, H, W] the last layer of backbone conv
      labels: [N, C] classification groundtruth

    Returns:
      loss_dis: discriminitive loss
      loss_div: diverse loss

    """
    assert len(features) == 4
    n, c, h, w = features.shape

    # dynamic generate mask
    with torch.no_grad():
      submask = [1] * (self.cnum - int(self.cnum / 2))
      submask += [0] * int(self.cnum / 2)
      mask = []
      for i in range(self.num_classes):
        random.shuffle(submask)
        mask += submask
      mask = [mask for i in range(self.bs)]
      mask = torch.tensor(mask).float()
      mask = mask.reshape(self.bs, self.num_classes * self.cnum, 1, 1)
      mask = mask.to(self.device)

    # diveristy branch
    b1 = features.resize(n, c, h * w)
    b1 = b1.softmax(dim=2)
    b1 = b1.resize(n, c, h, w)
    b1 = self.ccmp(b1)
    b1 = b1.resize(n, self.num_classes, h * w)
    loss_div = 1.0 - 1.0 * b1.sum(dim=2).mean() / self.cnum

    # discriminted branch
    b0 = features * mask
    b0 = self.ccmp(b0)
    b0 = self.gap(b0)
    b0 = torch.flatten(b0, 1).sigmoid()
    loss_dis = nn.functional.binary_cross_entropy(b0, labels)

    return loss_dis, loss_div


#!<-----------------------------------------------------------------------------
#!< Label Smooth Loss
#!<-----------------------------------------------------------------------------

class LabelSmoothLoss(nn.modules.loss._WeightedLoss):

  def __init__(self, weight=None, reduction='mean', smoothing=0.0):
    super().__init__(weight=weight, reduction=reduction)
    self.smoothing = smoothing
    self.weight = weight
    self.reduction = reduction

  @staticmethod
  def _smooth_one_hot(targets: torch.Tensor, n_classes: int, smoothing=0.0):
    assert 0 <= smoothing < 1
    with torch.no_grad():
      targets = torch.empty(size=(targets.size(0), n_classes), device=targets.device) \
          .fill_(smoothing / (n_classes-1)) \
          .scatter_(1, targets.data.unsqueeze(1), 1.-smoothing)
    return targets

  def forward(self, inputs, targets):
    r"""

    Args:
      inputs:
      targets:

    Returns:
      loss:

    """
    targets = LabelSmoothLoss._smooth_one_hot(targets, inputs.size(-1), self.smoothing)
    lsm = F.log_softmax(inputs, -1)

    if self.weight is not None:
      lsm = lsm * self.weight.unsqueeze(0)

    loss = -(targets * lsm).sum(-1)

    if self.reduction == 'sum':
      loss = loss.sum()
    elif self.reduction == 'mean':
      loss = loss.mean()

    return loss


#!<-----------------------------------------------------------------------------
#!< Energy based loss
#!<-----------------------------------------------------------------------------


class EBMLoss(nn.Module):
  r"""Energy Based Loss"""

  def __init__(self, num_samples,
               gmm_stds,
               method='nce',
               **kwargs):
    super(EBMLoss, self).__init__()
    from tw.nn.random import GMMSampler

    self.num_samples = num_samples
    self.sampler = GMMSampler(gmm_stds)

    # select method
    if method == 'mcis':
      self.ebm_loss = self.mcis
    elif method == 'mcis_hybrid':
      self.ebm_loss = self.mcis_hybrid
    elif method == 'kldis':
      self.prior_dist = torch.distributions.normal.Normal(loc=0.0, scale=0.025)
      self.ebm_loss = self.kldis
    elif method == 'dsm':
      pass
    elif method == 'mcmc':
      self.step = 16  # Langevin dynamics
      self.alpha = 0.05
      self.ebm_loss = self.mcmc
    elif method == 'nce':
      self.ebm_loss = self.nce
    elif method == 'nce+':
      pass
    elif method == 'sm':
      pass
    else:
      raise NotImplementedError(method)

  def forward(self, predictor, features, labels, device):
    r"""Eenergy-based Loss

      Args:
        features: [N, C]
        labels: [N, ]

      Returns:
        loss:
    """
    features = features.squeeze()
    labels = labels.squeeze()

    if features.dim() == 4:  # [N, C, H, W]
      features = features.mean(dim=(2, 3))
    elif features.dim() == 3:
      features = features.mean(dim=2)

    assert features.dim() == 2
    assert len(labels.shape) == 1

    labels = labels.float().unsqueeze(1).to(device)

    return self.ebm_loss(predictor, features, labels, device)

  def mcis(self, predictor, features, labels, device):
    r"""Monte-Carlo Importance Sampler: Negative Log-Likehood Minimize"""
    # predictor
    targets = labels  # [bs, 1]
    scores_gt = predictor(features, targets).squeeze()  # [bs, ]

    # sample center value and dist
    center, prob = self.sampler(self.num_samples)  # [k, 1], [k, ]
    prob = prob.unsqueeze(0).to(device)  # [1, k]
    center = center.to(device).squeeze(1).unsqueeze(0)  # [1, k]

    # offset to y
    y = targets + center  # [bs, k]
    score_samples = predictor(features, y)  # [bs, k]

    # logz
    logz = (score_samples.exp() / prob).mean(dim=1).log()  # [bs, ]

    # sum
    loss = torch.mean(logz - scores_gt)

    return loss

  def mcis_hybrid(self, predictor, features, labels, device):
    r"""-log(e^f(x,y) / sum(e^f(x_i, y)))"""
    scores_gt = predictor(features, labels).squeeze()  # [bs, ]
    bs = scores_gt.size(0)
    return torch.stack([predictor(features, labels[i].repeat(bs, 1)).logsumexp(dim=0) - scores_gt for i in range(bs)], dim=0).mean()  # nopep8

  def kldis(self, predictor, features, labels, device):
    r"""KL Divergence with Importance Sampling"""
    # predictor
    targets = labels  # [bs, 1]
    # scores_gt = predictor(features, targets).squeeze()  # [bs, ]

    # sample center value and dist
    center, prob = self.sampler(self.num_samples)  # [k, 1], [k, ]
    prob = prob.unsqueeze(0).to(device)  # [1, k]
    center = center.to(device).squeeze(1).unsqueeze(0)  # [1, k]

    # p(y|yi) from Normal distribution
    # we sample from center is identical to center + offset
    p_y_samples = self.prior_dist.log_prob(center).exp().to(device)  # [1, k]

    # offset to y
    y = targets + center  # [bs, k]
    score_samples = predictor(features, y)  # [bs, k]

    # logz
    logz = (score_samples.exp() / prob).mean(dim=1).log()  # [bs, ]

    # sum
    loss = torch.mean(logz - (score_samples * (p_y_samples / prob)).mean(dim=1))  # nopep8

    return loss

  def nce(self, predictor, features, labels, device):
    r"""Noise Contrastive Estimation
    """
    # predictor
    targets = labels  # [bs, 1]
    scores_gt = predictor(features, targets).squeeze()  # [bs, ]

    # sample center value and dist
    center, prob = self.sampler(self.num_samples)  # [k, 1], [k, ]
    prob0 = self.sampler.gmm_density_centered(torch.zeros_like(center), self.sampler.stds)  # nopep8

    # to device
    prob0 = (prob0[0] * torch.ones(scores_gt.size(0))).to(device)  # [k, ]
    prob = prob.unsqueeze(0).to(device)  # [1, k]
    center = center.to(device).squeeze(1).unsqueeze(0)  # [1, k]

    # offset to y
    y = targets + center  # [bs, k]
    score_samples = predictor(features, y)  # [bs, k]

    # sum
    up = scores_gt - prob0.log()
    down = up.exp() + torch.sum((score_samples - prob.log()).exp(), dim=1)
    loss = - torch.mean(up - torch.log(down))

    return loss

  def mcmc(self, predictor, features, labels, device):
    r"""ML with MCMC"""
    # predictor
    targets = labels  # [bs, 1]
    scores_gt = predictor(features, targets).squeeze()  # [bs, ]

    # sample center value and dist
    center, prob = self.sampler(self.num_samples)  # [k, 1], [k, ]
    prob = prob.unsqueeze(0).to(device)  # [1, k]
    center = center.to(device).squeeze(1).unsqueeze(0)  # [1, k]

    # offset to y
    y = targets + center  # [bs, k]

    # mcmc
    for _ in range(self.step):
      y.requires_grad_(True)
      scores = predictor(features, y)
      grad_y = torch.autograd.grad(scores.sum(), y, create_graph=True)[0]
      y = y + (0.5 * self.alpha ** 2) * grad_y + self.alpha * torch.randn(y.size()).to(device)  # nopep8
      y.detach_()

    # select last one
    scores = predictor(features, y)
    loss = torch.mean(torch.mean(scores, dim=1) - scores_gt)

    return loss
