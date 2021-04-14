from polzybackend.models import GamificationActivity
from polzyFunctions.Activities.LoginActivity import LoginActivity
import json


def recordActivityDecorator(method):
    """
    This is a decorator that will write into GamificationActivity table.
    :param method: The method to be executed
    :return:
    """
    def wrapper(self, *args, **kwargs):
        writer = WriteActivity(self)
        writer.activityWriter()
        return method(self, *args, **kwargs)

    return wrapper


class WriteActivity:
    """
    Writes an activity to gamification table.
    """
    def __init__(self, instanceOfAntragPolicyOrActivity):
        from polzyFunctions.Activities.AntragActivity import AntragActivity
        from polzyFunctions.Activities.Activity import Activity
        from polzyFunctions.Dataclasses.Antrag import Antrag
        # FIXME: Fix after policy refactor
        #from fasifu.Activities.PolicyActivity import PolicyActivity
        #from fasifu.Dataclasses.Polizze import Polizze

        self.activity: Activity = None
        self.antrag: Antrag = None
        self.polizze = None
        self.login: LoginActivity = None

        self.callingClassRef = instanceOfAntragPolicyOrActivity

        if isinstance(instanceOfAntragPolicyOrActivity, AntragActivity):
            self.activity = instanceOfAntragPolicyOrActivity
            self.event = 4  # "AntragActivity"
        elif "PolicyActivity" in instanceOfAntragPolicyOrActivity.__class__.__name__:
            self.activity = instanceOfAntragPolicyOrActivity
            self.event = 3  # "PolicyActivity"
        elif isinstance(instanceOfAntragPolicyOrActivity, Antrag):
            self.antrag = instanceOfAntragPolicyOrActivity
            self.event = 1  # "Antrag"
        elif "Polizze" in instanceOfAntragPolicyOrActivity.__class__.__name__:
            self.polizze = instanceOfAntragPolicyOrActivity
            self.event = 2  # "Polizze"
        elif isinstance(instanceOfAntragPolicyOrActivity, LoginActivity):
            self.login = instanceOfAntragPolicyOrActivity
            self.event = 6

    def activityWriter(self):
        user = None
        eventDetails = None

        if self.polizze:
            try:
                user = self.polizze.user
            except AttributeError:
                # This is most probably an error record, e.g. because the policy doesn' exist.
                return
            eventDetails = self.__getEventDetailsPolizze()
        elif self.antrag:
            user = self.antrag.user
            eventDetails = self.__getEventDetailsAntrag()
        elif self.activity:
            try:
                user = self.activity.antrag.user
                self.antrag = self.activity.antrag
                eventDetails = self.__getEventDetailsAntrag()
            except:
                user = self.activity.polizze.user
                self.polizze = self.activity.polizze
                eventDetails = self.__getEventDetailsPolizze()
            eventDetails.update({"Activity": self.callingClassRef.__class__.__name__})
        elif self.login:
            user = self.login.user
            eventDetails = self.login.event_details

        GamificationActivity.new(user=user, event=self.event, event_details=json.dumps(eventDetails))

    def __getEventDetailsPolizze(self):
        eventDetails = {"polizzenNummer": self.polizze.polizzenNummer,
                        "stage": self.polizze.user.stage,
                        "sapClient": self.polizze.sapClient,
                        "lineOfBusiness": self.polizze.lineOfBusiness,
                        "productName": self.polizze.productName}
        return eventDetails

    def __getEventDetailsAntrag(self):
        eventDetails = {"lineOfBusiness": self.antrag.lineOfBusiness,
                        "stage": self.antrag.user.stage,
                        "sapClient": self.antrag.sapClient,
                        "productName": self.antrag.productName}
        return eventDetails
