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
r"""Facial Enhancement Network"""

import torch
from torch import nn


class Scale(nn.Module):
  def __init__(self, in_channels):
    super(Scale, self).__init__()
    self.weight = nn.Parameter(torch.ones(in_channels), requires_grad=True)

  def forward(self, x):
    return self.weight.reshape(1, -1, 1, 1) * x


class IMDBModule(nn.Module):
  def __init__(self, channels, mask=None):
    super(IMDBModule, self).__init__()
    assert channels % 4 == 0
    self.small = channels // 4
    self.large = self.small * 3
    self.conv1 = nn.Sequential(nn.Conv2d(channels, channels, 3, 1, 1), nn.ReLU())  # nopep8
    self.conv2 = nn.Sequential(nn.Conv2d(self.large, channels, 3, 1, 1), nn.ReLU())  # nopep8
    self.conv3 = nn.Sequential(nn.Conv2d(self.large, channels, 3, 1, 1), nn.ReLU())  # nopep8
    self.conv4 = nn.Sequential(nn.Conv2d(self.large, self.small, 3, 1, 1), nn.ReLU())  # nopep8
    self.conv5 = nn.Conv2d(channels, channels, 1, 1, 0)

  def forward(self, x):
    d1, r1 = torch.split(self.conv1(x), (self.small, self.large), dim=1)
    d2, r2 = torch.split(self.conv2(r1), (self.small, self.large), dim=1)
    d3, r3 = torch.split(self.conv3(r2), (self.small, self.large), dim=1)
    d4 = self.conv4(r3)
    res = self.conv5(torch.cat((d1, d2, d3, d4), dim=1))
    return x + res


class ResidualBlock(nn.Module):
  def __init__(self, channels, mask='IN'):
    super(ResidualBlock, self).__init__()
    if mask == 'IN':
      self.conv = nn.Sequential(
          nn.Conv2d(channels, channels, 3, 1, 1),
          nn.InstanceNorm2d(channels),
          nn.ReLU(inplace=True),
          nn.Conv2d(channels, channels, 3, 1, 1))
    elif mask == 'SCALE':
      self.conv = nn.Sequential(
          nn.Conv2d(channels, channels, 3, 1, 1),
          Scale(channels),
          nn.ReLU(inplace=True),
          nn.Conv2d(channels, channels, 3, 1, 1))
    elif mask == 'SCALE2':
      self.conv = nn.Sequential(
          nn.Conv2d(channels, channels, 3, 1, 1),
          Scale(channels),
          nn.ReLU(inplace=True),
          nn.Conv2d(channels, channels, 3, 1, 1),
          Scale(channels))
    elif mask == 'SCALE3':
      self.conv = nn.Sequential(
          nn.Conv2d(channels, channels, 3, 1, 1),
          nn.ReLU(inplace=True),
          nn.Conv2d(channels, channels, 3, 1, 1),
          Scale(channels))
    elif mask == 'BN':
      self.conv = nn.Sequential(
          nn.Conv2d(channels, channels, 3, 1, 1),
          nn.BatchNorm2d(channels),
          nn.ReLU(inplace=True),
          nn.Conv2d(channels, channels, 3, 1, 1))
    else:
      self.conv = nn.Sequential(
          nn.Conv2d(channels, channels, 3, 1, 1),
          nn.ReLU(inplace=True),
          nn.Conv2d(channels, channels, 3, 1, 1))

  def forward(self, x):
    fea = self.conv(x)
    return fea + x


class FENet(nn.Module):
  def __init__(self, channels=64):
    super(FENet, self).__init__()
    self.conv0 = nn.Conv2d(3, channels, 7, 1, 3)
    self.relu = nn.ReLU(inplace=True)
    blocks = []
    for _ in range(10):
      blocks.append(ResidualBlock(channels=channels, mask=None))
    self.block = nn.Sequential(*blocks)
    self.conv1 = nn.Conv2d(channels, 3, 7, 1, 3)

  def forward(self, x):
    f0 = self.conv0(x)
    fea = self.block(self.relu(f0))
    out = self.conv1(self.relu(f0 + fea))
    return out.tanh()


