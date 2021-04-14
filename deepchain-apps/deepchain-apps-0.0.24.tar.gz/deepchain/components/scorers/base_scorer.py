"""Base abstract class to implement Scorer adn App"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Tuple


class DeepChainApp(ABC):
    """
    A scorer instance is used to compute the criteria value for a genotype. This class
    is a template for DeepChain App Users.
    """

    def __init__(self):
        self._checkpoint_filename = None

    @staticmethod
    @abstractmethod
    def score_names() -> List[str]:
        """
        score names.
        """

    @abstractmethod
    def compute_scores(self, sequences: List[str]) -> List[Dict[str, float]]:
        """
        Score a list of genotype and for each of them return descriptors and score names.
        """

    def get_checkpoint_path(self, root_path: str) -> str:
        """
        Return solve checkpoint model path
        Args:
            root_path : path of the app file launch
        Raise:
            FileExistsError if no file are found inside the checkpoint folder
        """
        checkpoint_dir = (Path(root_path).parent / "../checkpoint").resolve()
        path_filename = checkpoint_dir / self._checkpoint_filename
        if not path_filename.is_file():
            raise FileExistsError(
                f"File {self._checkpoint_filename} not found in checkpoint folder."
                f" Set 'self._checkpoint_filename = None' if file not exists"
            )
        return path_filename


class Scorer(ABC):
    """
    A scorer instance is used to compute both the descriptors and the criteria value
    for a genotype. During the optimization process, the algorithm discover new
    genotypes through mutation and cross-over and use a scorer instance to evaluate
    them.
    """

    def __init__(self):
        pass

    @property
    @abstractmethod
    def criteria(self) -> List[str]:
        """
        Criteria names.
        """

    @property
    @abstractmethod
    def descriptors(self) -> List[str]:
        """
        Descriptors names.
        """

    @property
    @abstractmethod
    def descriptors_range(self) -> List[Tuple[float, float]]:
        """
        Descriptors ranges.
        """

    @property
    @abstractmethod
    def num_cells_per_dimension(self) -> List[int]:
        """
        Number of cells for each descriptor.
        """

    @property
    @abstractmethod
    def population_size(self) -> int:
        """
        Number of genotypes the scorer can score a once. Important when the scorer is
        distributed.
        """

    @abstractmethod
    def compute_scores(
        self, genotypes: List[Any]
    ) -> List[Tuple[Dict[str, float], Dict[str, float]]]:
        """
        Score a list of genotype and for each of them return descriptors and criteria.
        """
