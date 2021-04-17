from itertools import zip_longest
from typing import Any, Dict, Iterable, List, Text

import torch
from datasets import Dataset as HFDataset
from formerbox.data.data_collator import collate_batch
from formerbox.utils import iter_stride
from formerbox.data.dataset_iterators import DatasetIteratorBase
from transformers import PreTrainedTokenizerFast as Tokenizer


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


class DocumentPairDataset(DatasetIteratorBase):
    def __init__(
        self,
        dataset: HFDataset,
        tokenizer: Tokenizer,
        batch_size: int,
    ) -> None:
        self.dataset = dataset
        self.tokenizer = tokenizer
        self.batch_size = batch_size

    def __len__(self) -> int:
        return len(self.dataset)

    def __getitem__(self, index: int) -> Dict[Text, Any]:
        record = self.dataset[index]
        assert isinstance(record, dict)

        old_documents: List[List[Dict[Text, Any]]] = []
        new_documents: List[List[Dict[Text, Any]]] = []

        documents = zip(record["old_documents"], record["new_documents"])
        for old_document, new_document in documents:
            old_document_batches: Dict[Text, Any] = {}
            new_document_batches: Dict[Text, Any] = {}

            for key in old_document.keys():
                batches = make_batches(old_document[key], self.batch_size)
                old_document_batches[key] = self._collate_batches(batches)

            for key in new_document.keys():
                batches = make_batches(new_document[key], self.batch_size)
                new_document_batches[key] = self._collate_batches(batches)

            old_documents.append(flatten(old_document_batches))
            new_documents.append(flatten(new_document_batches))

        return {
            "old_documents": old_documents,
            "new_documents": new_documents,
            "labels": record["label"],
        }

    def collate_fn(self, samples: List[Any]) -> Any:
        if len(samples) == 1:
            return samples[0]
        return samples

    def _collate_batches(self, batches: Iterable[List[Any]]) -> List[torch.Tensor]:
        return [collate_batch(batch, self.tokenizer) for batch in batches]