class OutBlock(nn.Module):
  def __init__(self, in_channels, conv_kernel_size, conv_stride, conv_pad, use_bias, lrelu_slope, output_scale, channels=64):
    super(OutBlock, self).__init__()
    self.conv2d_1 = nn.Conv2d(in_channels, channels, conv_kernel_size, conv_stride, padding=conv_pad, bias=use_bias)  # output channel num: channels # nopep8
    self.lrelu_1 = nn.LeakyReLU(lrelu_slope, inplace=True)
    self.conv2d_2 = nn.Conv2d(channels, 2, conv_kernel_size, conv_stride, padding=conv_pad, bias=use_bias)  # output channel num: 2 # nopep8
    self.tanh = nn.Tanh()
    self.output_scale = output_scale


class FENetWithBranch(nn.Module):
  def __init__(self, with_1x,
               with_2x,
               with_4x,
               in_channels=3,
               channels=64,
               num_blocks=[4, 2, 2, 2],  # base, 1x, 2x, 4x
               mask=None,
               block_type='residual'):
    super(FENetWithBranch, self).__init__()
    assert channels % 4 == 0
    assert block_type in ['residual', 'imdb']

    # output channel
    if in_channels == 1:
      out_channels = 1
    else:
      out_channels = 3

    if block_type.lower() == 'residual':
      block_fn = ResidualBlock
    elif block_type.lower() == 'imdb':
      block_fn = IMDBModule

    self.with_1x = with_1x
    self.with_2x = with_2x
    self.with_4x = with_4x

    num_base_block = num_blocks[0]
    num_1x_block = num_blocks[1]
    num_2x_block = num_blocks[2]
    num_4x_block = num_blocks[3]

    self.stem = nn.Conv2d(in_channels, channels, 7, 1, 3)
    self.relu = nn.ReLU(inplace=True)

    blocks = []
    for _ in range(num_base_block):
      blocks.append(block_fn(channels=channels, mask=mask))
    self.block_base = nn.Sequential(*blocks)

    if self.with_1x:
      blocks = []
      for _ in range(num_1x_block):
        blocks.append(block_fn(channels=channels, mask=mask))
      self.block_1x = nn.Sequential(*blocks)
      self.out1 = nn.Conv2d(channels, out_channels, 7, 1, 3)

    if self.with_2x:
      blocks = []
      for _ in range(num_2x_block):
        blocks.append(block_fn(channels=channels, mask=mask))
      self.block_2x = nn.Sequential(*blocks)
      self.block_2x_up = nn.PixelShuffle(2)
      self.out2 = nn.Conv2d(channels // 4, out_channels, 7, 1, 3)

    if self.with_4x:
      blocks = []
      for _ in range(num_4x_block):
        blocks.append(block_fn(channels=channels, mask=mask))
      self.block_4x = nn.Sequential(*blocks)
      self.block_4x_up = nn.PixelShuffle(4)
      self.out4 = nn.Conv2d(4, out_channels, 7, 1, 3)

  def forward(self, x):
    x = self.stem(x)
    base_x = self.block_base(self.relu(x))
    output = {}
    if self.with_1x:
      base_x = self.block_1x(self.relu(base_x))
      out_1x = self.relu(x + base_x)
      out_1x = self.out1(out_1x)
      output['1x'] = out_1x.tanh()
    if self.with_2x:
      base_x = self.block_2x(self.relu(base_x))
      out_2x = self.relu(self.block_2x_up(x + base_x))
      out_2x = self.out2(out_2x)
      output['2x'] = out_2x.tanh()
    if self.with_4x:
      base_x = self.block_4x(self.relu(base_x))
      out_4x = self.relu(self.block_4x_up(x + base_x))
      out_4x = self.out4(out_4x)
      output['4x'] = out_4x.tanh()
    return output
