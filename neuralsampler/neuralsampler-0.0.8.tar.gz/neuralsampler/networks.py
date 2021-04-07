import torch
import torch.nn as nn
from torch.nn import Parameter


class SmallMLP(nn.Module):
    def __init__(self, n_dims, n_out=1, n_hid=200, layer=nn.Linear, UseSpectral=False):
        """Build the neural network for generator and discriminator

        Args:
            n_dims (scalar): the input dimension 
            n_out (int, optional): output dimensions. Defaults to 1.
            n_hid (int, optional): hidden layer dimension. Defaults to 200.
            layer (nn.Module, optional): fully connected layer. Defaults to nn.Linear.
            UseSpectral (bool, optional): whether to use spectral normalization. Defaults to False.
        """
        super(SmallMLP, self).__init__()
        self.net = nn.Sequential(
            layer(n_dims, n_hid) if not UseSpectral else SpectralNorm(layer(n_dims, n_hid)),
            nn.SiLU(),
            layer(n_hid, n_hid) if not UseSpectral else SpectralNorm(layer(n_hid, n_hid)),
            nn.SiLU(),
            layer(n_hid, n_hid) if not UseSpectral else SpectralNorm(layer(n_hid, n_hid)),
            nn.SiLU(),
            layer(n_hid, n_out) if not UseSpectral else SpectralNorm(layer(n_hid, n_out)),
        )

    def forward(self, x):
        out = self.net(x)
        out = out.squeeze()
        return out



# utils 
def l2normalize(v, eps=1e-12):
    return v / (v.norm() + eps)

class SpectralNorm(nn.Module):
    def __init__(self, module, name='weight', power_iterations=1):
        super(SpectralNorm, self).__init__()
        self.module = module
        self.name = name
        self.power_iterations = power_iterations
        if not self._made_params():
            self._make_params()

    def _update_u_v(self):
        u = getattr(self.module, self.name + "_u")
        v = getattr(self.module, self.name + "_v")
        w = getattr(self.module, self.name + "_bar")

        height = w.data.shape[0]
        for _ in range(self.power_iterations):
            v.data = l2normalize(torch.mv(torch.t(w.view(height,-1).data), u.data))
            u.data = l2normalize(torch.mv(w.view(height,-1).data, v.data))

        # sigma = torch.dot(u.data, torch.mv(w.view(height,-1).data, v.data))
        sigma = u.dot(w.view(height, -1).mv(v))
        setattr(self.module, self.name, w / sigma.expand_as(w))

    def _made_params(self):
        try:
            u = getattr(self.module, self.name + "_u")
            v = getattr(self.module, self.name + "_v")
            w = getattr(self.module, self.name + "_bar")
            return True
        except AttributeError:
            return False


    def _make_params(self):
        w = getattr(self.module, self.name)

        height = w.data.shape[0]
        width = w.view(height, -1).data.shape[1]

        u = Parameter(w.data.new(height).normal_(0, 1), requires_grad=False)
        v = Parameter(w.data.new(width).normal_(0, 1), requires_grad=False)
        u.data = l2normalize(u.data)
        v.data = l2normalize(v.data)
        w_bar = Parameter(w.data)

        del self.module._parameters[self.name]

        self.module.register_parameter(self.name + "_u", u)
        self.module.register_parameter(self.name + "_v", v)
        self.module.register_parameter(self.name + "_bar", w_bar)


    def forward(self, *args):
        self._update_u_v()
        return self.module.forward(*args)
