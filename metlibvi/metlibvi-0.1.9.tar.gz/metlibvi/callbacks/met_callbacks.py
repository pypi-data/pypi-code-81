import torch

from metlibvi.plotting import plot_true_prop_accept


def on_transition_end_callback(z_target=None, z_accepted=None, z_proposal=None, acceptance_logprobs=None, verbosity=1,
                               current_iter=1, use_callback=False, **kwargs):
    if use_callback:
        if current_iter % verbosity == 0:
            with torch.no_grad():
                plot_true_prop_accept(z_target=z_target, z_accepted=z_accepted, z_proposal=z_proposal,
                                      acceptance_logprobs=acceptance_logprobs,
                                      **kwargs)
                acceptance_rate = ((z_accepted == z_proposal) * 1.).mean(-1).mean()
                print('Mean acceptance rate is', acceptance_rate)
