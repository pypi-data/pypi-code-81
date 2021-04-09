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
r"""attention blocks
"""

import torch
import torch.nn as nn
from torch.autograd.function import once_differentiable

try:
  from tw import _C
except ImportError:
  _C = None

#!<-----------------------------------------------------------------------------
#!< PSA Block
#!<-----------------------------------------------------------------------------


class _PSACollect(torch.autograd.Function):

  @staticmethod
  def forward(ctx, hc):
    out = _C.psa_forward(hc, 1)
    ctx.save_for_backward(hc)
    return out

  @staticmethod
  @once_differentiable
  def backward(ctx, dout):
    hc = ctx.saved_tensors
    dhc = _C.psa_backward(dout, hc[0], 1)
    return dhc


class _PSADistribute(torch.autograd.Function):

  @staticmethod
  def forward(ctx, hc):
    out = _C.psa_forward(hc, 2)
    ctx.save_for_backward(hc)
    return out

  @staticmethod
  @once_differentiable
  def backward(ctx, dout):
    hc = ctx.saved_tensors
    dhc = _C.psa_backward(dout, hc[0], 2)
    return dhc


psa_collect = _PSACollect.apply
psa_distribute = _PSADistribute.apply


class CollectAttention(nn.Module):
  """Collect Attention Generation Module"""

  def __init__(self):
    super(CollectAttention, self).__init__()

  def forward(self, x):
    out = psa_collect(x)
    return out


class DistributeAttention(nn.Module):
  """Distribute Attention Generation Module"""

  def __init__(self):
    super(DistributeAttention, self).__init__()

  def forward(self, x):
    out = psa_distribute(x)
    return out
