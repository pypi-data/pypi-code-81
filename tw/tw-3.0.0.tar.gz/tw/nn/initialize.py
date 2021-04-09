# Copyright 2017 The KaiJIN Authors. All Rights Reserved.
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

from torch import nn


def constant(module, val, bias=0):
  nn.init.constant_(module.weight, val)
  if hasattr(module, 'bias') and module.bias is not None:
    nn.init.constant_(module.bias, bias)


def xavier(module, gain=1, bias=0, distribution='normal'):
  assert distribution in ['uniform', 'normal']
  if distribution == 'uniform':
    nn.init.xavier_uniform_(module.weight, gain=gain)
  else:
    nn.init.xavier_normal_(module.weight, gain=gain)
  if hasattr(module, 'bias') and module.bias is not None:
    nn.init.constant_(module.bias, bias)


def normal(module, mean=0, std=1, bias=0):
  nn.init.normal_(module.weight, mean, std)
  if hasattr(module, 'bias') and module.bias is not None:
    nn.init.constant_(module.bias, bias)


def uniform(module, a=0, b=1, bias=0):
  nn.init.uniform_(module.weight, a, b)
  if hasattr(module, 'bias') and module.bias is not None:
    nn.init.constant_(module.bias, bias)


def kaiming(module, a=0, mode='fan_out', nonlinearity='relu', bias=0, distribution='normal'):
  assert distribution in ['uniform', 'normal']
  if distribution == 'uniform':
    nn.init.kaiming_uniform_(module.weight, a=a, mode=mode, nonlinearity=nonlinearity)
  else:
    nn.init.kaiming_normal_(module.weight, a=a, mode=mode, nonlinearity=nonlinearity)
  if hasattr(module, 'bias') and module.bias is not None:
    nn.init.constant_(module.bias, bias)


def caffe2_xavier(module, bias=0):
  # `XavierFill` in Caffe2 corresponds to `kaiming_uniform_` in PyTorch
  # Acknowledgment to FAIR's internal code
  kaiming(module, a=1, mode='fan_in', nonlinearity='leaky_relu', distribution='uniform')
