import datetime
import os
import pytz
import time

from datupapi.configure.config import Config

class Utils(Config):

    def __init__(self, config_file, logfile, log_path, *args, **kwargs):
        Config.__init__(self, config_file=config_file, logfile=logfile)
        self.log_path = log_path


    def set_timestamp(self, timezone='America/Chicago'):
        """
        Return a timestamp with the specified timezone and format YYYYmmDDTHMS

        :param timezone: Timezone in string format. Default America/Lima
        :return timestamp: Current timestamp with format YYYYmmDDTHMS

        >>> timestamp = set_timestamp(timezone='America/Chicago')
        >>> timestamp = '20210407T081538'
        """

        timestamp_utc = pytz.utc.localize(datetime.datetime.now())
        timestamp = timestamp_utc.astimezone(pytz.timezone(timezone)).strftime("%Y%m%dT%H%M%S")
        return timestamp








