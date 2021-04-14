from flask import Response, jsonify

from ..CommandHandler.Outcome.Failure import Failure
from ..Service import RequestIdProvider


class JSend:
    def __init__(self, request_id_provider: RequestIdProvider, api_version: str = ""):
        self.__request_id_provider = request_id_provider
        self.__api_version = api_version

    def build_success_response(self, data: dict = None) -> Response:
        meta = self.__get_meta()
        return jsonify({"status": "success", "data": data, "meta": meta})

    def build_fail_response(self, failure: Failure) -> Response:
        return jsonify(
            {
                "status": "fail",
                "data": {
                    "reason": failure.get_id(),
                    "description": failure.get_message(),
                    "details": failure.get_details(),
                },
                "meta": self.__get_meta(),
            }
        )

    def build_error_response(self) -> Response:
        return jsonify(
            {
                "status": "error",
                "message": "Internal server error.",
                "meta": self.__get_meta(),
            }
        )

    def __get_meta(self):
        return {
            "requestId": self.__request_id_provider.get_request_id(),
            "apiVersion": self.__api_version,
        }
