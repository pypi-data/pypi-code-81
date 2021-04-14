import logging
from typing import Optional, Dict

import annotell.input_api.model as IAM
from annotell.input_api.file_resource_client import FileResourceClient
from annotell.input_api.http_client import HttpClient
from annotell.input_api.util import get_image_dimensions

log = logging.getLogger(__name__)


class CreateableInputAPIResource(FileResourceClient):

    def __init__(self, client: HttpClient, file_resource_client: FileResourceClient):
        super().__init__()
        self._client = client
        self._file_resource_client = file_resource_client

    def _post_input_request(self, resource_path: str,
                           input_request: dict,
                           project: Optional[str],
                           batch: Optional[str],
                           input_list_id: Optional[int],
                           dryrun: bool = False) -> Optional[IAM.InputJobCreated]:
        """
        Send input to Input API. if not dryrun is true, only validation is performed
        Otherwise, returns `InputJobCreated`
        """
        if input_list_id and project:
            error_message = "Supplying `input_list_id` and `project` is not allowed."
            raise Exception(error_message)

        if input_list_id is not None:
            input_request['inputListId'] = input_list_id

        log.debug("POST:ing to %s input %s", resource_path, input_request)

        request_url = self._resolve_request_url(resource_path, project, batch)
        json_resp = self._client.post(request_url, json=input_request, dryrun=dryrun)
        if not dryrun:
            response = IAM.InputJobCreated.from_json(json_resp)

            if (len(response.files) > 0):
                self._file_resource_client.upload_files(response.files)
                self._client.post(
                    f"v1/inputs/input-jobs/{response.input_uuid}/commit",
                    json=False,
                    discard_response=True
                )

            return response

    @staticmethod
    def _resolve_request_url(resource_path: str,
                             project: Optional[str] = None,
                             batch: Optional[str] = None) -> str:
        """
        Resolves which request url to use for input based on if project and batch is specified
        """
        url = f"v1/inputs/"

        if project is not None:
            url += f"project/{project}/"
            if batch is not None:
                url += f"batch/{batch}/"

        url += resource_path

        return url

    def _set_sensor_settings(self, camera: IAM.CameraInput):
        def _create_sensor_settings():
            first_camera_frame = camera.get_first_camera_frame()
            return self._get_camera_dimensions(first_camera_frame)

        if camera.sensor_specification is None:
            camera.sensor_specification = IAM.SensorSpecification(
                sensor_settings=_create_sensor_settings())
        elif camera.sensor_specification.sensor_settings is None:
            camera.sensor_specification.sensor_settings = _create_sensor_settings()

    @staticmethod
    def _get_camera_dimensions(camera_frame: IAM.CameraFrame) -> Dict[str, IAM.CameraSettings]:
        def _get_camera_settings(width_height_dict: dict) -> IAM.CameraSettings:
            return IAM.CameraSettings(width_height_dict['width'], width_height_dict['height'])

        image_settings = {}
        video_settings = {}
        if len(camera_frame.images) != 0:
            image_settings = {
                image.sensor_name:
                    _get_camera_settings(get_image_dimensions(image.filename)) for image in camera_frame.images
             }
        if len(camera_frame.video_frames) != 0:
            # TODO: Support this for VIDEO
            pass

        return {**image_settings, **video_settings}

    def get_upload_urls(self, files_to_upload: IAM.FilesToUpload) -> IAM.UploadUrls:
        """Get upload urls to cloud storage"""
        json_resp = self._client.get("v1/inputs/upload-urls", json=files_to_upload.to_dict())
        return IAM.UploadUrls.from_json(json_resp)
