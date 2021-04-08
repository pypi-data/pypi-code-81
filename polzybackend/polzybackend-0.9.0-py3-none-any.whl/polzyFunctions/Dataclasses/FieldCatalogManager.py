from polzyFunctions.Activities.ActivitiesDataClasses import FieldDefinition, InputFieldTypes, FieldDataType, \
    FieldVisibilityTypes
from fasifu.GlobalConstants import GlobalConstants
from datetime import datetime   # Needed because dynamically called
from logging import getLogger
from polzyFunctions.translator import Translator
from polzyFunctions.ConfigurationEngine.ConfigurationProvider import ConfigurationProvider
from polzyFunctions.Dataclasses.CommonFieldnames import CommonFieldnames
import codecs
import json
import os

logger = getLogger(GlobalConstants.loggerName)
lTranslator = Translator(default=ConfigurationProvider.getInstance().language)  # <-- This will lead to English.


def get_field_catalog_dictionary(JsonFilesDirectory):
    """
    This function is used to get dictionary based on file/function name. Fields can be stored in JSON-Files
    in the form:
    [
    {
        "fieldVisibilityType": "$(FieldVisibilityTypes.visible)",
        "name": "$(CommonFieldnames.policyBeginDate.value)",
        "tooltip": "Policy beginn date ",
        "shortDescription": "Policy begin date",
        "fieldDataType": "$(FieldDataType(typeName=InputFieldTypes.TYPEDATE))"
    },
    ...
    ]

    These JSON-files can have the same name as each activity.

    :return:
    """

    field_data = dict()
    if JsonFilesDirectory is None:
        return

    filenames = os.listdir(JsonFilesDirectory)
    for filename in filenames:
        if filename[-5:].lower() != ".json":
            continue
        json_file = os.path.join(JsonFilesDirectory, filename)
        with codecs.open(json_file, "r", encoding="utf-8") as file:  # using codecs with utf-8 encoding to avoid errors
            dic = json.load(file)
        field_data[filename[:-5]] = dic  # storing key as filename without extension in order to match function name
    return field_data


class ManageFieldCatalog:
    """
    Here are all field definitions for all policy activities and types of quotations

    The fields are loaded from JSON-files, which have the same name as the Antrag or Activity.
    The are in ../Dataclasses/JsonFiles. See method updateFieldDefinition for details.

    If you want to debug the processing of a JSON-file, put a key "breakpoint" with any value into the JSON and
    we'll issue a breakpoint-statement.
    """

    # This class attribute is necessary and you must call it in sub class and supply FieldCatalog Json Files directory
    # as argument for "JsonFilesDirectory". This method will return a dictionary containing FieldCatalog data for all
    # activities

    # getting dictionary of FieldCatalog data for all functions
    field_data = get_field_catalog_dictionary(JsonFilesDirectory=None)  # None supplied only for making dummy

    @staticmethod
    def addFields(self):
        if not hasattr(ManageFieldCatalog, self.__class__.__name__):
            logger.debug(f"There is no field list for {self.__class__.__name__}. Most probably OK")
            return

        ManageFieldCatalog.determineLanguage(self)  # set Translator to proper Language

        # Execute filling the field catalog for either the antrag, Policy or Activity.
        try:
            getattr(ManageFieldCatalog, self.__class__.__name__)(self)
            logger.debug(f"FielCatalog created for {self.__class__.__name__}")
        except AttributeError as e:
            logger.exception(f"Building field catalog for {self.__class__.__name__} failed. Error was: {e}")

        # Now, that the field-catalog is built, check if we have default values from
        self.deriveDefaultsFromUserOrCompany()

    @staticmethod
    def determineLanguage(self):
        """
        Try to get the user's language for the translator based on User-Object, which is in Antrag or via
        Activity.antrag. If found, we set it as translation language, otherwise we let it in english.
        :param self:
        :return:
        """
        global lTranslator


        desiredLanguage = None
        try:
            desiredLanguage = self.antrag.user.language
        except AttributeError:
            pass

        if not desiredLanguage:
            try:
                desiredLanguage = self.user.language
            except AttributeError:
                pass

        if desiredLanguage:
            lTranslator = Translator(default=desiredLanguage)

    @staticmethod
    def evaluate_value(value, self):
        """
        this function converts string to python literal and treat it as statement. It is used in FieldCatalog values.
        :param value: a value, that can be evaluated to an expression, e.g. "$(True)" will evaluate to bool True.
        :param self: the current instance (of an activity or antrag)
        :return:
        """

        if isinstance(value, dict):  # if it is a dict we need to convert it to json
            for key_, value_ in value.items():
                value[key_] = ManageFieldCatalog.evaluate_value(value_, self)
            value = json.dumps(value)

        # if it has $ prefix with parenthesis in starting then it is a python statement, evaluate it and return it.
        if isinstance(value, str) and len(value) >= 4 and str(value)[:2] + str(value)[-1] == "$()":
            value = eval(value[2:-1])
        return value

    @classmethod
    def updateFieldDefinition(cls, name, self, keys=None, **kwargs):
        """

        :param name: Name of the JSON-File to load the field definition from (this was already cached during init)
        :param self: The object (Either an Antrag-instance or an Activity-Instance)
        :param keys: Keys to load from the JSON. If not provided all records will be loaded
        :param kwargs: Additional arguments, that will be included in the resulting fields, e.g. "backgroundcolor"
        :return:
        """
        field_data_list = cls.field_data.get(name)  # getting list of fieldCatalog data by function name
        for key, value in kwargs.items():  # some functions needs various variables in arguments. These variables are
            globals()[key] = value  # not same always. So, for flexibility we are taking kwargs input and make
        globals()["self"] = self  # them global variable. This is mainly used while evaluating string statement
        # as python literal.

        for data in field_data_list:
            if "breakpoint" in data.keys():
                breakpoint()
                del data["breakpoint"]
            if keys:  # if keys list is supplied that means we need to update FieldCatalog only for those fields.
                field_name = cls.evaluate_value(data.get("name"), self)  # getting evaluated value for name
                if field_name not in keys:
                    continue
            dic = {}
            for key, value in data.items():
                evaluated_value = cls.evaluate_value(value, self)  # evaluating value
                dic[key] = evaluated_value
            self._addFieldForActivity(FieldDefinition(**dic))  # supplying dictionary of evaluated values as kwargs
        for key in kwargs.keys():  # removing globals variable we set above
            del globals()[key]

    @staticmethod
    def AntragCommon(self):
        """
        Common fields for all Antrag instances
        :param self:
        :return:
        """
        ManageFieldCatalog.updateFieldDefinition(name="AntragCommon", self=self)
