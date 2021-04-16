from typing import Tuple

import pydantic
from requests import Response

from .abc import AbstractDataLoader, ContentUrl


class ImageData(pydantic.BaseModel):
    content_type: str
    content: bytes


class ImageLoader(AbstractDataLoader):
    def extract_data(self, data_service_response: Response, url: ContentUrl) -> ImageData:
        data = ImageData(content_type=data_service_response.headers['content-type'],
                         content=data_service_response.content)
        return data

    def entity(self) -> str:
        return 'Images/file'

    def get_content(self, entity_id: int) -> Tuple[ContentUrl, ImageData]:
        return super().get_content(entity_id)
