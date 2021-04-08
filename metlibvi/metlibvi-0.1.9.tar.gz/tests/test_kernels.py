import torch

from metlibvi.mcmc import HMC, ULA, MALA, run_chain


def get_precision(kernel, target):
    true_loc = target.loc
    samples = run_chain(kernel=kernel, z_init=torch.zeros_like(true_loc)[None], target_logprob=target.log_prob,
                        n_steps=500,
                        burnin=500,
                        return_trace=True)
    sampled_loc = samples.mean(0)
    return torch.abs(true_loc - sampled_loc).mean()


# @pytest.mark.skip(reason='Not implemented yet')
def test_hmc_precision(get_gaussian_target):
    target = get_gaussian_target
    kernel = HMC(n_leapfrogs=3, step_size=0.1)
    assert get_precision(kernel, target) <= 75e-2


# @pytest.mark.skip(reason='Not implemented yet')
def test_mala_precision(get_gaussian_target):
    target = get_gaussian_target
    kernel = MALA(step_size=0.1)
    assert get_precision(kernel, target) <= 75e-2


# @pytest.mark.skip(reason='Not implemented yet')
def test_ula_precision(get_gaussian_target):
    target = get_gaussian_target
    kernel = ULA(step_size=0.1)
    assert get_precision(kernel, target) <= 75e-2
