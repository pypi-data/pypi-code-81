import logging
from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional, Text, Type

import torch
from formerbox.common.dataclass_argparse import MISSING, DataclassBase
from formerbox.common.has_params import HasParsableParams
from formerbox.common.registrable import Registrable
from formerbox.data.dataset_iterators import DatasetIterator, DatasetIteratorBase
from formerbox.data.indexed_dataset import IndexedDatasetBase
from pytorch_lightning import LightningDataModule
from pytorch_lightning.core.datamodule import _DataModuleWrapper
from torch.utils.data import DataLoader
from transformers import DataCollator
from transformers import PreTrainedTokenizerFast as Tokenizer

try:
    from typing_extensions import _ProtocolMeta  # type: ignore
except ImportError:
    from typing import _ProtocolMeta  # type: ignore

logger = logging.getLogger(__name__)


class DataLoadingMixin:
    def __init__(
        self,
        max_tokens: Optional[int],
        batch_size: Optional[int],
    ) -> None:
        super().__init__()
        self.max_tokens = max_tokens
        self.batch_size = batch_size

    def get_dataset_itr(
        self,
        dataset: IndexedDatasetBase,
        collator: DataCollator,
        shuffle: bool,
        drop_last: bool,
    ) -> DatasetIterator:
        dataset_itr = DatasetIterator(
            dataset,
            collator=collator,
            max_tokens=self.max_tokens,
            batch_size=self.batch_size,
            shuffle=shuffle,
            drop_last=drop_last,
        )

        return dataset_itr


class _MetaDataModule(_ProtocolMeta, _DataModuleWrapper):
    """Implements both meta classes to avoid TypeError exceptions."""


class TransformerDataModule(
    DataLoadingMixin,
    LightningDataModule,
    Registrable,
    HasParsableParams,
    metaclass=_MetaDataModule,
):
    @dataclass
    class Params(DataclassBase):
        train_data_prefix: Text = field(
            default=MISSING,
            metadata={"help": "A prefix path for the train dataset file."},
        )
        val_data_prefix: Text = field(
            default=MISSING,
            metadata={"help": "A prefix path for the validation dataset file."},
        )
        batch_size: Optional[int] = field(
            default=None,
            metadata={"help": "A number of instances/sentences in a batch."},
        )
        max_tokens: Optional[int] = field(
            default=None,
            metadata={"help": "A number of tokens in a batch."},
        )
        num_workers: int = field(
            default=0,
            metadata={"help": "A number of workers for data loading."},
        )
        pin_memory: bool = field(
            default=False,
            metadata={"help": ""},
        )

    params: Params
    params_type: Type[Params] = Params

    def __init__(self, tokenizer: Tokenizer, params: Params) -> None:
        super().__init__(params.max_tokens, params.batch_size)

        self.tokenizer = tokenizer
        self.params = params
        self.train_iterator: Optional[DatasetIteratorBase] = None
        self.val_iterator: Optional[DatasetIteratorBase] = None

    def prepare_data(self, *args: Any, **kwargs: Any) -> None:
        return

    def transfer_batch_to_device(self, batch: Any, device: torch.device) -> Any:
        return batch

    @abstractmethod
    def setup(self, stage: Optional[Text] = None) -> None:
        raise NotImplementedError()

    def train_dataloader(self, *args: Any, **kwargs: Any) -> DataLoader:
        del args, kwargs  # use initialized properties to make a dataloader
        assert self.train_iterator is not None
        return DataLoader(
            dataset=self.train_iterator,
            collate_fn=self.train_iterator.collate_fn,
            num_workers=self.params.num_workers,
            pin_memory=self.params.pin_memory,
        )

    def val_dataloader(self, *args: Any, **kwargs: Any) -> DataLoader:
        del args, kwargs  # use initialized properties to make a dataloader
        assert self.val_iterator is not None
        return DataLoader(
            dataset=self.val_iterator,
            collate_fn=self.train_iterator.collate_fn,
            num_workers=self.params.num_workers,
            pin_memory=self.params.pin_memory,
        )

    def test_dataloader(self, *args: Any, **kwargs: Any) -> DataLoader:
        raise RuntimeError("Test test partition is not supported yet")
