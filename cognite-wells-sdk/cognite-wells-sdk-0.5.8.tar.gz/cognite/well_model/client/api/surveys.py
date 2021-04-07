import logging
from typing import List, Optional

from requests import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.api_base import BaseAPI
from cognite.well_model.client.models.survey_rows import SurveyRows
from cognite.well_model.client.utils._auxiliary import extend_class
from cognite.well_model.client.utils.multi_request import cursor_multi_request
from cognite.well_model.models import Survey, SurveyData, SurveyDataRequest, SurveyRow

logger = logging.getLogger("WellsAPI")


class SurveysAPI(BaseAPI):
    def __init__(self, wells_client: APIClient):
        super().__init__(wells_client)

        @extend_class(Survey)
        def data(survey) -> SurveyRows:
            return self.get_data(survey_id=survey.id, limit=None)

    def get_trajectory(self, wellbore_id: int) -> Optional[Survey]:
        """
        Get trajectory from a cdf asset id

        @param wellbore_id: cdf asset id
        @return: Survey object
        """
        path = self._get_path(f"/wellbores/{wellbore_id}/trajectory")
        response: Response = self.wells_client.get(path)
        survey: Survey = Survey.parse_obj(response.json())
        return survey

    def get_data(
        self,
        survey_id: int,
        start: Optional[int] = None,
        end: Optional[int] = None,
        columns: Optional[List[str]] = None,
        limit: Optional[int] = 100,
    ) -> SurveyRows:
        """
        Get data from a survey id and other parameters

        @param survey_id: id of the cdf sequence
        @param start: first depth (in meters) that rows should be returned from
        @param end: last depth (in meters) that rows should be returned from
        @param columns: columns that should be included in the returned rows
        @param limit: maximum amount of rows to be returned
        @return: SurveyData object
        """

        responses = []

        def request(cursor):
            data_request = SurveyDataRequest(id=survey_id, start=start, end=end, columns=columns, limit=limit)
            data_request.cursor = cursor
            path = self._get_path("/surveys/data")
            response: Response = self.wells_client.post(path, data_request.json())
            survey_data: SurveyData = SurveyData.parse_obj(response.json())
            responses.append(survey_data)
            return survey_data

        rows = cursor_multi_request(
            get_cursor=self._get_cursor, get_items=self._get_items, limit=limit, request=request
        )
        last_response = responses[-1]
        last_response.rows = rows
        return SurveyRows.from_survey_data(last_response)

    @staticmethod
    def _get_cursor(data: SurveyData) -> Optional[str]:
        return data.next_cursor

    @staticmethod
    def _get_items(data: SurveyData) -> List[SurveyRow]:
        return data.rows
