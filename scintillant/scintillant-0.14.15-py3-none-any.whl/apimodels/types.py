from http import HTTPStatus
from typing import Optional, Dict, List
from datetime import datetime
from pydantic import BaseModel


class SkillResponseType(BaseModel):
    status: str
    out_text: Optional[str]
    choices: Optional[List]
    client_app_action: Optional[str]
    requested_field_code: Optional[str]
    context: Optional[Dict]
    redirect_to: Optional[str]

    @classmethod
    async def from_json_response(cls, response: Dict): ...

    @classmethod
    async def from_response(cls, response): ...

    def serialize_json(self) -> Dict: ...


# ==============================
class Client(BaseModel):
    name: str
    type: str
    _meta_: Optional[Dict]


class User(BaseModel):
    user_id: str
    client: Client
    global_id: Optional[str]


class Update(BaseModel):
    in_text: Optional[str]
    in_choice: Optional[str]
    datetime: Optional[datetime]


class SkillRequestType(BaseModel):

    user: User
    update: Update
    context: Dict

    def serialize_json(self) -> Dict: ...

    @classmethod
    async def from_dict(cls, request): ...


class ClientResponseType(BaseModel):
    out_text: str
    status_code: HTTPStatus or int
    choices: Optional[List]
    client_app_action: Optional[str]
    requested_field_code: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict): ...

    @classmethod
    def from_skill_response(cls, response: SkillResponseType): ...

    def serialize_json(self) -> Dict: ...


class DialogAnswerRequestType(BaseModel):
    client_id: str
    client_app: str
    client_type: str
    in_text: Optional[str]
    in_choice: Optional[str]

    @classmethod
    async def from_dict(cls, request): ...

    def serialize_json(self) -> Dict: ...
