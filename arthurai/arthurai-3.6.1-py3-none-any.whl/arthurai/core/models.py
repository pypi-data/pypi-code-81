import logging
import re
import sys
from datetime import datetime
from http import HTTPStatus
from typing import Optional, Union, List, Dict, Any
import json

import numpy as np
import pyarrow.parquet as pq
from dataclasses import dataclass, InitVar
from pandas import DataFrame, Series

from arthurai.version import __version__
from arthurai import util as arthur_util
from arthurai.core import util as core_util
from arthurai.client.base import BaseApiClient
from arthurai.client import validation
from arthurai.common.constants import Stage, InputType, OutputType, ValueType, TextDelimiter, Enrichment
from arthurai.common.exceptions import MethodNotApplicableError, MissingParameterError, UserValueError, \
    UserTypeError, ArthurUserError, ExpectedParameterNotFoundError, arthur_excepted, InternalTypeError
from arthurai.core.base import ArthurBaseJsonDataclass, NumberType
from arthurai.core.attributes import ArthurAttribute, AttributeCategory, AttributeBin
from arthurai.core.data_service import DatasetService
from arthurai.explainability.explanation_packager import ExplanationPackager
from arthurai.core.alerts import AlertRule, AlertRuleSeverity, AlertRuleBound, AlertMetric
from arthurai.core.viz.visualizer import DataVisualizer

logger = logging.getLogger(__name__)

INFERENCE_DATA_RETRIES = 3


@dataclass
class ExplainabilityParameters(ArthurBaseJsonDataclass):
    enabled: bool
    explanation_algo: Optional[str] = None
    model_server_cpu: Optional[str] = None
    model_server_memory: Optional[str] = None
    explanation_nsamples: Optional[int] = None


