from logging import getLogger
from polzyFunctions.GlobalConstants import GlobalConstants
from polzyFunctions.Dataclasses.Antrag import Antrag
# Also import all the possible activites candidate here, they will be dynamically imported

logger = getLogger(GlobalConstants.loggerName)


class AntragActivitiesDerive:
    """
    Determines which activities are possible based on the application status, product, etc.

    If there are already activities for this application, then use the existing activities accordingly,
    do not re-instantiate.

    This class is an example and you should create a sub class to achieve goal by referring to this implementation.
    """
    def __init__(self, antrag: Antrag):
        self.antrag = antrag
        self.possibleActivities = []  # store possible activities in this

        existingActivities = []  # store already existing activities in this. It will be used to avoid re-instantiate
        if hasattr(antrag, "Activities"):
            for activity in antrag.Activities:  # loop through already existing activity and store their class name
                existingActivities.append(activity.__class__.__name__)

        possibleActivitiesCandidates = []  # ["activity1", "activity2"] store possible activities name in string here

        alreadyInitiatedActivities = []  # store activities which are not possible with current status here

        if hasattr(antrag, "Activities"):
            for activity in possibleActivitiesCandidates:
                existingActivity = self.antrag.get_activity(activity, optional=True)
                if existingActivity:
                    # This activity was already there, do not re-instantiate.
                    alreadyInitiatedActivities.append(activity)

            for alreadyInitiatedActivity in alreadyInitiatedActivities:
                possibleActivitiesCandidates.remove(alreadyInitiatedActivity)

        # In PossibleActivities there are now all activities that are theoretically possible, but not yet
        # were instantiated. these must now be generated.
        for newActivity in possibleActivitiesCandidates:
            tmpClassReference = globals()[newActivity]
            self.possibleActivities.append(tmpClassReference(antrag=antrag))  # initiate and store activity

        # In getActivitiesforAntrag we return ALL activities for the application, so we have to
        # Now add the existing activities again.
        if hasattr(antrag, "Activities"):
            antrag.Activities.extend(self.possibleActivities)
            self.possibleActivities = antrag.Activities

    def getActivitiesForAntrag(self):
        """
        Go through all the activities and ask them if they want to be active
        :return:
        """
        # call method checkIsActivityValidForStatus of activity to know if it is suitable for current stats
        self.possibleActivities = [x for x in self.possibleActivities if x.checkIsActivityValidForStatus()]

        logger.debug(f"List of possible Activities for this Antrag in state {self.antrag.status} is: \n{self.possibleActivities}")
        return self.possibleActivities
