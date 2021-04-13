from datetime import datetime, timezone

import responses
import pytest

from arthurai.common.constants import InputType, OutputType
from arthurai.core.models import ArthurModel
from tests.base_test import BaseTest
from arthurai import util as arthur_util


class TestInferences(BaseTest):

    def _mock_posting_inferences(self, model_id):
        server_response = {
            "counts": {
                "success": 1,
                "failure": 0,
                "total": 1
            },
            "failures": [
                {
                    "message": "Success",
                    "status": 200
                }
            ]
        }

        self.mockPost(f"/api/v3/models/{model_id}/inferences", server_response, status=207)

    def _create_mock_model(self):
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
        return model

    def test_format_inference_no_gt(self):
        model = self._create_mock_model()

        inference = model._format_inference_request(
            inference_timestamp=datetime(2020, 8, 13, 17, 44, 31, tzinfo=timezone.utc),
            partner_inference_id="1234",
            model_pipeline_input=ArthurModel._replace_nans_and_infinities_in_dict({"attr": 5}),
            non_input_data=ArthurModel._replace_nans_and_infinities_in_dict({"Gender": "male"}),
            predicted_value=ArthurModel._replace_nans_and_infinities_in_dict({"prediction": 800}),
            ground_truth=ArthurModel._replace_nans_and_infinities_in_dict(None)
        )

        inferences = arthur_util.format_timestamps([inference])
        assert len(inferences) == 1
        assert inferences[0]["inference_timestamp"] == "2020-08-13T17:44:31Z"
        assert "ground_truth_timestamp" not in inferences[0]
        assert "ground_truth" not in inferences[0]


    @responses.activate
    def test_format_inference_request(self):
        model = self._create_mock_model()

        inf = model._format_inference_request(
            inference_timestamp="2020-08-13T17:44:31.552125Z",
            partner_inference_id="1234",
            model_pipeline_input={"attr": 5},
            non_input_data={"Gender": "male"},
            predicted_value={"prediction": 800},
            ground_truth={"actual_value": 812}
        )

        expected = {
            "inference_timestamp": "2020-08-13T17:44:31.552125Z",
            "partner_inference_id": "1234",
            "inference_data": {"attr": 5, "Gender": "male", "prediction": 800},
            "ground_truth_timestamp": "2020-08-13T17:44:31.552125Z",
            "ground_truth_data": {"actual_value": 812}
        }

        assert inf == expected

    def test_update_inference_timestamp(self):
        inference_incorrect_timestamps = [
            {
                "inference_timestamp": datetime(2020, 8, 13, 17, 44, 31, tzinfo=timezone.utc),
                "partner_inference_id": "1234",
                "inference_data": {"attr": 5, "Gender": "male", "prediction": 800},
                "ground_truth_timestamp": datetime(2020, 8, 13, 17, 44, 31, tzinfo=timezone.utc),
                "ground_truth_data": {"actual_value": 812}
            },
            {
                "inference_timestamp": datetime(2020, 8, 13, 17, 44, 31, tzinfo=timezone.utc),
                "partner_inference_id": "1234",
                "inference_data": {"attr": 5, "Gender": "male", "prediction": 800},
                "ground_truth_timestamp": datetime(2020, 8, 13, 17, 44, 31, tzinfo=timezone.utc),
                "ground_truth_data": {"actual_value": 812}
            }
        ]

        reformatted_inferences = arthur_util.format_timestamps(inference_incorrect_timestamps)
        for inf in reformatted_inferences:
            assert inf["inference_timestamp"] == inf["ground_truth_timestamp"] == "2020-08-13T17:44:31Z"

    def test_string_update_inference_timestamp(self):
        inference_incorrect_timestamps = [
            {
                "inference_timestamp": datetime(2020, 8, 13, 17, 44, 31, tzinfo=timezone.utc),
                "partner_inference_id": "1234",
                "inference_data": {"attr": 5, "Gender": "male", "prediction": 800},
                "ground_truth_timestamp": "2020-08-13T17:44:31.552125",
                "ground_truth_data": {"actual_value": 812}
            },
            {
                "inference_timestamp": "2020-08-13T17:44:31.552125",
                "partner_inference_id": "1234",
                "inference_data": {"attr": 5, "Gender": "male", "prediction": 800},
                "ground_truth_timestamp": datetime(2020, 8, 13, 17, 44, 31, tzinfo=timezone.utc),
                "ground_truth_data": {"actual_value": 812}
            }
        ]

        reformatted_inferences = arthur_util.format_timestamps(inference_incorrect_timestamps)
        for inf in reformatted_inferences:
            assert inf["inference_timestamp"] in ["2020-08-13T17:44:31Z", "2020-08-13T17:44:31.552125Z"]
            assert inf["ground_truth_timestamp"] in ["2020-08-13T17:44:31Z", "2020-08-13T17:44:31.552125Z"]

        # TODO: uncomment this block and delete one above to depreciate support for strings
        # for obj in inference_incorrect_timestamps:
        #     with pytest.raises(TypeError):
        #         arthur_util.format_timestamps([obj])

    def test_format_timestamp_with_location(self):
        unaware_timestamp = datetime(2021, 2, 8, 12, 10, 5)
        assert arthur_util.format_timestamp(unaware_timestamp, "America/Phoenix") == "2021-02-08T19:10:05Z" 
        