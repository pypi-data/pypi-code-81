import torch
import torch.nn as nn

from metlibvi.mcmc.utils import get_acceptance_ratio, compute_grad


class BaseKernel(nn.Module):
    """
    Base mcmc kernel class
    """

    def __init__(self, step_size, use_barker=False, learnable=False):
        """

        :param step_size: stepsize for transition
        :param use_barker: If True -- Barker ratios applied. MH otherwise
        :param learnable: whether learnable (usage for Met model) or not
        """
        super().__init__()
        self.use_barker = use_barker
        self.learnable = learnable
        self.register_buffer('zero', torch.tensor(0., dtype=torch.float32))
        self.register_buffer('one', torch.tensor(1., dtype=torch.float32))
        self.log_stepsize = nn.Parameter(torch.log(torch.tensor(step_size, dtype=torch.float32)),
                                         requires_grad=learnable)

    @property
    def step_size(self):
        return torch.exp(self.log_stepsize)


class HMC(BaseKernel):
    def __init__(self, n_leapfrogs, partial_ref=False, **kwargs):
        """
        HMC kernel class
        :param n_leapfrogs: number of leapfrog iterations
        :param partial_ref: whether use partial refresh or not
        """
        super().__init__(**kwargs)
        self.n_leapfrogs = n_leapfrogs
        self.partial_ref = partial_ref
        self.alpha_logit = nn.Parameter(self.zero, requires_grad=self.learnable)  # for partial refreshment
        self.name = "HMC"

    @property
    def alpha(self):
        return torch.sigmoid(self.alpha_logit)

    def _forward_step(self, z_old, x=None, target_logprob=None, p_old=None):
        p_ = p_old + self.step_size / 2. * compute_grad(z=z_old, target_logprob=target_logprob,
                                                        x=x)
        z_ = z_old
        for current_l in range(self.n_leapfrogs):
            z_ = z_ + self.step_size * p_
            if current_l != self.n_leapfrogs - 1:
                p_ = p_ + self.step_size * compute_grad(z=z_, target_logprob=target_logprob,
                                                        x=x)
        p_ = p_ + self.step_size / 2. * compute_grad(z=z_, target_logprob=target_logprob,
                                                     x=x)
        return z_, p_

    def _make_transition(self, z_old, target_logprob, p_old=None, x=None):

        std_normal = torch.distributions.Normal(loc=self.zero, scale=self.one)

        ############ Then we compute new points and densities ############
        z_upd, p_upd = self.forward_step(z_old=z_old, p_old=p_old, target_logprob=target_logprob, x=x)

        target_log_density_f = target_logprob(z=z_upd, x=x) + std_normal.log_prob(p_upd).sum(-1)
        target_log_density_old = target_logprob(z=z_old, x=x) + std_normal.log_prob(p_old).sum(-1)

        log_t = target_log_density_f - target_log_density_old
        log_1pt = torch.logsumexp(torch.cat([torch.zeros_like(log_t).view(-1, 1),
                                             log_t.view(-1, 1)], dim=-1), dim=-1)  # log(1+t)

        a, current_log_alphas, _ = get_acceptance_ratio(log_t=log_t, log_1pt=log_1pt, use_barker=self.use_barker)

        z_new = z_upd
        z_new[~a] = z_old[~a]

        p_new = -p_upd
        p_new[~a] = -p_old[~a]

        return z_new, p_new, a.to(torch.float32), current_log_alphas

    def forward_step(self, z_old, x=None, target_logprob=None, p_old=None):
        z_, p_ = self._forward_step(z_old=z_old, x=x, target_logprob=target_logprob, p_old=p_old)
        return z_, p_

    def forward(self, z, target_logprob, x=None, p=None):
        """

        :param z: current state
        :param target_logprob: target log prob
        :param x: batch of objects
        :param p: current momentum
        :return: (new state, new momentum, decisions casted to float, logs of corresponding alphas
        """
        if p is None:
            p = torch.randn_like(z)
        if self.partial_ref:
            p = p * self.alpha + torch.sqrt(self.one - self.alpha ** 2) * torch.randn_like(p)
        z_new, p_new, a, current_log_alphas = self._make_transition(z_old=z,
                                                                    target_logprob=target_logprob, p_old=p, x=x)
        return {"z_new": z_new,
                "p_new": p_new,
                "decisions": a.to(torch.float32),
                "current_log_alphas": current_log_alphas}


