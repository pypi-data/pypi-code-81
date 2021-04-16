from typing import Optional, List

from arthurai.common.constants import InputType, OutputType, TextDelimiter
from arthurai.common.exceptions import MissingParameterError, UserValueError, arthur_excepted
from arthurai.core.models import ArthurModel
from arthurai.client.base import BaseApiClient
from arthurai.client.validation import validate_response_status

from http import HTTPStatus


class ArthurAI(object):
    """A client that interacts with Arthur's servers."""

    def __init__(self, config=None, verify_ssl=True, *args, **kwargs):
        if config:
            self.client = BaseApiClient(base_path='/api/v3', verify_ssl=verify_ssl, **config)
        else:
            self.client = BaseApiClient(base_path='/api/v3', verify_ssl=verify_ssl, *args, **kwargs)

    def model(self,
              partner_model_id: str,
              input_type: InputType,
              output_type: Optional[OutputType] = None,
              model_type: Optional[OutputType] = None,
              display_name: Optional[str] = None,
              description: Optional[str] = None,
              tags: Optional[List[str]] = None,
              classifier_threshold: Optional[float] = None,
              is_batch: bool = False,
              text_delimiter: Optional[TextDelimiter] = None,
              expected_throughput_gb_per_day: Optional[int] = None) -> ArthurModel:
        """Create a new multistage model.

        :param: partner_model_id: The string external id of the model
        :param: input_type: the :py:class:`.InputType`
        :param: output_type: the :py:class:`.OutputType`
        :param: model_type: .. deprecated:: version 2.0.0 Use `output_type` instead.
        :param: display_name: Optional name to display on dashboard, will default to the external id
        :param: description: Optional description for the model
        :param: tags: A list of string tags to associate with the model
        :param: classifier_threshold: For binary classification models this is the threshold to determine a positive class, defaults to 0.5
        :param: is_batch boolean value which signifies whether the model sends inferences by batch or streaming
        :param: text_delimiter TextDelimiter used in NLP models to split documents into tokens for explanations
        :param expected_throughput_gb_per_day: Expected amount of throughput. Used to provision resources

        :return: An :py:class:`~arthurai.client.apiv3.model.ArthurModel`
        """
        if output_type is None and model_type is None:
            raise MissingParameterError("Either 'output_type' or 'model_type' parameter must be specified")
        output_type = output_type if output_type is not None else model_type

        return ArthurModel(
            client=self.client,
            partner_model_id=partner_model_id,
            input_type=input_type,
            output_type=output_type,
            display_name=display_name,
            description=description,
            tags=tags,
            classifier_threshold=classifier_threshold,
            is_batch=is_batch,
            text_delimiter=text_delimiter,
            expected_throughput_gb_per_day=expected_throughput_gb_per_day
        )

    @arthur_excepted("failed to retrieve model")
    def get_model(self, identifier: str, id_type: str = 'id') -> ArthurModel:
        """Retrieve an existing model by id

        :param: identifier: Id to get the model by
        :param: id_type: Type of id the identifier is, possible options are ['id', 'partner_model_id']

        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        if id_type in ['partner_model_id', 'id']:
            url = self.client.base_path+f'/models/{identifier}?id_type={id_type}&expand=attributes'
        else:
            raise UserValueError(f"Invalid id_type: {id_type}, must be one of the following ['id', 'partner_model_id]")

        resp = self.client.get(url, return_raw_response=True)
        validate_response_status(resp, expected_status_code=HTTPStatus.OK)

        # accuracy data is only used by the UI not needed in the SDK
        model_data = resp.json()
        if "accuracy_enabled" in model_data:
            del model_data["accuracy_enabled"]

        model = ArthurModel.from_dict(model_data)
        model._client = self.client
        return model
