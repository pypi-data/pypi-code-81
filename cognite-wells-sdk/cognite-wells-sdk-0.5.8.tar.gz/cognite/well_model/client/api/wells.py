import logging
from typing import List, Optional

from requests import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.api_base import BaseAPI
from cognite.well_model.client.api.wellbores import WellboresAPI
from cognite.well_model.client.models.resource_list import WellboreList, WellList
from cognite.well_model.client.utils._auxiliary import extend_class
from cognite.well_model.client.utils.multi_request import cursor_multi_request
from cognite.well_model.models import (
    MeasurementFilters,
    PolygonFilter,
    TrajectoryFilter,
    Well,
    WellFilter,
    WellItems,
    WellType,
)

logger = logging.getLogger("WellsAPI")


class WellsAPI(BaseAPI):
    def __init__(self, wells_client: APIClient, wellbores_api: WellboresAPI):
        super().__init__(wells_client)
        self.wellbores_api = wellbores_api

        # wrap all wells with a lazy method
        @extend_class(Well)
        def wellbores(well) -> WellboreList:
            return self.wellbores_api.get_from_well(well_id=well.id)

    def _get_label_prefix(self, prefix: str) -> List[str]:
        """
        list valid values for prefix

        @param prefix: which label to filter on
        @return: list of valid label values
        """
        path: str = self._get_path(f"/wells/{prefix}")
        response: Response = self.wells_client.get(url_path=path)
        data: List[str] = response.json()
        return data

    def blocks(self) -> List[str]:
        """ List valid block values """
        return self._get_label_prefix("blocks")

    def fields(self) -> List[str]:
        """ List valid field values """
        return self._get_label_prefix("fields")

    def operators(self) -> List[str]:
        """ List valid operator values """
        return self._get_label_prefix("operators")

    def quadrants(self) -> List[str]:
        """ List valid quadrant values """
        return self._get_label_prefix("quadrants")

    def sources(self) -> List[str]:
        """ List valid source values """
        return self._get_label_prefix("sources")

    def measurements(self) -> List[str]:
        """ List valid measurement type values """
        return self._get_label_prefix("measurements")

    def get_by_id(self, well_id: int) -> Well:
        """
        Get well from a cdf asset id

        @param well_id: cdf asset id
        @return: Well object
        """
        path: str = self._get_path(f"/wells/{well_id}")
        response: Response = self.wells_client.get(url_path=path)
        well: Well = Well.parse_raw(response.text)
        return well

    def list(self, limit=100) -> WellList:
        """
        list all wells

        @param limit
        @return: WellItems object
        """

        def request(cursor):
            path: str = self._get_path("/wells")
            response: Response = self.wells_client.get(url_path=path, params={"cursor": cursor})
            well_items: WellItems = WellItems.parse_raw(response.text)
            return well_items

        items = cursor_multi_request(
            get_cursor=self._get_cursor, get_items=self._get_items, limit=limit, request=request
        )
        return WellList(items)

    def filter(
        self,
        well_type: Optional[WellType] = None,
        string_matching: Optional[str] = None,
        quadrants: Optional[List[str]] = None,
        blocks: Optional[List[str]] = None,
        fields: Optional[List[str]] = None,
        operators: Optional[List[str]] = None,
        sources: Optional[List[str]] = None,
        has_trajectory: Optional[TrajectoryFilter] = None,
        has_measurements: Optional[MeasurementFilters] = None,
        polygon: Optional[PolygonFilter] = None,
        output_crs: Optional[str] = None,
        limit=100,
    ) -> WellList:
        """
        Get wells that matches the filter

        @param well_type - type of well, for example exploration
        @param string_matching - string to fuzzy match on description and name
        @param quadrants - list of quadrants to find wells within
        @param blocks - list of blocks to find wells within
        @param fields - list of fields to find wells within
        @param operators - list of well operators to filter on
        @param sources - list of source system names
        @param has_trajectory - filter wells which have trajectory between certain depths
        @param has_measurements - filter wells which have measurements between certain depths in their logs
        @param polygon - geographic area to find wells within
        @param output_crs - crs for the returned well head
        @param limit - number of well objects to fetch
        @return: WellItems object
        """

        def request(cursor):
            well_filter = WellFilter(
                well_type=well_type,
                string_matching=string_matching,
                quadrants=quadrants,
                blocks=blocks,
                fields=fields,
                operators=operators,
                sources=sources,
                has_trajectory=has_trajectory,
                has_measurements=has_measurements,
                polygon=polygon,
                output_crs=output_crs,
            )
            path: str = self._get_path("/wells/list")
            response: Response = self.wells_client.post(
                url_path=path, json=well_filter.json(), params={"cursor": cursor}
            )
            well_items_data: WellItems = WellItems.parse_raw(response.text)
            return well_items_data

        items = cursor_multi_request(
            get_cursor=self._get_cursor, get_items=self._get_items, limit=limit, request=request
        )
        return WellList(items)

    @staticmethod
    def _get_items(well_items: WellItems) -> List[Well]:
        return well_items.items

    @staticmethod
    def _get_cursor(well_items: WellItems) -> Optional[str]:
        return well_items.next_cursor
