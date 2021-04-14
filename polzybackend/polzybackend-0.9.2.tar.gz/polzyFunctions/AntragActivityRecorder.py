from polzyFunctions.GlobalConstants import logger
from polzybackend.models import AntragActivityRecords


def recordAntragDecorator(method):
    """
    Decorator to write the current status after the activity was execute to Database.
    :param method:
    :return:
    """
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        if hasattr(self, "antrag"):
            self.antrag.latestDBTimestamp = activityWriter(self)
        else:
            self.latestDBTimestamp = activityWriter(self)
        return result
    return wrapper


def activityWriter(inInstance):
    """
    The usage of "Antrag" here is wrong, usually it's an AntragActivitiy that will be provided in the call.
    It is anyway important to have this reference because otherwise the "where used" doesn't work for "setSearchString"

    """
    from polzyFunctions.Dataclasses.Antrag import Antrag

    lInstance = None
    try:
        lInstance = inInstance.antrag
    except AttributeError:
        pass

    if not lInstance:
        # this will work if the instance itself is an Antrag (happens so far only when the Tag is changed by
        # frontend
        lInstance:Antrag = inInstance

    logger.debug(f"classname = {lInstance.__class__.__name__}")
    # Update search string in this antrag instance. It is the main search criteria.
    try:
        lInstance.setSearchString()
    except AttributeError:
        logger.critical(f"We have instance of Type {type(inInstance)}. We can't currently work with that.")
        return

    record = AntragActivityRecords.new(lInstance)
    logger.debug(f"Activity recorded with id: {record.id}")
    return record.timestamp
