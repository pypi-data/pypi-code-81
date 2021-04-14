from polzyFunctions.Dataclasses.Antrag import Antrag
from polzyFunctions.Activities.Activity import Activity
from polzyFunctions.GamificationActivityRecorder import recordActivityDecorator
from polzyFunctions.AntragActivityRecorder import recordAntragDecorator
from polzyFunctions.GlobalConstants import GlobalConstants
from logging import getLogger


logger = getLogger(GlobalConstants.loggerName)


class AntragActivity(Activity):
    """
    All activities are called with an instance of Polizze and effectiveDate (Effective date)

    The first call for each activity is to method 'checkIsActivityValidForPolicy'.
        For instance a cancel-activity will switch itself of, if the policy is already in status cancelled.
        The activity will not be offered to the user.

    Next a remote system would call 'getFieldsForActivity' method to know, which attributes need to be provided
        for this activity to run.

    It is advisable to call 'checkAndUpdateInput' if the attribute of an updated field has the value bool True
        in field inputTriggersComplexUpdates

    With method 'executeActivity' the activity is executed.

    Internally each activity will use or implement additional methods, e.g.
        'addFieldForActivity'
        'createFieldcatalogForActivity'

    """

    def __init__(self, antrag: Antrag, **kwargs):
        super(AntragActivity, self).__init__()
        self.antrag = antrag

    def checkIsActivityValidForStatus(self) -> bool:
        """
        Define, whether this activity is valid for the current status of the current instance. Each instance must
        implement this method
        :return: True if valid/active, False if not valid/activ
        """
        logger.exception(f"Activity not properly implemented! Doesn't know if it's valid for status or not! "
                         f"{self.__class__}")
        raise NotImplementedError((f"Activity not properly implemented! Doesn't know if it's valid for status or not! "
                                   f"{self.__class__}"))

    def setSingleFieldValue(self, fieldNameToSearchFor, valueToSet):
        """
        When we get new values from the frontend or from within the acivities logic, they are processed here

        :param fieldNameToSearchFor:
        :param valueToSet:
        :return:
        """
        self.updateFieldValues({fieldNameToSearchFor: valueToSet})

    def setSingleFieldFieldType(self, fieldNameToSearchFor, fieldVisibilityTypeToSet):
        """
        Sets visibility of a field
        :param fieldNameToSearchFor:
        :param fieldVisibilityTypeToSet: Any of the values of FieldVisibilityTypes (e.g. hidden, visible)
        :return:
        """
        lFeld = self.antrag.Fields.getField(name=fieldNameToSearchFor)
        if lFeld:
            lFeld.fieldVisibilityType = fieldVisibilityTypeToSet
        else:
            logger.warning(f"Should have set FieldType {fieldVisibilityTypeToSet} for field {fieldNameToSearchFor}. But field"
                           f"is not there")

    @recordAntragDecorator
    @recordActivityDecorator
    def executeActivity(self) -> bool:
        """
        Executes this activity. See description in superclass.
        :return: True if successful, False if not successful.
        """
        return super().executeActivity()