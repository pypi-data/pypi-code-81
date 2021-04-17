import logging
import typing
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Text, Type, Union

from formerbox.models.document_pair_classifier import DocumentPairClassifier, InputTypes
from formerbox.modules.transformer_module import TransformerModule
from torch import Tensor
from transformers import BartConfig, BartModel
from transformers import PreTrainedTokenizerFast as Tokenizer
from transformers.file_utils import ModelOutput

DocumentType = List[Dict[Text, InputTypes]]
DocumentList = List[DocumentType]
Batch = Dict[Text, Union[DocumentList, Tensor]]

logger = logging.getLogger(__name__)


# pylint: disable=arguments-differ
class DocumentPairClassificationModule(TransformerModule):
    @dataclass
    class Params(TransformerModule.Params):
        use_pooling: bool = field(
            default=False,
            metadata={"help": ""},
        )

    params: Params
    params_type: Type[Params] = Params

    def __init__(
        self,
        model: BartModel,
        tokenizer: Tokenizer,
        params: Params,
    ) -> None:
        super().__init__(model, tokenizer, params)

        self.classifier = DocumentPairClassifier(model, self.params.use_pooling)

        # save the arguments to easily restore
        # from the saved pytorch checkpoint
        self.save_hyperparameters()

    def forward(
        self,
        old_documents: DocumentList,
        new_documents: DocumentList,
        labels: Tensor,
        **kwargs: Any,
    ) -> ModelOutput:
        # put the module into train mode
        self.classifier.train()

        # make a forward pass with our transformer model
        outputs = self.classifier.forward(
            old_documents=old_documents,
            new_documents=new_documents,
            labels=labels,
            return_dict=True,
            **kwargs,
        )

        # the model should return a `ModelOutput` instance
        assert isinstance(outputs, ModelOutput)

        # return the model outputs
        return outputs

    def training_step(
        self,
        batch: Batch,
        batch_idx: int,
        optimizer_idx: Optional[int] = None,
        hiddens: Optional[Tensor] = None,
    ) -> Tensor:
        del batch_idx, optimizer_idx, hiddens  # nouse

        # make a model forward pass
        model_output = self.forward(**batch)

        # get the loss based on model output
        loss = model_output["loss"]
        loss = typing.cast(Tensor, loss)

        # prepare other metrics to log
        # perplexity = self.perplexity.forward(loss.detach())
        batch_size = self._batch_size(batch)
        learning_rate = self.learning_rate

        metrics = {
            "train_loss": loss,
            # "train_ppl": perplexity,
            "train_lr": learning_rate,
            "train_bsz": batch_size,
            "global_step": self.trainer.global_step,
        }

        # log training metrics
        self.log_dict(metrics, prog_bar=True)

        return loss

    def validation_step(
        self,
        batch: Dict[Text, Tensor],
        batch_idx: int,
        **kwargs: Any,
    ) -> None:
        del batch_idx, kwargs  # nouse

        # make a model forward pass
        model_output = self.forward(**batch)

        # get the loss based on model output
        loss = model_output["loss"]
        loss = typing.cast(Tensor, loss)

        # prepare other metrics to log
        # perplexity = self.perplexity.forward(loss.detach())
        metrics = {"val_loss": loss}

        # log validation metrics
        self.log_dict(metrics, prog_bar=True)

    def _document_batch_size(self, document: DocumentType) -> int:
        sentence_sample = document[0]
        sentence_input_ids = sentence_sample["input_ids"]
        assert isinstance(sentence_input_ids, Tensor)
        return sentence_input_ids.size(0)

    def _batch_size(self, batch: Batch) -> int:
        old_documents = batch["old_documents"]
        new_documents = batch["new_documents"]
        assert isinstance(old_documents, list)
        assert isinstance(new_documents, list)

        document: DocumentType
        if old_documents:
            document = old_documents[0]
        elif new_documents:
            document = new_documents[0]
        else:
            raise RuntimeError("Corrupted data. Documents must not be empty.")

        batch_size = self._document_batch_size(document)

        return batch_size
