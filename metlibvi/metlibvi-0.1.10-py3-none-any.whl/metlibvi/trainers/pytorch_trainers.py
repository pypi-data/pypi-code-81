import numpy as np
import torch
import torch.nn as nn
from tqdm.auto import tqdm

from metlibvi.train_utils import metropolized_vi_forward, metropolized_loss, vanilla_vi_forward, kl_loss


def train_met_vi(transitions, target, prior, n_batches=1000, batch_size=150, lr=5e-3):
    if transitions[0].name == "RealNVP":
        logit_p = nn.Parameter(torch.tensor(np.zeros(len(transitions)), dtype=torch.float32))
        additional_params = [logit_p]
    else:
        logit_p = None
        additional_params = []
    optimizer = torch.optim.Adam(list(transitions.parameters()) + additional_params, lr=lr)
    for _ in tqdm(range(n_batches)):
        z = prior.sample((batch_size,))
        output = metropolized_vi_forward(transitions=transitions, forward_logit_prob=logit_p,
                                         target_logprob=target.log_prob, z=z)
        loss = metropolized_loss(final_samples=output["z_new"], z=z, x=None, prior=prior,
                                 sum_log_jac=output["aggregated_log_jac"],
                                 sum_log_alphas=output["sum_log_alphas"], sum_log_probs=output["sum_log_probs"],
                                 target_logprob=target.log_prob,
                                 loss_variant="standard")
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

    return transitions, logit_p


def train_vi(transitions, target, prior, n_batches=1000, batch_size=150, lr=5e-3):
    optimizer = torch.optim.Adam(list(transitions.parameters()), lr=lr)
    for _ in tqdm(range(n_batches)):
        z = prior.sample((batch_size,))
        output = vanilla_vi_forward(transitions=transitions, z=z, )
        kl = kl_loss(final_samples=output["z_new"], z=z, prior=prior, sum_log_jac=output["aggregated_log_jac"],
                     target_logprob=target.log_prob, loss_variant="standard", x=None)
        kl.backward()
        optimizer.step()
        optimizer.zero_grad()

    return transitions
