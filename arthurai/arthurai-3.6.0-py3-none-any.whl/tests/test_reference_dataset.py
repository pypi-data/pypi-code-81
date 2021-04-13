import pandas as pd
import responses
from arthurai.common.constants import InputType, OutputType

from arthurai.core.models import ArthurModel
from tests.base_test import BaseTest


class TestReferenceData(BaseTest):

    def _mock_sending_reference_set(self, model_id):
        server_response = {
            "counts": {
                "success": 0,
                "failure": 1,
                "total": 1
            },
            "failures": [
                {
                    "message": "missing field",
                    "status": 400
                }
            ]
        }

        self.mockPost(f"/api/v3/models/{model_id}/reference_data", server_response, status=207)
        self.mockPost(f"/api/v3/models/{model_id}/reference_data", request_type=responses.PATCH, status=200,
                      dict_to_return={"message": "success"})

    @responses.activate
    def test_send_parquet_file(self):
        model_data = {
            "partner_model_id": "",
            "input_type": InputType.Tabular,
            "output_type": OutputType.Regression,
            "display_name": "",
            "description": "",
            "attributes": [],
        }
        model = ArthurModel(client=self.arthur.client, **model_data)
        model.id = "1234"
        self._mock_sending_reference_set("1234")
        resp, resp_close = model.set_reference_data(data=pd.DataFrame({"col": [1, 2, 3, 4]}))
        assert resp["counts"]["failure"] == 1
        assert resp_close is None
