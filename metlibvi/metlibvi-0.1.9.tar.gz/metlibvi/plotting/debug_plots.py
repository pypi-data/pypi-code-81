import matplotlib.pyplot as plt
import numpy as np
import torch


def plot_true_prop_accept(z_target=None, z_accepted=None, z_proposal=None, acceptance_logprobs=None, **kwargs):
    '''
    Plots scatter plot with target points, proposal and accepted (scaled according to acceptance ratio if provided)
    :param z_target: target samples
    :param z_proposal: proposal samples
    :param z_accepted: accepted samples
    :param acceptance_logprobs: acceptance logprobs
    :return: scatterplot
    '''
    plt.close()

    if acceptance_logprobs is not None:
        acceptance_probs = np.exp(acceptance_logprobs.cpu().detach().numpy())
    else:
        acceptance_probs = torch.ones_like(z_accepted[:, 1]).cpu().detach().numpy()

    plt.figure(**kwargs)

    if z_target is not None:
        z_target = z_target.cpu().detach().numpy()
        plt.scatter(x=z_target[:, 0], y=z_target[:, 1], c='b', label='Target')

    if z_proposal is not None:
        z_proposal = z_proposal.cpu().detach().numpy()
        plt.scatter(x=z_proposal[:, 0], y=z_proposal[:, 1], c='r', label='Proposal')

    if z_accepted is not None:
        z_accepted = z_accepted.cpu().detach().numpy()
        plt.scatter(x=z_accepted[:, 0], y=z_accepted[:, 1], c='g', label='Accepted', s=acceptance_probs + 15)

    plt.legend()
    plt.show()
