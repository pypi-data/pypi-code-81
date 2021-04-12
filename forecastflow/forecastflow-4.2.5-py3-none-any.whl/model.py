import logging
import time
from collections import OrderedDict
from typing import TYPE_CHECKING, Dict

from . import prediction
from .api.v3 import create_prediction
from .enums import FileType, Status
from .exceptions import InvalidID, OperationFailed
from .firebase_api import cloud_firestore
from .firebase_api.exceptions import NotFound

if TYPE_CHECKING:
    from . import DataSource, Prediction, Project, User

logger = logging.getLogger(__name__)


class Model:
    """
    ForecastFlow model object
    """

    def __init__(self, project: 'Project', model_id: str):
        """
        Instantiate object with given model ID.

        Args:
            project:
                Project which model belong to.

            model_id:
                ID of model you want to open.
        """
        self.project = project
        self.model_id = model_id
        self._predictions: Dict[str, 'Prediction'] = {}

        try:
            document = self._document
        except NotFound:
            raise InvalidID('Given Mode ID is not found')
        self.name = document['name']
        self.status = document['status']

    def create_prediction(
        self,
        data_source: 'DataSource',
        name: str,
        description: str = '',
        filetype: 'FileType' = FileType.CSV,
    ) -> 'Prediction':
        """
        Create prediction with data_source.

        Args:
            data_source:
                Data to predict with.

            name:
                Name of predict.

            description:
                Description of predict.

        Returns:
            ForecastFlow prediction object which predicts with given data.
        """
        self.wait_until_done()
        prediction_id = create_prediction(
            id_token=self.project.user.id_token,
            name=name,
            description=description,
            pid=self.project.project_id,
            did=data_source.data_source_id,
            mid=self.model_id,
            filetype=filetype,
        )
        self._predictions[prediction_id] = prediction.Prediction(self, prediction_id)
        return self._predictions[prediction_id]

    @property
    def _document(self) -> dict:
        """
        Returns:
            A document of this model on database
        """
        doc = cloud_firestore.get(
            f'users/{self.user.user_id}/projects/{self.project.project_id}'
            f'/models/{self.model_id}',
            self.user.id_token,
        )
        return doc['fields']

    def get_prediction(self, prediction_id: str) -> 'Prediction':
        """
        Get prediction object with given ID.

        Args:
            prediction_id:
                ID of predict you want.
        Returns:
            ForecastFlow predict object with given ID.
        """
        if prediction_id not in self._predictions:
            self._predictions[prediction_id] = prediction.Prediction(
                self, prediction_id
            )
        return self._predictions[prediction_id]

    @property
    def mid(self) -> str:
        return self.model_id

    @property
    def prediction_schema(self) -> OrderedDict:
        """
        Returns:
            OrderedDict which maps column name to type string like 'float'.

        Notes:
            You want to use forecastflow.util.parse_type if you need native Python type.
        """
        schema_json = self._document['predictionSchema']  # [{key: type}, ...]
        schema = OrderedDict()
        for column in schema_json:
            key = list(column.keys())[0]
            type_ = column[key]
            schema[key] = type_
        return schema

    @property
    def user(self) -> 'User':
        return self.project.user

    def update(self):
        """
        Update name, status
        """
        try:
            document = self._document
        except NotFound:
            raise InvalidID('Given Model ID is not found')

        self.name = document['name']

        if (
            document['status'] == Status.COMPLETED.value
        ):  # TODO: use status instead of profile in future
            self.status = Status.COMPLETED
        else:
            self.status = Status(document['status'])

        logger.info(f"Training '{self.name}': {self.status.value}")

    def wait_until_done(self):
        """
        Wait until ForecastFlow finish training.
        """
        while self.status != Status.COMPLETED and self.status != Status.ERROR:
            self.update()
            time.sleep(5)

        if self.status == Status.ERROR:
            document = self._document
            error_info = document.get('errorInfo')
            if error_info is None:
                raise OperationFailed("Training quit with Error")
            else:
                raise OperationFailed(
                    f"{error_info['message']}\n"
                    f"error_log_id: {error_info['errorLogId']}"
                )
