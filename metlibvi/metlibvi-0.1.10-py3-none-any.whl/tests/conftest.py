import pytest
import torch

from metlibvi.targets import Gaussian

device = torch.device("cpu")  # "cuda" if torch.cuda.is_available() else "cpu")


@pytest.fixture(scope="session")
def get_gaussian_target():
    loc = torch.tensor([10., -10.], device=device)
    cov = torch.eye(2, device=device)
    target = Gaussian(loc=loc, covariance_matrix=cov)
    return target
