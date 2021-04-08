from pydantic.main import BaseModel
from ....messages.types import  RESERVE, UNRESERVE
from ....messages.base import MessageDataModel, MessageMetaExtensionsModel, MessageMetaModel, MessageModel
from typing import List, Optional



class ProvideMetaExtensionsModel(MessageMetaExtensionsModel):
    # Set by postman consumer
    progress: Optional[str]
    callback: Optional[str]

class ProvideMetaModel(MessageMetaModel):
    type: str = UNRESERVE
    extensions: Optional[ProvideMetaExtensionsModel]

class ProvideDataModel(MessageDataModel):
    reference: Optional[str] 


class UnreserveMessage(MessageModel):
    data: ProvideDataModel
    meta: ProvideMetaModel