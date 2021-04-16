import pydantic
from requests import Response

from .abc import AbstractDataLoader, ContentUrl


class ResponseSchema(pydantic.BaseModel):
    id: int
    uidLoaderData: str
    content: str


class TextLoader(AbstractDataLoader):
    def extract_data(self, data_service_response: Response, url: ContentUrl) -> str:
        data = self._extract_data_by_schema(data_service_response, ResponseSchema)
        return data.content

    def entity(self) -> str:
        return 'Texts'
