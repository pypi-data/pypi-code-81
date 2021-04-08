from ....messages.types import CANCEL_RESERVE, CANCEL_UNRESERVE
from ....messages.base import MessageDataModel, MessageMetaExtensionsModel, MessageMetaModel, MessageModel
from typing import Optional


class CancelProvideMetaModel(MessageMetaModel):
    type: str = CANCEL_UNRESERVE

class CancelProvideDataModel(MessageDataModel):
    reference: str


class CancelUnreserveMessage(MessageModel):
    data: CancelProvideDataModel
    meta: CancelProvideMetaModel