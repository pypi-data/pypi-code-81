import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, List, Optional, Text

import pandas as pd
import torch
from formerbox.data.data_collator import DataCollator, EncodedInput, collate_batch
from formerbox.data.dataset_iterators import DatasetIteratorBase
from transformers import PreTrainedTokenizerFast as Tokenizer

import datasets
from datasets import ClassLabel, load_dataset

from .utils import DiffPreprocessor, flatten


class Dataset(DatasetIteratorBase):
    def __init__(self, dataset: datasets.Dataset) -> None:
        super().__init__()
        self.dataset = dataset

    def __len__(self) -> int:
        return len(self.dataset)

    def __getitem__(self, index: int) -> Dict[Text, torch.Tensor]:
        item = self.dataset[index]
        assert isinstance(item, dict)
        return item

    def collate_fn(self, samples):
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
        list_labels = []
        for feature in features:
            list_input_ids.append(feature["input_ids"])
            list_attention_mask.append(feature["attention_mask"])
            list_labels.append(feature["labels"])

        input_ids = collate_batch(
            sequences=list_input_ids,
            tokenizer=self.tokenizer,
        )
        attention_mask = collate_batch(
            sequences=list_attention_mask,
            tokenizer=self.tokenizer,
        )
        labels = collate_batch(
            sequences=list_labels,
            tokenizer=self.tokenizer,
        )

        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": labels,
        }


class SentenceBinarizer:
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
        all_sentences = []
        for record in dataset:
            assert isinstance(record, dict)
            sentences = record["sentences"]
            all_sentences.extend(sentences)
        dataset = datasets.Dataset.from_pandas(pd.DataFrame(all_sentences))

        # convert outputs to pytorch tensors and save
        # columns = ["input_ids", "attention_mask"]
        # if "labels" in dataset.features:
        #     columns.append("labels")
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

        sentences = []
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
            document = dict(encoding.items())
            document = flatten(document)

            for sentence in document:
                label: Optional[Text]
                if not column["labels"]:
                    label = None
                elif self.is_test(sentence, old_filepath, new_filepath):
                    label = "test"
                elif self.is_unknown(sentence):
                    label = "unknown"
                else:
                    label = column["labels"][0]

                if label is not None:
                    sentence["labels"] = self.labels.str2int(label)
                sentences.append(sentence)

        return {"sentences": sentences}

    def get_labels(self, dataset: datasets.Dataset) -> ClassLabel:
        all_labels: List[Text] = []
        for labels in dataset["labels"]:
            assert isinstance(labels, list)
            if not labels:
                break
            assert isinstance(labels[0], str)
            all_labels.append(labels[0])

        all_labels = sorted(set(all_labels)) + ["unknown"]
        return ClassLabel(names=all_labels)

    def is_test(
        self, sentence: Dict[Any, Any], source_filename: Text, target_filename: Text
    ) -> bool:
        contains_test_substring = False
        if "tests" in source_filename or "test_" in source_filename:
            contains_test_substring = True
        elif "tests" in target_filename or "test_" in target_filename:
            contains_test_substring = True

        if not contains_test_substring:
            return False

        input_ids = sentence["input_ids"]
        assert isinstance(input_ids, (torch.Tensor, list))

        for token_id in self.meta_special_tokens():
            if token_id in input_ids:
                return True

        for token_id in self.diff_special_tokens():
            if token_id in input_ids:
                return True

        return False

    def is_unknown(self, sentence: Dict[Any, Any]) -> bool:
        input_ids = sentence["input_ids"]
        assert isinstance(input_ids, (torch.Tensor, list))

        for token_id in self.diff_special_tokens():
            if token_id in input_ids:
                return False

        return True

    @lru_cache(maxsize=8)
    def all_special_tokens(self) -> List[int]:
        tokens = [
            self.preprocessor.add_start_token,
            self.preprocessor.del_start_token,
        ]

        special_tokens = self.tokenizer.convert_tokens_to_ids(tokens)
        assert isinstance(special_tokens, list)
        return special_tokens

    @lru_cache(maxsize=8)
    def meta_special_tokens(self) -> List[int]:
        tokens = [
            self.preprocessor.fromfile_start_token,
            self.preprocessor.tofile_start_token,
        ]

        special_tokens = self.tokenizer.convert_tokens_to_ids(tokens)
        assert isinstance(special_tokens, list)
        return special_tokens

    @lru_cache(maxsize=8)
    def diff_special_tokens(self) -> List[int]:
        tokens = [
            self.preprocessor.add_start_token,
            self.preprocessor.del_start_token,
        ]

        special_tokens = self.tokenizer.convert_tokens_to_ids(tokens)
        assert isinstance(special_tokens, list)
        return special_tokens
