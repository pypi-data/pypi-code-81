import typing
from dataclasses import dataclass, field
from itertools import zip_longest
from typing import Any, Dict, Iterable, List, Optional, Text, Tuple, Union

import pytorch_lightning as pl
import torch
import torch.nn as nn
from formerbox import RobertaTokenizer
from formerbox.data.data_collator import DataCollator, EncodedInput, collate_batch
from formerbox.data.dataset_iterators import DatasetIteratorBase
from formerbox.optim import AdamW, get_polynomial_decay_with_warmup, weight_decay_params
from formerbox.utils import iter_stride
from pytorch_lightning.callbacks import ModelCheckpoint
from torch.optim import Optimizer
from torch.utils.data import DataLoader
from transformers import PreTrainedModel
from transformers import PreTrainedTokenizerFast as Tokenizer
from transformers import RobertaConfig, RobertaModel, get_linear_schedule_with_warmup
from transformers.file_utils import ModelOutput
from transformers.modeling_outputs import SequenceClassifierOutput
from transformers.models.roberta.modeling_roberta import RobertaPreTrainedModel

import datasets
from datasets import ClassLabel, Sequence, Value


def make_batches(sequences: Iterable[Any], batch_size: int) -> Iterable[List[Any]]:
    return iter_stride(sequences, batch_size, stride=0)


def flatten(nested_dict: Dict[Any, List[Any]]) -> List[Dict[Any, Any]]:
    result: List[Dict[Text, Any]] = []
    packed_values = zip_longest(*nested_dict.values())
    for packed_value in packed_values:
        flat_dict: Dict[Text, Any] = {}
        for key, value in zip(nested_dict.keys(), packed_value):
            if value is None:
                continue
            flat_dict[key] = value
        result.append(flat_dict)
    return result


class Dataset(DatasetIteratorBase):
    def __init__(
        self,
        dataset: datasets.Dataset,
        collator: DataCollator,
        batch_size: int,
    ) -> None:
        self.dataset = dataset
        self.collator = collator
        self.batch_size = batch_size

    def __len__(self) -> int:
        return len(self.dataset)

    def __getitem__(self, index: int) -> Dict[Text, Any]:
        record = self.dataset[index]
        assert isinstance(record, dict)

        sentences: List[Dict[Text, torch.Tensor]] = []
        for sentence in make_batches(record["sentences"], self.batch_size):
            sentences.append(self.collator(sentence))

        labels = record.get("labels")

        return {"sentences": sentences, "labels": labels}

    def collate_fn(self, samples: List[Any]) -> Any:
        if len(samples) == 1:
            return samples[0]
        return samples


@dataclass
class DataCollatorForClassification(DataCollator):
    def __call__(
        self, features: List[Dict[Text, EncodedInput]]
    ) -> Dict[Text, torch.Tensor]:
        list_input_ids = []
        list_attention_mask = []
        for feature in features:
            list_input_ids.append(feature["input_ids"])
            list_attention_mask.append(feature["attention_mask"])

        input_ids = collate_batch(
            sequences=list_input_ids,
            tokenizer=self.tokenizer,
        )
        attention_mask = collate_batch(
            sequences=list_attention_mask,
            tokenizer=self.tokenizer,
        )

        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
        }
