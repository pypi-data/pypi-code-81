"""
ohe
~~~
Identity one-hot encoding.
"""

import numpy as np
from typing import Dict, Iterable

from deepbio.feat.featurizer import Featurizer
from deepbio.utils import nucleotide_list as _nucleotide_list


def _generate_identity_codebook(nucleotide_list: Iterable[str]) -> Dict[str, str]:
    identity = {}
    for i, aa in enumerate(nucleotide_list):
        ohe = np.zeros(len(nucleotide_list))
        ohe[i] = 1
        identity[aa] = np.squeeze(ohe)
    # Remove singleton dimensions that perturbe shape.
    return identity


class OHE(Featurizer):

    """One-hot encoding / identity vector representation of residues."""

    def __init__(self):
        super().__init__()
        self._codebook = _generate_identity_codebook(_nucleotide_list)

    def featurize(self, X: Iterable[str], log: bool = False):
        """Converts residue string to one-hot encoding.

        Args:
            X (Iterable[str]): An iterator of sequences.
            log (bool): A flag to indicate logging during featurization
        """

        def _char_to_vec(char):
            vec = self._codebook.get(char)
            if vec is None:
                return np.zeros(len(_nucleotide_list))
            else:
                return vec

        return np.transpose(np.array([_char_to_vec(char) for char in X]))

    def __unicode__(self):
        return "<OHE Featurizer>"

    def __repr__(self):
        return "<OHE Featurizer>"
