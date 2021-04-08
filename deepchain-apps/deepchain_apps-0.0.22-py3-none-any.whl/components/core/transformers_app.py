"""Base transformers apps to train an embedding"""

import re
from time import sleep
from typing import Dict, List, Tuple

import numpy as np
import torch
from deepchainapps import log
from esm import pretrained

PATTERN = r"esm.+_t(\d{1,2}).+"

BACKEND = [
    "esm1_t12_85M_UR50S",
    "esm1_t34_670M_UR100",
    "esm1_t34_670M_UR50D",
    "esm1_t34_670M_UR50S",
    "esm1_t6_43M_UR50S",
    "esm1b_t33_650M_UR50S",
    "esm_msa1_t12_100M_UR50S",
]

NATURAL_AAS = "ACDEFGHIKLMNPQRSTVWY"

Probs = Dict[str, float]
SequenceProbs = List[Probs]


class TransformersApp:
    """Class provide embedding, logelikelihood function"""

    def __init__(
        self, device: str, model_uri: str = None, model_type: str = "esm1_t6_43M_UR50S"
    ):
        """
        Use ESM embedding : possibility to have 6 models of different size in backend
        """
        self.model_type = model_type
        self.device = torch.device(device)
        self.model_uri = model_uri

        if device == "cpu" and model_type != "esm1_t6_43M_UR50S":
            log.warning(
                "You should choose esm1_t6_43M_UR50S" "based on your cpu configuration."
            )
            sleep(2)
        try:
            model_fn = getattr(pretrained, model_type)
        except:
            msg = (
                f"Couldn't find model type {model_type} in backend "
                f"Choose model inside list {' / '.join(BACKEND)}"
            )
            raise ImportError(msg)

        self.model, self.token = model_fn()
        self.model = self.model.to(self.device)
        self.emb_version = int(re.findall(PATTERN, model_type)[0])

    @classmethod
    def list_esm_backend(cls) -> None:
        """Get all possible backend for the ESM model"""

        log.info("Use ESM backend in this list %s", " / ".join(BACKEND))

    def _predict(self, sequences: List[str], type: str = "logits") -> np.array:
        """Return the model prediction of a sequence of Am.Ac."""

        batch_converter = self.token.get_batch_converter()
        sequences = self.convert_batch_format(sequences)
        batch_labels, batch_strs, batch_tokens = batch_converter(sequences)

        with torch.no_grad():
            output = self.model(
                batch_tokens.to(self.device), repr_layers=[self.emb_version]
            )

        if type == "logits":
            output = output["logits"]
        else:
            output = (
                output["representations"][self.emb_version].detach()[:, :, :].mean(1)
            )

        return output.detach().cpu().numpy()

    def _softmaxbh(self, x: torch.Tensor) -> np.array:
        """Compute softmax values for each sets of scores in x."""

        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=-1, keepdims=True)

    def predict_embedding(self, sequences: List[str]) -> np.ndarray:
        pred = self._predict(sequences, type="representations")
        return pred

    def predict_logits(self, sequences: List[str]) -> np.ndarray:
        pred = self._predict(sequences, type="logits")
        return pred

    def _compute_loglikelihood(self, scores: List[float]) -> np.array:
        """"Compute loglikelihood of AA scores"""

        return np.sum(np.log(scores))

    def _compute_probs_from_sequence(self, sequence: str) -> SequenceProbs:
        """Compute probabilities for each AA"""

        results = self._predict([sequence], type="logits")
        res = np.array(results[0, 1 : (len(sequence) + 1)])
        probs = self._softmaxbh(res)

        probs_list = []
        for position in range(len(sequence)):
            probas = dict(
                [
                    (token, probs[position, aa_index])
                    for aa_index, token in enumerate(self.token.all_toks)
                    if token in NATURAL_AAS
                ]
            )
            probs_list.append(probas)
        return probs_list

    def _scores_from_probs(
        self, probs_list: SequenceProbs, sequence: str
    ) -> List[float]:
        """Select probs of AA for each position"""

        score = [
            probs[aa]
            for probs, aa in zip(probs_list, list(sequence))
            if aa in NATURAL_AAS
        ]
        return score

    def predict_loglikelihood(self, sequences: List[str]) -> np.array:
        """
        Predict the loglikehood of a list of protein.
        The prediction of probabilities is done base on the transformers backend choosen
        """
        #  Get the logits : token 0 is always a beginning-of-sequence token
        #  , so the first residue is token 1.
        loglikelihood_list = []
        for sequence in sequences:
            probs_list = self._compute_probs_from_sequence(sequence)
            scores = self._scores_from_probs(probs_list, sequence)
            loglikelihood = self._compute_loglikelihood(scores)
            loglikelihood_list.append(loglikelihood)

        return np.array(loglikelihood_list)

    def convert_batch_format(self, sequences: str) -> List[Tuple[str, str]]:
        """Convert to the correct format exptected by the model"""

        return [(f"protein_{i}", seq) for i, seq in enumerate(sequences)]
