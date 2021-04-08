import torch

from metlibvi.mcmc import get_acceptance_ratio


def test_pre_acceptance_mh():
    """
    Tests if current_log_alphas_pre (acceptance prob if we would use it) is correct
    :return:
    """
    log_t = torch.tensor([torch.log(torch.tensor(0.8)), torch.log(torch.tensor(0.35))])
    log_1pt = torch.tensor([torch.log(torch.tensor(1.8)), torch.log(torch.tensor(1.35))])
    use_barker = False
    _, _, current_log_alphas_pre = get_acceptance_ratio(log_t.clone(), log_1pt.clone(), use_barker)
    assert sum(current_log_alphas_pre == torch.min(log_t, torch.zeros_like(log_t))) == 2


def test_pre_acceptance_barker():
    """
    Tests if current_log_alphas_pre (acceptance prob if we would use it) is correct
    :return:
    """
    log_t = torch.tensor([torch.log(torch.tensor(0.8)), torch.log(torch.tensor(0.35))])
    log_1pt = torch.tensor([torch.log(torch.tensor(1.8)), torch.log(torch.tensor(1.35))])
    use_barker = True
    _, _, current_log_alphas_pre = get_acceptance_ratio(log_t.clone(), log_1pt.clone(), use_barker)
    assert sum(current_log_alphas_pre == log_t - log_1pt) == 2
