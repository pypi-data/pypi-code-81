import torch
import torch.nn as nn
from pyro.distributions.transforms import AffineAutoregressive, BlockAutoregressive, AffineCoupling, \
    ConditionalAffineCoupling
from pyro.nn import AutoRegressiveNN, DenseNN, ConditionalDenseNN


class NormFlow(nn.Module):
    def __init__(self, flow_type, num_flows, hidden_dim=20, need_permute=False, **kwargs):
        super(NormFlow, self).__init__()
        self.need_permute = need_permute
        self.name = flow_type
        self.condition = False
        if flow_type == 'IAF':
            self.flow = nn.ModuleList(
                [AffineAutoregressive(AutoRegressiveNN(input_dim=hidden_dim, param_dims=[2 * hidden_dim], **kwargs),
                                      stable=True) for _ in
                 range(num_flows)])
        elif flow_type == 'BNAF':
            self.flow = nn.ModuleList(
                [BlockAutoregressive(input_dim=hidden_dim, **kwargs) for _ in
                 range(num_flows)])
        elif flow_type == 'RealNVP':
            split_dim = hidden_dim // 2
            param_dims = [hidden_dim - split_dim, hidden_dim - split_dim]
            self.flow = nn.ModuleList(
                [AffineCoupling(split_dim, DenseNN(input_dim=split_dim, param_dims=param_dims, **kwargs)) for _ in
                 range(num_flows)])
        elif flow_type == "CondRealNVP":
            split_dim = hidden_dim // 2
            param_dims = [hidden_dim - split_dim, hidden_dim - split_dim]
            self.flow = nn.ModuleList(
                [ConditionalAffineCoupling(split_dim,
                                           ConditionalDenseNN(input_dim=split_dim, param_dims=param_dims, **kwargs)) for
                 _ in
                 range(num_flows)])
            self.condition = True
        else:
            raise NotImplementedError
        even = [i for i in range(0, hidden_dim, 2)]
        odd = [i for i in range(1, hidden_dim, 2)]
        undo_eo = [i // 2 if i % 2 == 0 else (i // 2 + len(even)) for i in range(hidden_dim)]
        undo_oe = [(i // 2 + len(odd)) if i % 2 == 0 else i // 2 for i in range(hidden_dim)]
        self.register_buffer('eo', torch.tensor(even + odd, dtype=torch.int64))
        self.register_buffer('oe', torch.tensor(odd + even, dtype=torch.int64))
        self.register_buffer('undo_eo', torch.tensor(undo_eo, dtype=torch.int64))
        self.register_buffer('undo_oe', torch.tensor(undo_oe, dtype=torch.int64))

    def permute(self, z, i, undo=False):
        if not undo:
            if i % 2 == 0:
                z = torch.index_select(z, 1, self.eo)
            else:
                z = torch.index_select(z, 1, self.oe)
        else:
            if i % 2 == 0:
                z = torch.index_select(z, 1, self.undo_eo)
            else:
                z = torch.index_select(z, 1, self.undo_oe)
        return z

    def forward(self, z, **kwargs):
        """
        Forward method
        :param z: initial state
        :return: a pair -- z_new and log_jacobian of the resulting transformation
        """
        log_jacob = torch.zeros_like(z[:, 0], dtype=torch.float32)
        for i in range(len(self.flow)):
            if self.need_permute:
                z = self.permute(z, i)

            if not self.condition:
                current_flow = self.flow[i]
            else:
                current_flow = self.flow[i].condition(**kwargs)

            z_new = current_flow(z)
            log_jacob += current_flow.log_abs_det_jacobian(z, z_new)

            if self.need_permute:
                z_new = self.permute(z_new, i, undo=True)
            z = z_new
        return {"z_new": z, "aggregated_log_jac": log_jacob}

    def inverse(self, z, **kwargs):
        """
        Inverse method (effective only for affine transform)
        :param z: initial state
        :return: a pair -- z_new and log_jacobian of the resulting transformation
        """
        log_jacob = torch.zeros_like(z[:, 0], dtype=torch.float32)
        for i in range(len(self.flow))[::-1]:
            if self.need_permute:
                z = self.permute(z, i)

            if not self.condition:
                current_flow = self.flow[i]
            else:
                current_flow = self.flow[i].condition(**kwargs)

            z_new = current_flow._inverse(z)
            log_jacob -= current_flow.log_abs_det_jacobian(z, z_new)
            if self.need_permute:
                z_new = self.permute(z_new, i, undo=True)
            z = z_new
        return {"z_new": z, "aggregated_log_jac": log_jacob}
