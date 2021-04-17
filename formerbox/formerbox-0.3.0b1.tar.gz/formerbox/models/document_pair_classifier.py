import typing
from copy import deepcopy
from typing import Any, Dict, List, Optional, Text, Tuple, Union
from dataclasses import dataclass
import torch
import torch.nn as nn
from transformers import BartConfig, BartModel
from transformers.modeling_outputs import ModelOutput
from transformers.models.bart.modeling_bart import BartClassificationHead

InputTypes = Union[
    Optional[torch.Tensor],
    Optional[Tuple[torch.Tensor, ...]],
    Optional[bool],
]


@dataclass
class DocumentPairClassifierOutput(ModelOutput):
    logits: torch.Tensor
    loss: Optional[torch.Tensor] = None


class SentenceEmbedding(nn.Module):
    def __init__(self, pretrained_model: BartModel, use_pooling: bool = False) -> None:
        super().__init__()

        assert isinstance(pretrained_model.config, BartConfig)
        self.config = deepcopy(pretrained_model.config)
        self.pretrained_model = pretrained_model
        self.use_pooling = use_pooling

    def forward(
        self,
        input_ids: Optional[torch.Tensor] = None,
        attention_mask: Optional[torch.Tensor] = None,
        decoder_input_ids: Optional[torch.Tensor] = None,
        decoder_attention_mask: Optional[torch.Tensor] = None,
        encoder_outputs: Optional[Tuple[torch.Tensor, ...]] = None,
        past_key_values: Optional[Tuple[torch.Tensor, ...]] = None,
        inputs_embeds: Optional[torch.Tensor] = None,
        decoder_inputs_embeds: Optional[torch.Tensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
    ) -> torch.Tensor:
        if return_dict is None:
            return_dict = self.config.use_return_dict

        if input_ids is None and inputs_embeds is not None:
            raise RuntimeError(
                f"Passing input embeddings is currently not supported for {self.__class__.__name__}"
            )

        outputs = self.pretrained_model(
            input_ids,
            attention_mask=attention_mask,
            decoder_input_ids=decoder_input_ids,
            decoder_attention_mask=decoder_attention_mask,
            encoder_outputs=encoder_outputs,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            decoder_inputs_embeds=decoder_inputs_embeds,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )

        last_hidden_state = outputs[0]

        if self.use_pooling:
            sentence_embedding = torch.mean(last_hidden_state, dim=1)
        else:
            eos_mask = input_ids.eq(self.config.eos_token_id)

            sentence_embedding = last_hidden_state[eos_mask, :]
            sentence_embedding = sentence_embedding.view(
                last_hidden_state.size(0), -1, last_hidden_state.size(-1)
            )

            sentence_embedding = sentence_embedding[:, -1, :]

        return sentence_embedding


class DocumentEmbedding(nn.Module):
    def __init__(self, pretrained_model: BartModel, use_pooling: bool = False) -> None:
        super().__init__()

        self.config = deepcopy(pretrained_model.config)
        self.pretrained_model = pretrained_model
        self.sentence_embedder = SentenceEmbedding(pretrained_model, use_pooling)

    def forward(
        self, document: List[Dict[Text, InputTypes]], **kwargs: Any
    ) -> torch.Tensor:
        sentence_embeddings = []
        for sentence in document:
            sentence_embedding = self.sentence_embedder.forward(**sentence, **kwargs)
            sentence_embeddings.append(sentence_embedding.detach())

        inputs_embeddings = torch.cat(sentence_embeddings)
        inputs_embeddings = inputs_embeddings.unsqueeze(dim=0)

        outputs = self.pretrained_model(
            inputs_embeds=inputs_embeddings,
            decoder_inputs_embeds=inputs_embeddings,
        )

        last_hidden_state = outputs[0]
        document_embedding = torch.mean(last_hidden_state, dim=1)

        return document_embedding


class DocumentPairEmbedding(nn.Module):
    def __init__(self, pretrained_model: BartModel, use_pooling: bool = False) -> None:
        super().__init__()

        assert isinstance(pretrained_model.config, BartConfig)
        self.config = deepcopy(pretrained_model.config)
        self.pretrained_model = pretrained_model
        self.document_embedder = DocumentEmbedding(pretrained_model, use_pooling)

    def forward(
        self,
        old_document: List[Dict[Text, InputTypes]],
        new_document: List[Dict[Text, InputTypes]],
        **kwargs: Any,
    ) -> torch.Tensor:
        old_document_embedding = self.document_embedder(old_document, **kwargs)
        new_document_embedding = self.document_embedder(new_document, **kwargs)

        document_pair_embedding = torch.cat(
            (
                old_document_embedding,
                new_document_embedding,
                torch.abs(old_document_embedding - new_document_embedding),
            )
        )

        document_pair_embedding = torch.mean(document_pair_embedding, dim=0)
        document_pair_embedding = document_pair_embedding.unsqueeze(0)

        return document_pair_embedding


class DocumentPairClassifier(nn.Module):
    def __init__(self, pretrained_model: BartModel, use_pooling: bool = False) -> None:
        super().__init__()

        assert isinstance(pretrained_model.config, BartConfig)
        self.config = deepcopy(pretrained_model.config)
        self.pretrained_model = pretrained_model
        self.document_pair_embedder = DocumentPairEmbedding(
            pretrained_model, use_pooling
        )

        self.classification_head = BartClassificationHead(
            self.config.d_model,
            self.config.d_model,
            self.config.num_labels,
            self.config.classifier_dropout,
        )

    def forward(
        self,
        old_documents: List[List[Dict[Text, InputTypes]]],
        new_documents: List[List[Dict[Text, InputTypes]]],
        labels: Optional[torch.Tensor] = None,
        return_dict: Optional[bool] = None,
        **kwargs: Any,
    ) -> Union[Tuple[torch.Tensor, ...], DocumentPairClassifierOutput]:
        if return_dict is None:
            assert isinstance(self.config.return_dict, bool)
            return_dict = self.config.return_dict

        documents = zip(old_documents, new_documents)
        document_pair_embeddings = []

        for old_document, new_document in documents:
            document_pair_embedding = self.document_pair_embedder(
                old_document, new_document, **kwargs
            )
            document_pair_embeddings.append(document_pair_embedding)

        embeddings = torch.cat(document_pair_embeddings, dim=0)
        embeddings = torch.mean(embeddings, dim=0)

        logits = self.classification_head(embeddings)
        logits = typing.cast(torch.Tensor, logits)
        output = (logits,)

        loss: Optional[torch.Tensor] = None
        if labels is not None:
            criterion = nn.CrossEntropyLoss()
            loss = criterion(logits.view(-1, self.config.num_labels), labels.view(-1))
            loss = typing.cast(torch.Tensor, loss)
            output = (loss,) + output

        if not return_dict:
            return output

        return DocumentPairClassifierOutput(logits=logits, loss=loss)
