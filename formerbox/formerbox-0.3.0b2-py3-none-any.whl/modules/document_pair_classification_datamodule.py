import logging
from dataclasses import dataclass, field
from typing import Optional, Text, Type, Any

import datasets
from formerbox.common.dataclass_argparse import MISSING
from formerbox.models.document_pair_dataset import DocumentPairDataset
from formerbox.modules.transformer_datamodule import TransformerDataModule
from transformers import PreTrainedTokenizerFast as Tokenizer
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler

logger = logging.getLogger(__name__)


class DocumentPairClassificationDataModule(TransformerDataModule):
    @dataclass
    class Params(TransformerDataModule.Params):
        train_data_prefix: Text = field(
            default=MISSING,
            metadata={"help": "A prefix path for the train dataset file."},
        )
        val_data_prefix: Text = field(
            default=MISSING,
            metadata={"help": "A prefix path for the validation dataset file."},
        )
        batch_size: int = field(
            default=MISSING,
            metadata={"help": "A number of instances/sentences in a batch."},
        )

    params: Params
    params_type: Type[Params] = Params

    def __init__(self, tokenizer: Tokenizer, params: Params) -> None:
        super().__init__(tokenizer, params)
        self.tokenizer = tokenizer
        self.params = params

    def setup(self, stage: Optional[Text] = None) -> None:
        # prepare a train dataset iterator
        train_path = str(self.params.train_data_prefix)
        train_dataset = datasets.load_from_disk(train_path)
        assert isinstance(train_dataset, datasets.Dataset)

        self.train_iterator = DocumentPairDataset(
            dataset=train_dataset,
            tokenizer=self.tokenizer,
            batch_size=self.params.batch_size,
        )

        # prepare a validation dataset iterator
        val_path = str(self.params.val_data_prefix)
        val_dataset = datasets.load_from_disk(val_path)
        assert isinstance(val_dataset, datasets.Dataset)

        self.val_iterator = DocumentPairDataset(
            dataset=val_dataset,
            tokenizer=self.tokenizer,
            batch_size=self.params.batch_size,
        )

    def train_dataloader(self, *args: Any, **kwargs: Any) -> DataLoader:
        assert self.train_iterator is not None
        return DataLoader(
            dataset=self.train_iterator,
            collate_fn=self.train_iterator.collate_fn,
            num_workers=self.params.num_workers,
            pin_memory=self.params.pin_memory,
            sampler=RandomSampler(self.train_iterator),
        )

    def val_dataloader(self, *args: Any, **kwargs: Any) -> DataLoader:
        assert self.val_iterator is not None
        return DataLoader(
            dataset=self.val_iterator,
            collate_fn=self.train_iterator.collate_fn,
            num_workers=self.params.num_workers,
            pin_memory=self.params.pin_memory,
            sampler=SequentialSampler(self.val_iterator),
        )
