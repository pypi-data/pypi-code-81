import torch


def get_acceptance_ratio(log_t, log_1pt, use_barker):
    """
    The function computes acceptance ratio, amenable for backpropagation
    :param log_t: logarithm of acceptance ratio
    :param log_1pt: logarithm of 1 + t, computed in numerically accurate way
    :param use_barker: whether to use barker ratio or not
    :return: decision, corresponding log_ratios and acceptance log ratios
    """
    if use_barker:
        current_log_alphas_pre = log_t - log_1pt
    else:
        current_log_alphas_pre = torch.min(log_t, torch.zeros_like(log_t))

    log_probs = torch.log(torch.rand_like(log_t))
    a = log_probs <= current_log_alphas_pre
    if use_barker:
        current_log_alphas = current_log_alphas_pre.clone()
        current_log_alphas[~a] = (-log_1pt)[~a]
    else:
        expression = torch.ones_like(current_log_alphas_pre) - torch.exp(current_log_alphas_pre)
        corr_expression = torch.log(expression + 1e-8)
        current_log_alphas = current_log_alphas_pre.clone()
        current_log_alphas[~a] = corr_expression[~a]

    return a, current_log_alphas, current_log_alphas_pre.detach()


def compute_grad(z, target_logprob, x):
    flag = z.requires_grad  # True, if requires grad (means that we propagate gradients to some parameters)
    if not flag:
        z_ = z.detach().requires_grad_(True)
    else:
        z_ = z
    with torch.enable_grad():
        grad = get_grad(z=z_, target_logprob=target_logprob, x=x)
        if not flag:
            grad = grad.detach()
            z_.requires_grad_(False)
        return grad


def get_grad(z, target_logprob, x=None):
    s = target_logprob(x=x, z=z)
    grad = torch.autograd.grad(s.sum(), z, create_graph=True, only_inputs=True)[0]
    return grad


def run_chain(kernel, z_init, target_logprob, x=None, n_steps=100, return_trace=False, burnin=0):
    """
    The function launches mcmc chain.
    :param kernel: mcmc kernel
    :param z_init: initial state
    :param target_logprob: target_logprob (must have log_prob method, which returns a batch)
    :param x: data object (if given)
    :param n_steps: number of transitions
    :param return_trace: whether to return trajectory (True), or only final state (False)
    :param burnin: number of burnin steps
    :return: either trajectory or final samples
    """
    samples = z_init
    if not return_trace:
        for _ in range(burnin + n_steps):
            samples = kernel(z=samples, target_logprob=target_logprob, x=x)["z_new"].detach()
        return samples
    else:
        final = torch.tensor([], device=z_init.device, dtype=torch.float32)
        for i in range(burnin + n_steps):
            samples = kernel(z=samples, target_logprob=target_logprob, x=x)["z_new"].detach()
            if i >= burnin:
                final = torch.cat([final, samples])
        return final
