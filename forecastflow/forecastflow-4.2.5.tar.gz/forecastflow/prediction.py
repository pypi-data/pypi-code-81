import logging
import time
from io import BytesIO
from typing import TYPE_CHECKING

import pandas as pd

from .api.v3 import get_predict
from .enums import FileType, Status
from .exceptions import ForecastFlowError, InvalidID, OperationFailed
from .firebase_api import cloud_firestore, storage
from .firebase_api.exceptions import NotFound

if TYPE_CHECKING:
    from . import Model, Project, User

logger = logging.getLogger(__name__)


class Prediction:
    """
    ForecastFlow prediction object
    """

    def __init__(self, model: 'Model', prediction_id: str):
        """
        Instantiate object with given prediction ID.

        Args:
            model:
                Model which makes this predict.

            prediction_id:
                ID of prediction you want to open.
        """
        self.model = model
        self.prediction_id = prediction_id
        self.name = None
        self.status = None
        self.update()

    @property
    def _document(self):
        try:
            document = cloud_firestore.get(
                f'users/{self.user.user_id}/projects/{self.project.project_id}'
                f'/predicts/{self.prediction_id}',
                self.user.id_token,
            )
        except NotFound:
            raise InvalidID('Given Prediction ID is not found')
        return document['fields']

    def get_result(self) -> pd.DataFrame:
        """
        Download the result from ForecastFlow.

        Returns:
            result with primary key and predicted values.
        """
        self.wait_until_done()
        uris = get_predict(
            id_token=self.user.id_token,
            uid=self.user.uid,
            pid=self.project.pid,
            rid=self.rid,
        )
        filetype = self.filetype
        df_list = []
        for uri in uris:
            with BytesIO() as f:
                storage.download(
                    uri,
                    f,
                    self.user.id_token,
                )
                f.seek(0)
                if filetype == FileType.CSV:
                    df_list.append(pd.read_csv(f))
                elif filetype == FileType.TSV:
                    df_list.append(pd.read_csv(f, delimiter='\t'))
                elif filetype == FileType.PARQUET:
                    df_list.append(pd.read_parquet(f))
                else:
                    raise ForecastFlowError(f'{filetype} not supported.')
        return pd.concat(df_list, ignore_index=True)

    @property
    def project(self) -> 'Project':
        return self.model.project

    @property
    def rid(self) -> str:
        return self.prediction_id

    @property
    def filetype(self) -> 'FileType':
        return FileType(self._document.get('type', FileType.CSV))

    def update(self):
        """
        update name, status
        """
        document = self._document

        if document['mid'] != self.model.model_id:
            raise InvalidID('Given Prediction ID is not for this model')

        self.name = document['name']
        self.status = Status(document['status'])

        logger.info(f"Prediction '{self.name}': {self.status.value}")

    @property
    def user(self) -> 'User':
        return self.model.project.user

    def wait_until_done(self):
        """
        Wait until ForecastFlow finish prediction.
        """
        while self.status != Status.COMPLETED and self.status != Status.ERROR:
            self.update()
            time.sleep(5)

        if self.status == Status.ERROR:
            document = self._document
            error_info = document.get('errorInfo')
            if error_info is None:
                raise OperationFailed("Predictor quit with Error")
            else:
                raise OperationFailed(
                    f"{error_info['message']}\n"
                    f"error_log_id: {error_info['errorLogId']}"
                )
