from dataclasses import dataclass
from itertools import zip_longest
from typing import Any, Dict, Iterable, List, Text

import torch
from datasets import Dataset as HFDataset
from formerbox.data.data_collator import DataCollator, EncodedInput, collate_batch
from formerbox.data.dataset_iterators import DatasetIteratorBase
from formerbox.utils import iter_stride


def make_batches(sequences: Iterable[Any], batch_size: int) -> Iterable[List[Any]]:
    return iter_stride(sequences, batch_size, stride=0)


def flatten(nested_dict: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    result: List[Dict[Text, Any]] = []
    packed_values = zip_longest(*nested_dict.values())
    for packed_value in packed_values:
        flat_dict = {}
        for key, value in zip(nested_dict.keys(), packed_value):
            if value is None:
                continue
            flat_dict[key] = value
        result.append(flat_dict)
    return result


@dataclass
class DataCollatorForDocumentClassification(DataCollator):
    def __call__(
        self, features: List[Dict[Text, EncodedInput]]
    ) -> Dict[Text, torch.Tensor]:
        seq_input_ids: List[EncodedInput] = []
        seq_attention_mask: List[EncodedInput] = []
        seq_labels: List[EncodedInput] = []
        for feature in features:
            seq_input_ids.append(feature["input_ids"])
            seq_attention_mask.append(feature["attention_mask"])
            seq_labels.append(feature["labels"])

        input_ids = collate_batch(
            sequences=seq_input_ids,
            tokenizer=self.tokenizer,
        )
        attention_mask = collate_batch(
            sequences=seq_attention_mask,
            tokenizer=self.tokenizer,
        )
        labels = collate_batch(
            sequences=seq_labels,
            tokenizer=self.tokenizer,
        )

        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": labels,
        }


class DocumentDataset(DatasetIteratorBase):
    def __init__(
        self,
        dataset: HFDataset,
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

        documents: List[List[Dict[Text, torch.Tensor]]] = []
        for document in record["documents"]:
            sentences: List[Dict[Text, torch.Tensor]] = []
            for sentence in make_batches(document, self.batch_size):
                sentences.append(self.collator(sentence))
            documents.append(sentences)

        labels = record.get("labels")

        return {"documents": documents, "labels": labels}

    def collate_fn(self, samples: List[Any]) -> Any:
        if len(samples) == 1:
            return samples[0]
        return samples
