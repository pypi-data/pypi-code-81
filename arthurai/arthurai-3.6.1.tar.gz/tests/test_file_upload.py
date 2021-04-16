from typing import Any

import os

import pandas as pd
import responses
from arthurai.common.constants import InputType, OutputType

from arthurai import ArthurModel
from tests.base_test import BaseTest


class TestFileUpload(BaseTest):

    def _mock_file_upload(self, model_id, batch_id):
        server_response = {
            "counts": {
                "success": 100,
                "failure": 0,
                "total": 100
            },
            "failures": []
        }

        self.mockPost(f"/api/v3/models/{model_id}/inferences/file", server_response, status=207)
        self.mockPost(f"/api/v3/models/{model_id}/batches/{batch_id}", request_type=responses.PATCH, status=200,
                      dict_to_return={"message": "success"})

    def _mock_failed_batch_upload(self, model_id, batch_id):
        self.mockPost(f"/api/v3/models/{model_id}/inferences/file", {}, status=400)

    def _mock_failed_batch_close(self, model_id, batch_id):
        server_response = {
            "counts": {
                "success": 100,
                "failure": 0,
                "total": 100
            },
            "failures": []
        }

        self.mockPost(f"/api/v3/models/{model_id}/inferences/file", server_response, status=207)
        self.mockPost(f"/api/v3/models/{model_id}/batches/{batch_id}", request_type=responses.PATCH, status=404,
                      dict_to_return={"message": "batch not found"})

    @responses.activate
    def test_send_batch_inferences(self):
        model = self._set_up_test_and_get_model()
        resp, resp_close = model.send_batch_inferences(
            data=pd.DataFrame({
                "inference_timestamp": [1, 2, 3, 4],
                'partner_inference_id': ["1", "2", "3", "4"],
                "inference_timestamp": ['1', '2', '3', '4'],
                "partner_inference_id": ['1', '2', '3', '4'],
                "batch_id": ['1', '1', '1', '1']
            }),
            batch_id='batch_1')
        self._assert_result(resp)
        self.assertEqual(resp_close, {"dataset_close_result": "success"})

    @responses.activate
    def test_send_batch_inferences_auto_retry(self):
        model = self._set_up_test_and_get_model(failed_batch_upload=True)
        resp, resp_close = model.send_batch_inferences(
            data=pd.DataFrame({
                "inference_timestamp": [1, 2, 3, 4],
                'partner_inference_id': ["1", "2", "3", "4"],
                "inference_timestamp": ['1', '2', '3', '4'],
                "partner_inference_id": ['1', '2', '3', '4'],
                "batch_id": ['1', '1', '1', '1']
            }),
            batch_id='batch_1')
        self.assertEqual(len(responses.calls), 4)
        resp_400 = 0
        for http_call in responses.calls:
            if http_call.response.status_code == 400:
                resp_400 += 1
        self.assertEqual(resp_400, 4)

    @responses.activate
    def test_send_batch_close_auto_retry(self):
        model = self._set_up_test_and_get_model(failed_batch_close = True)
        resp, resp_close = model.send_batch_inferences(
            data=pd.DataFrame({
                "inference_timestamp": [1, 2, 3, 4],
                'partner_inference_id': ["1", "2", "3", "4"],
                "inference_timestamp": ['1', '2', '3', '4'],
                "partner_inference_id": ['1', '2', '3', '4'],
                "batch_id": ['1', '1', '1', '1']
            }),
            batch_id='batch_1')
        self.assertEqual(len(responses.calls), 5)
        resp_404 = 0
        for http_call in responses.calls:
            if http_call.response.status_code == 404:
                resp_404 += 1
        self.assertEqual(resp_404, 4)
        self.assertEqual(resp_close, {'dataset_close_result': {"message": "batch not found"}})

    @responses.activate
    def test_send_batch_ground_truth(self):
        model = self._set_up_test_and_get_model()
        resp = model.send_batch_ground_truths(data=pd.DataFrame({"col": [1, 2, 3, 4]}))
        self._assert_result(resp)

    @responses.activate
    def test_send_parquet_batch(self):
        model = self._set_up_test_and_get_model()
        file_loc = os.path.join(os.path.dirname(__file__), 'data', 'inference_batch_data')
        resp, close_resp = model.send_batch_inferences(batch_id="batch_1", directory_path=file_loc)
        self._assert_result(resp)
        self.assertEqual(close_resp, {"dataset_close_result": "success"})

    def _set_up_test_and_get_model(self, failed_batch_upload: bool = False, failed_batch_close: bool = False):
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
        if failed_batch_upload:
            self._mock_failed_batch_upload("1234", "batch_1")
        elif failed_batch_close:
            self._mock_failed_batch_close("1234", "batch_1")
        else:
            self._mock_file_upload("1234", "batch_1")
        return model

    @staticmethod
    def _assert_result(resp: Any, success_count: int = 100, failure_count: int = 0, total_count: int = 100):
        assert resp["counts"]["success"] == success_count
        assert resp["counts"]["failure"] == failure_count
        assert resp["counts"]["total"] == total_count
