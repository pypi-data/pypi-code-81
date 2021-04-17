import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Text

import pandas as pd
import torch
from formerbox.data.data_collator import DataCollator, EncodedInput, collate_batch
from formerbox.data.dataset_iterators import DatasetIteratorBase
from transformers import PreTrainedTokenizerFast as Tokenizer

import datasets
from datasets import ClassLabel, load_dataset

from .utils import DiffPreprocessor, flatten, make_batches


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


class DocumentBinarizer:
    def __init__(self, tokenizer: Tokenizer) -> None:
        self.tokenizer = tokenizer
        self.preprocessor = DiffPreprocessor()
        self.labels: Optional[ClassLabel] = None

    def process(self, script_path: Text, dataset_path: Text, output_path: Text) -> None:
        # load classification dataset
        dataset = load_dataset(
            path=script_path,
            data_files=[dataset_path],
            split="train",
        )

        # prepare dataset labels
        assert isinstance(dataset, datasets.Dataset)
        self.labels = self.get_labels(dataset)

        # add diff preprocessor special tokens
        special_tokens: List[Any] = self.preprocessor.special_tokens
        self.tokenizer.add_tokens(special_tokens)

        # tokenize loaded dataset
        dataset = dataset.map(
            function=self.encode,
            num_proc=4,
            remove_columns=["commit", "labels", "repository"],
            load_from_cache_file=False,
        )

        # flatten tokenized chunks
        all_documents = []
        for record in dataset:
            assert isinstance(record, dict)
            documents = record["documents"]
            all_documents.extend(documents)
        dataset = datasets.Dataset.from_pandas(pd.DataFrame(all_documents))

        # convert outputs to pytorch tensors and save
        # columns = ["sentences", "labels"]
        dataset.features["labels"] = self.labels
        # dataset.set_format(type="torch", columns=columns)
        dataset.save_to_disk(output_path)

        # save pretrained tokenizer
        token_config_kwargs = getattr(self.tokenizer, "init_kwargs", {})
        token_config_kwargs.pop("name_or_path", None)
        token_config_kwargs.pop("special_tokens_map_file", None)
        setattr(self.tokenizer, "init_kwargs", token_config_kwargs)

        tokenizer_path = os.path.join(output_path, "tokenizer")
        self.tokenizer.save_pretrained(tokenizer_path, legacy_format=False)

    def encode(self, column: Dict[Text, Any]) -> Dict[Text, Any]:
        assert self.labels is not None
        commit = column["commit"]
        modifications = commit["modifications"]

        documents = []
        for modification in modifications:
            old_filepath = modification["old_filepath"] or ""
            old_content = modification["old_content"] or ""
            new_filepath = modification["new_filepath"] or ""
            new_content = modification["new_content"] or ""

            inputs = self.preprocessor.preprocess(
                source_content=old_content,
                target_content=new_content,
                source_file=old_filepath,
                target_file=new_filepath,
                context_size=4,
            )

            encoding = self.tokenizer(
                inputs,
                stride=0,
                padding=True,
                truncation=True,
                pad_to_multiple_of=8,
                return_overflowing_tokens=True,
            )

            del encoding["overflow_to_sample_mapping"]
            sentences = dict(encoding.items())
            sentences = flatten(sentences)

            label: Text
            if self.is_test(old_filepath, new_filepath):
                label = "test"
            else:
                label = column["labels"][0]

            documents.append(
                {"sentences": sentences, "labels": self.labels.str2int(label)}
            )

        return {"documents": documents}

    def get_labels(self, dataset: datasets.Dataset) -> ClassLabel:
        all_labels: List[Text] = []
        for labels in dataset["labels"]:
            assert isinstance(labels, list)
            assert isinstance(labels[0], str)
            all_labels.append(labels[0])

        all_labels = sorted(set(all_labels))
        return ClassLabel(names=all_labels)

    def is_test(self, source_filename: Text, target_filename: Text) -> bool:
        contains_test_substring = False
        if "tests" in source_filename or "test_" in source_filename:
            contains_test_substring = True
        elif "tests" in target_filename or "test_" in target_filename:
            contains_test_substring = True

        if not contains_test_substring:
            return False

        return False
