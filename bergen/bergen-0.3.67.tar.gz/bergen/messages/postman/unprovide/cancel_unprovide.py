from ....messages.types import CANCEL_PROVIDE, CANCEL_UNPROVIDE
from ....messages.base import MessageDataModel, MessageMetaExtensionsModel, MessageMetaModel, MessageModel
from typing import Optional


class CancelProvideMetaModel(MessageMetaModel):
    type: str = CANCEL_UNPROVIDE

class CancelProvideDataModel(MessageDataModel):
    reference: str


class CancelUnprovideMessage(MessageModel):
    data: CancelProvideDataModel
    meta: CancelProvideMetaModel