class MALA(BaseKernel):
    def __init__(self, **kwargs):
        """
        MALA kernel class

        :param use_barker: If True -- Barker ratios applied. MH otherwise
        """
        super().__init__(**kwargs)
        self.name = "MALA"

    def _forward_step(self, z_old, x=None, target_logprob=None):
        eps = torch.randn_like(z_old)
        forward_grad = compute_grad(z=z_old,
                                    target_logprob=target_logprob,
                                    x=x)
        update = torch.sqrt(2 * self.step_size) * eps + self.step_size * forward_grad
        return z_old + update, update, eps, forward_grad

    def forward(self, z, target_logprob, x=None):
        """

        :param z: current state
        :param target_logprob: target log prob
        :param x: batch of objects
        :return: (new state, decisions casted to float, logs of corresponding alphas
        """
        ############ Then we compute new points and densities ############
        std_normal = torch.distributions.Normal(loc=self.zero, scale=self.one)

        z_upd, update, eps, forward_grad = self._forward_step(z_old=z, x=x, target_logprob=target_logprob)

        target_log_density_upd = target_logprob(z=z_upd, x=x)
        target_log_density_old = target_logprob(z=z, x=x)

        eps_reverse = (-update - self.step_size * compute_grad(z=z_upd, target_logprob=target_logprob,
                                                               x=x)) / torch.sqrt(
            2 * self.step_size)
        proposal_density_numerator = std_normal.log_prob(eps_reverse).sum(1)
        proposal_density_denominator = std_normal.log_prob(eps).sum(1)

        log_t = target_log_density_upd - target_log_density_old - proposal_density_denominator + \
                proposal_density_numerator
        log_1pt = torch.logsumexp(torch.cat([torch.zeros_like(log_t).view(-1, 1),
                                             log_t.view(-1, 1)], dim=-1), dim=-1)  # log(1+t)

        a, current_log_alphas, _ = get_acceptance_ratio(log_t, log_1pt, use_barker=self.use_barker)

        z_new = torch.empty_like(z_upd)
        z_new[a] = z_upd[a]
        z_new[~a] = z[~a]

        return {"z_new": z_new,
                "decisions": a.to(torch.float32),
                "current_log_alphas": current_log_alphas,
                "forward_grad": forward_grad}


