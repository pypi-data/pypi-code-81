import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import torch


class BaseTarget:
    """
    Class for base target
    """

    def log_prob(self, z, x=None):
        """
        The function returns logarithmic density of point z given x (if any)
        :param z: Input state
        :param x: Input object
        :return: logarithmic density. Tensor of batch size (z.shape[0])
        """
        pass

    def sample(self, shape):
        """

        :param shape: The function returns samples of size shape (iterable).
        :return:
        """
        pass

    def plot_distr(self, lims, npts, device, figsize=(10, 4), dpi=100):
        x_lim = lims[0]
        y_lim = lims[1]

        xside = np.linspace(-x_lim - 1, x_lim + 1, npts)
        yside = np.linspace(-y_lim - 1, y_lim + 1, npts)
        xx, yy = np.meshgrid(xside, yside)

        z = torch.tensor(np.hstack([xx.reshape(-1, 1), yy.reshape(-1, 1)]), device=device, dtype=torch.float32)
        logdens = self.log_prob(z)
        p = np.exp(logdens.cpu().detach().numpy().reshape(npts, npts))

        fig, ax = plt.subplots(ncols=2, figsize=figsize, sharex='all', sharey='all', dpi=dpi)
        ax[0].set_title('Target density')
        ax[0].pcolormesh(xx, yy, p, norm=mcolors.PowerNorm(0.5))
        ax[0].contour(xx, yy, p, 15, colors='black', alpha=0.2)
        ax[0].set_xlim(-x_lim, x_lim)
        ax[0].set_ylim(0, y_lim)
        ax[0].set_xticks(np.arange(-x_lim, x_lim + 1, 10))
        ax[0].set_yticks(np.arange(-y_lim, y_lim + 1, 10))

        ax[1].set_title('Target samples')
        samples = self.sample((5000,)).cpu().detach().numpy()
        ax[1].scatter(samples[:, 0], samples[:, 1], alpha=0.075)
        ax[1].set_xticks(np.arange(-x_lim, x_lim + 1, 10))
        ax[1].set_yticks(np.arange(-y_lim, y_lim + 1, 10))


class Gaussian(BaseTarget):
    def __init__(self, loc, covariance_matrix):
        super().__init__()
        self.loc = loc
        self.covariance_matrix = covariance_matrix
        self.distribution = torch.distributions.MultivariateNormal(loc=self.loc,
                                                                   covariance_matrix=self.covariance_matrix)

    def log_prob(self, z, x=None):
        return self.distribution.log_prob(z)

    def sample(self, shape):
        return self.distribution.sample(shape)


class GMM(BaseTarget):
    def __init__(self, locs, covariance_matrices):
        super().__init__()
        self.locs = torch.tensor([], device=locs[0].device)
        self.covariance_matrices = torch.tensor([], device=covariance_matrices[0].device)
        self.distributions = []
        self.device = locs[0].device
        for i in range(len(locs)):
            self.distributions.append(
                torch.distributions.MultivariateNormal(loc=locs[i], covariance_matrix=covariance_matrices[i]))

    def log_prob(self, z, x=None):
        log_p = torch.tensor([], device=z.device)
        for i in range(len(self.distributions)):
            log_paux = self.distributions[i].log_prob(z).view(-1, 1)
            log_p = torch.cat([log_p, log_paux], dim=-1)
        log_density = torch.logsumexp(log_p, dim=1)
        return log_density

    def sample(self, shape):
        p = np.random.choice(a=len(self.distributions), size=shape[0])
        samples = torch.tensor([], device=self.device)
        for idx in p:
            z = self.distributions[idx].sample((1,))
            samples = torch.cat([samples, z])
        return samples


