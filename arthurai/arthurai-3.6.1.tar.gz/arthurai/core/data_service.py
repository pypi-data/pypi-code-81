import logging
import os
import tempfile
from typing import Dict, Optional, Any, TYPE_CHECKING, List

from pandas import DataFrame

from arthurai.common.constants import Stage
from arthurai.common.exceptions import UserValueError
from arthurai.core import util
#  imports ArthurModel for type checking, required due to circular import
if TYPE_CHECKING:
    from arthurai.core.models import ArthurModel

logger = logging.getLogger(__name__)


class DatasetService:
    COUNTS = "counts"
    SUCCESS = "success"
    FAILURE = "failure"
    TOTAL = "total"
    FAILURES = "failures"

    @staticmethod
    def convert_dataframe(model_id: str, stage: Optional[Stage], df: DataFrame) -> str:
        """Convert a dataframe to parquet named {model.id}-{stage}.parquet in the system tempdir

        :param model_id: a model id
        :param stage: the :py:class:`.Stage`
        :param df: the dataframe to convert

        Returns:
            The filename of the parquet file that was created
        """
        name = "{0}-{1}.parquet".format(model_id, stage) if stage else "{0}.parquet".format(model_id)
        filename = os.path.join(tempfile.mkdtemp(), name)
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass

        df.to_parquet(filename, index=False, allow_truncated_timestamps=True)
        return filename

    @staticmethod
    def send_parquet_files_from_dir_iteratively(model: 'ArthurModel', directory_path: str,
                                                url: str, upload_file_param_name: str,
                                                additional_form_params: Optional[Dict[str, Any]] = None,
                                                retries: int = 0):
        """Sends parquet files iteratively from a specified directory to a specified url for a given model

        :param retries: Number of times to retry the request if it results in a 400 or higher response code
        :param model:    the :py:class:`!arthurai.client.apiv2.model.ArthurModel`
        :param directory_path:    local path containing parquet files to send
        :param url:    POST url endpoint to send files to
        :param upload_file_param_name:     name to use in body with attached files
        :param additional_form_params: dictionary of additional form file params to send along with parquet file

        :raises MissingParameterError: the request failed

        :returns A list of files which failed to upload
        """
        files = util.retrieve_parquet_files(directory_path)
        if not files:
            raise UserValueError("The directory supplied does not contain any parquet files to upload")

        failed_files = []
        succeeded_files = []
        expected_keys = {DatasetService.SUCCESS, DatasetService.FAILURE, DatasetService.TOTAL}

        counts = {
            DatasetService.SUCCESS: 0,
            DatasetService.FAILURE: 0,
            DatasetService.TOTAL: 0
        }
        failures: List[Any] = []

        for file in files:
            if file.suffix == '.parquet':
                with open(file, 'rb') as parquet_file:
                    headers = {'Content-Type': 'multipart/form-data'}
                    form_parts = {} if additional_form_params is None else additional_form_params
                    form_parts.update({upload_file_param_name: parquet_file})
                    resp = model._client.post(url, data=None, files=form_parts, headers=headers,
                                              return_raw_response=True, retries=retries)
                    if resp.status_code == 201:
                        logger.info(f"Uploaded completed: {file}")
                        succeeded_files.append(file)
                    elif resp.status_code == 207:
                        logger.info(f"Upload completed: {file}")
                        result: Dict[str, Dict[str, int]] = resp.json()
                        # ensure the response is in the correct format
                        if DatasetService.COUNTS in result and DatasetService.FAILURES in result \
                                and set(result[DatasetService.COUNTS].keys()) == expected_keys:
                            counts[DatasetService.SUCCESS] += \
                                result[DatasetService.COUNTS][DatasetService.SUCCESS]
                            counts[DatasetService.FAILURE] += \
                                result[DatasetService.COUNTS][DatasetService.FAILURE]
                            counts[DatasetService.TOTAL] += \
                                result[DatasetService.COUNTS][DatasetService.TOTAL]
                            failures.append(result[DatasetService.FAILURES])
                        else:
                            failures.append(result)
                    else:
                        logger.error(f"Failed to upload file: {resp.text}")
                        failed_files.append(file)
                        failures.append(resp.json())
                        counts[DatasetService.FAILURE] += 1
                        counts[DatasetService.TOTAL] += 1

        file_upload_info = {
            DatasetService.COUNTS: counts,
            DatasetService.FAILURES: failures
        }

        # Only log failed or succeeded files if they exist
        if len(failed_files) > 0:
            logger.error(f'Failed to upload {len(failed_files)} files')
        if len(succeeded_files) > 0:
            logger.info(f'Successfully uploaded {len(succeeded_files)} files')
        return failed_files, file_upload_info
