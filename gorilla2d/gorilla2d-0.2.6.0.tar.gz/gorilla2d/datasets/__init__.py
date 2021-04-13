# copy from https://github.com/thuml/Transfer-Learning-Library
from .imagelist import ImageList
from ._utils import download as download_data, check_exits
from .office31 import Office31
from .officehome import OfficeHome
from .visda2017 import VisDA2017
from .officecaltech import OfficeCaltech
from .domainnet import DomainNet
from .digit import Digit
# Registry mechanism support defining custom Dataset class in a project.
# auto_registry should be placed behind all Dataset class and in front of
# other class (it doesn't matter for functions)
from gorilla import DATASETS, auto_registry
auto_registry(DATASETS, globals())

from .transforms import ResizeImage
from .randaugment import RandAugmentMC
# this command should be bottom to avoid that some packages have not been imported when used
from .dataloader import build_dataloaders

__all__ = ["ImageList", "Office31", "OfficeHome", "VisDA2017", "OfficeCaltech", "DomainNet"]
