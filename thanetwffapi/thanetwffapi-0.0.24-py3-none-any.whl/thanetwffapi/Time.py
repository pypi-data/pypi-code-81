import time
from datetime import datetime, timedelta


class Time(object):

    def __init__(self):
        pass

    @staticmethod
    def __validate_time(time):
        datetime_format = '%Y%m%d-%H%M%S'
        try:
            time = datetime.strptime(time, datetime_format)
        except ValueError:
            print('Incorrect format, should be on format {}'.format(datetime_format))
        return time

    @staticmethod
    def get_time_duration(start_time, **kwargs):
        kwargs_list = ['days', 'seconds', 'microseconds', 'milliseconds', 'minutes', 'hours', 'weeks']

        datetime.timedelta(days=64, seconds=29156, microseconds=10)
        delta = timedelta(days=50,
                          seconds=27,
                          microseconds=10,
                          milliseconds=29000,
                          minutes=5,
                          hours=8,
                          weeks=2)

        start_time = Time.__validate_time(start_time)

    @staticmethod
    def convert_time_duration(start_time, end_time=None, duration=None):
        if (end_time is None) and (duration is None):
            raise ValueError('Error: set end_time or duration')

        start_time = Time.__validate_time(start_time)

        if end_time:
            end_time = Time.__validate_time(end_time)
        elif duration:
            print('Not yet implemented')
            end_time = Time.__validate_time(duration)

        return start_time, end_time

    @staticmethod
    def standardize_datetime_24h(file_datetime):
        datetime_format = '%Y%m%d-%H%M%S'

        tpl = (int(file_datetime[0:4]), int(file_datetime[4:6]), int(file_datetime[6:8]),
               int(file_datetime[9:11]), int(file_datetime[11:13]), int(file_datetime[13:15]), 0, 1, -1)

        timestamp = time.mktime(tpl)
        date = datetime.fromtimestamp(timestamp)
        return date.strftime(datetime_format)


    @staticmethod
    def validate_date_file(file, t_start, t_end):
        datetime_format = '%Y%m%d-%H%M%S'

        try:
            file_datetime = file.split('/')[-1][4:-11]
            if file_datetime[9:11] == '24':
                file_datetime = Time.standardize_datetime_24h(file_datetime)
            file_datetime = datetime.strptime(file_datetime, datetime_format)
        except ValueError as e:
            print('Error {}\n'.format(e))
            print('File {} could not convert date to correct format'.format(file))
            return False

        if (file_datetime >= t_start) and (file_datetime <= t_end):
            return True
        else:
            return False
