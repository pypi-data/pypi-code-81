import logging
from typing import Optional

import annotell.input_api.model.input as InputModel
import annotell.input_api.model.input.cameras_sequence as CamerasSeqModel
from annotell.input_api.resources.abstract import CreateableInputAPIResource

log = logging.getLogger(__name__)


class CamerasSequence(CreateableInputAPIResource):
    path = "cameras-sequence"

    def create(self,
               cameras_sequence: CamerasSeqModel.CamerasSequence,
               project: Optional[str] = None,
               batch: Optional[str] = None,
               input_list_id: Optional[int] = None,
               dryrun: bool = False) -> Optional[InputModel.CreateInputResponse]:
        """
        Upload files and create an input of type ``cameras-sequence``.

        :param cameras_sequence: class containing 2D resources that constitute the input
        :param project: project to add input to
        :param batch: batch, defaults to latest open batch
        :param input_list_id: input list to add input to (alternative to project-batch)
        :param dryrun: If True the files/metadata will be validated but no input job will be created.
        :returns InputJobCreated: Class containing id of the created input job, or None if dryrun.

        The files are uploaded to annotell GCS and an input will be created shortly after submission.
        """

        self._set_sensor_settings(cameras_sequence)

        payload = cameras_sequence.to_dict()

        response = self._post_input_request(self.path, payload,
                                            project=project,
                                            batch=batch,
                                            input_list_id=input_list_id,
                                            dryrun=dryrun)

        if dryrun:
            return None

        log.info(
            f"Created inputs for files with uuid={response.input_uuid}")
        return InputModel.CreateInputResponse.from_input_job_response(response)
