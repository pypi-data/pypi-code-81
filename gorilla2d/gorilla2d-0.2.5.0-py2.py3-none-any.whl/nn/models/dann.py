# Copyright (c) Gorilla-Lab. All rights reserved.
import numpy as np

import torch
import torch.nn as nn
from torch.autograd import Function
from gorilla.nn import resnet

from ..modules.dann import Extractor, Class_classifier, Domain_classifier, Bottleneck

class DANN(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        if cfg.arch == "resnet18" or cfg.arch == "resnet34":
            feature_dim = 512
        elif cfg.arch == "resnet50":
            feature_dim = 2048
        else:
            raise NotImplementedError(cfg.arch)

        bottleneck_dim = cfg.get("bottleneck_dim", 256)
        self.G_f = Extractor(cfg)
        self.G_b = Bottleneck(feature_dim, bottleneck_dim)
        self.G_y = Class_classifier(bottleneck_dim, num_classes=cfg.num_classes) # 512 for ResNet18 and 32, 2048 for ResNet50
        self.G_d = Domain_classifier(bottleneck_dim, hidden_size=1024)
        if torch.cuda.is_available():
            self.G_f = self.G_f.cuda()
            self.G_b = self.G_b.cuda()
            self.G_y = self.G_y.cuda()
            self.G_d = self.G_d.cuda()
        self.gamma = cfg.gamma
        self.max_iters = cfg.pop("max_iters", cfg.epochs * cfg.iters_per_epoch)

    def forward(self, source_data, target_data, cur_iter):
        feature_source = self.G_b(self.G_f(source_data))
        feature_target = self.G_b(self.G_f(target_data))

        # compute the category output
        cate_output_source = self.G_y(feature_source)
        cate_output_target = self.G_y(feature_target)

        # compute the domain output
        p = float(cur_iter) / self.max_iters
        constant = 2. / (1. + np.exp(-self.gamma * p)) - 1
        domain_output_source = self.G_d(feature_source, constant)
        domain_output_target = self.G_d(feature_target, constant)

        return dict(cate_src = cate_output_source,
                    cate_tgt = cate_output_target,
                    domain_src = domain_output_source,
                    domain_tgt = domain_output_target)

    def forward_test(self, target_data):
        feature_target = self.G_b(self.G_f(target_data))
        cate_output_target = self.G_y(feature_target)

        return dict(cate_tgt = cate_output_target)
