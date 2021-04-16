from typing import Optional, Type, Callable

import torch
from pipcs import Config, Required, required

from .nes import Policy, NES


def after_optimize_hook(self):
    pass


default_config = Config()


@default_config('environment')
class EnvironmentConfig():
    """
    :var id (str): Gym environment id
    """
    id: Required['str'] = required


@default_config('policy')
class PolicyConfig():
    """
    :var policy (Required[Type[Policy]]): torch.nn.Module with a rollout method
    :var device (str): torch device
    """
    policy: Required[Type[Policy]] = required
    device: str = 'cpu'


@default_config('optimizer')
class OptimizerConfig():
    """

    :var lr (float): Learning rate
    :var optim_type (Required[Type[torch.optim.Optimizer]]): torch optim module
    """
    lr: float = 0.02
    optim_type: Required[Type[torch.optim.Optimizer]] = required


@default_config('nes')
class NESConfig():
    """
    :var population_size (Required[int]): Population Size, higher means lower variance in gradient calculation but higher memory consumption.
    :var n_step (Required[int]): Number of training steps
    :var sigma (float): Standart deviation for population sampling
    :var n_rollout (int): Number of episodes per sampled policy.
    :var seed (Optional[int]): Random seed
    :var after_optimize_hook: Executed after optim.step()
    """
    n_rollout: int = 1
    n_step: Required[int] = required
    l2_decay: float = 0.005
    population_size: Required[int] = required
    sigma: float = 0.02
    seed: Optional[int] = None
    after_optimize_hook: Callable[[NES], None] = after_optimize_hook
