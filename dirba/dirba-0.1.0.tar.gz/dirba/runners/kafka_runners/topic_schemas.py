from typing import Optional
from uuid import UUID

import pydantic

from ...models.abc import Author


class LoaderMessage(pydantic.BaseModel):
    """
    Формат, принимаемый моделью (после этапа сохранения загруженного материала)
    """
    uid_query: UUID
    query_id: int
    driver_id: int
    category_id: Optional[int]
    type_id: int
    uid_search: UUID
    uid_filter_link: UUID
    uid_loader: UUID
    uid_loaded_data: UUID
    author: Author
    type_content: str
    result: int


class ModelOutput(pydantic.BaseModel):
    category: int
    estimate: float


class AnalysisResult(pydantic.BaseModel):
    type_content: str
    content_ref: int
    model: ModelOutput


class AnalysisMessage(pydantic.BaseModel):
    """
    Формат, отправляемый моделями
    """
    uid_query: UUID
    query_id: int
    driver_id: int
    category_id: Optional[int]
    type_id: int
    uid_search: UUID
    uid_filter_link: UUID
    uid_loader: UUID
    uid_loaded_data: UUID
    uid_analysis: UUID
    author: Author
    result: AnalysisResult
