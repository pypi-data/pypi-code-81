class LoginActivity:
    # this class is made just to use recordActivityDecorator in order to record login activity
    def __init__(self, user):
        self.user = user
        self.id = user.id
        self.event_details = user.to_json()

    def record_login_activity(self):
        # we are importing direct methods here as importing decorator on starting was causing import error
        from polzyFunctions.GamificationActivityRecorder import WriteActivity
        writer = WriteActivity(self)
        writer.activityWriter()
        return True
