from .schemas import *
from ehelply_python_sdk.services.service_sdk_base import SDKBase


class MonitorSDK(SDKBase):
    def get_base_url(self) -> str:
        return super().get_base_url() + "/monitors"

    def get_docs_url(self) -> str:
        return super().get_docs_url()

    def get_service_version(self) -> str:
        return super().get_service_version()

    def search_projects(
            self,
            name: str = None,
            is_spend_maxed: bool = None,
            pagination: Pagination = None
    ) -> Union[GenericHTTPResponse, PageResponse]:
        params: dict = {}

        if name is not None:
            params["name"] = name

        if is_spend_maxed is not None:
            params["is_spend_maxed"] = is_spend_maxed

        if pagination:
            params["page"] = pagination.next_page
            params["page_size"] = pagination.page_size

        response: PageResponse = transform_response_to_schema(
            self.requests_session.get(
                self.get_base_url() + "/projects/projects",
                params=params
            ),
            schema=PageResponse
        )

        if is_response_error(response):
            return response

        response.transform_dict(pydantic_type=SearchProjectItem)

        return response

    def get_project(
            self,
            project_uuid: str
    ) -> Union[GenericHTTPResponse, GetProjectResponse]:
        return transform_response_to_schema(
            self.requests_session.get(
                self.get_base_url() + "/projects/projects/" + project_uuid
            ),
            schema=GetProjectResponse
        )

    def get_all_project_usage(
            self,
            project_uuid: str,
            year: int = None,
            month: int = None
    ) -> Union[GenericHTTPResponse, GetUsageResponse]:
        params: dict = {}

        if year is not None:
            params["year"] = year

        if month is not None:
            params["month"] = month

        return transform_response_to_schema(
            self.requests_session.get(
                self.get_base_url() + "/projects/projects/" + project_uuid + "/usage",
                params=params
            ),
            schema=GetUsageResponse
        )