class ULA(BaseKernel):
    def __init__(self, transforms=None, ula_skip_threshold=0.0, **kwargs):
        """
        ULA kernel class

        :param step_size:
        :param learnable:
        :param transforms:
        :param ula_skip_threshold:
        """
        super().__init__(**kwargs)
        self.ula_skip_threshold = ula_skip_threshold
        self.name = "ULA"
        self.transforms = False
        self.add_nn = None
        self.scale_nn = None
        self.score_matching = False
        if transforms is not None:
            self.transforms = True
            self.add_nn = transforms()
            self.scale_nn = transforms()  ###just test with step size at the moment
            self.score_matching = True

    def _forward_step(self, z_old, x=None, target_logprob=None):
        eps = torch.randn_like(z_old)
        self.log_jac = torch.zeros_like(z_old[:, 0])
        if not self.transforms:
            add = torch.zeros_like(z_old)
            forward_grad = compute_grad(
                z=z_old,
                target_logprob=target_logprob,
                x=x)
            update = torch.sqrt(2 * self.step_size) * eps + self.step_size * forward_grad
            z_new = z_old + update
            eps_reverse = (z_old - z_new - self.step_size * compute_grad(z=z_new, target_logprob=target_logprob,
                                                                         x=x)) / torch.sqrt(
                2 * self.step_size)
            score_match_cur = add
        else:
            add = self.add_nn(z=z_old, x=x)
            z_new = z_old + self.step_size * add + torch.sqrt(2 * self.step_size) * eps
            eps_reverse = (z_old - z_new - self.step_size * self.add_nn(z=z_new, x=x)) / torch.sqrt(2 * self.step_size)
            score_match_cur = (add - compute_grad(z=z_old, target_logprob=target_logprob, x=x)) ** 2
            forward_grad = add
        return z_new, eps, eps_reverse, score_match_cur, forward_grad

    def scale_transform(self, z, sign='+'):
        S = torch.sigmoid(self.scale_nn(z))
        sign = {"+": 1., "-": -1.}[sign]
        self.log_jac += torch.sum(torch.log(S), dim=1) * sign
        return S

    def forward(self, z, target_logprob, x=None, reverse_kernel=None, mu_amortize=None, **kwargs):
        """
        Input:
        z_old - current position
        target_logprob - target_logprob distribution
        x - data object (optional)
        Output:
        z_new - new position
        current_log_alphas - current log_alphas, corresponding to sampled decision variables
        a - decision variables (0 or +1)
        """

        ############ Then we compute new points and densities ############
        std_normal = torch.distributions.Normal(loc=self.zero, scale=self.one)

        z_upd, eps, eps_reverse, score_match_cur, forward_grad = self._forward_step(z_old=z, x=x,
                                                                                    target_logprob=target_logprob)

        if reverse_kernel is None:
            proposal_density_numerator = std_normal.log_prob(eps_reverse).sum(1)
        else:
            mu, logvar = reverse_kernel(torch.cat([z_upd, mu_amortize], dim=1))
            proposal_density_numerator = torch.distributions.Normal(loc=mu + z_upd,
                                                                    scale=torch.exp(0.5 * logvar)).log_prob(
                z).sum(1)

        proposal_density_denominator = std_normal.log_prob(eps).sum(1)

        z_new = z_upd

        # ###
        # with torch.no_grad():
        #     target_log_density_upd = target_logprob(z=z_upd, x=x)
        #     target_log_density_old = target_logprob(z=z, x=x)
        #     log_t = target_log_density_upd + proposal_density_numerator - target_log_density_old - proposal_density_denominator + self.log_jac
        #     log_1pt = torch.logsumexp(torch.cat([torch.zeros_like(log_t).view(-1, 1),
        #                                          log_t.view(-1, 1)], dim=-1), dim=-1)  # log(1+t)
        #     if self.ula_skip_threshold > 0.:
        #         a, _, current_log_alphas_pre = get_acceptance_ratio(log_t, log_1pt, use_barker=False)
        #         acceptance_probs = torch.exp(current_log_alphas_pre)
        #         reject_mask = acceptance_probs <= self.ula_skip_threshold
        #     else:
        #         a, current_log_alphas, _ = get_acceptance_ratio(log_t, log_1pt, use_barker=False)
        #         reject_mask = torch.zeros_like(a) < -1.
        # ###
        # if reject_mask.sum():
        #     # z_new[reject_mask] = z[reject_mask]
        #     z_new = torch.where(reject_mask[..., None], z, z_new)
        #     proposal_density_numerator[reject_mask] = torch.zeros_like(proposal_density_numerator[reject_mask])
        #     proposal_density_denominator[reject_mask] = torch.zeros_like(proposal_density_denominator[reject_mask])
        #     score_match_cur[reject_mask] = torch.zeros_like(score_match_cur[reject_mask])

        return {"z_new": z_new,
                "aggregated_log_jac": self.log_jac,
                "aux_for_acceptance_ratio": proposal_density_numerator - proposal_density_denominator}
