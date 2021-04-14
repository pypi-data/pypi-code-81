import logging
from typing import Optional

import annotell.input_api.model.input as InputModel
from annotell.input_api.resources.abstract import CreateableInputAPIResource

log = logging.getLogger(__name__)


class LidarsAndCamerasSequence(CreateableInputAPIResource):

    path = 'lidars-and-cameras-sequence'

    def create(self,
               lidars_and_cameras_sequence: InputModel.LidarsAndCamerasSequence,
               project: Optional[str] = None,
               batch: Optional[str] = None,
               input_list_id: Optional[int] = None,
               dryrun: bool = False) -> Optional[InputModel.CreateInputResponse]:
        """
        Upload files and create an input of type ``LidarsAndCamerasSequence``.

        :param lidars_and_cameras_sequence: class containing 2D and 3D resources that constitute the input
        :param project: project to add input to
        :param batch: batch, defaults to latest open batch
        :param input_list_id: input list to add input to (alternative to project-batch)
        :param dryrun: If True the files/metadata will be validated but no input job will be created.
        :returns InputJobCreated: Class containing id of the created input job, or None if dryrun.

        The files are uploaded to annotell GCS and an input_job is submitted to the inputEngine.
        In order to increase annotation tool performance the supplied pointcloud-file is converted
        into potree after upload (server side). Supported fileformats for pointcloud files are
        currently .csv & .pcd (more information about formatting can be found in the readme.md).
        The job is successful once it converts the pointcloud file into potree, at which time an
        input of type 'lidars_and_cameras_sequence' is created for the designated `project` `batch` or `input_list_id`.
        If the input_job fails (cannot perform conversion) the input is not added. To see if
        conversion was successful please see the method `get_input_jobs_status`.
        """

        self._set_sensor_settings(lidars_and_cameras_sequence)

        payload = lidars_and_cameras_sequence.to_dict()

        response = self._post_input_request(self.path, payload,
                                            project=project,
                                            batch=batch,
                                            input_list_id=input_list_id,
                                            dryrun=dryrun)

        if dryrun:
            return None

        log.info(f"Created inputs for files with uuid={response.input_uuid}")
        return InputModel.CreateInputResponse.from_input_job_response(response)