class Funnel(BaseTarget):
    def __init__(self, dim, device):
        super().__init__()
        self.d = dim
        self.device = device
        self.std_normal = torch.distributions.Normal(loc=torch.tensor(0., dtype=torch.float32, device=self.device),
                                                     scale=torch.tensor(1., dtype=torch.float32, device=self.device), )

    def log_prob(self, z, x=None):
        d = z.shape[1]
        fst_component = z[:, 0]
        log_density = -fst_component ** 2 / 2 - torch.sum(z[:, 1:] ** 2., dim=1) * torch.exp(
            -2. * fst_component) / 2. - (d - 1) * fst_component
        return log_density

    def sample(self, shape):
        samples = torch.zeros((shape[0], self.d), device=self.device)
        for i in range(shape[0]):
            samples[i][0] = self.std_normal.sample((1,))
            component_normal = torch.distributions.Normal(
                loc=torch.zeros(self.d - 1, device=self.device, dtype=torch.float32),
                scale=torch.exp(samples[i][0]) * torch.ones(self.d - 1, device=self.device, dtype=torch.float32))
            samples[i][1:] = component_normal.sample()
        return samples


class Banana(BaseTarget):
    def __init__(self, dim, a, b, rho, device):
        super().__init__()
        self.device = device
        self.initial_gaussian = torch.distributions.MultivariateNormal(loc=torch.zeros(dim, device=self.device),
                                                                       covariance_matrix=rho)
        self.a = a
        self.b = b
        self.rho = rho[0, 1]

    def log_prob(self, z, x=None):
        x = z[:, 0]
        y = z[:, 1]
        log_density = -1. / (2 * (1. - self.rho ** 2)) * ((x / self.a) ** 2
                                                          + self.a ** 2 * (
                                                                  y - self.b * x ** 2 / self.a ** 2 - self.b * self.a ** 2) ** 2
                                                          - 2 * self.rho * (
                                                                  y - self.b * x ** 2 / self.a ** 2 - self.b * self.a ** 2))
        return log_density

    def sample(self, shape):
        # sample from true target
        gaussian_samples = self.initial_gaussian.sample(shape)
        x = self.a * gaussian_samples[:, 0]
        y = gaussian_samples[:, 1] / self.a + self.b * (gaussian_samples[:, 0] ** 2 + self.a ** 2)
        samples = torch.cat([x[:, None], y[:, None]], dim=-1)
        return samples


class BananaMixture(BaseTarget):
    # TODO: Debug this
    def __init__(self, dim, locs, cov, a, b, rho, device):
        super().__init__()
        self.device = device
        self.locs = locs
        self.device = device
        self.a = a
        self.b = b
        self.logprob = torch.tensor(np.log(1. / len(self.locs)), dtype=torch.float32, device=self.device)
        self.rho = rho[0, 1]
        self.initial_gaussian = torch.distributions.MultivariateNormal(loc=torch.zeros(dim, device=self.device),
                                                                       covariance_matrix=cov)

    def log_prob(self, z, x=None):
        x = z[:, 0]
        y = z[:, 1]
        log_density = torch.tensor([], device=self.device)
        for i in range(len(self.locs)):
            x_c = x - self.locs[i][0]
            y_c = y - self.locs[i][1]
            log_paux = self.logprob - 1. / (2 * (1. - self.rho ** 2)) * ((x_c / self.a[i]) ** 2
                                                                         + self.a[i] ** 2 * (
                                                                                 y_c - self.b[i] * x_c ** 2 / self.a[
                                                                             i] ** 2 - self.b[
                                                                                     i] * self.a[i] ** 2) ** 2
                                                                         - 2 * self.rho * (
                                                                                 y_c - self.b[i] * x_c ** 2 / self.a[
                                                                             i] ** 2 - self.b[i] *
                                                                                 self.a[i] ** 2))

            log_density = torch.cat([log_density, log_paux[None, :]], dim=0)
        log_density = torch.logsumexp(log_density, dim=0)
        return log_density

    def sample(self, shape):
        # sample from true target
        gaussian_samples = self.initial_gaussian.sample(shape)
        p = np.random.choice(a=len(self.locs), size=shape[0])
        x = self.a[p] * (gaussian_samples[:, 0] + self.locs[p, 0])
        y = gaussian_samples[:, 1] / self.a[p] + self.b[p] * (
                gaussian_samples[:, 0] ** 2 + self.a[p] ** 2)  ##Only valid for mu_y = 0 !!
        samples = torch.cat([x[:, None], y[:, None]], dim=-1)
        return samples
