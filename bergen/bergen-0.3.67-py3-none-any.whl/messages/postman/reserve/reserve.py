from .params import ReserveParams
from pydantic.main import BaseModel
from ....messages.types import  RESERVE
from ....messages.base import MessageDataModel, MessageMetaExtensionsModel, MessageMetaModel, MessageModel
from typing import List, Optional



class ProvideMetaExtensionsModel(MessageMetaExtensionsModel):
    # Set by postman consumer
    progress: Optional[str]
    callback: Optional[str]

class ProvideMetaModel(MessageMetaModel):
    type: str = RESERVE
    extensions: Optional[ProvideMetaExtensionsModel]

class ProvideDataModel(MessageDataModel):

    node: Optional[str] #TODO: Maybe not optional
    template: Optional[str]
    params: Optional[ReserveParams]


class ReserveMessage(MessageModel):
    data: ProvideDataModel
    meta: ProvideMetaModel