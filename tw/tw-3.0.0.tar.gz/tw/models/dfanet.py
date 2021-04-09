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
import torch
import torch.nn as nn
import torch.nn.functional as F
from .utils import _ConvBNReLU
from .xception import Enc, FCAttention, xception_a


class DFANet(nn.Module):
  def __init__(self, num_classes, arch='xception_a', **kwargs):
    super(DFANet, self).__init__()
    self.backbone = xception_a(**kwargs)

    self.enc2_2 = Enc(240, 48, 4, **kwargs)
    self.enc3_2 = Enc(144, 96, 6, **kwargs)
    self.enc4_2 = Enc(288, 192, 4, **kwargs)
    self.fca_2 = FCAttention(192, **kwargs)

    self.enc2_3 = Enc(240, 48, 4, **kwargs)
    self.enc3_3 = Enc(144, 96, 6, **kwargs)
    self.enc3_4 = Enc(288, 192, 4, **kwargs)
    self.fca_3 = FCAttention(192, **kwargs)

    self.enc2_1_reduce = _ConvBNReLU(48, 32, 1, **kwargs)
    self.enc2_2_reduce = _ConvBNReLU(48, 32, 1, **kwargs)
    self.enc2_3_reduce = _ConvBNReLU(48, 32, 1, **kwargs)
    self.conv_fusion = _ConvBNReLU(32, 32, 1, **kwargs)

    self.fca_1_reduce = _ConvBNReLU(192, 32, 1, **kwargs)
    self.fca_2_reduce = _ConvBNReLU(192, 32, 1, **kwargs)
    self.fca_3_reduce = _ConvBNReLU(192, 32, 1, **kwargs)
    self.conv_out = nn.Conv2d(32, num_classes, 1)

  def forward(self, x):
    # backbone
    stage1_conv1 = self.backbone.conv1(x)
    stage1_enc2 = self.backbone.enc2(stage1_conv1)
    stage1_enc3 = self.backbone.enc3(stage1_enc2)
    stage1_enc4 = self.backbone.enc4(stage1_enc3)
    stage1_fca = self.backbone.fca(stage1_enc4)
    stage1_out = F.interpolate(stage1_fca, scale_factor=4, mode='bilinear', align_corners=True) # nopep8

    # stage2
    stage2_enc2 = self.enc2_2(torch.cat([stage1_enc2, stage1_out], dim=1))
    stage2_enc3 = self.enc3_2(torch.cat([stage1_enc3, stage2_enc2], dim=1))
    stage2_enc4 = self.enc4_2(torch.cat([stage1_enc4, stage2_enc3], dim=1))
    stage2_fca = self.fca_2(stage2_enc4)
    stage2_out = F.interpolate(stage2_fca, scale_factor=4, mode='bilinear', align_corners=True) # nopep8

    # stage3
    stage3_enc2 = self.enc2_3(torch.cat([stage2_enc2, stage2_out], dim=1))
    stage3_enc3 = self.enc3_3(torch.cat([stage2_enc3, stage3_enc2], dim=1))
    stage3_enc4 = self.enc3_4(torch.cat([stage2_enc4, stage3_enc3], dim=1))
    stage3_fca = self.fca_3(stage3_enc4)

    stage1_enc2_decoder = self.enc2_1_reduce(stage1_enc2)
    stage2_enc2_docoder = F.interpolate(self.enc2_2_reduce(stage2_enc2), scale_factor=2, mode='bilinear', align_corners=True) # nopep8
    stage3_enc2_decoder = F.interpolate(self.enc2_3_reduce(stage3_enc2), scale_factor=4, mode='bilinear', align_corners=True) # nopep8
    fusion = stage1_enc2_decoder + stage2_enc2_docoder + stage3_enc2_decoder
    fusion = self.conv_fusion(fusion)

    stage1_fca_decoder = F.interpolate(self.fca_1_reduce(stage1_fca), scale_factor=4, mode='bilinear', align_corners=True) # nopep8
    stage2_fca_decoder = F.interpolate(self.fca_2_reduce(stage2_fca), scale_factor=8, mode='bilinear', align_corners=True) # nopep8
    stage3_fca_decoder = F.interpolate(self.fca_3_reduce(stage3_fca), scale_factor=16, mode='bilinear', align_corners=True) # nopep8
    fusion = fusion + stage1_fca_decoder + stage2_fca_decoder + stage3_fca_decoder

    out = self.conv_out(fusion)
    out = F.interpolate(out, scale_factor=4, mode='bilinear', align_corners=True)
    return out #tuple(outputs)
