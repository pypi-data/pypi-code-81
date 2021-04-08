import torch
import torch.nn as nn

from metlibvi.mcmc import ULA
from metlibvi.trainers import train_met_vi, train_vi, metropolized_vi_forward
from metlibvi.vi import NormFlow

device = torch.device("cpu")  # "cuda" if torch.cuda.is_available() else "cpu")


def get_precision(samples, target):
    true_loc = target.loc
    sampled_loc = samples.mean(0)
    return torch.abs(true_loc - sampled_loc).mean()


def test_rnvp(get_gaussian_target):
    """
    Tests if RealNVP provides good VI
    :return:
    """
    target = get_gaussian_target
    nf = NormFlow(flow_type='RealNVP', num_flows=3, hidden_dim=2, need_permute=True, hidden_dims=[2]).to(device)
    prior = torch.distributions.MultivariateNormal(loc=torch.tensor([0., 0.], device=device),
                                                   covariance_matrix=torch.eye(2, device=device))

    nf = train_vi(transitions=nf, target=target, prior=prior, lr=7e-3, n_batches=5000)

    samples = nf(prior.sample((1000,)))["z_new"]
    inverse_samples = nf.inverse(target.sample((1000,)))["z_new"]
    assert get_precision(samples, target) <= 75e-2 and get_precision(inverse_samples, prior)


def test_met_ula(get_gaussian_target):
    """
    Tests is metropolized ULA provides good VI
    :param get_gaussian_target:
    :return:
    """
    target = get_gaussian_target
    transitions = nn.ModuleList([ULA(step_size=0.01, learnable=True) for _ in range(5)]).to(device)
    prior = torch.distributions.MultivariateNormal(loc=torch.tensor([0., 0.], device=device),
                                                   covariance_matrix=torch.eye(2, device=device))

    transitions, _ = train_met_vi(transitions=transitions, target=target, prior=prior, lr=7e-3)

    with torch.no_grad():
        samples = metropolized_vi_forward(transitions=transitions, target_logprob=target.log_prob,
                                          z=prior.sample((1000,)), )["z_new"]
    assert get_precision(samples, target) <= 75e-2


def test_met_realnvp(get_gaussian_target):
    """
    Tests is metropolized RealNVP (metflow) provides good VI
    :param get_gaussian_target:
    :return:
    """
    target = get_gaussian_target
    transitions = nn.ModuleList(
        [NormFlow(flow_type="RealNVP", num_flows=2, need_permute=True, hidden_dim=2, hidden_dims=(2,)) for _ in
         range(2)]).to(device)
    prior = torch.distributions.MultivariateNormal(loc=torch.tensor([0., 0.], device=device),
                                                   covariance_matrix=torch.eye(2, device=device))

    transitions, logit_p = train_met_vi(transitions=transitions, target=target, prior=prior, n_batches=10000, lr=7e-3)

    with torch.no_grad():
        samples = \
            metropolized_vi_forward(transitions=transitions, forward_logit_prob=logit_p, target_logprob=target.log_prob,
                                    z=prior.sample((1000,)), )["z_new"]

    assert get_precision(samples, target) <= 75e-2
