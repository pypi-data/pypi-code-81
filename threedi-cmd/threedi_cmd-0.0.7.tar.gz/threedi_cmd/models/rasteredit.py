from .base import EventWrapper
from openapi_client import SimulationsApi
from openapi_client import ThreedimodelsApi
from typing import Dict
from openapi_client.models import RasterEdit


class RasterEditError(Exception):
    pass


class RasterEditWrapper(EventWrapper):
    api_class = SimulationsApi
    model = RasterEdit
    api_path: str = "raster_edits"
    scenario_name = "rasteredit"
    raster_type = None

    def initialize_instance(self, data: Dict):
        self.raster_type = data.pop("raster__type", None)
        if self.raster_type is None and "raster" not in data:
            raise RasterEditError(
                f"Please proved either `raster__type` or `raster`"
                f"the RasterEdit: {data}"
            )

        if self.raster_type is not None:
            # Try to lookup/find the raster.
            api = ThreedimodelsApi(self._api_client)
            res = api.threedimodels_rasters_list(
                self.simulation.threedimodel, type=self.raster_type
            )
            if res.count != 1:
                raise RasterEditError(
                    f"Could not find raster_type, raster_list "
                    f"response whas {res}"
                )

            # Set raster
            data["raster"] = res.results[0].id

        super().initialize_instance(data)


WRAPPERS = [RasterEditWrapper]