@dataclass
class ArthurModel(ArthurBaseJsonDataclass):
    """
    Arthur Model class represents the metadata which represents a registered model in the application

    :param client: :class:`arthurai.client.Client` object which manages data storage
    :param partner_model_id: Client provided unique id to associate with the model. This field must be unique across
                             all active models cannot be changed once set.
    :param input_type: :class:`arthurai.common.constants.InputType` representing the model's input data type.
    :param output_type: :class:`arthurai.common.constants.InputType` representing the model's output data format.
    :param explainability:  :class:`arthurai.core.models.ExplainabilityParameters` object representing parameters that
                            will be used to create inference explanations.
    :param id: The auto-generated unique UUID for the model. Will be overwritten if set by the user.
    :param display_name: An optional display name for the model.
    :param description: Optional description of the model.
    :param is_batch: Boolean value to determine whether the model sends inferences in batch or streaming format.
                     Defaults to False.
    :param archived: Indicates whether or not a model has been archived, defaults to false.
    :param created_at: UTC timestamp in ISO8601 format of when the model was created. Will be overwritten if set by the
                       user.
    :param updated_at: UTC timestamp in ISO8601 format of when the model was last updated. Will be overwritten if set by
                       the user.
    :param attributes: List of :class:`arthurai.core.attributes.ArthurAttribute` objects registered to the model
    :param tags: List of string keywords to associate with the model.
    :param classifier_thresholds: Threshold value for classification models, default is 0.5.
    :param text_delimiter: Only valid for models with input_type equal to
                           :py:attr:`arthurai.common.constants.InputType.NLP`. Represents the text delimiter
                           to divide input strings.
    :param expected_throughput_gb_per_day: Expected amount of throughput.
    """

    partner_model_id: str
    input_type: InputType
    output_type: OutputType
    # This is just used during init and will not be associated with
    # an instance of this class, instead reference ArthurModel._client
    client: InitVar[Optional[BaseApiClient]] = None
    explainability: Optional[ExplainabilityParameters] = None
    id: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    is_batch: bool = False
    archived: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    attributes: Optional[List[ArthurAttribute]] = None
    tags: Optional[List[str]] = None
    classifier_threshold: Optional[float] = None
    text_delimiter: Optional[TextDelimiter] = None
    expected_throughput_gb_per_day: Optional[int] = None

    def __post_init__(self, client: BaseApiClient):
        # variables created here will only be accessible directly on the object itself, they will not be in the result
        # of object.to_dict() even if marked as public (does not have preceding underscore)
        self._client = client
        self._explainer: Optional[ExplanationPackager] = None
        self.viz = DataVisualizer(self)

    def __str__(self):
        return str(self.to_dict())

    @arthur_excepted("failed to save model")
    def save(self) -> str:
        """Check and save this model.  Sets and returns the ID on successful upload.

        :return: The model id

        :raise: Exception: the model has already been saved
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        # if the model has not been set yet
        if self.id is not None:
            raise MethodNotApplicableError("Cannot save a registered model; use update instead.")

        self._check_model_valid()

        if self.display_name is None:
            self.display_name = self.partner_model_id

        data = self.to_dict()
        resp = self._client.post(self._client.base_path + "/models", data=data, return_raw_response=True)
        validation.validate_response_status(resp, expected_status_code=HTTPStatus.CREATED)
        if 'id' not in resp.json():
            raise ExpectedParameterNotFoundError(f"An error occurred: {resp}, {resp.status_code}, {resp.content}")

        # update fields with response from API
        self.id = resp.json()['id']

        # TODO: if explainability is enabled send resources

        return self.id  # type: ignore

    def _check_model_valid(self) -> bool:
        """Check the validity of the model before saving, and prints out any errors it finds.

        (As time passes we can add more to this function to enforce more requirements.)

        :return: True if the model is valid, False otherwise.
        """

        # has attributes
        if self.attributes is None:
            # future enhancement, attributes should be initialized to empty not None
            raise InternalTypeError("attributes is None")
        if len(self.attributes) == 0:
            raise MissingParameterError("must add attributes to model before saving; see below for requirements.")

        # contains ground truth, input, and predicted attributes
        contains_gt = False
        contains_pred = False
        contains_ipt = False
        for attr in self.attributes:
            if attr.stage == Stage.GroundTruth:
                contains_gt = True
            if attr.stage == Stage.PredictedValue:
                contains_pred = True
            if attr.stage == Stage.ModelPipelineInput or attr.stage == Stage.PredictFunctionInput:
                contains_ipt = True
        if not contains_gt:
            raise MissingParameterError("does not contain any attribute with Stage.GroundTruth.")
        if not contains_pred:
            raise MissingParameterError("does not contain any attribute with Stage.PredictedValue.")
        if not contains_ipt:
            raise MissingParameterError("does not have any attribute with Stage.ModelPipelineInput or Stage.PredictFunctionInput.")

        # for binary models, need one predicted attribute to be positive
        predicted_value_attributes = self.get_attributes(stage=Stage.PredictedValue)
        if len(predicted_value_attributes) == 2 and self.output_type == OutputType.Multiclass:  # is binary model
            has_pos_pred = False
            for pred in predicted_value_attributes:
                if pred.is_positive_predicted_attribute:
                    has_pos_pred = True
            if not has_pos_pred:
                raise MethodNotApplicableError("binary models must have a positive predicted attribute; use "
                                               "add_binary_classifier_output_attributes instead.")

        return True

    @arthur_excepted("failed to update model")
    def update(self):
        """Update the the current model object 

        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        if self.id is None:
            raise MethodNotApplicableError("Model has not been created yet, use save() to instantiate this model object")

        data = self.to_dict()
        resp = self._client.put(self._client.base_path + f"/models/{self.id}", data=data, return_raw_response=True)
        validation.validate_response_status(resp, expected_status_code=HTTPStatus.OK)

    @staticmethod
    def _get_attribute_data(value_type: ValueType, attribute_data_series: Series) -> Dict:
        """Generates metadata about a specific attribute based on a supplied dataframe

        :param value_type:                          DataType of the values in the series
        :param attribute_data_series:              Pandas Series of data for the specific attribute
        :return: Dictionary of attribute metadata and values inferred from the pandas series
        """
        if attribute_data_series.isnull().any():
            raise UserValueError("Column contains null value. Null values are not supported in reference or "
                                 f"inference data, please replace before proceeding.")

        cnt_distinct = len(attribute_data_series.unique())
        pct_distinct = cnt_distinct / float(len(attribute_data_series))
        attribute_data: Dict[str, Optional[Any]] = {'is_unique': True if pct_distinct == 1.0 else False}

        categorical = False
        if value_type == ValueType.Timestamp:
            categorical = False

        elif (value_type == ValueType.Float and
              cnt_distinct == 2 and
              attribute_data_series.max() == 1 and
              attribute_data_series.min() == 0):
            # exactly [0.0, 1.0]
            categorical = True

        elif value_type == ValueType.Float:
            categorical = False
        elif value_type == ValueType.Integer and cnt_distinct <= 20:
            categorical = True
        elif value_type == ValueType.Integer:
            categorical = False
        elif value_type == ValueType.Unstructured_Text:
            categorical = True
        else:
            categorical = True

        # even if unstructured text attributes aren't unique, we don't want categories
        if categorical and not attribute_data["is_unique"] and not value_type == ValueType.Unstructured_Text:
            attribute_data["categories"] = [AttributeCategory(value=str(cat)) for cat in
                                            list(set(attribute_data_series))]
        elif not categorical:
            attribute_data["min_range"] = core_util.NumpyEncoder.convert_value(attribute_data_series.min())
            attribute_data["max_range"] = core_util.NumpyEncoder.convert_value(attribute_data_series.max())

        attribute_data["categorical"] = categorical

        return attribute_data

    @staticmethod
    def _to_arthur_dtype( dtype: str) -> ValueType:
        """Select an :py:class:`.DataType` based on a pandas dtype

        :param dtype: the pandas dtype
        :return: The :py:class:`.DataType` corresponding to the pandas dtype
        """

        if dtype in ["string", "object"]:
            return ValueType.String
        elif dtype in ["bool", "boolean"]:
            return ValueType.Boolean
        elif re.search("u?int*", dtype, flags=re.I) or re.search("u?Int*", dtype, flags=re.I):
            return ValueType.Integer
        elif re.search("float*", dtype, flags=re.I):
            return ValueType.Float
        elif re.search("(datetime|timestamp).*", dtype, flags=re.I):
            return ValueType.Timestamp

    @arthur_excepted("failed to parse dataframe")
    def from_dataframe(self, data: Union[DataFrame, Series], stage: Stage) -> None:
        """ Attempt to autogenerate attributes based on input data. 
        
        Note that this does *not* automatically set reference
        data; this method only reads the passed-in data, and then infers attribute names, types, etc. and sets them up 
        within the ArthurModel. 

        For PredictedValue and GroundTruth stages, use the correct `add_<modeltype>_output_attributes()` method instead.

        :param data: the data to infer attribute metadata from
        :param stage: :py:class:`.Stage` of the data
        :return: None
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """

        if stage == Stage.PredictedValue or stage == Stage.GroundTruth:
            raise MethodNotApplicableError("Use either add_regression_output_attributes(), "
                                           "add_multiclass_classifier_output_attributes(), "
                                           "or add_binary_classifier_output_attributes() to add output attributes.")

        if isinstance(data, DataFrame):
            df = data
        elif isinstance(data, Series):
            df = data.to_frame()
        else:
            raise UserTypeError("Unsupported data type: a pandas.DataFrame or pandas.Series is required")

        for idx, column in enumerate(df.columns):

            series = core_util.standardize_pd_obj(df[column], dropna=True, replacedatetime=False)
            value_type = self._to_arthur_dtype(series.dtype.name)

            try:
                attribute_data = self._get_attribute_data(value_type, series)
            except ArthurUserError as e:
                raise ArthurUserError(f"Error in column: {column}: {str(e)}")

            if value_type == ValueType.String and self.input_type == InputType.NLP:
                value_type = ValueType.Unstructured_Text
                # even if unstructured text attributes are not unique we don't want to store categories
                attribute_data['categories'] = None

            attribute_data["position"] = idx
            arthur_attribute = ArthurAttribute(
                name=column,
                stage=stage,
                value_type=value_type,
                **attribute_data
            )
            self._add_attribute_to_model(arthur_attribute)

    def _add_attribute_to_model(self, attribute: ArthurAttribute) -> ArthurAttribute:
        """Adds an already-made ArthurAttribute to the model. 

        :param attribute: ArthurAttribute Object to add to the model
        :return: ArthurAttribute Object
        """
        if self.attributes is None:
            self.attributes = [attribute]
        else:
            self.attributes.append(attribute)

        return attribute

    @arthur_excepted("failed to add attribute")
    def add_attribute(self,
                      name: Optional[str] = None,
                      value_type: Optional[ValueType] = None,
                      stage: Optional[Stage] = None,
                      label: Optional[str] = None,
                      position: Optional[int] = None,
                      categorical: bool = False,
                      min_range: Optional[Union[float, int]] = None,
                      max_range: Optional[Union[float, int]] = None,
                      monitor_for_bias: bool = False,
                      categories: Optional[List[Union[str, AttributeCategory]]] = None,
                      bins: Optional[List[Union[NumberType, AttributeBin]]] = None,
                      is_unique: bool = False,
                      is_positive_predicted_attribute: bool = False,
                      attribute_link: Optional[str] = None,
                      arthur_attribute: Optional[ArthurAttribute] = None,
                      gt_pred_attrs_map: Optional[Dict] = None) -> List[ArthurAttribute]:
        """Adds a new attribute to the model and returns the attribute. 
        
        Also validates that Stage is not PredictedValue or GroundTruth. Additionally, attribute names must contain
        only letters, numbers, and underscores, and cannot begin with a number.

        :param attribute_link: Only applicable for `GroundTruth` or `PredictedValue` staged attributes.
        If stage is equal to `GroundTruth`, this represents the associated `PredictedValue` attribute and vice versa
        :param is_positive_predicted_attribute: Only applicable for `PredictedValue` attributes on a Binary
        Classification model. Should be set to `True` on the positive predicted value attribute.
        :param is_unique: Boolean value used to signal if the values of this attribute are unique.
        :param bins: List of bin cut-offs used to discretize continuous attributes. Use `None` as an open ended value.
                     `[None, 18, 65, None]` represents the three following bins:
                     `value < 18, 18 < value < 65, value > 65`
        :param monitor_for_bias: boolean value set to `True` if the attribute should be monitored for bias
        :param max_range: Max value for a continuous attribute
        :param min_range: Min value for a continuous attribute
        :param categorical: Boolean value set to `True` if the attribute has categorical values.
        :param position: The array position of attribute within the stage. Required in the PREDICT_FUNCTION_INPUT stage.
        :param label: Label for attribute. If attribute has an encoded name, a more readable label can be set.
        :param stage: :class:`arthurai.common.constants.Stage` of this attribute in the model pipeline
        :param value_type: :class:`arthurai.common.constants.ValueType` associated with this attributes values
        :param name: Name of the attribute. Attribute names can only contain alpha-numeric characters and underscores
        and cannot start with a number.
        :param categories: [Only for Categorical Attributes] If the attribute is categorical, this will contain the
        attribute's categories. It is required only if the categorical flag is set to true.
        :param arthur_attribute: Optional ArthurAttribute to add to the model
        :param gt_pred_attrs_map: .. deprecated:: version 2.0.0 Use `ArthurModel.add_[model_type]_output_attributes()` instead
        
        :return: ArthurAttribute Object
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        if arthur_attribute is None:
            if stage is None or value_type is None or name is None:
                raise MissingParameterError("At minimum stage, value_type, and name must be provided for an attribute")
            elif stage == Stage.PredictedValue or stage == Stage.GroundTruth or gt_pred_attrs_map is not None:
                raise MethodNotApplicableError("Use either add_regression_output_attributes(), "
                                               "add_multiclass_classifier_output_attributes(), "
                                               "or add_binary_classifier_output_attributes() to add output attributes.")

            if not self._validate_attribute_name(name):
                raise UserValueError("Invalid attribute name: must contain only numbers, letters, and underscores, "
                                     "and cannot start with a number.")

            # Add categories or bins if supplied
            attribute_categories = [AttributeCategory(value=c) if not isinstance(c, AttributeCategory) else c
                                    for c in categories] if categories else None

            attribute_bins: Optional[List[Any]] = None
            if bins and not isinstance(bins[0], AttributeBin):
                attribute_bins = [AttributeBin(bins[i], bins[i + 1]) for i in range(len(bins) - 1)]
            elif bins and isinstance(bins[0], AttributeBin):
                attribute_bins = bins

            attribute_to_add = ArthurAttribute(
                name=name,
                value_type=value_type,
                stage=stage,
                label=label,
                position=position,
                categorical=categorical,
                min_range=min_range,
                max_range=max_range,
                monitor_for_bias=monitor_for_bias,
                categories=attribute_categories,
                bins=attribute_bins,
                is_unique=is_unique,
                is_positive_predicted_attribute=is_positive_predicted_attribute,
                attribute_link=attribute_link
            )
            return [self._add_attribute_to_model(attribute_to_add)]

        else:
            self._validate_attribute_name(arthur_attribute.name)
            return [self._add_attribute_to_model(arthur_attribute)]

    @staticmethod
    def _validate_attribute_name(attribute_name: str) -> bool:
        """Checks that attribute name is valid. 

        :param attribute_name: name of the attribute to add to the model
        :return: boolean indicating whether the name is valid. 
        """

        if bool(re.compile('\d').search(attribute_name[0])):  # \d is all the digits 0-9
            print("Attribute name cannot start with a number.")
            return False

        if bool(re.compile('\W').search(attribute_name)):  # \W is the complement of all alphanumeric characters and _.
            print("Attribute name can only contain numbers, letters, and underscores.")
            return False

        return True

    @arthur_excepted("failed to add regression output attributes")
    def add_regression_output_attributes(self, pred_to_ground_truth_map: Dict[str, str], value_type: ValueType) \
            -> Dict[str, ArthurAttribute]:
        """ Registers ground truth and predicted attribute parameters for regression models. 
        This function will register two ArthurAttribute objects to the model, a predicted value attribute 
        and ground truth attribute.

        :param pred_to_ground_truth_map: Map of predicted value attributes to their corresponding ground truth attribute names.
                                  The names provided in the dictionary will be used to register the one-hot encoded
                                  version of the attributes.
        :param value_type: Value type of regression model output attribute (usually either ValueType.Integer or ValueType.Float)
        
        :return: Mapping of added attributes string name -> ArthurAttribute Object
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        attributes_added = {}
        for pred_attr, gt_attr in pred_to_ground_truth_map.items():
            arthur_gt_attr = ArthurAttribute(
                name=gt_attr,
                stage=Stage.GroundTruth,
                value_type=value_type,
                categorical=False,
                attribute_link=pred_attr,
                position=0
            )
            arthur_pred_attr = ArthurAttribute(
                name=pred_attr,
                stage=Stage.PredictedValue,
                value_type=value_type,
                categorical=False,
                attribute_link=gt_attr,
                position=0
            )
            self._add_attribute_to_model(arthur_gt_attr)
            self._add_attribute_to_model(arthur_pred_attr)
            attributes_added[arthur_pred_attr.name] = arthur_pred_attr
            attributes_added[arthur_gt_attr.name] = arthur_gt_attr
        return attributes_added

    @arthur_excepted("failed to add output attributes")
    def add_multiclass_classifier_output_attributes(self, pred_to_ground_truth_map: Dict[str, str]) \
            -> Dict[str, ArthurAttribute]:
        """Registers ground truth and predicted attribute parameters. This function will create a predicted value and
        ground truth attribute for each mapping specified in pred_to_ground_truth_map.

        :param pred_to_ground_truth_map: Map of predicted value attributes to their corresponding ground truth attribute names.
                                  The names provided in the dictionary will be used to register the one-hot encoded
                                  version of the attributes. Ensure the ordering of items in this dictionary is an accurate
                                  representation of how model predictions (probability vectors) will be generated.
        :return: Mapping of added attributes string name -> ArthurAttribute Object
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """

        if len(pred_to_ground_truth_map) == 2:
            raise MethodNotApplicableError(
                "To add output attributes to a multiclass model with two output attributes, use `add_binary_classifier_output_attributes`.")

        attributes_added = {}
        for (index, (pred_attr, gt_attr)) in enumerate(pred_to_ground_truth_map.items()):
            arthur_gt_attr = ArthurAttribute(
                name=gt_attr,
                stage=Stage.GroundTruth,
                value_type=ValueType.Integer,
                categorical=True,
                categories=[AttributeCategory(value="0"), AttributeCategory(value="1")],
                attribute_link=pred_attr,
                position=index
            )
            arthur_pred_attr = ArthurAttribute(
                name=pred_attr,
                stage=Stage.PredictedValue,
                value_type=ValueType.Float,
                min_range=0,
                max_range=1,
                attribute_link=gt_attr,
                position=index
            )
            self._add_attribute_to_model(arthur_gt_attr)
            self._add_attribute_to_model(arthur_pred_attr)
            attributes_added[arthur_pred_attr.name] = arthur_pred_attr
            attributes_added[arthur_gt_attr.name] = arthur_gt_attr
        return attributes_added

    @arthur_excepted("failed to add output attributes")
    def add_binary_classifier_output_attributes(self, positive_predicted_attr: str,
                                                pred_to_ground_truth_map: Dict[str, str],
                                                threshold: float = 0.5) -> Dict[str, ArthurAttribute]:
        """Registers ground truth and predicted attribute parameters and their thresholds. 
        
        This function will create a predicted value and ground truth attribute for each mapping specified in 
        pred_to_ground_truth_map. 
        
        For binary models, `GroundTruth` is always an integer, and `PredictedAttribute` is always a float. 
        Additionally, `PredictedAttribute` is expected to be a probability (e.g. the output of a scikit-learn
        model's `predict_proba` method), rather than a classification to 0/1. 

        This assumes that separate columns for predicted values and ground truth values have already been created, 
        and that they have both been broken into two separate (pseudo-onehot) columns: for example, the column 
        `ground_truth_label` becomes `ground_truth_label=0` and `ground_truth_label=1`, and the column `pred_prob`
        becomes `pred_prob=0` and `pred_prob=1`. The pandas function `pd.get_dummies()` can be useful for reformatting
        the ground truth column, but be sure that the datatype is specified correctly as an int.

        :param positive_predicted_attr: string name of the predicted attribute to register as the positive predicted attribute
        :param pred_to_ground_truth_map: Map of predicted value attributes to their corresponding ground truth attribute names.
                                  The names provided in the dictionary will be used to register the one-hot encoded
                                  version of the attributes. For example: `{'pred_0': 'gt_0', 'pred_1': 'gt_1'}`,
                                  Ensure the ordering of items in this dictionary is an accurate
                                  representation of how model predictions (probability vectors) will be generated.
        :param threshold: Threshold to use for the classifier model, defaults to 0.5
        
        :return: Mapping of added attributes string name -> ArthurAttribute Object
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        if len(pred_to_ground_truth_map) != 2:
            raise UserValueError((f"Binary classifiers must have two output attributes, but pred_to_ground_truth_map "
                                  f"has {len(pred_to_ground_truth_map)}. To add more than two output attributes to a "
                                  f"multiclass model, use add_multiclass_classifier_output_attributes()."))
        if positive_predicted_attr not in pred_to_ground_truth_map.keys():
            raise UserValueError((f"The positive_predicted_attr must be included in the mapping "
                                  f"pred_to_ground_truth_map. positive_predicted_attr {positive_predicted_attr} not "
                                  f"found in pred_to_ground_truth_map keys: {pred_to_ground_truth_map.keys()}."))
        attributes_added = {}
        for (index, (pred_attr, gt_attr)) in enumerate(pred_to_ground_truth_map.items()):
            is_pos_pred_attr = True if positive_predicted_attr == pred_attr else False
            arthur_gt_attr = ArthurAttribute(
                name=gt_attr,
                stage=Stage.GroundTruth,
                value_type=ValueType.Integer,
                categorical=True,
                categories=[AttributeCategory(value="0"), AttributeCategory(value="1")],
                attribute_link=pred_attr,
                position=index
            )
            arthur_pred_attr = ArthurAttribute(
                name=pred_attr,
                stage=Stage.PredictedValue,
                value_type=ValueType.Float,
                min_range=0,
                max_range=1,
                attribute_link=gt_attr,
                is_positive_predicted_attribute=is_pos_pred_attr,
                position=index
            )
            self._add_attribute_to_model(arthur_gt_attr)
            self._add_attribute_to_model(arthur_pred_attr)
            attributes_added[arthur_pred_attr.name] = arthur_pred_attr
            attributes_added[arthur_gt_attr.name] = arthur_gt_attr
        self.classifier_threshold = threshold
        return attributes_added

    @arthur_excepted("failed to get attribute")
    def get_attribute(self, name: str, stage: Optional[Stage] = None) -> ArthurAttribute:
        """Retrieves an attribute by name and stage

        :param name: string name of the attribute to retrieve
        :param stage: Optional `Stage` of attribute to retrieve
        
        :return: ArthurAttribute Object
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        if self.attributes is None:
            raise MethodNotApplicableError("model does not have any attributes")
        for attr in self.attributes:
            if stage is not None and attr.name == name and attr.stage == Stage:
                return attr
            elif attr.name == name:
                return attr

        raise UserValueError(f"Attribute with name: {name} in stage: {stage} does not exist")

    @arthur_excepted("failed to get attributes")
    def get_attributes(self, stage: Optional[Stage]) -> Optional[List[ArthurAttribute]]:
        """Returns a list of attributes for the specified stage

        :param stage: :class:`arthurai.common.constants.Stage` to filter by
        :return: List of :class:`arthurai.attributes.ArthurAttribute`
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        if self.attributes is None:
            return None
        return [attr for attr in self.attributes if stage and attr.stage == stage]

    @arthur_excepted("failed to get attribute names")
    def get_attribute_names(self, stage: Optional[Stage]) -> List[str]:
        """ Returns a list of all attribute names. If stage is supplied it will only return the attribute names which
        are in the specified stage.

        :param stage: :class:`arthurai.common.constants.Stage` to filter by
        :return: List of string attribute names
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        if self.attributes is None:
            raise MethodNotApplicableError("model does not have any attributes")
        return [attr.name for attr in self.attributes if stage and attr.stage == stage]

    @arthur_excepted("failed to rename attribute")
    def rename_attribute(self, old_name: str, new_name: str, stage: Stage) -> ArthurAttribute:
        """Renames an attribute by name and stage

        :param old_name: string name of the attribute to rename
        :param new_name: string new name of the attribute
        :param stage: `Stage` of attribute
        
        :return: ArthurAttribute Object
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        attribute = self.get_attribute(old_name, stage)
        attribute.name = new_name

        return attribute

    @arthur_excepted("failed to set attribute labels")
    def set_attribute_labels(self, attribute_name: str, labels: Dict[Union[int, str], str],
                             attribute_stage: Optional[Stage] = None):
        """
        Sets labels for individual categories of a specific attribute
        :param attribute_name: Attribute name to set the categories labels
        :param attribute_stage: Optional stage of the attribute which is being updated
        :param labels: Dictionary where the key is the categorical value and the value is the string categorical label
        :return: None
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        attr_to_update = self.get_attribute(name=attribute_name, stage=attribute_stage)
        categories = []
        for cat_value, cat_label in labels.items():
            categories.append(AttributeCategory(value=cat_value, label=cat_label))
        attr_to_update.categories = categories

    @arthur_excepted("failed to generate summary")
    def review(self, stage: Stage = None, props: Optional[List[str]] = None, print_df=True) -> None:
        """Prints a summary of the properties of all attributes in the model.

        :param stage: restrict the output to a particular :py:class:`.Stage` (defaults to all stages)
        :param props: a list of properties to display in the summary
                   valid properties are data_type, categorical, is_unique, categories, cutoffs, range, monitor_for_bias, position
                   (defaults to data_type, categorical, is_unique)
        :param print_df: boolean value whether to print df or return it, defaults to False

        :return: Optional[pandas.Dataframe]
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """

        if props is None:
            props = ["value_type", "categorical", "is_unique", "categories", "bins", "range", "monitor_for_bias"]

        attributes: Optional[List[ArthurAttribute]] = None
        if stage is None:
            attributes = self.attributes
            display_items = ["name", "stage"] + props
        else:
            attributes = self.get_attributes(stage=stage)
            display_items = ["name"] + props
        if attributes is None:
            raise MissingParameterError("model does not have any attributes")

        result_df = DataFrame(columns=display_items)
        for attribute in attributes:
            row: Dict[str, Union[str, List[str]]] = {}
            for item in display_items:
                if item == 'range':
                    row[item] = f"[{attribute.min_range}, {attribute.max_range}]"
                elif item == 'categories':
                    string_categories = []
                    categories = [] if attribute.categories is None else attribute.categories
                    for cat in categories:
                        if cat.label is not None:
                            string_categories.append("{" + f"label: {cat.label}, value: {cat.value}" + "}")
                        else:
                            string_categories.append("{" + f"value: {cat.value}" + "}")
                    row[item] = string_categories
                else:
                    row[item] = attribute.__getattribute__(item)
            result_df = result_df.append(row, ignore_index=True)

        if print_df:
            try:
                display(result_df) # type: ignore
            except NameError:
                print(result_df)
        else:
            return result_df

    @arthur_excepted("failed to set predict function input order")
    def set_predict_function_input_order(self, attributes: List[str]) -> None:
        """Sets the expected order of attributes used by the prediction function.

        :param attributes: a list of attribute names

        :return: None
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        for idx, name in enumerate(attributes):
            attribute = self.get_attribute(name, Stage.ModelPipelineInput)
            attribute.position = idx

    @arthur_excepted("failed to set attribute as sensitive")
    def set_attribute_as_sensitive(self, attribute_name: str, attribute_stage: Optional[Stage] = None) -> None:
        """Sets the passed-in attribute to be sensitive by setting `attr.monitor_for_bias` = True.

        You will need to call `self.save()` or `self.update()` after this method; we do not
        automatically call the API in this method.

        :param attribute_name: Name of attribute to set as sensitive.
        :param attribute_stage: Stage of attribute to set as sensitive.

        :return: None

        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        attribute = self.get_attribute(attribute_name, attribute_stage)

        attribute.monitor_for_bias = True

    @arthur_excepted("failed to enable explainability")
    def enable_explainability(self, df: DataFrame,
                              project_directory: str,
                              user_predict_function_import_path: str,
                              streaming_explainability_enabled: Optional[bool] = True,
                              requirements_file: str = "requirements.txt",
                              python_version: str = sys.version,
                              sdk_version: str = __version__,
                              model_server_num_cpu: Optional[str] = None,
                              model_server_memory: Optional[str] = None,
                              model_server_max_replicas: Optional[int] = None,
                              inference_consumer_num_cpu: Optional[str] = None,
                              inference_consumer_memory: Optional[str] = None,
                              inference_consumer_thread_pool_size: Optional[int] = None,
                              inference_consumer_score_percent: Optional[float] = None,
                              explanation_nsamples: Optional[int] = None,
                              explanation_algo: Optional[str] = None,
                              ignore_dirs: List = None) -> None:
        """Enable explainability for this model.

        :param df:                                a dataframe containing the :py:class:`.Stage.ModelPipelineInput` values for this model
        :param project_directory:                 the name of the directory containing the model source code
        :param user_predict_function_import_path: the name of the file that implements or wraps the predict function
        :param streaming_explainability_enabled:  Defaults to true. flag to turn on streaming explanations which will explain every inference sent to the platform. If false, explanations will need to be manually generated for each inference via the Arthur API. Set to false if worried about compute cost.
        :param requirements_file:                 the name of the file that contains the pip requirements (default: requirements.txt)
        :param python_version:                    the python version (default: sys.version)
        :param sdk_version:                       the version of the sdk to initialize the model servier with
        :param model_server_num_cpu:              string number of CPUs to provide to model server docker container. If not provided, 1 CPU is used. Specified in the format of Kubernetes CPU resources. '1', '1.5', '100m', etc. (default: None)
        :param model_server_memory:               The amount of memory to allocate to the model server docker container. Provided in the format of kubernetes memory resources "1Gi" or "500Mi" (default: None).
        :param model_server_max_replicas          The max number of model servers to create
        :param inference_consumer_num_cpu:        string number of CPUs to provide to inference consumer docker container. If not provided, 1 CPU is used. Specified in the format of Kubernetes CPU resources. '1', '1.5', '100m', etc. (default: '1')
        :param inference_consumer_memory:         The amount of memory to allocate to the model server docker container. Provided in the format of kubernetes memory resources "1Gi" or "500Mi" (default: '1G').
        :param inference_consumer_thread_pool_size  The number of inference consumer workers, this determines how many requests to the model server can be made in parallel. Default of 5. If increasing, CPU should be increased as well.
        :param inference_consumer_score_percent   What percent of inferences should get scored. Should be a value between 0.0 and 1.0. Default 1.0 (everything is scored)
        :param explanation_nsamples:              number of predictions to use in the explanation. For SHAP the default is 2048 + 2(num features). For LIME, the default is 5000. (default: None)
        :param explanation_algo:                  the algorithm to use for explaining inferences. Valid values are 'lime' and 'shap'. Defaults to 'lime'.
        :param ignore_dirs:                       a list of directories within the project_directory that you do not want to include when uploading the model.  Path is relative to project_directory.
        :return: None
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        if self.input_type == InputType.NLP and self.text_delimiter is None:
            raise MissingParameterError("Must set a text delimiter for NLP models prior to enabling explainability")
        explainability_config = dict(
            df=df,
            project_directory=project_directory,
            ignore_dirs=ignore_dirs if ignore_dirs else [],
            user_predict_function_import_path=user_predict_function_import_path,
            streaming_explainability_enabled=streaming_explainability_enabled,
            requirements_file=requirements_file,
            python_version=python_version,
            sdk_version=sdk_version,
            explanation_nsamples=explanation_nsamples,
            explanation_algo=explanation_algo,
            model_server_num_cpu=model_server_num_cpu,
            model_server_memory=model_server_memory,
            model_server_max_replicas=model_server_max_replicas,
            inference_consumer_num_cpu=inference_consumer_num_cpu,
            inference_consumer_memory=inference_consumer_memory,
            inference_consumer_thread_pool_size=inference_consumer_thread_pool_size,
            inference_consumer_score_percent=inference_consumer_score_percent
        )
        return self.update_enrichment(Enrichment.Explainability, True, explainability_config)

    def _check_model_save(self, msg="You must save the model before sending"):
        if self.id is None:
            raise MethodNotApplicableError(msg)

    @arthur_excepted("failed to send inferences")
    def send_inferences(self, inferences: List[Dict[str, Any]], fail_silently: bool = False):
        """Uploads an list of json inferences of the format below.
        
        All inferences should follow the column format specified in `add_<modeltype>_classifier_output_attributes()`.
        Additionally, all inferences must have `partner_inference_id` and `inference_timestamp` fields. If
        `ground_truth_data` is supplied then `ground_truth_timestamp` is required. All timestamps should be in UTC
        ISO 8601 format. `inference_data` Should contain a key/value pair for every registered attribute name and value.

        :param inferences: a list of json inference objects to upload:

         .. code-block:: JSON

            [
                {
                    "inference_timestamp": "string",
                    "partner_inference_id": "string",
                    "batch_id": "string",
                    "inference_data": {},
                    "ground_truth_timestamp": "string",
                    "ground_truth_data": {}
                }
            ]
        :param fail_silently: if True, log failed inferences but do not raise an exception

        :return: Upload status response in the following format:

         .. code-block:: JSON

            {
              "counts": {
                "success": 0,
                "failure": 0,
                "total": 0
              },
              "results": [
                {
                  "message": "success",
                  "status": 200
                }
              ]
            }

        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        self._check_model_save(msg="Must save model before sending inferences.")

        inferences = arthur_util.format_timestamps(inferences)
        
        for i in range(len(inferences)):
            inferences[i]["inference_data"] = self._replace_nans_and_infinities_in_dict(inferences[i]["inference_data"])
            inferences[i]['inference_data'] = self._convert_numpy_to_native(inferences[i]["inference_data"])
            if 'ground_truth_data' in inferences[i]:
                inferences[i]['ground_truth_data'] = self._convert_numpy_to_native(inferences[i]["ground_truth_data"])

        url = f"{self._client.base_path}/models/{self.id}/inferences"
        resp = self._client.post(url, data=inferences, return_raw_response=True)

        user_failures, internal_failures = \
            validation.validate_multistatus_response_and_get_failures(resp, raise_on_failures=(not fail_silently))
        if fail_silently and (len(user_failures) > 0) or (len(internal_failures) > 0):
            message = "not all inferences succeeded!"
            message += f" user failures: {user_failures}." if len(user_failures) > 0 else ""
            message += f" internal failures: {internal_failures}." if len(internal_failures) > 0 else ""
            logger.error(message)

        return resp.json()

    def _format_inference_request(self, inference_timestamp: Union[str, datetime],
                                  partner_inference_id: Optional[str] = None,
                                  model_pipeline_input=None,
                                  non_input_data=None,
                                  predicted_value=None,
                                  ground_truth=None):
        """takes in an inference to send following the old sdk contract and converts the data to the request body
        of the new api format.


        :param inference_timestamp: a mapping of the name of ground truth attributes to their value
        :param partner_inference_id: an external id (partner_inference_id) to assign to the inferences
        :param model_pipeline_input: a mapping of the name of pipeline input attributes to their value
        :param non_input_data: a mapping of the name of non-input data attributes to their value
        :param predicted_value: a mapping of the name of predicted value attributes to their value
        :param ground_truth: a mapping of the name of ground truth attributes to their value

        :return: dictionary object which can be used to send the inference
        """
        if model_pipeline_input is None:
            model_pipeline_input = {}
        if non_input_data is None:
            non_input_data = {}
        if predicted_value is None:
            predicted_value = {}

        model_pipeline_input.update(predicted_value)
        model_pipeline_input.update(non_input_data)
        inference = {
            "inference_timestamp": inference_timestamp,
            "partner_inference_id": partner_inference_id,
            "inference_data": model_pipeline_input,
        }

        if ground_truth is not None:
            inference["ground_truth_timestamp"] = inference_timestamp
            inference["ground_truth_data"] = ground_truth

        return inference

    @staticmethod
    def _replace_nans_and_infinities_in_dict(dict_to_update) -> Optional[Dict]:
        if dict_to_update is None:
            return None

        return dict(
            (k, v if ((type(v) != float or not np.isnan(v)) and v != np.Inf and v != -np.inf and v != np.inf) else None)
            for k, v in dict_to_update.items())

    @staticmethod
    def _convert_numpy_to_native(dict_to_update) -> Dict:
        final_dict = {}
        for k, v in dict_to_update.items():
            if isinstance(v, np.generic):
                final_dict[k] = v.item()
            else:
                final_dict[k] = v
        return final_dict

    @arthur_excepted("failed to send inference")
    def send_inference(self, inference_timestamp: Union[str, datetime],
                       partner_inference_id: str = "",
                       model_pipeline_input=None,
                       non_input_data=None,
                       predicted_value=None,
                       ground_truth=None):
        """Uploads an inference with or without ground truth; this sends a single inference.

        All inferences should follow the column format specified in `add_<modeltype>_classifier_output_attributes()`. 
        Additionally, external_id and inference_timestamp must be provided. 

        :param inference_timestamp: timestamp for inference to send; generated by external partner (not Arthur)
        :param partner_inference_id: an external id (partner_inference_id) to assign to the inferences
        :param model_pipeline_input: a mapping of the name of pipeline input attributes to their value
        :param non_input_data: a mapping of the name of non-input data attributes to their value
        :param predicted_value: a mapping of the name of predicted value attributes to their value
        :param ground_truth: a mapping of the name of ground truth attributes to their value
        
        :return: Upload status response in the following format:

         .. code-block:: JSON

            {
                "counts": {
                    "success": 0,
                    "failure": 0,
                    "total": 0
                },
                "results": [
                    {
                        "message": "success",
                        "status": 200
                    }
                ]
            }

        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        if predicted_value is None:
            predicted_value = {}
        if non_input_data is None:
            non_input_data = {}
        if model_pipeline_input is None:
            model_pipeline_input = {}

        self._check_model_save(msg="Must save model before sending inferences.")

        inference = self._format_inference_request(
            inference_timestamp=inference_timestamp,
            partner_inference_id=partner_inference_id,
            model_pipeline_input=ArthurModel._replace_nans_and_infinities_in_dict(model_pipeline_input),
            non_input_data=ArthurModel._replace_nans_and_infinities_in_dict(non_input_data),
            predicted_value=ArthurModel._replace_nans_and_infinities_in_dict(predicted_value),
            ground_truth=ArthurModel._replace_nans_and_infinities_in_dict(ground_truth)
        )
        return self.send_inferences([inference])

    @arthur_excepted("failed to update inference ground truths")
    def update_inference_ground_truths(self, ground_truths: List[Dict[str, Any]], fail_silently: bool = False):
        """Updates a list of inferences with the supplied ground truth values.
        Ground truth json must include fields "ground_truth_timestamp", "partner_inference_id",
        and "ground_truth_data".
        Field "ground_truth_data" is a dictionary with keys corresponding to attributes names
        from Stage.GroundTruth.

        :param ground_truths: a mapping of the name of a ground truth attribute name to its value

            ..  code-block:: JSON

                [
                  {
                    "ground_truth_timestamp": "string",
                    "partner_inference_id": "string",
                    "ground_truth_data": {
                      "gt_fraud": 1,
                      "gt_not_fraud": 0
                    }
                  }
                ]
        :param fail_silently: if True, log failed inferences but do not raise an exception

        :return: Upload status response in the following format:

            .. code-block:: JSON

                {
                    "counts": {
                        "success": 0,
                        "failure": 0,
                        "total": 0
                    },
                    "results": [
                        {
                            "message": "success",
                            "status": 200
                        }
                    ]
                }

        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        self._check_model_save()

        ground_truths = arthur_util.format_timestamps(ground_truths)

        url = f"{self._client.base_path}/models/{self.id}/inferences"
        resp = self._client.patch(url, data=ground_truths, return_raw_response=True)
        user_failures, internal_failures = \
            validation.validate_multistatus_response_and_get_failures(resp, raise_on_failures=(not fail_silently))
        if fail_silently and (len(user_failures) > 0) or (len(internal_failures) > 0):
            message = "not all ground truth updates succeeded!"
            message += f" user failures: {user_failures}." if len(user_failures) > 0 else ""
            message += f" internal failures: {internal_failures}." if len(internal_failures) > 0 else ""
            logger.error(message)

        return resp.json()

    @arthur_excepted("failed to binarize")
    def binarize(self, attribute_value):
        """Creates a binary class probability based on classes defined in a :py:attr:`.ModelType.Multiclass` model.

        :param attribute_value: a mapping of the name of a predicted value attribute to its value

        :return: A two-value dictionary with probabilities for both predicted classes.
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """

        if len(attribute_value) > 1:
            raise UserValueError("A dictionary containing a key, value pair for one ground truth attribute is required")

        name, value = attribute_value.popitem()
        name = str(name)
        predicted_value = self.get_attributes(Stage.PredictedValue)
        if name not in [attr.name for attr in predicted_value]:
            raise UserValueError(f"Attribute {name} not found in {Stage.PredictedValue}")

        valid_type = lambda attr: attr.value_type == ValueType.Float and attr.min_range == 0.0 and attr.max_range == 1.0
        if len(predicted_value) == 2 and all([valid_type(attr) for attr in predicted_value]):
            return dict([(attr.name, value if attr.name == name else 1 - value) for attr in predicted_value])
        else:
            raise MethodNotApplicableError("This model is not a binary classification model.")

    @arthur_excepted("failed to one hot encode")
    def one_hot_encode(self, value):
        """Creates a one hot encoding of a class label based on classes defined in a :py:attr:`.ModelType.Multiclass` model.

        :param value: the ground truth value

        :return: A dictionary with a one hot encoding of possible ground truth values.
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        name = str(value)
        ground_truth = self.get_attribute_names(stage=Stage.GroundTruth)
        if name not in ground_truth:
            raise UserValueError(f"Attribute {name} not found in {Stage.GroundTruth}")
        elif self.output_type != OutputType.Multiclass:
            raise MethodNotApplicableError("This model is not a Multiclass model")
        else:
            return dict([(attr_name, 1 if attr_name == name else 0) for attr_name in ground_truth])

    def _send_parquet_files(self,
                            url: str,
                            file_name: str,
                            directory_path: Optional[str] = None,
                            data: Optional[Union[DataFrame, Series]] = None,
                            initial_form_data: Optional[Dict[str, Any]] = None,
                            retries: int = 0):

        self._check_model_save(msg="Must save model before uploading reference data")

        if directory_path is None and data is None:
            raise MissingParameterError("Either directory_path or data must be provided")

        if data is not None:
            if isinstance(data, DataFrame):
                filename = DatasetService.convert_dataframe(model_id=self.id, stage=None, df=data)
            elif isinstance(data, Series):
                filename = DatasetService.convert_dataframe(model_id=self.id, stage=None, df=data.to_frame())
            else:
                raise UserTypeError("Unsupported data type: a pandas.DataFrame or pandas.Series is required")
            directory_path = filename[:filename.rfind('/')]

        _, file_info = DatasetService.send_parquet_files_from_dir_iteratively(self,
                                                                              directory_path,
                                                                              url,
                                                                              file_name,
                                                                              additional_form_params=initial_form_data,
                                                                              retries=retries)
        return file_info

    @arthur_excepted("failed to set reference data")
    def set_reference_data(self, directory_path: Optional[str] = None, data: Optional[Union[DataFrame, Series]] = None):
        """Validates and sets the reference data for the given stage to the provided data.
        
        Either directory_path or data must be provided. Additionally, there must be 
        one column per `ModelPipelineInput` and `NonInput` attribute. 

        :param directory_path: file path to a directory of parquet files to upload for batch data
        :param data:  a DataFrame or Series containing the ground truth data

        :return: Returns a tuple, the first variable is the response from sending the reference set and the second
        is the response from closing the dataset.

        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        if directory_path is None and data is None:
            raise MissingParameterError("Either directory_path or data must be provided")

        if data is not None:
            data = core_util.standardize_pd_obj(data, dropna=False, replacedatetime=False)

        url = f"{self._client.base_path}/models/{self.id}/reference_data"
        res = self._send_parquet_files(url, 'reference_data.parquet', directory_path, data)

        ref_set_close_res = None
        if res[DatasetService.COUNTS][DatasetService.FAILURE] != 0:
            logger.warning(f"{res[DatasetService.COUNTS][DatasetService.FAILURE]} inferences failed to upload")
            logger.warning("Reference dataset auto-close was aborted because not all "
                           "inferences in the reference set were successfully uploaded")
        else:
            if data is None:
                files = core_util.retrieve_parquet_files(directory_path)
                num_rows = self._count_parquet_num_rows(files, check_cols=False)
            else:
                num_rows = len(data)

            if num_rows == 0:
                raise UserValueError("data provided does not have any rows")

            ref_set_close_res = self._close_datatset(f"{self._client.base_path}/models/{self.id}/reference_data", num_rows)
        return res, ref_set_close_res

    @arthur_excepted("failed to send batch ground truths")
    def send_batch_ground_truths(self, directory_path: Optional[str] = None,
                                 data: Optional[Union[DataFrame, Series]] = None):
        """ Uploads parquet files containing a columns for partner_inference_id, ground_truth_timestamp, and column(s) for
        inference ground truth

        :param directory_path: file path to a directory of parquet files containing ground truth data
        :param data:  a DataFrame or Series containing the reference data for the :py:class:`Stage`

        :return: Upload status response in the following format:

            .. code-block:: JSON

                {
                    "counts": {
                        "success": 0,
                        "failure": 0,
                        "total": 0
                    },
                    "results": [
                        {
                            "message": "success",
                            "status": 200
                        }
                    ]
                }
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """

        self._check_model_save()

        if directory_path is None and data is None:
            raise MissingParameterError("Either directory_path or data must be provided")

        url = f"{self._client.base_path}/models/{self.id}/inferences/file"
        return self._send_parquet_files(url, 'ground_truths.parquet', directory_path, data,
                                        retries=INFERENCE_DATA_RETRIES)

    @arthur_excepted("failed to send batch inferences")
    def send_batch_inferences(self,
                              batch_id: str,
                              directory_path: Optional[str] = None,
                              data: Optional[DataFrame] = None,
                              complete_batch: bool = True):
        """Validates and uploads parquet files containing columns for inference data, partner_inference_id,
        inference_timestamp, and optionally a batch_id and ground truth data. Either directory_path or data must be
        specified.

        The columns for predicted attributes should follow the column format specified in 
        `add_<modeltype>_classifier_output_attributes()`.  Additionally, `partner_inference_id`, 
        `inference_timestamp`, must be specified for all inferences.

        :param directory_path: file path to a directory of parquet files containing ground truth data
        :param data:  a DataFrame containing the reference data. 
        :param batch_id: string id for the batch to upload; if supplied, this will override any batch_id column
                      specified in the provided dataset
        :param complete_batch: Defaults to true and will automatically close a batch once it is sent

        :return: A tuple of the batch upload response and the close batch response.
        The batch upload response is in the following format:

            .. code-block:: JSON

                {
                    "counts": {
                        "success": 0,
                        "failure": 0,
                        "total": 0
                    },
                    "results": [
                        {
                            "message": "success",
                            "status": 200
                        }
                    ]
                }
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        initial_form_data = {'batch_id': (None, batch_id)}
        url = f"{self._client.base_path}/models/{self.id}/inferences/file"

        if directory_path is None and data is None:
            raise MissingParameterError("Either directory_path or data must be provided.")

        if data is not None:
            if isinstance(data, DataFrame):
                num_rows = len(data)
                self._check_batch_inference_columns(data.columns)
                data = core_util.standardize_pd_obj(data, dropna=False, replacedatetime=False)
            else:
                raise UserTypeError("Unsupported data type: a pandas.DataFrame is required")
        else:
            files = core_util.retrieve_parquet_files(directory_path)
            num_rows = self._count_parquet_num_rows(files, check_cols=True)

        if num_rows == 0:
            raise UserValueError("data provided does not have any rows")

        res = self._send_parquet_files(url, 'inferences.parquet', directory_path, data,
                                       initial_form_data=initial_form_data,
                                       retries=INFERENCE_DATA_RETRIES)
        batch_res = None
        if res[DatasetService.COUNTS][DatasetService.FAILURE] != 0:
            logger.warning(f"{res[DatasetService.COUNTS][DatasetService.FAILURE]} inferences failed to upload")
            if complete_batch:
                logger.warning("Batch auto-close was aborted because not all inferences were successfully uploaded")
        elif complete_batch:
            url = f"{self._client.base_path}/models/{self.id}/batches/{batch_id}"
            batch_res = self._close_datatset(url, num_rows)
        return res, batch_res

    def _count_parquet_num_rows(self, file_paths: List[str], check_cols: bool = False) -> int:
        num_rows = 0
        for file in file_paths:
            pqfile = pq.ParquetFile(file)
            num_rows += pqfile.metadata.num_rows
            cols = [pqfile.schema[i].name for i in range(len(pqfile.schema))]
            if check_cols:
                self._check_batch_inference_columns(cols)

        return num_rows

    def _close_datatset(self, url: str, num_inferences: Optional[int] = None) -> Dict:
        body: Dict[str, Union[str, int]] = {
            "status": "uploaded"
        }
        if num_inferences is not None:
            body["total_record_count"] = num_inferences

        batch_res = self._client.patch(url=url, data=body, return_raw_response=True, retries=INFERENCE_DATA_RETRIES)
        if batch_res.status_code != 200:
            batch_message = batch_res.json()
            logger.warning(f"dataset auto-close failed: {batch_message}")
        else:
            batch_message = "success"
        return {"dataset_close_result": batch_message}

    @arthur_excepted("failed to close batch")
    def close_batch(self, batch_id: str, num_inferences: Optional[int] = None) -> Dict:
        """Closes the specified batch, optionally can supply the number of inferences that are contained in the batch

        :param batch_id: String batch_id associated with the batch that will be closed
        :param num_inferences: Optional number of inferences that are contained in the batch
        :return: Response of the batch close rest call
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        url = f"{self._client.base_path}/models/{self.id}/batches/{batch_id}"
        return self._close_datatset(url, num_inferences)

    @staticmethod
    def _check_batch_inference_columns(columns):
        error_message = ""
        if 'inference_timestamp' not in columns:
            error_message += '`inference_timestamp` must be a column in the data. '
        if 'partner_inference_id' not in columns:
            error_message += '`partner_inference_id` must be a column in the data. '

        if error_message != "":
            raise MissingParameterError(error_message)

    @arthur_excepted("failed to delete explainer")
    def delete_explainer(self) -> None:
        """Spin down the model explainability server.

        :return: the server response

        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        if not hasattr(self, "_explainer"):
            raise MethodNotApplicableError(f"There is no explainability server to delete for model {self.id}")

        url = f"{self._client.base_path}/models/{self.id}/explainability"
        resp = self._client.delete(url, return_raw_response=True)

        validation.validate_response_status(resp, expected_status_code=HTTPStatus.NO_CONTENT)
        logger.info(f"Successfully removed explainability server for model {self.id}")

    @arthur_excepted("failed to archive model")
    def archive(self):
        """Archives the model with a DELETE request.

        :return: the server response
        :raise: Exception: the model has no ID, or the model has not been archived
        """
        self._check_model_save(msg="Cannot archive an unregistered model.")

        url = f"{self._client.base_path}/models/{self.id}"
        resp = self._client.delete(url, return_raw_response=True)
        validation.validate_response_status(resp, expected_status_code=HTTPStatus.NO_CONTENT)

    @arthur_excepted("failed to execute query")
    def query(self, body: Dict[str, Any], query_type='base'):
        """ Execute query against the model's inferences.
        For full description of possible functions, aggregations, and transformations, see
        https://docs.arthur.ai/api-documentation/query_guide.html
        For queries pertaining to datadrift metrics, please see
        https://docs.arthur.ai/api-documentation/query_endpoint_documentation.html#data-drift

        :param body: dict
        :param query_type: str Can be either 'base' or 'drift'

        .. code-block:: python

            body = {
                       "select":[
                          {"property":"batch_id"},
                          {
                             "function":"count",
                             "alias":"inference_count"
                          }
                       ],
                       "group_by":[
                          {"property":"batch_id"}
                       ]
                    }

        .. code-block:: python

            body = {
                       "select":[,
                          {"property":"batch_id"},
                          {
                             "function":"rate",
                             "alias":"positive_rate",
                             "parameters":{
                                "property":"predicted_1",
                                "comparator":"gt",
                                "value":0.75
                             }
                          }
                       ],
                       "group_by":[
                          {"property":"batch_id"}
                       ]
                    }


        :return: the query response as documented in https://docs.arthur.ai/api-documentation/query_guide.html
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        self._check_model_save(msg="You must save model before querying.")

        url = f"{self._client.base_path}/models/{self.id}/inferences/query"
        if query_type == "drift":
            url = f"{url}/data_drift"
        resp = self._client.post(url, data=body, return_raw_response=True)

        validation.validate_response_status(resp, expected_status_code=HTTPStatus.OK)

        return resp.json()["query_result"]

    @arthur_excepted("failed to create alert rule")
    def create_alert_rule(self,
                          bound: Optional[AlertRuleBound] = None,
                          threshold: Optional[NumberType] = None,
                          metric: Optional[Union[AlertMetric, str]] = None,
                          severity: Optional[AlertRuleSeverity] = None,
                          query: Optional[dict] = None,
                          lookback_period: Optional[NumberType] = None,
                          subsequent_alert_wait_time: Optional[NumberType] = None,
                          check_batch_idle_time: Optional[NumberType] = None,
                          attribute_id: Optional[str] = None,
                          attribute_name: Optional[str] = None,
                          enabled: bool = True,
                          alert_rule: Optional[AlertRule] = None) -> AlertRule:
        """
        :param bound:
        :param threshold:
        :param metric:
        :param severity:
        :param query:
        :param lookback_period:
        :param subsequent_alert_wait_time:
        :param check_batch_idle_time:
        :param attribute_id:
        :param attribute_name:
        :param enabled:
        :param alert_rule:
        :return: the created alert rule
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        if alert_rule is not None:
            if not isinstance(alert_rule, AlertRule):
                raise UserTypeError("alert_rule supplied must be an AlertRule Object")
            # cannot have a set id for an alert rule that hasn't been created yet
            alert_rule.id = None
        else:
            alert_rule = AlertRule(
                bound=bound,
                threshold=threshold,
                metric=metric,
                severity=severity,
                query=query,
                lookback_period=lookback_period,
                subsequent_alert_wait_time=subsequent_alert_wait_time,
                check_batch_idle_time=check_batch_idle_time,
                attribute_id=attribute_id,
                attribute_name=attribute_name,
                enabled=enabled
            )

        url = f"{self._client.base_path}/models/{self.id}/alert_rules"
        resp = self._client.post(url, data=alert_rule.to_dict(), return_raw_response=True)

        validation.validate_response_status(resp, expected_status_code=HTTPStatus.OK)

        return AlertRule.from_dict(resp.json())

    @arthur_excepted("failed to get model alert rules")
    def get_model_alert_rules(self, page: int = 1, page_size: int = 20) -> List[AlertRule]:
        """Returns a paginated list of alert rules registered to this model

        :param page: page of alert rules to retrieve, defaults to 1
        :param page_size: number of alert rules to return per page, defaults to 20
        :return: List of :class:`arthurai.client.apiv3.AlertRule` objects
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        url = f"{self._client.base_path}/models/{self.id}/alert_rules?page_size={page_size}&page={page}"
        resp = self._client.get(url, return_raw_response=True)

        validation.validate_response_status(resp, expected_status_code=HTTPStatus.OK)
        if 'data' not in resp.json():
            raise ExpectedParameterNotFoundError("An error occurred when retrieving alert rules: {0}".format(resp.json()))

        alert_rules = []
        for rule in resp.json()['data']:
            alert_rules.append(AlertRule.from_dict(rule))
        return alert_rules

    @arthur_excepted("failed to update alert rule")
    def update_alert_rule(self, alert_rule: AlertRule, alert_rule_id: Optional[str] = None):
        """Updates alert rule fields included in the `alert_rule` object for the specified alert rule id. If the
        alert rules id field is present in the `alert_rule` parameter that is used otherwise `alert_rule_id`
        must be supplied

        :param alert_rule: Object which contains fields to update on the specified alert rule
        :param alert_rule_id: If the alert rule id is not specified in the `alert_rule_to_update` object then this
                              must be provided to determine which alert rule to update.
        :return: Updates alert rule object
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        if alert_rule.id is None and alert_rule_id is None:
            raise MethodNotApplicableError("alert_rule_to_update must have a valid id, if the alert rule has not been "
                                           "created yet call model.create_alert_rule(...)")

        alert_rule_id = alert_rule.id if alert_rule.id is not None else alert_rule_id
        alert_rule.id = None

        url = f"{self._client.base_path}/models/{self.id}/alert_rules/{alert_rule_id}"
        resp = self._client.patch(url, data=alert_rule.to_dict(), return_raw_response=True)

        validation.validate_response_status(resp, expected_status_code=HTTPStatus.OK)

        return AlertRule.from_dict(resp.json())

    @arthur_excepted("failed to get enrichments")
    def get_enrichments(self) -> Dict[str, Any]:
        """Returns configuration for all enrichments.

        :return: Upload status response in the following format:

            .. code-block:: JSON

                {
                    "anomaly_detection": {
                        "enabled": false
                    },
                    "explainability": {
                        "config": {
                            "python_version": "3.7",
                            "sdk_version": "3.0.11",
                            "streaming_explainability_enabled": false,
                            "user_predict_function_import_path": "entrypoint",
                            "shap_expected_values": "[0.7674405187893311, 0.23255948121066888]",
                            "model_server_cpu": "2",
                            "model_server_memory": "1Gi",
                            "model_server_max_replicas": "5",
                            "explanation_nsamples": 1000,
                            "explanation_algo": "lime",
                            "inference_consumer_cpu": "100m",
                            "inference_consumer_memory": "512Mi",
                            "inference_consumer_score_percent": "1.0",
                            "inference_consumer_thread_pool_size": "1",
                            "service_account_id": "8231affb-c107-478e-a1b4-e24e7f1f6619"
                        },
                        "enabled": true
                    }
                }
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        url = f"{self._client.base_path}/models/{self.id}/enrichments"
        resp = self._client.get(url, return_raw_response=True)
        validation.validate_response_status(resp, expected_status_code=HTTPStatus.OK)
        return resp.json()

    @arthur_excepted("failed to get enrichment")
    def get_enrichment(self, enrichment: Enrichment) -> Dict[str, Any]:
        """Returns configuration for the specified enrichment.

        :param enrichment: Enrichment constant
        :return: Enrichment config

            .. code-block:: JSON

                {
                    "enabled": true,
                    "config": {
                        "python_version": "3.7",
                        "sdk_version": "3.0.11",
                        "streaming_explainability_enabled": false,
                        "user_predict_function_import_path": "entrypoint",
                        "shap_expected_values": "[0.7674405187893311, 0.23255948121066888]",
                        "model_server_cpu": "2",
                        "model_server_memory": "1Gi",
                        "model_server_max_replicas": "5",
                        "explanation_nsamples": 1000,
                        "explanation_algo": "lime",
                        "inference_consumer_cpu": "100m",
                        "inference_consumer_memory": "512Mi",
                        "inference_consumer_score_percent": "1.0",
                        "inference_consumer_thread_pool_size": "1",
                        "service_account_id": "8231affb-c107-478e-a1b4-e24e7f1f6619"
                    }
                }
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        url = f"{self._client.base_path}/models/{self.id}/enrichments/{enrichment}"
        resp = self._client.get(url, return_raw_response=True)
        validation.validate_response_status(resp, expected_status_code=HTTPStatus.OK)
        return resp.json()

    @arthur_excepted("failed to update enrichments")
    def update_enrichments(self, enrichment_configs: Dict[Union[str, Enrichment], Any]) -> Dict[str, Any]:
        """Update the configuration for 1 or more enrichments.
        See the enrichments guide at http://docs.arthur.ai/guides/enrichments.html.

        :param enrichment_configs: Dict containing the configuration for each enrichment

            .. code-block:: JSON

            {
                    "anomaly_detection": {
                        "enabled": false
                    },
                    "explainability": {
                        "config": {
                            "streaming_explainability_enabled": false,
                            "explanation_nsamples": 1000,
                            "explanation_algo": "lime",
                            "inference_consumer_score_percent": "1.0"
                        },
                        "enabled": true
                    }
                }
        :return: the resulting enrichments configuration
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """

        files = []
        # handle specifics for different enrichments
        if Enrichment.Explainability in enrichment_configs and enrichment_configs[Enrichment.Explainability]['enabled']:
            explanationPackager = ExplanationPackager(self, **enrichment_configs[Enrichment.Explainability]['config'])

            # check to see if user is trying to update files
            onePresent, allPresent = explanationPackager.contains_file_fields()
            if onePresent and not allPresent:
                raise MissingParameterError(f"If updating model files for explainability, all of the following fields must be present in the config {ExplanationPackager.FILE_FIELDS}")
            # package explainer files
            elif allPresent:
                explanationPackager.make_zip()
                explanationPackager.create()
                files += explanationPackager.get_request_files()
            # replace passed in config (has file specific fields) with actual config
            enrichment_configs[Enrichment.Explainability]["config"] = explanationPackager.get_request_config()

        # build and make request
        headers = {"Content-Type": "multipart/form-data"}
        url = f"{self._client.base_path}/models/{self.id}/enrichments"
        data = {"config": json.dumps(enrichment_configs)}
        # we need to make sure when we send no files, the config dict is still marked as multipart with a boundary
        # to do this, we trick requests into thinking there are files, but there aren't
        if files == []:
            files.append(('',''))

        resp = self._client.patch(url, data, files=files, headers=headers, return_raw_response=True)
        validation.validate_response_status(resp, expected_status_code=HTTPStatus.ACCEPTED)
        return resp.json()

    @arthur_excepted("failed to update enrichment")
    def update_enrichment(self, enrichment: Enrichment, enabled: bool, config: Dict[str, Any]) -> Dict[str, Any]:
        """Update the configuration for a single enrichment.
        :param enrichment: the enrichment to update
        :param enabled: whether the enrichment should be enabled or disabled
        :param config: the configuration for the enrichment
        :raise: ArthurUserError: failed due to user error
        :raise: ArthurInternalError: failed due to an internal error
        """
        return self.update_enrichments({
            enrichment: {"enabled": enabled, "config": config}
        })
