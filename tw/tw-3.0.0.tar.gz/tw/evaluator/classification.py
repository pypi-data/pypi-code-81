# Copyright 2018 The KaiJIN Authors. All Rights Reserved.
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
from .base import Evaluator


class TopkEvaluator(Evaluator):

  def __init__(self, topk, offset=0):
    self.topk = [i + 1 for i in range(topk)]
    self.offset = offset
    self.metrics = []

  def reset(self):
    self.metrics.clear()

  def append(self, values):
    r"""values should be a confusion_matrix"""
    self.metrics.append(values)

  def compute(self, preds, targets):
    r"""Computes the precision@k for the specified values of k

    Args:
      preds: [N, C]
      targets: [N, ]

    Returns:
      list with shape(k): the correct percentage among N inputs.

    """
    maxk = max(self.topk)
    batch_size = targets.size(0)

    _, pred = preds.topk(maxk, 1, True, True)
    pred = self.offset + pred.t()
    correct = pred.eq(targets.view(1, -1).expand_as(pred))

    tops = []
    for k in self.topk:
      correct_k = correct[:k].view(-1).float().sum(0)
      tops.append(correct_k.mul_(100.0 / batch_size))
      
    return tops

  def TopN(self, n):
    result = 0.0
    for metric in self.metrics:
      result += metric[n - 1].cpu().item()
    return result / len(self.metrics)

  def Top1(self):
    return self.TopN(1)

  def Top5(self):
    return self.TopN(5)

  def accumulate(self):
    return {'top1': self.Top1(), 'top5': self.Top5(), }


class MultiLabelClsEvaluator(Evaluator):
  def __init__(self, topk, num_classes):
    self.topk = topk
    self.num_classes = num_classes
    self.metrics = []

  def reset(self):
    self.metrics.clear()

  def append(self, values):
    r"""values should be a confusion_matrix"""
    self.metrics.append(values)

  def compute(self, preds, targets):
    r"""Computes the precision@k for the specified values of k

    Arguments:
      preds: [N, C] float value range from 0 to 1
      targets: [N, C] long value 0 or 1

    Returns:
      list with shape(k): the correct percentage among N inputs.
    """
    device = preds.device
    preds = torch.where(preds > 0.5, torch.tensor(1).to(device), torch.tensor(0).to(device))

    tops = []
    for i in range(self.topk):
      acc = ((preds == targets).sum(dim=1) >= (self.num_classes - i)).sum()
      acc = acc.float() / preds.size(0)
      tops.append(acc)

    return tops

  def TopN(self, n):
    result = 0.0
    for metric in self.metrics:
      result += metric[n - 1].cpu().item()
    return result / len(self.metrics)

  def accumulate(self):
    acc = {}
    for i in range(self.topk):
      acc['top%d' % (i+1)] = self.TopN(i+1)
    return acc
