import logging
from typing import Any, List, Optional, cast

from requests import Response

from cognite.well_model._asset_model import Asset
from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.api_base import BaseAPI
from cognite.well_model.client.api.surveys import SurveysAPI
from cognite.well_model.client.models.resource_list import SequenceList, WellboreList
from cognite.well_model.client.models.sequence_rows import SequenceRows
from cognite.well_model.client.utils._auxiliary import extend_class
from cognite.well_model.client.utils.multi_request import cursor_multi_request
from cognite.well_model.models import (
    GetSequenceDTO,
    Measurement,
    MeasurementType,
    SequenceDataRequestDTO,
    SequenceGetData,
    SequenceRowDTO,
    Survey,
    Wellbore,
    WellIds,
)

logger = logging.getLogger("WellboresAPI")


class WellboresAPI(BaseAPI):
    def __init__(self, wells_client: APIClient, survey_api: SurveysAPI):
        super().__init__(wells_client)
        self.survey_api = survey_api

        # wrap all wellbores with a lazy method
        @extend_class(Wellbore)
        def trajectory(wellbore) -> Optional[Survey]:
            return survey_api.get_trajectory(wellbore.id)

        @extend_class(Wellbore)
        def source_assets(wellbore, source_label: Optional[str] = None) -> List[Asset]:
            return self.get_sources(wellbore_id=wellbore.id, source_label=source_label)

    def get_by_id(self, wellbore_id: int) -> Wellbore:
        """
        Get wellbore from a cdf asset id

        @param wellbore_id: cdf asset id
        @return: Wellbore object
        """
        path: str = self._get_path(f"/wellbores/{wellbore_id}")
        response: Response = self.wells_client.get(url_path=path)
        wb: Wellbore = Wellbore.parse_raw(response.text)
        return wb

    def get_from_well(self, well_id: int) -> WellboreList:
        """
        get wellbores from a well id

        @param well_id: well id of interest
        @return: wellbores that has the well of interest as parent
        """
        path: str = self._get_path(f"/wells/{well_id}/wellbores")
        response: Response = self.wells_client.get(url_path=path)
        return WellboreList([Wellbore.parse_obj(x) for x in response.json()])

    def get_from_wells(self, well_ids: List[int]) -> WellboreList:
        """
        Return multiple wellbores from multiple input well ids

        @param well_ids: list of well ids we want the wellbores from
        @return: list of wellbores
        """
        path: str = self._get_path("/wellbores/bywellids")
        ids = WellIds(items=well_ids)
        well_ids_serialized = ids.json()
        response: Response = self.wells_client.post(url_path=path, json=well_ids_serialized)
        return WellboreList([Wellbore.parse_obj(x) for x in response.json()])

    def get_measurement(self, wellbore_id: int, measurement_type: MeasurementType) -> List[Measurement]:
        """
        retrieve measurements for a wellbore

        @param wellbore_id: The wellbore id of interest
        @param measurement_type: The measurement type of interest
        @return: list of measurements
        """
        path: str = self._get_path(f"/wellbores/{wellbore_id}/measurements/{measurement_type}")
        response: Response = self.wells_client.get(url_path=path)
        return [Measurement.parse_obj(x) for x in response.json()["items"]]

    def get_sources(self, wellbore_id: int, source_label: Optional[str] = None) -> List[Asset]:
        """
        Return all source assets associated to a wellbore

        @param wellbore_id: The wellbore id of interest
        @param source_label: the source label for the wellbore object
        @return: list of assets
        """
        path: str = f"/wellbores/{wellbore_id}/sources"
        if source_label is not None:
            path += f"/{source_label}"
        path = self._get_path(path)
        response: Response = self.wells_client.get(url_path=path)
        assets: List[Asset] = [Asset.parse_obj(x) for x in response.json()]
        return assets

    def get_casings(self, well_or_wellbore_id: int) -> SequenceList:
        """
        @param well_or_wellbore_id:
        @return:
        """
        path = self._get_path(f"/wells/{well_or_wellbore_id}/casings")
        response: Response = self.wells_client.get(path)
        items = [GetSequenceDTO.parse_obj(x) for x in response.json()]
        return SequenceList(items)

    def get_casings_data(
        self,
        casing_id: int,
        start: Optional[int] = None,
        end: Optional[int] = None,
        columns: Optional[List[str]] = None,
        limit: Optional[int] = 100,
    ) -> SequenceRows:
        """
        Get data from a survey id and other parameters

        @param casing_id: id of the cdf sequence
        @param start: first depth (in meters) that rows should be returned from
        @param end: last depth (in meters) that rows should be returned from
        @param columns: columns that should be included in the returned rows
        @param limit: maximum amount of rows to be returned
        @return: SequenceRows object
        """
        responses = []

        def request(cursor):
            data_request = SequenceDataRequestDTO(id=casing_id, start=start, end=end, columns=columns, limit=limit)
            data_request.cursor = cursor
            path = self._get_path("/wells/casings/data")
            response: Response = self.wells_client.post(path, data_request.json())
            sequence_data: SequenceGetData = SequenceGetData.parse_obj(response.json())
            responses.append(sequence_data)
            return sequence_data

        rows = cursor_multi_request(get_cursor=self._get_cursor, get_items=self._get_rows, limit=limit, request=request)
        last_response = responses[-1]
        last_response.rows = rows
        return SequenceRows.from_sequence_data(last_response)

    @staticmethod
    def _get_cursor(data: SequenceGetData) -> Optional[str]:
        return cast(Optional[str], data.next_cursor)

    @staticmethod
    def _get_rows(data: SequenceGetData) -> List[SequenceRowDTO]:
        return cast(List[Any], data.rows)
