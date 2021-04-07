from swissarmykit.conf import *
from swissarmykit.lib.core import Singleton
from swissarmykit.service.slackutils import SlackBot
from swissarmykit.utils.preferences import Preferences
from swissarmykit.utils.preferences import OtherProcessTmp
from swissarmykit.utils.preferences import ProcessTmp


@Singleton
class App:

    def get_slack(self):  # type: () -> SlackBot
        return SlackBot.instance()

    def get_preferences(self): # type: () -> Preferences
        return Preferences.instance()

    def get_process_tmp(self, other_db=False): # type: (bool) -> ProcessTmp
        if other_db:
            return OtherProcessTmp.instance()
        else:
            return ProcessTmp.instance()

if __name__ == '__main__':
    app = App.instance()
    slack = app.get_slack()
    slack.notify('hello')
